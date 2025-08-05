import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from datetime import datetime
from config import HISTORY_DIR, BASE_DIR
import warnings

# 忽略警告
warnings.filterwarnings("ignore", category=UserWarning)


# 设置中文字体支持
def set_chinese_font():
    try:
        # 尝试使用系统字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

        # 检查字体是否可用
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        chinese_fonts = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']

        # 如果没有找到中文字体，尝试使用内置字体
        if not any(font in available_fonts for font in chinese_fonts):
            # 使用内置的WenQuanYi Micro Hei字体
            plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei']

            # 如果仍然不可用，尝试下载并注册字体
            if 'WenQuanYi Micro Hei' not in available_fonts:
                try:
                    import os
                    from urllib.request import urlretrieve

                    # 下载字体文件
                    font_url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf"
                    font_path = os.path.join(BASE_DIR, "NotoSansCJKsc-Regular.otf")

                    if not os.path.exists(font_path):
                        print("下载中文字体文件...")
                        urlretrieve(font_url, font_path)

                    # 注册字体
                    font_prop = fm.FontProperties(fname=font_path)
                    fm.fontManager.addfont(font_path)
                    plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
                    print(f"已注册字体: {font_prop.get_name()}")
                except Exception as e:
                    print(f"字体下载失败: {e}")
                    # 回退到默认字体
                    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    except Exception as e:
        print(f"设置中文字体失败: {e}")


# 初始化字体设置
set_chinese_font()


def generate_price_chart(item_names, days=7, output_file="price_trend.png"):
    """生成价格趋势图"""
    plt.figure(figsize=(14, 8))

    for item_name in item_names:
        # 加载物品历史数据
        item_file = os.path.join(HISTORY_DIR, "items", f"{item_name}.csv")
        if not os.path.exists(item_file):
            print(f"警告: 找不到 {item_name} 的历史数据")
            continue

        try:
            df = pd.read_csv(item_file, parse_dates=['timestamp'])

            # 过滤最近N天的数据
            cutoff_date = datetime.now() - pd.Timedelta(days=days)
            df = df[df['timestamp'] >= cutoff_date]

            if df.empty:
                print(f"警告: {item_name} 最近 {days} 天没有数据")
                continue

            # 按时间排序并绘制
            df = df.sort_values('timestamp')
            plt.plot(df['timestamp'], df['price_g'], label=item_name, marker='o')
        except Exception as e:
            print(f"处理物品 {item_name} 时出错: {e}")

    plt.title(f"物品价格趋势 ({days}天)")
    plt.xlabel("时间")
    plt.ylabel("价格 (G)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"价格趋势图已保存至: {output_file}")
    plt.close()


def generate_availability_chart(item_names, days=7, output_file="availability_trend.png"):
    """生成可购买数量趋势图"""
    plt.figure(figsize=(14, 8))

    for item_name in item_names:
        # 加载物品历史数据
        item_file = os.path.join(HISTORY_DIR, "items", f"{item_name}.csv")
        if not os.path.exists(item_file):
            print(f"警告: 找不到 {item_name} 的历史数据")
            continue

        try:
            df = pd.read_csv(item_file, parse_dates=['timestamp'])

            # 过滤最近N天的数据
            cutoff_date = datetime.now() - pd.Timedelta(days=days)
            df = df[df['timestamp'] >= cutoff_date]

            if df.empty:
                print(f"警告: {item_name} 最近 {days} 天没有数据")
                continue

            # 按时间排序并绘制
            df = df.sort_values('timestamp')
            plt.bar(df['timestamp'], df['available'], label=item_name, alpha=0.7)
        except Exception as e:
            print(f"处理物品 {item_name} 时出错: {e}")

    plt.title(f"物品可购买数量趋势 ({days}天)")
    plt.xlabel("时间")
    plt.ylabel("可购买数量")
    plt.legend()
    plt.grid(True, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"可购买数量趋势图已保存至: {output_file}")
    plt.close()


def generate_correlation_chart(item_name1, item_name2, days=30, output_file="price_correlation.png"):
    """生成两个物品价格相关性图"""
    plt.figure(figsize=(14, 8))

    # 加载两个物品的历史数据
    item1_file = os.path.join(HISTORY_DIR, "items", f"{item_name1}.csv")
    item2_file = os.path.join(HISTORY_DIR, "items", f"{item_name2}.csv")

    if not os.path.exists(item1_file) or not os.path.exists(item2_file):
        print("错误: 缺少物品历史数据")
        return

    try:
        df1 = pd.read_csv(item1_file, parse_dates=['timestamp'])
        df2 = pd.read_csv(item2_file, parse_dates=['timestamp'])

        # 过滤最近N天的数据
        cutoff_date = datetime.now() - pd.Timedelta(days=days)
        df1 = df1[df1['timestamp'] >= cutoff_date]
        df2 = df2[df2['timestamp'] >= cutoff_date]

        if df1.empty or df2.empty:
            print("错误: 数据不足")
            return

        # 合并数据集
        merged_df = pd.merge(df1, df2, on='timestamp', suffixes=(f'_{item_name1}', f'_{item_name2}'))

        # 计算相关性
        correlation = merged_df[f'price_g_{item_name1}'].corr(merged_df[f'price_g_{item_name2}'])

        # 绘制散点图
        plt.scatter(merged_df[f'price_g_{item_name1}'], merged_df[f'price_g_{item_name2}'], alpha=0.6)
        plt.title(f"{item_name1} 与 {item_name2} 价格相关性 (r={correlation:.2f})")
        plt.xlabel(f"{item_name1} 价格 (G)")
        plt.ylabel(f"{item_name2} 价格 (G)")
        plt.grid(True)

        # 添加趋势线
        z = np.polyfit(merged_df[f'price_g_{item_name1}'], merged_df[f'price_g_{item_name2}'], 1)
        p = np.poly1d(z)
        plt.plot(merged_df[f'price_g_{item_name1}'], p(merged_df[f'price_g_{item_name1}']), "r--")

        plt.tight_layout()
        plt.savefig(output_file)
        print(f"价格相关性图已保存至: {output_file}")
        plt.close()
    except Exception as e:
        print(f"生成相关性图时出错: {e}")

def test_font_support():
    """测试中文字体支持"""
    plt.figure(figsize=(10, 3))
    plt.text(0.5, 0.5, "中文测试: 幽冥铁矿石 铜矿石 孔雀石",
             fontsize=20, ha='center')
    plt.axis('off')
    plt.savefig("chinese_font_test.png")
    plt.close()
    print("字体测试图已保存至: chinese_font_test.png")

# 在文件末尾调用测试
if __name__ == "__main__":
    test_font_support()