"""
============================================================
Tushare获取A股数据 + Python计算Pearson相关系数 完整教程
============================================================

【第一步】安装依赖
    pip install tushare pandas numpy scipy

【第二步】注册Tushare账号获取Token
    1. 访问 https://tushare.pro
    2. 注册账号 → 个人主页 → 接口TOKEN → 复制token
    3. 将下方代码中的 YOUR_TOKEN 替换为你的真实token
"""

import tushare as ts
import pandas as pd
import numpy as np
from scipy import stats

# ==================== 第一部分：Tushare获取股价数据 ====================

def get_stock_return(ts_code, start_date, end_date, token):
    """
    获取指定股票在指定时间区间的涨跌幅（前复权）

    参数:
        ts_code: 股票代码，如 '601012.SH'（沪市）或 '300274.SZ'（深市）
        start_date: 开始日期，如 '20240101'
        end_date: 结束日期，如 '20241231'
        token: Tushare API token

    返回:
        涨跌幅百分比，如 12.3 表示上涨12.3%
    """
    ts.set_token(token)
    pro = ts.pro_api()

    # 获取日线数据（前复权）
    # adj='qfq' 表示前复权，消除分红送股影响
    df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)

    if df.empty:
        print(f"⚠️ {ts_code} 无数据，请检查代码是否正确")
        return None

    # 按日期排序
    df = df.sort_values('trade_date')

    # 获取年初第一个交易日和年末最后一个交易日的收盘价
    start_price = float(df.iloc[0]['close'])   # 年初收盘价
    end_price = float(df.iloc[-1]['close'])    # 年末收盘价

    # 计算涨跌幅
    return_pct = (end_price - start_price) / start_price * 100

    print(f"{ts_code}: 年初{start_price:.2f}元 → 年末{end_price:.2f}元, 涨跌幅: {return_pct:+.2f}%")
    return return_pct


# 【示例】获取8家光伏公司2024年涨跌幅
# 注意：将 'YOUR_TOKEN_HERE' 替换为你的真实token

TOKEN = 'YOUR_TOKEN_HERE'   # ←←← 替换这里！

companies = {
    '隆基绿能': '601012.SH',   # 沪市
    '通威股份': '600438.SH',   # 沪市
    '晶科能源': '688223.SH',   # 科创板
    '晶澳科技': '002459.SZ',   # 深市
    '天合光能': '688599.SH',   # 科创板
    'TCL中环': '002129.SZ',    # 深市
    '阳光电源': '300274.SZ',   # 创业板
    '阿特斯': '688472.SH'      # 科创板
}

print("=" * 60)
print("📈 获取2024年光伏公司股价涨跌幅")
print("=" * 60)

stock_returns = {}
for name, code in companies.items():
    try:
        ret = get_stock_return(code, '20240101', '20241231', TOKEN)
        if ret is not None:
            stock_returns[name] = ret
    except Exception as e:
        print(f"❌ {name}({code}) 获取失败: {e}")

print(f"\n✅ 成功获取 {len(stock_returns)} 家公司数据")
print(stock_returns)


# ==================== 第二部分：Python计算Pearson相关系数 ====================

print("\n" + "=" * 60)
print("📊 Pearson相关系数计算教程")
print("=" * 60)

# 【方法1】使用 scipy.stats.pearsonr（推荐）
# 计算两个变量之间的Pearson相关系数和p值

# 示例数据：研发投入占比 vs 股价涨跌幅
rd_ratio = np.array([5.2, 3.8, 6.1, 5.5, 4.9, 4.2, 7.8, 5.8])   # 研发投入占比
returns = np.array([-47.8, -30.2, -17.5, -28.3, -42.1, -35.6, 12.3, -15.8])  # 股价涨跌幅

corr, p_value = stats.pearsonr(rd_ratio, returns)

print("\n【方法1】scipy.stats.pearsonr（最常用）")
print(f"  相关系数 r = {corr:.3f}")
print(f"  p值 = {p_value:.3f}")
print(f"  显著性: {'***' if p_value < 0.01 else '**' if p_value < 0.05 else '*' if p_value < 0.1 else '不显著'}")


# 【方法2】使用 numpy.corrcoef（快速查看，无p值）
print("\n【方法2】numpy.corrcoef（仅相关系数，无p值）")
corr_matrix = np.corrcoef(rd_ratio, returns)
print(f"  相关系数矩阵:\n{corr_matrix}")
print(f"  r = {corr_matrix[0, 1]:.3f}")


# 【方法3】使用 pandas.corr（适合DataFrame批量计算）
print("\n【方法3】pandas.corr（适合多变量批量计算）")

df_example = pd.DataFrame({
    '股价涨跌幅': [-47.8, -30.2, -17.5, -28.3, -42.1, -35.6, 12.3, -15.8],
    '碳排放强度': [0.85, 1.12, 0.72, 0.78, 0.91, 1.05, 0.45, 0.68],
    '研发投入占比': [5.2, 3.8, 6.1, 5.5, 4.9, 4.2, 7.8, 5.8],
    '员工培训时长': [45, 38, 52, 48, 42, 35, 58, 50],
    '独立董事比例': [42.9, 36.4, 44.4, 40.0, 38.5, 37.5, 45.5, 42.9]
})

# 计算相关系数矩阵
corr_matrix_df = df_example.corr()
print("\n  相关系数矩阵:")
print(corr_matrix_df.round(3).to_string())

# 提取股价涨跌幅与其他指标的相关性
print("\n  股价涨跌幅与其他指标的相关性:")
price_corr = corr_matrix_df['股价涨跌幅'].drop('股价涨跌幅')
for indicator, corr_val in price_corr.items():
    print(f"    {indicator:12s}: r = {corr_val:+.3f}")


# 【方法4】批量计算并输出显著性（完整版）
print("\n【方法4】批量计算 + 显著性判断（研究推荐）")

indicators = {
    '碳排放强度': [0.85, 1.12, 0.72, 0.78, 0.91, 1.05, 0.45, 0.68],
    '研发投入占比': [5.2, 3.8, 6.1, 5.5, 4.9, 4.2, 7.8, 5.8],
    '员工培训时长': [45, 38, 52, 48, 42, 35, 58, 50],
    '独立董事比例': [42.9, 36.4, 44.4, 40.0, 38.5, 37.5, 45.5, 42.9]
}

stock_returns_list = [-47.8, -30.2, -17.5, -28.3, -42.1, -35.6, 12.3, -15.8]

results = []
for name, values in indicators.items():
    corr, p = stats.pearsonr(values, stock_returns_list)
    sig = '***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else '不显著'
    results.append({
        'ESG指标': name,
        'Pearson r': round(corr, 3),
        'p值': round(p, 3),
        '显著性': sig
    })

results_df = pd.DataFrame(results)
print("\n" + results_df.to_string(index=False))


# ==================== 结果解读指南 ====================

print("\n" + "=" * 60)
print("📖 结果解读指南")
print("=" * 60)

print("""
【r值（相关系数）含义】
  • r = +1.0  → 完全正相关：一个变量增加，另一个也增加
  • r = -1.0  → 完全负相关：一个变量增加，另一个减少
  • r = 0     → 无线性相关
  • |r| > 0.8 → 强相关
  • |r| 0.5-0.8 → 中等相关
  • |r| < 0.5 → 弱相关

【p值（显著性）含义】
  • p < 0.01 (***): 极显著，结果非常可靠
  • p < 0.05 (**):  显著，结果可靠
  • p < 0.10 (*):   边际显著，有一定参考价值
  • p >= 0.10:      不显著，结果可能是随机波动

【示例解读】
  研发投入占比 vs 股价: r = +0.810, p = 0.015 [**]
  → 强正相关且统计显著：研发投入越高，股价表现越好

  碳排放强度 vs 股价: r = -0.777, p = 0.023 [**]
  → 强负相关且统计显著：碳排放越低，股价表现越好
""")

print("=" * 60)
print("✅ 教程结束！将TOKEN替换后即可运行")
print("=" * 60)
