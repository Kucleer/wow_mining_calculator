import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime, timedelta
from config import HISTORY_DIR, BASE_DIR
import matplotlib as mpl
import matplotlib.font_manager as fm
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


def load_strategy_history():
    """加载策略历史数据"""
    strategy_history_path = os.path.join(HISTORY_DIR, "strategy_history.csv")
    if not os.path.exists(strategy_history_path):
        print("找不到策略历史文件")
        return pd.DataFrame()

    try:
        df = pd.read_csv(strategy_history_path, parse_dates=['timestamp'])
        return df
    except Exception as e:
        print(f"加载策略历史数据出错: {e}")
        return pd.DataFrame()


def generate_strategy_trend(strategy_name, ore_name=None, days=30, output_file="strategy_trend.png"):
    """生成策略收益趋势图"""
    df = load_strategy_history()
    if df.empty:
        return

    # 过滤数据
    strategy_df = df[df['strategy'] == strategy_name]
    if ore_name:
        strategy_df = strategy_df[strategy_df['ore'] == ore_name]

    if strategy_df.empty:
        print(f"找不到策略 '{strategy_name}' 的历史数据")
        return

    # 过滤最近N天的数据
    cutoff_date = datetime.now() - timedelta(days=days)
    strategy_df = strategy_df[strategy_df['timestamp'] >= cutoff_date]

    if strategy_df.empty:
        print(f"策略 '{strategy_name}' 最近 {days} 天没有数据")
        return

    # 按时间排序
    strategy_df = strategy_df.sort_values('timestamp')

    # 创建图表
    plt.figure(figsize=(14, 8))

    # 绘制总收益
    plt.plot(strategy_df['timestamp'], strategy_df['total_profit_g'],
             label='总收益', marker='o', color='blue')

    # 绘制炸矿收益
    plt.plot(strategy_df['timestamp'], strategy_df['mining_profit_g'],
             label='炸矿收益', marker='x', linestyle='--', color='green')

    # 绘制分解收益
    plt.plot(strategy_df['timestamp'], strategy_df['disenchant_profit_g'],
             label='分解收益', marker='^', linestyle='-.', color='red')

    plt.title(f"策略收益趋势: {strategy_name} ({days}天)")
    plt.xlabel("时间")
    plt.ylabel("收益 (G)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"策略收益趋势图已保存至: {output_file}")
    plt.close()


def compare_strategies(strategy_names, ore_name=None, days=30, output_file="strategy_comparison.png"):
    """比较多个策略的收益"""
    df = load_strategy_history()
    if df.empty:
        return

    # 过滤数据
    if ore_name:
        df = df[df['ore'] == ore_name]

    # 过滤最近N天的数据
    cutoff_date = datetime.now() - timedelta(days=days)
    df = df[df['timestamp'] >= cutoff_date]

    if df.empty:
        print(f"最近 {days} 天没有策略数据")
        return

    # 创建图表
    plt.figure(figsize=(14, 8))

    # 为每个策略绘制收益趋势
    for strategy in strategy_names:
        strategy_df = df[df['strategy'] == strategy]
        if strategy_df.empty:
            continue

        strategy_df = strategy_df.sort_values('timestamp')
        plt.plot(strategy_df['timestamp'], strategy_df['total_profit_g'],
                 label=strategy, marker='o')

    plt.title(f"策略收益比较 ({days}天)")
    plt.xlabel("时间")
    plt.ylabel("总收益 (G)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"策略比较图已保存至: {output_file}")
    plt.close()


def generate_strategy_report(ore_name=None, days=30, output_file="strategy_report.csv"):
    """生成策略表现报告"""
    df = load_strategy_history()
    if df.empty:
        return None

    # 过滤数据
    if ore_name:
        df = df[df['ore'] == ore_name]

    # 过滤最近N天的数据
    cutoff_date = datetime.now() - timedelta(days=days)
    df = df[df['timestamp'] >= cutoff_date]

    if df.empty:
        print(f"最近 {days} 天没有策略数据")
        return None

    # 计算每个策略的统计指标
    report_data = []
    for strategy, group in df.groupby('strategy'):
        report_data.append({
            "strategy": strategy,
            "count": len(group),
            "avg_profit": group['total_profit_g'].mean(),
            "min_profit": group['total_profit_g'].min(),
            "max_profit": group['total_profit_g'].max(),
            "std_dev": group['total_profit_g'].std(),
            "avg_mining": group['mining_profit_g'].mean(),
            "avg_disenchant": group['disenchant_profit_g'].mean(),
            "last_profit": group.sort_values('timestamp', ascending=False).iloc[0]['total_profit_g']
        })

    # 创建DataFrame并排序
    report_df = pd.DataFrame(report_data)
    if report_df.empty:
        return None

    report_df = report_df.sort_values('avg_profit', ascending=False)

    # 保存报告
    report_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"策略报告已保存至: {output_file}")

    return report_df


def analyze_strategy_performance(strategy_name, ore_name=None, days=90):
    """分析策略表现并生成报告"""
    # 生成趋势图
    trend_file = f"{strategy_name}_trend.png"
    generate_strategy_trend(strategy_name, ore_name, days, trend_file)

    # 生成详细报告
    report_file = f"{strategy_name}_report.csv"
    report_df = generate_strategy_report(ore_name, days, report_file)

    # 如果有报告数据，打印摘要
    if report_df is not None and not report_df.empty:
        strategy_data = report_df[report_df['strategy'] == strategy_name]
        if not strategy_data.empty:
            data = strategy_data.iloc[0]
            print("\n策略表现摘要:")
            print(f"策略名称: {strategy_name}")
            print(f"分析天数: {days}天")
            print(f"平均收益: {data['avg_profit']:.2f}G")
            print(f"最小收益: {data['min_profit']:.2f}G")
            print(f"最大收益: {data['max_profit']:.2f}G")
            print(f"收益波动: {data['std_dev']:.2f} (标准差)")
            print(f"炸矿占比: {data['avg_mining'] / max(data['avg_profit'], 0.01) * 100:.1f}%")
            print(f"分解占比: {data['avg_disenchant'] / max(data['avg_profit'], 0.01) * 100:.1f}%")
            print(f"最新收益: {data['last_profit']:.2f}G")

    return {
        "trend_file": trend_file,
        "report_file": report_file
    }