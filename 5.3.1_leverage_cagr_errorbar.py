import numpy as np
import pandas as pd
import random as rd
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

# ==========================================
# 2. 데이터 불러오기 및 전처리
# ==========================================
df = pd.read_excel("NASDAQCOM.xlsx", sheet_name="Daily, Close")
df["observation_date"] = pd.to_datetime(df["observation_date"])
df = df.sort_values("observation_date").reset_index(drop=True)
df["NASDAQCOM"] = pd.to_numeric(df["NASDAQCOM"], errors="coerce").ffill()
df = df.dropna(subset=["NASDAQCOM"]).reset_index(drop=True)
df = df[df["observation_date"] <= pd.Timestamp("2026-06-12")].reset_index(drop=True)

nsd = df["NASDAQCOM"].values
rate = np.array([(nsd[i + 1] - nsd[i]) / nsd[i] for i in range(len(nsd) - 1)])

leverages = np.round(np.arange(1.0, 3.0 + 0.1, 0.1), 1)
trading_days_per_year = 254

annual_expense = {"QQQ": 0.0018, "QLD": 0.0095, "TQQQ": 0.0082}
daily_expense = {k: (1 + v) ** (1 / trading_days_per_year) - 1 for k, v in annual_expense.items()}

def get_daily_expense(lev):
    if 1.0 <= lev <= 2.0:
        w_qld = lev - 1.0
        w_qqq = 1.0 - w_qld
        return w_qqq * daily_expense["QQQ"] + w_qld * daily_expense["QLD"]
    w_tqqq = lev - 2.0
    w_qld = 1.0 - w_tqqq
    return w_qld * daily_expense["QLD"] + w_tqqq * daily_expense["TQQQ"]

leverage_expenses = np.array([get_daily_expense(lev) for lev in leverages])

# ==========================================
# 3. 몬테카를로 시뮬레이션 실행
# ==========================================
simulation_results = []

for k in tqdm(range(1000), desc="시뮬레이션 진행 중"):
    while True:
        rg = [rd.randrange(len(rate)), rd.randrange(len(rate))]
        rg.sort()
        if rg[1] - rg[0] >= 10000:
            break

    holding_years = (rg[1] - rg[0]) / trading_days_per_year

    for lev, expense in zip(leverages, leverage_expenses):
        final_value = 1
        for i in range(rg[1] - rg[0]):
            final_value *= 1 + rate[rg[0] + i] * lev - expense

        cagr = final_value ** (1 / holding_years) - 1

        simulation_results.append({
            "leverage": lev,
            "final_value": final_value,
            "cagr": cagr
        })

simulation_results = pd.DataFrame(simulation_results)

cagr_summary = (
    simulation_results
    .groupby("leverage")
    .agg(
        mean_cagr=("cagr", "mean"),
        std_cagr=("cagr", "std")
    )
    .reset_index()
)

# ==========================================
# 4. 결과 분석 및 시각화 준비
# ==========================================
plot_df = cagr_summary.copy()

plot_df["mean_pct"] = plot_df["mean_cagr"] * 100
plot_df["std_pct"] = plot_df["std_cagr"] * 100
plot_df["lower_bound"] = plot_df["mean_pct"] - plot_df["std_pct"] * 2
plot_df["upper_bound"] = plot_df["mean_pct"] + plot_df["std_pct"] * 2

x = plot_df["leverage"].values
y = plot_df["mean_pct"].values
yerr = plot_df["std_pct"].values * 2

# 평균 수익률이 가장 높은 지점
max_return_idx = plot_df["mean_pct"].idxmax()
max_return_x = plot_df.loc[max_return_idx, "leverage"]
max_return_y = plot_df.loc[max_return_idx, "mean_pct"]

# 에러바 하단값이 가장 높은 지점
best_lower_idx = plot_df["lower_bound"].idxmax()
best_lower_x = plot_df.loc[best_lower_idx, "leverage"]
best_lower_y = plot_df.loc[best_lower_idx, "mean_pct"]
best_lower_bound = plot_df.loc[best_lower_idx, "lower_bound"]


# ==========================================
# 5. 그래프 시각화
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

def plot_leverage_distribution(lang='ko'):
    if lang == 'ko':
        xlabel = '레버리지 배율'
        ylabel = '평균 연복리 수익률 (%)'
        title = '레버리지 배율에 따른 연복리 수익률(CAGR) 분포\n(NASDAQ 100 1999-2024 가상 시뮬레이션)'
        label_range = '평균 ± 표준편차 2배 범위'
        label_mean = '평균 연복리 수익률'
        label_peak_avg = '평균 수익률 최고점'
        label_peak_lower = '하단 기준 최고점'
        text_peak_avg = "평균 최고점\n{:.1f}배, {:.1f}%"
        text_peak_lower = "하단 기준 최고점\n{:.1f}배\n하단 {:.1f}%"
        save_name = "plots/5.3.1_leverage_cagr_errorbar.png"
    else:
        xlabel = 'Leverage Multiplier'
        ylabel = 'Average CAGR (%)'
        title = 'CAGR Distribution by Leverage Multiplier\n(Virtual Simulation of NASDAQ 100 1999-2024)'
        label_range = 'Mean ± 2 Standard Deviations Range'
        label_mean = 'Average CAGR'
        label_peak_avg = 'Peak Average Return'
        label_peak_lower = 'Lower Bound Peak'
        text_peak_avg = "Peak Average\n{:.1f}x, {:.1f}%"
        text_peak_lower = "Lower Bound Peak\n{:.1f}x\nLower {:.1f}%"
        save_name = "plots/5.3.1_leverage_cagr_errorbar_EN.png"

    plt.figure(figsize=(10, 7))

    # 에러바 영역을 연한 음영으로 표시
    plt.fill_between(
        x,
        plot_df["lower_bound"],
        plot_df["upper_bound"],
        alpha=0.12,
        label=label_range
    )

    # 기본 에러바
    plt.errorbar(
        x,
        y,
        yerr=yerr,
        fmt="o-",
        linewidth=2.4,
        markersize=5.5,
        elinewidth=1.6,
        capsize=4,
        capthick=1.4,
        alpha=0.9,
        label=label_mean
    )

    # 평균 수익률 최고점 하이라이트
    plt.scatter(
        max_return_x,
        max_return_y,
        s=150,
        color="crimson",
        edgecolor="black",
        linewidth=1.0,
        zorder=5,
        label=label_peak_avg
    )

    plt.annotate(
        text_peak_avg.format(max_return_x, max_return_y),
        xy=(max_return_x, max_return_y),
        xytext=(max_return_x - 0.45, max_return_y + 1.1),
        fontsize=12,
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.2,
            color="crimson"
        ),
        bbox=dict(
            facecolor="white",
            edgecolor="crimson",
            alpha=0.9,
            boxstyle="round,pad=0.3"
        )
    )

    # 에러바 하단값 최고점 하이라이트
    plt.scatter(
        best_lower_x,
        best_lower_y,
        s=150,
        color="darkgreen",
        edgecolor="black",
        linewidth=1.0,
        zorder=5,
        label=label_peak_lower
    )

    # 하단값 위치도 따로 표시
    plt.scatter(
        best_lower_x,
        best_lower_bound,
        s=90,
        color="darkgreen",
        marker="v",
        edgecolor="black",
        linewidth=0.8,
        zorder=5
    )

    plt.annotate(
        text_peak_lower.format(best_lower_x, best_lower_bound),
        xy=(best_lower_x, best_lower_bound),
        xytext=(best_lower_x + 0.18, best_lower_bound - 1.7),
        fontsize=12,
        arrowprops=dict(
            arrowstyle="->",
            linewidth=1.2,
            color="darkgreen"
        ),
        bbox=dict(
            facecolor="white",
            edgecolor="darkgreen",
            alpha=0.9,
            boxstyle="round,pad=0.3"
        )
    )

    # 그래프 설정
    plt.grid(True, linestyle="--", alpha=0.35)

    plt.xlabel(xlabel, fontsize=16, labelpad=15)
    plt.ylabel(ylabel, fontsize=16, labelpad=15)

    plt.title(
        title,
        fontsize=20,
        pad=20
    )

    plt.xticks(np.arange(1.0, 3.0 + 0.1, 0.1), rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    plt.legend(fontsize=12, loc="upper left")

    plt.tight_layout()

    plt.savefig(save_name, dpi=300, bbox_inches="tight")
    plt.show()

# 두 버전 모두 생성
plot_leverage_distribution('ko')
plot_leverage_distribution('en')