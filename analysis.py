import pandas as pd
import matplotlib.pyplot as plt

# 加载报告数据
df = pd.read_csv('data/reports/mining_report.csv')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# 按小时聚合
df_hourly = df.resample('H', on='Timestamp').mean()

# 绘制收益趋势
plt.figure(figsize=(14, 8))
plt.plot(df_hourly.index, df_hourly['Strategy Profit(G)'], label='总收益')
plt.plot(df_hourly.index, df_hourly['Mining Hourly(G)'], label='炸矿收益')
plt.plot(df_hourly.index, df_hourly['Disenchant Hourly(G)'], label='分解收益')
plt.title('每小时收益趋势')
plt.xlabel('时间')
plt.ylabel('收益 (G)')
plt.legend()
plt.grid(True)
plt.show()

# 分析最优策略分布
strategy_counts = df['Best Strategy'].value_counts()
plt.figure(figsize=(10, 6))
strategy_counts.plot(kind='bar')
plt.title('最优策略分布')
plt.xlabel('策略')
plt.ylabel('次数')
plt.show()