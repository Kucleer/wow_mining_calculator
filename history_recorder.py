import csv
import os
from datetime import datetime
from config import HISTORY_DIR


def record_market_data(market_data, timestamp=None):
    """记录市场数据到历史文件"""
    if not market_data:
        return

    if timestamp is None:
        timestamp = datetime.now()

    # 准备完整历史文件路径
    full_history_path = os.path.join(HISTORY_DIR, "full_history.csv")
    os.makedirs(HISTORY_DIR, exist_ok=True)

    # 写入完整历史文件
    file_exists = os.path.isfile(full_history_path)
    with open(full_history_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "item", "price_g", "available"])

        for item in market_data.values():
            price_g = item.price / 10000.0  # 转换为金币
            writer.writerow([
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                item.name,
                f"{price_g:.4f}",
                item.available
            ])

    # 按物品存储单独文件
    items_dir = os.path.join(HISTORY_DIR, "items")
    os.makedirs(items_dir, exist_ok=True)

    for item in market_data.values():
        item_file = os.path.join(items_dir, f"{item.name}.csv")
        file_exists = os.path.isfile(item_file)

        with open(item_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "price_g", "available"])

            price_g = item.price / 10000.0
            writer.writerow([
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                f"{price_g:.4f}",
                item.available
            ])

    print(f"已记录 {len(market_data)} 条物品数据到历史文件")