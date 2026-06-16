import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import platform

# ==========================================
# 1. 기본 설정
# ==========================================
# matplotlib 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 2. 데이터 불러오기
# ==========================================
file_path = 'WID_Data.xlsx'
sheet_name = 'PerCapitaGDP'

df = pd.read_excel(file_path, sheet_name=sheet_name)

# 열 이름 강제 재설정
cols = list(df.columns)
cols[0] = 'Year'
df.columns = cols

# ==========================================
# 3. 데이터 전처리 (1980-2024)
# ==========================================
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df_filtered = df.dropna(subset=['Year']).sort_values('Year').copy()
df_filtered = df_filtered[(df_filtered['Year'] >= 1980) & (df_filtered['Year'] <= 2024)]

# 미국 데이터가 0이거나 결측치인 경우를 제외하고 계산
countries = [col for col in df_filtered.columns if col != 'Year']

# 원본 데이터를 보존하면서 비율 데이터프레임 생성
df_ratio = df_filtered[['Year']].copy()

for country in countries:
    # 각 국가의 값을 미국의 값으로 나눔
    df_ratio[country] = df_filtered[country] / df_filtered['미국']

# ==========================================
# 4. 그래프 시각화
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

plt.figure(figsize=(10, 7))

markers = ['s', 'o', '^', 'v', 'D', 'p', '*', 'h', 'x', '<', '>']
colors = plt.cm.tab10(np.linspace(0, 1, len(countries)))
ms = 8

for i, country in enumerate(countries):
    country_data = df_ratio[['Year', country]].dropna()

    if country == '미국':
        plt.plot(country_data['Year'], country_data[country],
                 label=f'{country} (기준)',
                 color='black',
                 linewidth=3,
                 linestyle='--', # 미국은 점선으로 표시
                 zorder=10) # 가장 위로 올림
    else:
        plt.plot(country_data['Year'], country_data[country],
                 marker=markers[i % len(markers)],
                 markersize=ms,
                 label=country,
                 color=colors[i],
                 linewidth=2,
                 alpha=0.8)

# 축 및 레이블 설정
plt.xticks(range(1980, 2026, 5), fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('연도', fontsize=16, labelpad=15)
plt.ylabel('미국 대비 상대적 비율 (US = 1.0)', fontsize=16, labelpad=15)
plt.title('미국 1인당 GDP 대비 주요국 상대적 경제 수준 (1980-2024)', fontsize=20, pad=20)

# 기준선(1.0) 강조
plt.axhline(y=1.0, color='black', linestyle='-', linewidth=0.5, alpha=0.5)

# 범례 설정 (왼쪽 상단)
plt.legend(loc='center left', fontsize=12, frameon=True, shadow=True, ncol=2)

plt.grid(True, axis='both', linestyle='--', alpha=0.4)
plt.tight_layout()

plt.savefig('plots/2.3.3_wid_gdp_per_capita_relative_to_us.png', dpi=300, bbox_inches="tight")
plt.show()