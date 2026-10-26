import os
import glob


def convert_gb2312_to_utf8(folder_path):
    """直接将GB2312转换为UTF-8"""
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))

    for file_path in txt_files:
        try:
            # 用GB2312读取
            with open(file_path, 'r', encoding='gb2312') as f:
                content = f.read()

            # 用UTF-8写入
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"成功转换: {file_path}")

        except Exception as e:
            print(f"转换失败 {file_path}: {e}")
            # 如果GB2312失败，尝试GBK
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    content = f.read()
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"使用GBK成功转换: {file_path}")
            except:
                print(f"完全失败: {file_path}")

                convert_gb2312_to_utf8(r"C:\Users\natou\Desktop\longzu")
                #在引号内输入你要批量改变的文件的文件夹