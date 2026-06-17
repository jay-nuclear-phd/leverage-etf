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

# 열 이름 강제 재설정 (첫 번째 열을 Year로)
cols = list(df.columns)
cols[0] = 'Year'
df.columns = cols

# ==========================================
# 3. 데이터 전처리 (1980-2024)
# ==========================================
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
# 연도 기준 정렬 및 유효한 연도 데이터만 추출
df_filtered = df.dropna(subset=['Year']).sort_values('Year').copy()
df_filtered = df_filtered[(df_filtered['Year'] >= 1980) & (df_filtered['Year'] <= 2024)]

# ==========================================
# 4. 그래프 시각화
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

def plot_gdp(lang='ko'):
    if lang == 'ko':
        xlabel = '연도'
        ylabel = '달러 ($)'
        title = '주요국 1인당 GDP 성장 추이 (1980-2024)'
        save_name = 'plots/2.3.2_wid_per_capita_gdp.png'
    else:
        xlabel = 'Year'
        ylabel = 'USD ($)'
        title = 'Per Capita GDP Growth Trends of Major Countries (1980-2024)'
        save_name = 'plots/2.3.2_wid_per_capita_gdp_EN.png'

    country_mapping = {
        '한국': 'Korea',
        '미국': 'USA',
        '중국': 'China',
        '독일': 'Germany',
        '일본': 'Japan',
        '호주': 'Australia',
        '캐나다': 'Canada',
        '이탈리아': 'Italy',
        '스웨덴': 'Sweden',
        '프랑스': 'France'
    }

    plt.figure(figsize=(10, 7))

    # 국가별 열 목록 (Year 제외)
    countries = [col for col in df_filtered.columns if col != 'Year']

    markers = ['s', 'o', '^', 'v', 'D', 'p', '*', 'h', 'x', '<', '>']
    colors = plt.cm.tab10(np.linspace(0, 1, len(countries)))
    ms = 8

    for i, country in enumerate(countries):
        label = country
        if lang == 'en' and country in country_mapping:
            label = country_mapping[country]

        country_data = df_filtered[['Year', country]].dropna()
        plt.plot(country_data['Year'], country_data[country],
                    marker=markers[i % len(markers)],
                    markersize=ms,
                    label=label,
                    color=colors[i],
                    linewidth=2.5, # 선 굵기 강조
                    alpha=0.9)

    # 축 및 레이블 설정
    # 1820년부터 2024년까지 20년 단위로 눈금 표시
    plt.xticks(range(1980, 2026, 5), fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel(xlabel, fontsize=16, labelpad=15)
    plt.ylabel(ylabel, fontsize=16, labelpad=15)
    plt.title(title, fontsize=20, pad=20)

    # 범례 설정 (왼쪽 상단)
    plt.legend(loc='upper left', fontsize=12, frameon=True, shadow=True, ncol=2)
    plt.grid(True, axis='both', linestyle='--', alpha=0.4)
    plt.tight_layout()

    # 그래프 저장 및 출력
    plt.savefig(save_name, dpi=300, bbox_inches="tight")
    plt.show()

# 두 버전 모두 생성
plot_gdp('ko')
plot_gdp('en')