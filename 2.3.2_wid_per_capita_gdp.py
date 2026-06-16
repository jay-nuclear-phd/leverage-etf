import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import numpy as np

# 1. 한글 폰트 설치 및 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 불러오기
file_path = 'WID_Data.xlsx'
sheet_name = 'PerCapitaGDP'

df = pd.read_excel(file_path, sheet_name=sheet_name)

# 열 이름 강제 재설정 (첫 번째 열을 Year로)
cols = list(df.columns)
cols[0] = 'Year'
df.columns = cols

# 3. 데이터 전처리 (1820-2024 전체 기간)
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
# 연도 기준 정렬 및 유효한 연도 데이터만 추출
df_filtered = df.dropna(subset=['Year']).sort_values('Year').copy()
df_filtered = df_filtered[(df_filtered['Year'] >= 1980) & (df_filtered['Year'] <= 2024)]

# 4. 그래프 그리기
plt.figure(figsize=(10, 7))

# 국가별 열 목록 (Year 제외)
countries = [col for col in df_filtered.columns if col != 'Year']

markers = ['s', 'o', '^', 'v', 'D', 'p', '*', 'h', 'x', '<', '>']
colors = plt.cm.tab10(np.linspace(0, 1, len(countries)))
ms = 8

for i, country in enumerate(countries):
    country_data = df_filtered[['Year', country]].dropna()
    plt.plot(country_data['Year'], country_data[country],
                marker=markers[i % len(markers)],
                markersize=ms,
                label=country,
                color=colors[i],
                linewidth=2.5, # 선 굵기 강조
                alpha=0.9)

# 축 및 레이블 설정
# 1820년부터 2024년까지 20년 단위로 눈금 표시
plt.xticks(range(1980, 2026, 5), fontsize=12)
plt.xlabel('연도', fontsize=16, labelpad=15)
plt.ylabel('', fontsize=0)
plt.title('주요국 1인당 GDP 성장 추이 (1980-2024)', fontsize=20, pad=20)

# 범례 설정 (왼쪽 상단)
plt.legend(loc='upper left', fontsize=12, frameon=True, shadow=True, ncol=2)
plt.ylabel("달러 ($)")
plt.grid(True, axis='both', linestyle='--', alpha=0.4)
plt.tight_layout()

# 그래프 출력
plt.show()