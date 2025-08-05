import os

# 基础配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
HISTORY_DIR = os.path.join(DATA_DIR, "market_history")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")

# 确保目录存在
os.makedirs(HISTORY_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(os.path.join(HISTORY_DIR, "items"), exist_ok=True)

# 炸矿配方
MINING_RECIPES = {
    "幽冥铁矿石": [
        ("日曜石", 0.0091),
        ("朱砂玛瑙", 0.0091),
        ("河心石", 0.0091),
        ("源红石", 0.0091),
        ("皇紫晶", 0.0091),
        ("荒玉", 0.0091),
        ("潘达利亚榴石", 0.0494),
        ("青金石", 0.0494),
        ("日长石", 0.0494),
        ("虎纹石", 0.0494),
        ("紫翠玉", 0.0494),
        ("劣生石", 0.0494)
    ],
    "铜矿石": [
        ("孔雀石", 0.1),
        ("虎眼石", 0.1),
        ("暗影石", 0.02)
    ]
}

# 制作配方
CRAFTING_RECIPES = {
    "雕饰指环": {
        "materials": {"日长石": 1, "青金石": 1, "虎纹石": 1},
        "cost": 1.5
    },
    "影火项链": {
        "materials": {"劣生石": 1, "潘达利亚榴石": 1, "紫翠玉": 1},
        "cost": 1.5
    },
    "孔雀石坠饰": {
        "materials": {"孔雀石": 1, "精巧的铜线": 1},
        "cost": 0
    },
    "虎眼指环": {
        "materials": {"虎眼石": 1, "精巧的铜线": 1},
        "cost": 0
    }
}

# 分解配方
DISENCHANT_RESULTS = {
    "雕饰指环": {"神秘精华": 0.178, "灵魂尘": 2.285},
    "影火项链": {"神秘精华": 0.178, "灵魂尘": 2.285},
    "孔雀石坠饰": {"奇异之尘": 1.85, "强效魔法精华": 0.3, "小块微光碎片": 0.05},
    "虎眼指环": {"奇异之尘": 1.85, "强效魔法精华": 0.3, "小块微光碎片": 0.05}
}

# 系统参数
TAX_RATE = 0.05  # 5% 税收
MINING_TIME_PER_ORE = 0.4  # 秒/次
CRAFTING_TIME = 5  # 秒/次（制作+分解）
CRIT_RATE = 0.2  # 20% 暴击概率