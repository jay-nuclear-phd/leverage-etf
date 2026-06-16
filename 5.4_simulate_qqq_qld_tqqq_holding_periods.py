import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
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

trading_days_per_year = 254

# ==========================================
# 2. 나스닥 데이터 불러오기
# ==========================================
df = pd.read_excel("NASDAQCOM.xlsx", sheet_name="Daily, Close")

df["observation_date"] = pd.to_datetime(df["observation_date"])
df = df.sort_values("observation_date").reset_index(drop=True)

df["NASDAQCOM"] = pd.to_numeric(df["NASDAQCOM"], errors="coerce").ffill()
df = df.dropna(subset=["NASDAQCOM"]).reset_index(drop=True)

df = df[df["observation_date"] <= pd.Timestamp("2026-06-12")].reset_index(drop=True)


# ==========================================
# 3. 일일 수익률 계산
# ==========================================
df["daily_return"] = df["NASDAQCOM"].pct_change()
df = df.dropna(subset=["daily_return"]).reset_index(drop=True)


# ==========================================
# 4. 가상 QQQ, QLD, TQQQ 생성
# ==========================================
annual_expense = {
    "가상 QQQ": 0.0018,
    "가상 QLD": 0.0095,
    "가상 TQQQ": 0.0082,
}

daily_expense = {
    k: (1 + v) ** (1 / trading_days_per_year) - 1
    for k, v in annual_expense.items()
}

df["가상 QQQ"] = (
    1 + df["daily_return"] * 1 - daily_expense["가상 QQQ"]
).cumprod()

df["가상 QLD"] = (
    1 + df["daily_return"] * 2 - daily_expense["가상 QLD"]
).cumprod()

df["가상 TQQQ"] = (
    1 + df["daily_return"] * 3 - daily_expense["가상 TQQQ"]
).cumprod()


# ==========================================
# 5. 가능한 모든 실제 연속 구간 계산
# ==========================================
holding_years_list = list(range(1, 31))
products = ["가상 QQQ", "가상 QLD", "가상 TQQQ"]

simulation_results = []
all_period_results = []

for holding_years in tqdm(holding_years_list, desc="보유 기간별 전체 구간 계산"):
    holding_days = int(holding_years * trading_days_per_year)

    max_start_idx = len(df) - holding_days - 1

    if max_start_idx <= 0:
        continue

    for product in products:
        final_values = []

        for start_idx in range(0, max_start_idx + 1):
            end_idx = start_idx + holding_days

            start_value = df.loc[start_idx, product]
            end_value = df.loc[end_idx, product]

            final_value = end_value / start_value
            final_values.append(final_value)

            all_period_results.append({
                "투자 상품": product,
                "보유 기간": holding_years,
                "시작일": df.loc[start_idx, "observation_date"],
                "종료일": df.loc[end_idx, "observation_date"],
                "최종 자산 배율": final_value,
                "손실 여부": final_value < 1
            })

        final_values = np.array(final_values)

        simulation_results.append({
            "투자 상품": product,
            "보유 기간": holding_years,
            "전체 구간 수": len(final_values),
            "손실 확률(%)": np.mean(final_values < 1) * 100,
            "최종 자산 중앙값": np.median(final_values),
            "최종 자산 평균값": np.mean(final_values),
            "하위 5%": np.percentile(final_values, 5),
            "상위 95%": np.percentile(final_values, 95),
            "최소값": np.min(final_values),
            "최대값": np.max(final_values),
        })

simulation_results = pd.DataFrame(simulation_results)
all_period_results = pd.DataFrame(all_period_results)

# ==========================================
# 6. 결과 표 출력
# ==========================================
print(simulation_results)

# ==========================================
# 7. 손실 확률 그래프
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

plt.figure(figsize=(10, 7))

for product in products:
    temp = simulation_results[simulation_results["투자 상품"] == product]

    plt.plot(
        temp["보유 기간"],
        temp["손실 확률(%)"],
        marker="o",
        linewidth=2.5,
        label=product
    )

plt.title("보유 기간별 원금 손실 확률", fontsize=20, pad=20)
plt.xlabel("보유 기간 (년)", fontsize=16, labelpad=15)
plt.ylabel("원금 손실 확률 (%)", fontsize=16, labelpad=15)

plt.xticks(range(1, 31, 1), fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend(fontsize=12)

plt.tight_layout()
plt.savefig("plots/5.4_simulate_qqq_qld_tqqq_holding_periods.png", dpi=300, bbox_inches="tight")

plt.show()