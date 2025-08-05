from calculator import ProfitCalculator
from market_parser import parse_market_data

# 测试数据
test_data = '''
"价格","名称","物品等级","我的售品？","可购买"
120000,"幽冥铁矿石",86,"",38950
880000,"日曜石",90,"",19
4799998,"朱砂玛瑙",90,"",275
339992,"河心石",90,"",70
4989840,"源红石",90,"",81
3994198,"皇紫晶",90,"",82
4150000,"荒玉",90,"",123
299998,"潘达利亚榴石",87,"是",775
90000,"青金石",87,"是",1187
399998,"日长石",87,"是",1298
420000,"虎纹石",87,"是",1062
16000,"紫翠玉",87,"是",1195
299997,"劣生石",87,"是",757
68897,"精巧的铜线",20,"",146
9500,"孔雀石",7,"",308
9900,"虎眼石",15,"",103
58694,"铜矿石",10,"",7647
58700,"奇异之尘",10,"是",1177
169000,"强效魔法精华",15,"",281
3496,"小块微光碎片",20,"",328
'''

# 解析市场数据
market_data = parse_market_data(test_data)

# 创建计算器
calculator = ProfitCalculator(market_data)

# 测试计算
results = calculator.evaluate_strategies("铜矿石")
print("\n测试结果:")
print(f"最优策略: {results['best_strategy']}")
print(f"策略总收益: {results['strategy_profit_g']:.4f}G")
print(f"炸矿收益: {results['mining_profit_g']:.4f}G")
print(f"分解收益: {results['disenchant_profit_g']:.4f}G")

# 打印所有策略
if "all_strategies" in results:
    print("\n所有策略收益:")
    for strategy, data in results["all_strategies"].items():
        print(f"  - {strategy}: {data['profit']:.4f}G")