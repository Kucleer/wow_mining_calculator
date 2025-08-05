from strategy import StrategyEvaluator  # 修改为绝对导入
from config import MINING_TIME_PER_ORE  # 确保从 config 导入所需变量


class ProfitCalculator:
    def __init__(self, market_data):
        self.market_data = market_data
        # 精确计算每小时炸矿次数
        self.mining_cycles_per_hour = int(3600 / MINING_TIME_PER_ORE)
        # 策略评估器
        self.strategy_evaluator = StrategyEvaluator(market_data)

    def simulate_mining(self, ore_name, cycles):
        """模拟炸矿过程"""
        from config import MINING_RECIPES  # 在函数内部导入

        if ore_name not in MINING_RECIPES:
            return {}

        results = {}
        recipe = MINING_RECIPES[ore_name]

        # 使用更精确的浮点数计算
        for item, prob in recipe:
            expected_quantity = float(prob) * float(cycles)
            results[item] = expected_quantity

        return results

    def calculate_mining_profit(self, ore_name):
        """计算炸矿收益"""
        if ore_name not in self.market_data:
            return 0.0, 0.0, 0.0, {}

        ore_price = float(self.market_data[ore_name].price)
        mining_results = self.simulate_mining(ore_name, self.mining_cycles_per_hour)

        # 计算炸矿收益
        mining_profit = 0.0
        for item, quantity in mining_results.items():
            if item in self.market_data:
                item_price = float(self.market_data[item].price)
                item_price_after_tax = self.strategy_evaluator.calculate_after_tax(item_price)
                mining_profit += item_price_after_tax * quantity

        # 计算矿石总成本
        total_ore_cost = ore_price * self.mining_cycles_per_hour

        # 净收益
        net_mining_profit = mining_profit - total_ore_cost
        mining_profit_pct = (net_mining_profit / total_ore_cost) * 100.0 if total_ore_cost > 0 else 0.0

        # 转换为金币
        net_mining_profit_g = net_mining_profit / 10000.0
        mining_hourly_g = net_mining_profit_g

        return net_mining_profit_g, mining_profit_pct, mining_hourly_g, mining_results

    def evaluate_strategies(self, ore_name):
        """评估所有策略"""
        # 炸矿收益
        mining_profit_g, mining_profit_pct, mining_hourly_g, mining_results = self.calculate_mining_profit(ore_name)

        # 评估所有策略
        all_strategies, best_strategy_name, best_profit = self.strategy_evaluator.evaluate_all_strategies(
            ore_name, mining_results
        )

        # 提取最优策略的分解收益
        disenchant_profit_g = 0.0
        if best_strategy_name != "纯炸矿":
            # 策略利润 - 炸矿利润 = 分解收益
            disenchant_profit_g = best_profit - mining_profit_g

        return {
            "mining_profit_g": mining_profit_g,
            "mining_profit_pct": mining_profit_pct,
            "mining_hourly_g": mining_hourly_g,
            "disenchant_profit_g": disenchant_profit_g,
            "disenchant_hourly_g": disenchant_profit_g,  # 无时间消耗，所以等于总收益
            "best_strategy": best_strategy_name,
            "strategy_profit_g": best_profit,
            "all_strategies": all_strategies  # 用于调试
        }