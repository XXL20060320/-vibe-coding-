#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wx_official.py — 用公众号官方「发布能力」接口，拉取全部已发布文章

前提（缺一不可）：
  1. 该公众号的 AppID 与 AppSecret（公众号后台 → 设置与开发 → 基本配置）
  2. 服务器 IP 白名单里加上你运行脚本的出口 IP
  3. 账号已认证（未认证账号调发布接口会返回 48001 未授权）

用法：
    set WX_APPID=wx....      // Windows
    set WX_SECRET=....
    python wx_official.py check          :: 只验证凭据是否可用
    python wx_official.py index          :: 拉文章索引 -> out/公众号文章索引.csv
    python wx_official.py index --download  :: 顺便把正文存到 work/wx/
    python wx_official.py index --since 2026-01-01 --year 2026
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
WORK = ROOT / "work" / "wx"
TOKEN_CACHE = ROOT / ".wx_token.json"
API = "https://api.weixin.qq.com/cgi-bin"

ERR = {
    40001: "AppSecret 错误，请重新生成",
    40013: "AppID 无效",
    40125: "AppSecret 无效",
    40164: "调用 IP 不在白名单，请到公众号后台添加",
    45009: "接口调用超过当日限额",
    48001: "api 功能未授权：账号未认证，或没有发布能力权限",
    50001: "用户未授权该 api",
}


def _get(url: str, timeout: int = 30) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _post(url: str, payload: dict, timeout: int = 60) -> dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def explain(res: dict) -> str:
    code = res.get("errcode")
    if not code:
        return ""
    return f"[{code}] {ERR.get(code, res.get('errmsg', '未知错误'))}"


CRED_FILE = ROOT / ".wx_creds.json"


def creds(interactive: bool = False) -> tuple[str, str]:
    appid = os.environ.get("WX_APPID", "").strip()
    secret = os.environ.get("WX_SECRET", "").strip()

    if (not appid or not secret) and CRED_FILE.is_file():
        try:
            c = json.loads(CRED_FILE.read_text(encoding="utf-8"))
            appid = appid or str(c.get("appid", "")).strip()
            secret = secret or str(c.get("secret", "")).strip()
        except Exception:  # noqa: BLE001
            pass

    if (not appid or not secret) and interactive:
        print("\n首次运行，需要公众号开发者凭据。")
        print("位置：公众号后台 → 设置与开发 → 基本配置 → 开发者ID / 开发者密码\n")
        try:
            appid = input("AppID: ").strip()
            secret = input("AppSecret: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n未输入凭据，已取消。")
            appid = secret = ""
        if appid and secret:
            CRED_FILE.write_text(json.dumps({"appid": appid, "secret": secret}),
                                 encoding="utf-8")
            print(f"已保存到 {CRED_FILE.name}（本机文件，请勿外传或提交到 git）")

    if not appid or not secret:
        print("缺少凭据：可设置环境变量 WX_APPID / WX_SECRET，"
              "或运行一次 python wx_official.py check 按提示输入。")
        sys.exit(2)
    return appid, secret


def access_token(appid: str, secret: str, force: bool = False) -> str:
    if not force and TOKEN_CACHE.is_file():
        try:
            c = json.loads(TOKEN_CACHE.read_text(encoding="utf-8"))
            if c.get("appid") == appid and datetime.fromisoformat(c["expire"]) > datetime.now():
                return c["token"]
        except Exception:  # noqa: BLE001
            pass

    q = urllib.parse.urlencode({"grant_type": "client_credential",
                                "appid": appid, "secret": secret})
    res = _get(f"{API}/token?{q}")
    if "access_token" not in res:
        print("获取 access_token 失败 " + explain(res))
        sys.exit(1)
    tok = res["access_token"]
    exp = datetime.now() + timedelta(seconds=int(res.get("expires_in", 7200)) - 300)
    TOKEN_CACHE.write_text(json.dumps({"appid": appid, "token": tok,
                                       "expire": exp.isoformat()}), encoding="utf-8")
    print(f"access_token 获取成功（有效期至 {exp:%H:%M}）")
    return tok


def cmd_myip(args) -> int:
    """查本机出口 IP —— 公众号后台的 IP 白名单只认 IPv4，填这个。"""
    urls = ("https://ipv4.icanhazip.com", "https://api-ipv4.ip.sb/ip",
            "https://4.ipw.cn", "https://api.ipify.org")
    for u in urls:
        try:
            with urllib.request.urlopen(u, timeout=10) as r:
                ip = r.read().decode("utf-8", "replace").strip()
        except Exception:  # noqa: BLE001
            continue
        if not ip:
            continue
        if ":" in ip:
            print(f"只拿到 IPv6（{ip}），微信白名单不支持。")
            print("请在浏览器打开 https://4.ipw.cn 查看 IPv4 地址，或在有公网 IPv4 的机器上运行。")
            return 1
        print(f"本机出口 IPv4：{ip}")
        print("把它加到 公众号后台 → 设置与开发 → 基本配置 → IP白名单")
        return 0
    print("查询失败（可能没联网）。可在浏览器打开 https://4.ipw.cn 查看。")
    return 1


def cmd_check(args) -> int:
    appid, secret = creds()
    access_token(appid, secret, force=True)
    print("凭据可用，可以跑 index。")
    return 0


def pull_material(token: str, page: int = 20) -> list[dict]:
    """兜底：永久素材（图文）。老文章可能只在素材库，不在发布列表。"""
    items: list[dict] = []
    offset = 0
    total = None
    while True:
        res = _post(f"{API}/material/batchget_material?access_token={token}",
                    {"type": "news", "offset": offset, "count": page})
        if res.get("errcode"):
            print("  素材库拉取失败 " + explain(res))
            break
        if total is None:
            total = int(res.get("total_count", 0))
            print(f"  永久素材（图文）共 {total} 条")
        batch = res.get("item", []) or []
        if not batch:
            break
        items.extend(batch)
        offset += len(batch)
        if offset >= total:
            break
    return items


def pull_all(token: str, page: int = 20) -> list[dict]:
    """分页拉全部已发布文章。"""
    items: list[dict] = []
    offset = 0
    total = None
    while True:
        res = _post(f"{API}/freepublish/batchget?access_token={token}",
                    {"offset": offset, "count": page, "no_content": 0})
        if res.get("errcode"):
            print("拉取失败 " + explain(res))
            break
        if total is None:
            total = int(res.get("total_count", 0))
            print(f"已发布文章共 {total} 篇")
        batch = res.get("item", []) or []
        if not batch:
            break
        items.extend(batch)
        offset += len(batch)
        print(f"  已取 {offset}/{total}")
        if offset >= total:
            break
    return items


DATE_RE = re.compile(r"(\d{4})(\d{2})(\d{2})")


def flatten(items: list[dict]) -> list[dict]:
    """把 batchget 的嵌套结构摊平成一行一篇。"""
    rows = []
    for it in items:
        art = it.get("content", {}) or {}
        news = art.get("news_item", []) or []
        upd = int(it.get("update_time") or 0)
        date = datetime.fromtimestamp(upd).strftime("%Y-%m-%d") if upd else ""
        for n in news:
            rows.append({
                "日期": date,
                "标题": (n.get("title") or "").strip(),
                "作者": n.get("author") or "",
                "链接": n.get("url") or "",
                "摘要": (n.get("digest") or "").strip(),
                "正文": n.get("content") or "",
                "article_id": it.get("article_id") or "",
                "是否主条": "是" if n.get("is_deleted") in (None, 0) else "否",
            })
    rows.sort(key=lambda r: r["日期"], reverse=True)
    return rows


def cmd_index(args) -> int:
    appid, secret = creds()
    token = access_token(appid, secret)

    print("① 发布能力接口 freepublish")
    pub = pull_all(token)
    print("② 永久素材库 material（兜底：老文章可能只在这里）")
    mat = pull_material(token)

    rows = flatten(pub)
    rows2 = flatten(mat)
    seen: set = set()
    merged: list[dict] = []
    for r in rows + rows2:
        key = r["链接"] or (r["标题"], r["日期"])
        if key in seen:
            continue
        seen.add(key)
        merged.append(r)
    merged.sort(key=lambda r: r["日期"], reverse=True)
    print(f"合并去重后 {len(merged)} 条（发布 {len(rows)} / 素材 {len(rows2)}）")
    rows = merged

    if args.since:
        rows = [r for r in rows if r["日期"] >= args.since]
    if args.year:
        rows = [r for r in rows if r["日期"].startswith(str(args.year))]
    if args.keyword:
        kws = [k.strip() for k in args.keyword.split(",") if k.strip()]
        rows = [r for r in rows if any(k in r["标题"] + r["摘要"] for k in kws)]
    print(f"筛后 {len(rows)} 条")

    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "公众号文章索引.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["日期", "标题", "作者", "链接", "摘要", "article_id"])
        for r in rows:
            w.writerow([r["日期"], r["标题"], r["作者"], r["链接"], r["摘要"], r["article_id"]])
    print(f"索引 -> {csv_path.relative_to(ROOT)}")

    if args.download:
        import importlib
        c = importlib.import_module("crawl2026")
        WORK.mkdir(parents=True, exist_ok=True)
        n = 0
        for r in rows:
            text = c.site_to_text(r["正文"]) if r["正文"] else ""
            if len(text) < 100:
                continue
            safe = re.sub(r"[^\w\u4e00-\u9fa5]", "", r["标题"])[:40] or r["article_id"]
            (WORK / f"{r['日期']}_{safe}.md").write_text(
                f"来源：{r['链接']}\n标题：{r['标题']}\n\n{text}", encoding="utf-8")
            n += 1
        print(f"正文 {n} 篇 -> work/wx/")

    for r in rows[:15]:
        print(f"  {r['日期']}  {r['标题'][:52]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="公众号官方发布接口拉取")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    sub.add_parser("myip")
    p = sub.add_parser("index")
    p.add_argument("--since", default=None)
    p.add_argument("--year", type=int, default=None)
    p.add_argument("--keyword", default=None)
    p.add_argument("--download", action="store_true")
    args = ap.parse_args()
    return {"check": cmd_check, "index": cmd_index, "myip": cmd_myip}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
