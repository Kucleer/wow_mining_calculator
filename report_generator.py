import csv
import os
from datetime import datetime


def generate_report_entry(timestamp, ore_name, market_data, results):
    """生成报告条目"""
    ore_item = market_data.get(ore_name)
    ore_price_g = ore_item.price / 10000 if ore_item else 0.0

    # 计算投入金额（矿石总成本）
    investment = ore_price_g * results.get("mining_cycles", 9000)

    return {
        "timestamp": timestamp,
        "ore_name": ore_name,
        "investment_g": round(investment, 4),
        "buy_price_g": round(ore_price_g, 4),
        "mining_profit_g": round(results["mining_profit_g"], 4),
        "mining_profit_pct": round(results["mining_profit_pct"], 4),
        "mining_hourly_g": round(results["mining_hourly_g"], 4),
        "disenchant_profit_g": round(results["disenchant_profit_g"], 4),
        "disenchant_hourly_g": round(results["disenchant_hourly_g"], 4),
        "best_strategy": results["best_strategy"],
        "strategy_profit_g": round(results["strategy_profit_g"], 4)
    }


def save_report_entry(entry, filename="data/reports/mining_report.csv"):
    """保存报告条目到CSV"""
    file_exists = os.path.isfile(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Timestamp", "Ore", "Investment(G)", "Buy Price(G)", "Mining Profit(G)",
                "Mining Profit(%)", "Mining Hourly(G)", "Disenchant Profit(G)",
                "Disenchant Hourly(G)", "Best Strategy", "Strategy Profit(G)"
            ])

        writer.writerow([
            entry["timestamp"],
            entry["ore_name"],
            f"{entry['investment_g']:.4f}",
            f"{entry['buy_price_g']:.4f}",
            f"{entry['mining_profit_g']:.4f}",
            f"{entry['mining_profit_pct']:.4f}",
            f"{entry['mining_hourly_g']:.4f}",
            f"{entry['disenchant_profit_g']:.4f}",
            f"{entry['disenchant_hourly_g']:.4f}",
            entry["best_strategy"],
            f"{entry['strategy_profit_g']:.4f}"
        ])