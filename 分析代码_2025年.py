"""
A股光伏行业ESG表现与股价相关性分析（2025年数据验证）— 完整代码模板
运行环境：Python 3.8+，需安装 pandas, numpy, scipy, matplotlib
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# ==================== 第一步：数据准备 ====================

# 2025年全年股价涨跌幅数据（%）
stock_returns = {
    '隆基绿能': 13.9,
    '通威股份': 11.1,
    '晶科能源': -10.3,
    '晶澳科技': 6.1,
    '天合光能': 13.5,
    'TCL中环': -3.4,
    '阳光电源': 81.8,
    '阿特斯': 26.1
}

# 2024年年报ESG指标数据
esg_data = {
    '隆基绿能': {'碳排放强度': 0.82, '研发投入占比': 5.5, '员工培训时长': 48, '独立董事比例': 42.9, 'ESG评级': 'A'},
    '通威股份': {'碳排放强度': 1.08, '研发投入占比': 3.9, '员工培训时长': 40, '独立董事比例': 36.4, 'ESG评级': 'BBB'},
    '晶科能源': {'碳排放强度': 0.70, '研发投入占比': 6.0, '员工培训时长': 54, '独立董事比例': 44.4, 'ESG评级': 'A'},
    '晶澳科技': {'碳排放强度': 0.76, '研发投入占比': 5.6, '员工培训时长': 50, '独立董事比例': 40.0, 'ESG评级': 'A'},
    '天合光能': {'碳排放强度': 0.88, '研发投入占比': 5.1, '员工培训时长': 44, '独立董事比例': 38.5, 'ESG评级': 'BBB'},
    'TCL中环': {'碳排放强度': 1.02, '研发投入占比': 4.3, '员工培训时长': 36, '独立董事比例': 37.5, 'ESG评级': 'BBB'},
    '阳光电源': {'碳排放强度': 0.42, '研发投入占比': 8.0, '员工培训时长': 60, '独立董事比例': 45.5, 'ESG评级': 'AA'},
    '阿特斯': {'碳排放强度': 0.65, '研发投入占比': 6.0, '员工培训时长': 52, '独立董事比例': 42.9, 'ESG评级': 'A'}
}

# 构建DataFrame
companies = list(stock_returns.keys())
df = pd.DataFrame({
    '公司': companies,
    '股价涨跌幅_2025': [stock_returns[c] for c in companies],
    '碳排放强度': [esg_data[c]['碳排放强度'] for c in companies],
    '研发投入占比': [esg_data[c]['研发投入占比'] for c in companies],
    '员工培训时长': [esg_data[c]['员工培训时长'] for c in companies],
    '独立董事比例': [esg_data[c]['独立董事比例'] for c in companies],
    'ESG评级': [esg_data[c]['ESG评级'] for c in companies]
})

rating_map = {'AA': 5, 'A': 4, 'BBB': 3}
df['ESG评级数值'] = df['ESG评级'].map(rating_map)

print("=== 2025年版本数据汇总 ===")
print(df.to_string(index=False))
print()

# ==================== 第二步：相关性分析 ====================

print("=== Pearson相关性分析 ===")
esg_indicators = {
    'ESG评级数值': df['ESG评级数值'],
    '碳排放强度': df['碳排放强度'],
    '研发投入占比': df['研发投入占比'],
    '员工培训时长': df['员工培训时长'],
    '独立董事比例': df['独立董事比例']
}

for name, values in esg_indicators.items():
    corr, p = stats.pearsonr(values, df['股价涨跌幅_2025'])
    sig = '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else 'ns'
    print(f"{name:12s}: r = {corr:+.3f}, p = {p:.3f} [{sig}]")

print()

# ==================== 第三步：可视化 ====================

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('A股光伏行业ESG表现与股价相关性分析（2025年）', fontsize=16, fontweight='bold', y=1.02)

# 左图：柱状图
ax1 = axes[0]
x = np.arange(len(df))
width = 0.35
bars1 = ax1.bar(x - width/2, df['股价涨跌幅_2025'], width, label='2025年股价涨跌幅(%)',
                color=['#e74c3c' if v < 0 else '#27ae60' for v in df['股价涨跌幅_2025']], alpha=0.8)
ax1.set_ylabel('股价涨跌幅 (%)', color='#2c3e50')
ax1.set_xticks(x)
ax1.set_xticklabels(df['公司'], rotation=45, ha='right')
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.set_ylim(-20, 100)

ax1_twin = ax1.twinx()
bars2 = ax1_twin.bar(x + width/2, df['ESG评级数值'], width, label='ESG评级', color='#3498db', alpha=0.7)
ax1_twin.set_ylabel('ESG评级数值', color='#3498db')
ax1_twin.set_ylim(0, 6)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax1.set_title('各公司ESG评级 vs 股价涨跌幅')
ax1.grid(axis='y', alpha=0.3)

# 右图：散点图
ax2 = axes[1]
scatter = ax2.scatter(df['研发投入占比'], df['股价涨跌幅_2025'],
                     s=200, c=df['ESG评级数值'], cmap='RdYlGn',
                     edgecolors='black', linewidth=1.5, alpha=0.8)

for _, row in df.iterrows():
    ax2.annotate(row['公司'], (row['研发投入占比'], row['股价涨跌幅_2025']),
                xytext=(5, 5), textcoords='offset points', fontsize=9)

z = np.polyfit(df['研发投入占比'], df['股价涨跌幅_2025'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['研发投入占比'].min()-0.3, df['研发投入占比'].max()+0.3, 100)
ax2.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='趋势线 (r=0.76)')

cbar = plt.colorbar(scatter, ax=ax2)
cbar.set_label('ESG评级')
cbar.set_ticks([3, 4, 5])
cbar.set_ticklabels(['BBB', 'A', 'AA'])

ax2.set_xlabel('研发投入占比 (%)')
ax2.set_ylabel('2025年股价涨跌幅 (%)')
ax2.set_title('研发投入占比 vs 股价涨跌幅')
ax2.grid(True, alpha=0.3)
ax2.legend(loc='lower right')

plt.tight_layout()
plt.savefig('esg_pv_report_2025.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n报告已保存为 esg_pv_report_2025.png")
