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
# 2. 설정 정보
# ==========================================
file_path = 'WID_Data.xlsx'
# 시트명과 그래프 제목 매핑
sheet_info = {
    # 'IncomeTop10': '주요국 소득 상위 10% 점유율 추이 (1980-2024)',
    'IncomeTop1': '주요국 소득 상위 1% 점유율 추이 (1980-2024)',
    # 'WealthTop10': '주요국 자산 상위 10% 점유율 추이 (1980-2024)',
    'WealthTop1': '주요국 자산 상위 1% 점유율 추이 (1980-2024)'
}

# ==========================================
# 3. 데이터 처리 및 시각화
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

for sheet_name, title in sheet_info.items():
    # 데이터 불러오기
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 열 이름 강제 재설정 (첫 번째 열을 Year로)
    cols = list(df.columns)
    cols[0] = 'Year'
    df.columns = cols

    # 데이터 전처리 (1980-2024)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df_filtered = df[(df['Year'] >= 1980) & (df['Year'] <= 2024)].dropna(subset=['Year']).copy()

    # 브라질(BR) 제외 (이전 요청 반영)
    if 'BR' in df_filtered.columns:
        df_filtered = df_filtered.drop(columns=['BR'])

    # 4. 그래프 그리기
    plt.figure(figsize=(10, 7))

    # 국가별 열 목록 (Year 제외)
    countries = [col for col in df_filtered.columns if col != 'Year']

    # 시각적 설정
    markers = ['s', 'o', '^', 'v', 'D', 'p', '*', 'h', 'x', '<', '>']
    colors = plt.cm.tab10(np.linspace(0, 1, len(countries)))
    ms = 8

    for i, country in enumerate(countries):
        plt.plot(df_filtered['Year'], df_filtered[country],
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
    plt.ylabel('점유율', fontsize=16, labelpad=15)
    plt.title(title, fontsize=20, pad=20)

    # 범례 설정 (그래프 내부 왼쪽 상단)
    plt.legend(loc='upper left', fontsize=12, frameon=True, shadow=True)

    plt.grid(True, axis='both', linestyle='--', alpha=0.5)
    plt.tight_layout()

    # 그래프 저장 및 출력
    plt.savefig('plots/2.3.1_wid_inequality_trends.png', dpi=300, bbox_inches="tight")
    plt.show()