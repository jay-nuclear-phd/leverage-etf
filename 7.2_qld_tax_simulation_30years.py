import pandas as pd
import matplotlib.pyplot as plt
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

annual_contribution = 10_000_000.0  # 매년 투자금: 1,000만 원
annual_return = 0.15                # 연 수익률 15%
tax_free_amount = 2_500_000.0       # 연간 기본공제 250만 원
tax_rate = 0.22                     # 양도세 22%
max_years = 50

# ==========================================
# 2. 전략 1: 매년 말 매도 후 재매수
# ==========================================
annual_sell_results = []

portfolio_value = 0.0

for year in range(1, max_years + 1):
    # 매년 초 1,000만 원 추가 투자
    cost_basis = portfolio_value + annual_contribution

    # 연말 15% 수익 발생
    value_before_tax = cost_basis * (1 + annual_return)

    # 해당 연도 양도차익
    gain = value_before_tax - cost_basis

    # 250만 원 공제 후 세금 계산
    taxable_gain = max(gain - tax_free_amount, 0.0)
    tax = taxable_gain * tax_rate

    # 세후 금액으로 다음 해 재투자
    portfolio_value = value_before_tax - tax

    annual_sell_results.append({
        "연도": year,
        "매년 매도 전략_세전 금액": value_before_tax,
        "매년 매도 전략_양도차익": gain,
        "매년 매도 전략_세금": tax,
        "매년 매도 전략_세후 최종금액": portfolio_value,
    })

# ==========================================
# 3. 전략 2: 계속 보유 후 마지막에만 매도
# ==========================================
results = []

for target_year in range(1, max_years + 1):
    hold_value = 0.0
    total_invested = 0.0

    for year in range(1, target_year + 1):
        # 매년 초 1,000만 원 추가 투자
        hold_value += annual_contribution
        total_invested += annual_contribution

        # 그 해 15% 수익 발생
        hold_value *= (1 + annual_return)

    # 마지막 해 말에 전량 매도한다고 가정
    total_gain = hold_value - total_invested
    taxable_gain = max(total_gain - tax_free_amount, 0.0)
    final_tax = taxable_gain * tax_rate
    hold_after_tax_value = hold_value - final_tax

    annual_sell_row = annual_sell_results[target_year - 1]

    results.append({
        "연도": target_year,

        "매년 매도 전략_세후 최종금액": annual_sell_row["매년 매도 전략_세후 최종금액"],
        "매년 매도 전략_해당 연도 세금": annual_sell_row["매년 매도 전략_세금"],

        "계속 보유 전략_세전 최종금액": hold_value,
        "계속 보유 전략_총 투자원금": total_invested,
        "계속 보유 전략_총 양도차익": total_gain,
        "계속 보유 전략_최종 매도세금": final_tax,
        "계속 보유 전략_세후 최종금액": hold_after_tax_value,

        "계속 보유 - 매년 매도 차이": hold_after_tax_value - annual_sell_row["매년 매도 전략_세후 최종금액"],
    })

# ==========================================
# 4. 결과표 생성
# ==========================================
result_df = pd.DataFrame(results)

# float 그대로 유지
money_cols = [
    "매년 매도 전략_세후 최종금액",
    "매년 매도 전략_해당 연도 세금",
    "계속 보유 전략_세전 최종금액",
    "계속 보유 전략_총 투자원금",
    "계속 보유 전략_총 양도차익",
    "계속 보유 전략_최종 매도세금",
    "계속 보유 전략_세후 최종금액",
    "계속 보유 - 매년 매도 차이",
]

# ==========================================
# 5. 그래프 시각화
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

fig, ax = plt.subplots(figsize=(10, 7))

# 원 그래프 데이터
x = result_df["연도"]
y_sell = result_df["매년 매도 전략_세후 최종금액"] / 100_000_000
y_hold = result_df["계속 보유 전략_세후 최종금액"] / 100_000_000

# 메인 그래프
ax.plot(
    x,
    y_sell,
    marker="o",
    linewidth=1,
    label="매년 매도 후 재매수"
)

ax.plot(
    x,
    y_hold,
    marker="s",
    linewidth=1,
    label="계속 보유 후 최종 매도"
)

ax.set_title("매년 매도 전략 vs 계속 보유 전략 세후 최종금액", fontsize=20, pad=20)
ax.set_xlabel("투자 기간 (년)", fontsize=16, labelpad=15)
ax.set_ylabel("세후 최종금액 (억 원)", fontsize=16, labelpad=15)

ax.grid(True, linestyle="--", alpha=0.4)
ax.tick_params(axis='both', which='major', labelsize=12)

# 범례 오른쪽 아래
ax.legend(loc="lower right", fontsize=12)

# ==========================================
# 6. 보조 그래프: 최초 10년 차이
# ==========================================
inset_ax = ax.inset_axes([0.07, 0.50, 0.48, 0.42])

zoom_df = result_df[result_df["연도"] <= 10].copy()

# 차이: 매년 매도 전략 - 계속 보유 전략
zoom_df["매년 매도 - 계속 보유"] = (
    zoom_df["매년 매도 전략_세후 최종금액"]
    - zoom_df["계속 보유 전략_세후 최종금액"]
) / 10_000

inset_ax.plot(
    zoom_df["연도"],
    zoom_df["매년 매도 - 계속 보유"],
    marker="o",
    linewidth=1.8,
    markersize=5,
    color="crimson",
    label="매년 매도 - 계속 보유"
)

# 0 기준선
inset_ax.axhline(
    y=0,
    linewidth=1,
    linestyle="--",
    color="black",
    alpha=0.7
)

inset_ax.set_title("최초 10년 차이", fontsize=12)
inset_ax.set_xlim(1, 10)
inset_ax.set_xticks(range(1, 11, 1))
inset_ax.set_xlabel("투자 기간 (년)", fontsize=12)
inset_ax.set_ylabel("차이 (만 원)", fontsize=12)

inset_ax.grid(True, linestyle="--", alpha=0.35)
inset_ax.tick_params(axis="both", labelsize=12)

plt.tight_layout()

plt.savefig(
    "plots/7.2_qld_tax_simulation_30years.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()