import argparse
from chart_generator import generate_price_chart, generate_availability_chart, generate_correlation_chart
from strategy_analyzer import (generate_strategy_trend, compare_strategies,
                               generate_strategy_report, analyze_strategy_performance)
import matplotlib as mpl

import matplotlib.pyplot as plt


def set_chinese_font():
    """设置中文字体，返回是否成功"""
    try:
        # 方法1: 直接设置 rcParams（推荐）
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei']
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        # 方法2: 使用 FontProperties 对象（如果需要单独设置）
        # 注意：这里不需要访问 .name 属性
        # chinese_font = fm.FontProperties(fname='path/to/SimHei.ttf')
        # 然后在绘图时使用：plt.title("标题", fontproperties=chinese_font)

        print("中文字体设置成功")
        return True
    except Exception as e:
        print(f"设置中文字体失败: {e}")
        return False

# 在绘图前调用
set_chinese_font()

def main():
    parser = argparse.ArgumentParser(description="魔兽世界市场数据分析工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 价格趋势图命令
    price_parser = subparsers.add_parser("price", help="生成价格趋势图")
    price_parser.add_argument("items", nargs="+", help="物品名称列表")
    price_parser.add_argument("--days", type=int, default=7, help="分析天数 (默认: 7)")
    price_parser.add_argument("--output", default="price_trend.png", help="输出文件名")

    # 可购买数量趋势图命令
    avail_parser = subparsers.add_parser("availability", help="生成可购买数量趋势图")
    avail_parser.add_argument("items", nargs="+", help="物品名称列表")
    avail_parser.add_argument("--days", type=int, default=7, help="分析天数 (默认: 7)")
    avail_parser.add_argument("--output", default="availability_trend.png", help="输出文件名")

    # 价格相关性图命令
    corr_parser = subparsers.add_parser("correlation", help="生成价格相关性图")
    corr_parser.add_argument("item1", help="第一个物品名称")
    corr_parser.add_argument("item2", help="第二个物品名称")
    corr_parser.add_argument("--days", type=int, default=30, help="分析天数 (默认: 30)")
    corr_parser.add_argument("--output", default="price_correlation.png", help="输出文件名")

    # 策略分析命令
    strategy_parser = subparsers.add_parser("strategy", help="策略收益分析")
    strategy_subparsers = strategy_parser.add_subparsers(dest="strategy_command", help="策略分析命令")

    # 策略趋势图
    trend_parser = strategy_subparsers.add_parser("trend", help="生成策略收益趋势图")
    trend_parser.add_argument("strategy", help="策略名称")
    trend_parser.add_argument("--ore", help="矿石名称")
    trend_parser.add_argument("--days", type=int, default=30, help="分析天数 (默认: 30)")
    trend_parser.add_argument("--output", default="strategy_trend.png", help="输出文件名")

    # 策略比较图
    compare_parser = strategy_subparsers.add_parser("compare", help="比较多个策略收益")
    compare_parser.add_argument("strategies", nargs="+", help="策略名称列表")
    compare_parser.add_argument("--ore", help="矿石名称")
    compare_parser.add_argument("--days", type=int, default=30, help="分析天数 (默认: 30)")
    compare_parser.add_argument("--output", default="strategy_comparison.png", help="输出文件名")

    # 策略报告
    report_parser = strategy_subparsers.add_parser("report", help="生成策略表现报告")
    report_parser.add_argument("--ore", help="矿石名称")
    report_parser.add_argument("--days", type=int, default=30, help="分析天数 (默认: 30)")
    report_parser.add_argument("--output", default="strategy_report.csv", help="输出文件名")

    # 完整策略分析
    analyze_parser = strategy_subparsers.add_parser("analyze", help="完整策略分析")
    analyze_parser.add_argument("strategy", help="策略名称")
    analyze_parser.add_argument("--ore", help="矿石名称")
    analyze_parser.add_argument("--days", type=int, default=90, help="分析天数 (默认: 90)")

    args = parser.parse_args()

    if args.command == "price":
        generate_price_chart(args.items, args.days, args.output)
    elif args.command == "availability":
        generate_availability_chart(args.items, args.days, args.output)
    elif args.command == "correlation":
        generate_correlation_chart(args.item1, args.item2, args.days, args.output)
    elif args.command == "strategy":
        if args.strategy_command == "trend":
            generate_strategy_trend(args.strategy, args.ore, args.days, args.output)
        elif args.strategy_command == "compare":
            compare_strategies(args.strategies, args.ore, args.days, args.output)
        elif args.strategy_command == "report":
            generate_strategy_report(args.ore, args.days, args.output)
        elif args.strategy_command == "analyze":
            analyze_strategy_performance(args.strategy, args.ore, args.days)
        else:
            print("请指定有效的策略分析命令: trend, compare, report 或 analyze")
    else:
        print("请指定有效命令: price, availability, correlation 或 strategy")


if __name__ == "__main__":
    main()