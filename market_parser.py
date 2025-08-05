import csv
from io import StringIO
from collections import namedtuple

MarketItem = namedtuple('MarketItem', ['name', 'price', 'available'])


def parse_market_data(text_data):
    """
    解析市场数据文本
    格式："价格","名称","物品等级","我的售品？","可购买"
    """
    market_data = {}
    f = StringIO(text_data)
    reader = csv.reader(f)

    # 尝试跳过标题行
    try:
        headers = next(reader)  # 读取标题行
        # 验证标题行
        if len(headers) > 0 and "价格" in headers[0]:
            print(f"已跳过标题行: {headers}")
        else:
            # 如果没有标题行，重置reader
            f.seek(0)
            reader = csv.reader(f)
    except StopIteration:
        return market_data

    for row in reader:
        # 跳过空行
        if not row or len(row) < 5:
            continue

        try:
            # 提取价格列（第一列）
            price_str = row[0].strip().replace(',', '').replace('"', '')
            # 确保价格是数字
            if not price_str.isdigit():
                print(f"跳过非数字价格行: {row}")
                continue

            price = int(price_str)
            name = row[1].strip().strip('"')

            # 处理可购买数量列（第五列）
            available_str = row[4].strip().replace('"', '')
            available = int(available_str) if available_str.isdigit() else 0

            market_data[name] = MarketItem(name, price, available)
        except (ValueError, IndexError) as e:
            print(f"解析行时出错: {row} - {str(e)}")
            continue

    return market_data