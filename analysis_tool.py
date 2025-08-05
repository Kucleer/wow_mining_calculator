import argparse
from chart_generator import generate_price_chart, generate_availability_chart, generate_correlation_chart


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

    args = parser.parse_args()

    if args.command == "price":
        generate_price_chart(args.items, args.days, args.output)
    elif args.command == "availability":
        generate_availability_chart(args.items, args.days, args.output)
    elif args.command == "correlation":
        generate_correlation_chart(args.item1, args.item2, args.days, args.output)
    else:
        print("请指定有效命令: price, availability 或 correlation")


if __name__ == "__main__":
    main()