"""
支撑/阻力位（SR）持仓风险管理器 - 纯 Python 原生开箱即用版
无需安装 pandas/numpy 等第三方库，直接运行即可。
"""

import math
from typing import Dict, List, Optional, Tuple, Any


class SRPositionManager:
    """
    基于金融时间序列支撑/阻力位（SR）概率与记忆效应研究的持仓管理器插件
    论文模型依据:
    1. 动态滚动窗口与增量带宽 gamma 确定 SR 级别
    2. Beta-Binomial 贝叶斯推断计算历史反弹胜率 E[p(b|b_prev)]
    3. 时间衰减模型 (Temporal Decay) 用于风险预警
    """

    def __init__(self,
                 window_size: int = 60,
                 alpha_prior: float = 1.0,
                 beta_prior: float = 1.0,
                 decay_half_life: int = 120):
        """
        初始化持仓管理器
        :param window_size: 滚动窗口大小 (对应论文中的 i)
        :param alpha_prior: 贝叶斯 Beta 先验 alpha (默认 1.0 均匀先验)
        :param beta_prior: 贝叶斯 Beta 先验 beta (默认 1.0 均匀先验)
        :param decay_half_life: 时间衰减半衰期 (以 K线根数/时间步计算)
        """
        self.window_size = window_size
        self.alpha_prior = alpha_prior
        self.beta_prior = beta_prior
        self.decay_half_life = decay_half_life

        # 记录识别出的 SR 级别状态数据
        # 格式: { level_price: {'type': 'support'/'resistance', 'b_prev': int, 'total_touches': int, 'last_touch_step': int} }
        self.sr_levels: Dict[float, Dict[str, Any]] = {}

    def calculate_gamma(self, prices: List[float]) -> float:
        """
        计算平均价格增量 gamma (论文 2.2 节)
        gamma = mean(|x_t - x_{t-1}|)
        """
        if len(prices) < 2:
            return 0.0
        diffs = [abs(prices[i] - prices[i - 1]) for i in range(1, len(prices))]
        return sum(diffs) / len(diffs)

    def detect_sr_levels(self, klines: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        基于滚动窗口与 gamma 带宽识别动态支撑和阻力带
        :param klines: 包含 [{'high': float, 'low': float, 'close': float}, ...] 的列表
        :return: {'supports': [(min_price, gamma)], 'resistances': [(max_price, gamma)], 'gamma': float}
        """
        closes = [k['close'] for k in klines]
        highs = [k['high'] for k in klines]
        lows = [k['low'] for k in klines]

        gamma = self.calculate_gamma(closes)

        supports = []
        resistances = []

        if len(klines) >= self.window_size:
            window_highs = highs[-self.window_size:]
            window_lows = lows[-self.window_size:]

            max_p = max(window_highs)
            min_p = min(window_lows)

            supports.append((min_p, gamma))
            resistances.append((max_p, gamma))
        elif klines:
            max_p = max(highs)
            min_p = min(lows)
            supports.append((min_p, gamma))
            resistances.append((max_p, gamma))

        return {'supports': supports, 'resistances': resistances, 'gamma': gamma}

    def update_sr_memory(self, price: float, current_step: int, gamma: float, is_bounce: bool,
                         is_support: bool) -> None:
        """
        更新 SR 级别的“历史记忆”（反弹次数与穿透次数）
        :param price: 触发的 SR 价格
        :param current_step: 当前时间步
        :param gamma: 带宽
        :param is_bounce: 是否发生了反弹（True: 反弹, False: 穿透/突破）
        :param is_support: 是否为支撑位
        """
        matched_level = None
        for registered_price in self.sr_levels.keys():
            if abs(registered_price - price) <= gamma:
                matched_level = registered_price
                break

        if matched_level is None:
            matched_level = price
            self.sr_levels[matched_level] = {
                'type': 'support' if is_support else 'resistance',
                'b_prev': 0,
                'total_touches': 0,
                'last_touch_step': current_step
            }

        sr_data = self.sr_levels[matched_level]
        sr_data['total_touches'] += 1
        sr_data['last_touch_step'] = current_step
        if is_bounce:
            sr_data['b_prev'] += 1

    def calculate_bayes_bounce_probability(self, b_prev: int, total_touches: int) -> float:
        """
        论文核心逻辑：采用贝叶斯推断 (Beta-Binomial Conjugate) 计算期望反弹概率 E[p(b|b_prev)]
        E[p] = (b_prev + alpha) / (total_touches + alpha + beta)
        """
        return (b_prev + self.alpha_prior) / (total_touches + self.alpha_prior + self.beta_prior)

    def calculate_temporal_decay(self, last_touch_step: int, current_step: int) -> float:
        """
        计算微观时间衰减因子 (Temporal Decay)
        使用指数衰减: Exp(-ln(2) * delta_t / half_life)
        """
        delta_t = current_step - last_touch_step
        if delta_t <= 0:
            return 1.0
        return math.exp(-math.log(2) * delta_t / self.decay_half_life)

    def evaluate_position_risk(self,
                               position_type: str,
                               entry_price: float,
                               current_price: float,
                               current_step: int,
                               klines: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        持仓风险评估主接口：分析当前持仓离最近 SR 水平的距离、反弹概率与衰减状态
        :param position_type: 'long' (多头) 或 'short' (空头)
        :param entry_price: 入场价格
        :param current_price: 当前市场价格
        :param current_step: 当前时间步/K线序号
        :param klines: K线数据列表 [{'high': 10, 'low': 8, 'close': 9}, ...]
        """
        sr_info = self.detect_sr_levels(klines)
        gamma = sr_info['gamma']

        evaluation: Dict[str, Any] = {
            'position_type': position_type,
            'current_price': current_price,
            'pnl_pct': ((current_price - entry_price) / entry_price) if position_type == 'long' else (
                        (entry_price - current_price) / entry_price),
            'nearest_sr_type': None,
            'sr_price': None,
            'b_prev': 0,
            'bayes_bounce_prob': 0.5,
            'decay_factor': 1.0,
            'adjusted_bounce_prob': 0.5,
            'action_recommendation': 'HOLD',
            'warning': None
        }

        # 多头场景：分析下方最近支撑位
        if position_type == 'long':
            supports = sr_info['supports']
            if supports:
                sup_price, _ = supports[0]
                evaluation['nearest_sr_type'] = 'support'
                evaluation['sr_price'] = sup_price

                matched_data = None
                for lp, data in self.sr_levels.items():
                    if abs(lp - sup_price) <= gamma:
                        matched_data = data
                        break

                if matched_data:
                    b_prev = matched_data['b_prev']
                    touches = matched_data['total_touches']
                    last_step = matched_data['last_touch_step']

                    prob = self.calculate_bayes_bounce_probability(b_prev, touches)
                    decay = self.calculate_temporal_decay(last_step, current_step)

                    evaluation['b_prev'] = b_prev
                    evaluation['bayes_bounce_prob'] = prob
                    evaluation['decay_factor'] = decay
                    evaluation['adjusted_bounce_prob'] = prob * decay

                dist_to_sr = (current_price - sup_price) / current_price if current_price != 0 else 0
                if dist_to_sr <= (gamma / current_price) if current_price != 0 else True:
                    if evaluation['adjusted_bounce_prob'] > 0.65:
                        evaluation['action_recommendation'] = 'STRONG_HOLD_OR_ADD'
                        evaluation['warning'] = '价格触及高概率反弹支撑带，可考虑加仓或维持多头。'
                    elif evaluation['adjusted_bounce_prob'] < 0.45:
                        evaluation['action_recommendation'] = 'REDUCE_OR_STOP_LOSS'
                        evaluation['warning'] = '支撑位反弹概率低且存在衰减风险，建议收紧止损或减仓。'

        # 空头场景：分析上方最近阻力位
        elif position_type == 'short':
            resistances = sr_info['resistances']
            if resistances:
                res_price, _ = resistances[0]
                evaluation['nearest_sr_type'] = 'resistance'
                evaluation['sr_price'] = res_price

                matched_data = None
                for lp, data in self.sr_levels.items():
                    if abs(lp - res_price) <= gamma:
                        matched_data = data
                        break

                if matched_data:
                    b_prev = matched_data['b_prev']
                    touches = matched_data['total_touches']
                    last_step = matched_data['last_touch_step']

                    prob = self.calculate_bayes_bounce_probability(b_prev, touches)
                    decay = self.calculate_temporal_decay(last_step, current_step)

                    evaluation['b_prev'] = b_prev
                    evaluation['bayes_bounce_prob'] = prob
                    evaluation['decay_factor'] = decay
                    evaluation['adjusted_bounce_prob'] = prob * decay

                dist_to_sr = (res_price - current_price) / current_price if current_price != 0 else 0
                if dist_to_sr <= (gamma / current_price) if current_price != 0 else True:
                    if evaluation['adjusted_bounce_prob'] > 0.65:
                        evaluation['action_recommendation'] = 'STRONG_HOLD_OR_ADD'
                        evaluation['warning'] = '价格触及高概率阻力位（空头防守带），可考虑维持空单。'
                    elif evaluation['adjusted_bounce_prob'] < 0.45:
                        evaluation['action_recommendation'] = 'REDUCE_OR_STOP_LOSS'
                        evaluation['warning'] = '阻力位压制效力减弱，注意向上突破风险，建议止损。'

        return evaluation


# ==========================================
# 交互演示（直接运行本文件即可测试）
# ==========================================
if __name__ == "__main__":
    import random

    # 模拟 100 根 K 线数据
    random.seed(42)
    current_p = 100.0
    klines = []

    for _ in range(100):
        change = random.gauss(0, 0.5)
        current_p += change
        high = current_p + abs(random.gauss(0, 0.2))
        low = current_p - abs(random.gauss(0, 0.2))
        klines.append({'high': high, 'low': low, 'close': current_p})

    # 初始化持仓管理器
    pm = SRPositionManager(window_size=30, decay_half_life=50)

    # 模拟在价格 95.0 处已有 4 次成功反弹记录
    pm.update_sr_memory(price=95.0, current_step=10, gamma=0.3, is_bounce=True, is_support=True)
    pm.update_sr_memory(price=95.0, current_step=20, gamma=0.3, is_bounce=True, is_support=True)
    pm.update_sr_memory(price=95.0, current_step=35, gamma=0.3, is_bounce=True, is_support=True)
    pm.update_sr_memory(price=95.0, current_step=50, gamma=0.3, is_bounce=True, is_support=True)

    # 把最近的 K 线最低价设为 95.0
    for k in klines[-30:]:
        k['low'] = min(k['low'], 95.0)

    # 评估持仓
    result = pm.evaluate_position_risk(
        position_type='long',
        entry_price=98.0,
        current_price=95.2,
        current_step=80,
        klines=klines
    )

    print("=" * 45)
    print("      开箱即用 SR 持仓管理器评估结果")
    print("=" * 45)
    print(f"持仓类型       : {result['position_type']}")
    print(f"当前盈亏       : {result['pnl_pct'] * 100:.2f}%")
    print(f"临近 SR 类型   : {result['nearest_sr_type']} (参考位: {result['sr_price']:.2f})")
    print(f"历史反弹次数   : {result['b_prev']}")
    print(f"贝叶斯胜率预测 : {result['bayes_bounce_prob'] * 100:.2f}%")
    print(f"时间衰减因子   : {result['decay_factor']:.4f}")
    print(f"衰减修正胜率   : {result['adjusted_bounce_prob'] * 100:.2f}%")
    print(f"调仓建议       : {result['action_recommendation']}")
    print(f"风控提示       : {result['warning']}")
    print("=" * 45)