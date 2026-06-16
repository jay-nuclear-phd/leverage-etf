import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd

# 1. 한글 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
plt.rc('font', family='NanumGothic')

# 2. 데이터 준비
data = {
    'Year': [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
             2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
    'ExchangeRate': [929.8, 936.1, 1259.5, 1164.5, 1134.8, 1151.8, 1070.6, 1055.4, 1099.3, 1172.5,
                     1207.7, 1070.5, 1115.7, 1156.4, 1086.3, 1188.8, 1264.5, 1288.0, 1472.5, 1439.0],
    'BigMac_USD': [2.56, 3.08, 3.14, 2.59, 2.98, 3.5, 3.19, 3.41, 3.47, 3.78,
                   3.59, 3.68, 4.12, 4.02, 3.89, 4.1, 3.82, 3.97, 4.11, 3.84],
    'InterestRate': [4.54, 5.25, 5.98, 3.85, 3.58, 3.96, 3.48, 2.81, 2.45, 1.78,
                     1.54, 1.65, 1.99, 1.76, 1.07, 1.28, 3.63, 3.86, 3.44, 2.76]
}
df = pd.DataFrame(data)

# 3. 값 계산
df['BigMac_KRW'] = df['ExchangeRate'] * df['BigMac_USD']
balance = [1000000]
for rate in df['InterestRate']:
    balance.append(balance[-1] * (1 + rate / 100))
df['Investment_Value'] = balance[1:]
df['BigMac_Count'] = df['Investment_Value'] / df['BigMac_KRW']

# 4. 정규화 (Min-Max Scaling and Ratio-based Scaling)
def min_max_scaler(series):
    return (series - series.min()) / (series.max() - series.min())

# Calculate growth ratios for Investment_Value and BigMac_KRW
initial_investment = df['Investment_Value'].iloc[0]
initial_bigmac_krw = df['BigMac_KRW'].iloc[0]

investment_growth_ratio = df['Investment_Value'] / initial_investment
bigmac_krw_growth_ratio = df['BigMac_KRW'] / initial_bigmac_krw

# Determine a common scaling factor based on the maximum growth ratio
# This makes both series start at 0 and the highest growth series end at 1
max_growth_ratio = max(investment_growth_ratio.max(), bigmac_krw_growth_ratio.max())

df['Norm_Invest'] = (investment_growth_ratio - 1) / (max_growth_ratio - 1)
df['Norm_Price'] = (bigmac_krw_growth_ratio - 1) / (max_growth_ratio - 1)

# Keep BigMac_Count normalization as original min-max scaling
df['Norm_Count'] = min_max_scaler(df['BigMac_Count'])

# 5. 그래프 그리기
plt.figure(figsize=(14, 9))
ms = 12

plt.plot(df['Year'], df['Norm_Invest'], marker='s', markersize=ms, label='예금 자산 (원)', color='blue')
plt.plot(df['Year'], df['Norm_Price'], marker='o', markersize=ms, label='빅맥 가격 (원)', color='red')
plt.plot(df['Year'], df['Norm_Count'], marker='^', markersize=ms, label='구매 가능 개수', color='green')

plt.xticks(range(2006, 2027, 1), fontsize=14)
plt.xlabel('연도', fontsize = 18)
plt.yticks([])

# 상하 여백 설정
plt.ylim(-0.1, 1.1)

anno_font_size = 12
# 실제 데이터 값 표기
for i in range(len(df)):
    plt.annotate(f"{df['Investment_Value'][i]/10000:.0f}만", (df['Year'][i], df['Norm_Invest'][i]),
                 textcoords="offset points", xytext=(0,15), ha='center', fontsize=anno_font_size, color='blue')

    # Conditionally adjust xytext for BigMac_KRW for specific years
    if df['Year'][i] in [2008, 2009, 2011, 2015, 2021, 2024]:
        plt.annotate(f"{df['BigMac_KRW'][i]:.0f}", (df['Year'][i], df['Norm_Price'][i]),
                     textcoords="offset points", xytext=(0,15), ha='center', fontsize=anno_font_size, color='red')
    else:
        plt.annotate(f"{df['BigMac_KRW'][i]:.0f}", (df['Year'][i], df['Norm_Price'][i]),
                     textcoords="offset points", xytext=(0,-20), ha='center', fontsize=anno_font_size, color='red')

    # Conditionally adjust xytext for BigMac_Count for specific years
    if df['Year'][i] in [2008, 2015, 2018, 2019, 2021, 2022, 2024]:
        plt.annotate(f"{df['BigMac_Count'][i]:.0f}", (df['Year'][i], df['Norm_Count'][i]),
                     textcoords="offset points", xytext=(0,-20), ha='center', fontsize=anno_font_size, color='green')
    else:
        plt.annotate(f"{df['BigMac_Count'][i]:.0f}", (df['Year'][i], df['Norm_Count'][i]),
                     textcoords="offset points", xytext=(0,15), ha='center', fontsize=anno_font_size, color='green')

# 범례 상단 중앙 배치
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.), ncol=3, fontsize=16, frameon=True)

plt.grid(True, axis='x', linestyle='--')
plt.tight_layout()

plt.savefig("bigmac_index.png", dpi=300, bbox_inches="tight")

plt.show()