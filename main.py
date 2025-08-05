import time
from datetime import datetime
from market_parser import parse_market_data
from calculator import ProfitCalculator
from report_generator import generate_report_entry, save_report_entry
from history_recorder import record_market_data, record_all_strategies
import config


def main():
    print("魔兽世界炸矿与市场分析系统")
    print("=" * 70)
    print("功能:")
    print("1. 炸矿收益计算")
    print("2. 市场数据历史记录")
    print("3. 策略收益跟踪")
    print("4. 图表分析 (单独运行 analysis_tool.py)")
    print("=" * 70)

    while True:
        try:
            print("\n当前时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("请粘贴最新的市场数据（格式参考示例），输入空行结束:")
            print('示例格式：\n"价格","名称","物品等级","我的售品？","可购买"')
            print('129989,"幽冥铁矿石",86,"",43822')
            print('660998,"日曜石",90,"",75')
            print('...')

            # 获取多行输入
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)

            text_data = "\n".join(lines)

            # 解析市场数据
            market_data = parse_market_data(text_data)

            if not market_data:
                print("未解析到有效数据，请检查格式")
                continue

            print(f"成功解析 {len(market_data)} 条市场数据")

            # 记录市场数据到历史文件
            record_market_data(market_data)

            # 创建计算器
            calculator = ProfitCalculator(market_data)

            # 获取当前时间戳（用于记录策略）
            current_timestamp = datetime.now()

            # 对于每种矿石
            for ore_name in config.MINING_RECIPES:
                print(f"\n计算矿石: {ore_name}...")

                try:
                    # 计算收益
                    results = calculator.evaluate_strategies(ore_name)

                    # 生成报告条目
                    timestamp_str = current_timestamp.strftime("%Y-%m-%d %H:%M")
                    entry = generate_report_entry(timestamp_str, ore_name, market_data, results)

                    # 保存报告
                    save_report_entry(entry)

                    # 记录所有策略收益
                    if "all_strategies" in results:
                        record_all_strategies(current_timestamp, ore_name, results["all_strategies"])

                    # 显示结果
                    print("\n" + "=" * 70)
                    print(f"矿石: {ore_name}")
                    print(f"矿石单价: {entry['buy_price_g']:.4f}G")
                    print(f"投入金额: {entry['investment_g']:.4f}G")
                    print(f"炸矿收益: {entry['mining_profit_g']:.4f}G ({entry['mining_profit_pct']:.4f}%)")
                    print(f"炸矿每小时收益: {entry['mining_hourly_g']:.4f}G")
                    print(f"分解收益: {entry['disenchant_profit_g']:.4f}G")
                    print(f"分解每小时收益: {entry['disenchant_hourly_g']:.4f}G")
                    print(f"最优策略: {entry['best_strategy']}")
                    print(f"策略总收益: {entry['strategy_profit_g']:.4f}G")

                    # 显示所有策略（可选）
                    if "all_strategies" in results:
                        print("\n所有策略收益:")
                        for strategy, data in results["all_strategies"].items():
                            print(f"  - {strategy}: {data['profit']:.4f}G")

                    print("=" * 70)
                except Exception as e:
                    print(f"计算矿石 {ore_name} 时出错: {str(e)}")
                    import traceback
                    traceback.print_exc()

            print("\n所有矿石计算完成，数据已保存到报告文件。")
            print("下次更新将在1分钟后...")
            time.sleep(60)  # 每分钟更新一次

        except KeyboardInterrupt:
            print("\n程序已终止")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")
            import traceback
            traceback.print_exc()
            time.sleep(10)


if __name__ == "__main__":
    main()