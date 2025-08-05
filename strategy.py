from config import MINING_RECIPES, CRAFTING_RECIPES, DISENCHANT_RESULTS
from config import TAX_RATE, CRIT_RATE, MINING_TIME_PER_ORE


class StrategyEvaluator:
    def __init__(self, market_data):
        self.market_data = market_data
        # 计算每小时最大制作次数
        self.max_crafts_per_hour = 720  # 3600/5=720

    def calculate_after_tax(self, value, is_purchase=False):
        """计算税后价值"""
        if is_purchase:
            return value  # 采购不扣税
        return value * (1.0 - TAX_RATE)  # 出售扣税

    def calculate_crafting_profit(self, recipe_name, material_quantities={}, max_crafts_limit=None):
        """计算制作+分解收益 - 修复成本计算"""
        if recipe_name not in CRAFTING_RECIPES:
            return 0.0, 0.0

        recipe = CRAFTING_RECIPES[recipe_name]

        # 计算可制作次数（受材料限制）
        max_craft = float('inf')
        for material, needed in recipe['materials'].items():
            available = material_quantities.get(material, 0)
            # 避免除零错误
            if needed <= 0:
                continue
            max_craft = min(max_craft, available / needed)

        # 应用制作次数限制
        if max_crafts_limit is not None:
            max_craft = min(max_craft, max_crafts_limit)

        # 考虑暴击概率
        expected_craft = max_craft * (1 + CRIT_RATE)

        # 计算分解收益（税后）
        disenchant_profit = 0.0
        if recipe_name in DISENCHANT_RESULTS:
            disenchant_results = DISENCHANT_RESULTS[recipe_name]
            for material, quantity in disenchant_results.items():
                if material in self.market_data:
                    material_price = float(self.market_data[material].price)
                    # 分解产物出售需扣税
                    material_price_after_tax = self.calculate_after_tax(material_price)
                    disenchant_profit += material_price_after_tax * quantity * expected_craft

        # 减去制作成本（金币转换为铜币）
        crafting_cost = recipe['cost'] * 10000 * max_craft

        # 材料机会成本（正确计算采购成本）
        material_opportunity_cost = 0.0
        for material, needed in recipe['materials'].items():
            if material in self.market_data:
                material_price = float(self.market_data[material].price)

                # 判断材料来源
                is_purchased = True  # 默认视为采购

                # 如果是炸矿材料且数量充足
                if material in material_quantities and material_quantities[material] >= needed * max_craft:
                    # 使用炸矿材料的机会成本（税后）
                    material_price_after_tax = self.calculate_after_tax(material_price)
                    is_purchased = False
                else:
                    # 采购材料成本（税前）
                    material_price_after_tax = material_price

                material_opportunity_cost += material_price_after_tax * needed * max_craft

        # 净收益
        net_disenchant_profit = disenchant_profit - crafting_cost - material_opportunity_cost
        disenchant_profit_g = net_disenchant_profit / 10000.0  # 转换为金币

        return disenchant_profit_g, disenchant_profit_g  # 每小时收益=总收益（无时间消耗）

    def evaluate_purchase_strategy(self, recipe_name):
        """评估采购+制作策略 - 添加制作次数限制"""
        # 假设可以无限采购材料
        material_quantities = {}
        for material in CRAFTING_RECIPES[recipe_name]['materials']:
            material_quantities[material] = float('inf')  # 无限供应

        return self.calculate_crafting_profit(recipe_name, material_quantities, self.max_crafts_per_hour)

    def evaluate_hybrid_strategy(self, recipe_name, mining_materials):
        """评估混合策略（炸矿材料+采购补充） - 添加制作次数限制"""
        # 复制炸矿材料数据
        material_quantities = mining_materials.copy()

        # 对于配方中需要的材料，如果炸矿产出不足，假设可以采购补充
        for material in CRAFTING_RECIPES[recipe_name]['materials']:
            if material not in material_quantities:
                material_quantities[material] = float('inf')  # 无限供应

        return self.calculate_crafting_profit(recipe_name, material_quantities, self.max_crafts_per_hour)

    def evaluate_all_strategies(self, ore_name, mining_results):
        """评估所有策略 - 修复纯采购策略比较"""
        strategies = {}

        # 1. 纯炸矿策略
        mining_profit = 0.0
        ore_price = 0.0

        # 获取矿石价格
        if ore_name in self.market_data:
            ore_price = float(self.market_data[ore_name].price)

        # 计算炸矿成本
        mining_cost = 0.0

        # 计算炸矿收益（税后）
        for item, quantity in mining_results.items():
            if item in self.market_data:
                item_price = float(self.market_data[item].price)
                item_price_after_tax = self.calculate_after_tax(item_price)
                mining_profit += item_price_after_tax * quantity

        # 计算矿石成本（每小时）
        mining_cycles_per_hour = int(3600 / MINING_TIME_PER_ORE)
        mining_cost = ore_price * mining_cycles_per_hour

        # 炸矿净收益
        net_mining_profit = mining_profit - mining_cost
        mining_profit_g = net_mining_profit / 10000.0

        strategies["纯炸矿"] = {
            "profit": mining_profit_g,
            "type": "mining"
        }

        # 2. 炸矿+制作策略
        for recipe_name in CRAFTING_RECIPES:
            # 检查配方是否使用该矿石的产出材料
            recipe_materials = CRAFTING_RECIPES[recipe_name]['materials']
            if any(material in mining_results for material in recipe_materials):
                # 2a. 仅使用炸矿材料
                profit_g, _ = self.calculate_crafting_profit(recipe_name, mining_results, self.max_crafts_per_hour)
                strategy_name = f"炸矿+制作{recipe_name}"
                strategies[strategy_name] = {
                    "profit": mining_profit_g + profit_g,
                    "type": "crafting"
                }

                # 2b. 混合策略（炸矿材料+采购补充）
                hybrid_profit_g, _ = self.evaluate_hybrid_strategy(recipe_name, mining_results)
                hybrid_strategy_name = f"混合+制作{recipe_name}"
                strategies[hybrid_strategy_name] = {
                    "profit": mining_profit_g + hybrid_profit_g,
                    "type": "hybrid"
                }

        # 3. 纯采购+制作策略（独立于炸矿）
        for recipe_name in CRAFTING_RECIPES:
            profit_g, _ = self.evaluate_purchase_strategy(recipe_name)
            strategy_name = f"采购+制作{recipe_name}"
            strategies[strategy_name] = {
                "profit": profit_g,  # 纯采购策略不依赖炸矿收益
                "type": "purchase"
            }

        # 寻找最优策略
        best_strategy_name = "纯炸矿"
        best_profit = mining_profit_g

        for strategy_name, strategy_data in strategies.items():
            # 纯采购策略独立比较
            if strategy_data["type"] == "purchase":
                if strategy_data["profit"] > best_profit:
                    best_strategy_name = strategy_name
                    best_profit = strategy_data["profit"]
            # 其他策略基于炸矿收益
            elif strategy_data["profit"] > best_profit:
                best_strategy_name = strategy_name
                best_profit = strategy_data["profit"]

        return strategies, best_strategy_name, best_profit