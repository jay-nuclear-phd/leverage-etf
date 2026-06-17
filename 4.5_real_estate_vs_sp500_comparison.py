import numpy as np
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

# ==========================================
# 2. 기본 가정
# ==========================================
years = np.arange(0, 31)  # 0년 ~ 30년

house_price_initial = 10  # 주택 가격 10억
house_return = 0.06       # 서울 주택 연 6%

loan_initial = 6          # 대출 6억
loan_years = 30           # 30년 원금 균등 상환

sp_initial = 4            # S&P500 ETF 투자금 4억
sp_return = 0.10          # S&P500 ETF 연 10%

# ==========================================
# 3. 자산 가치 계산
# ==========================================
house_gross_value = house_price_initial * (1 + house_return) ** years

remaining_loan = loan_initial * np.maximum(
    (loan_years - years) / loan_years,
    0
)

house_net_value = house_gross_value - remaining_loan
sp_value = sp_initial * (1 + sp_return) ** years

# ==========================================
# 4. 두 자산의 역전 시점 계산
# ==========================================
# 0년 차는 둘 다 4억으로 같기 때문에 교차점 계산에서 제외
diff = sp_value - house_net_value

cross_year = None
cross_value = None

for i in range(1, len(years) - 1):
    if diff[i] == 0:
        cross_year = years[i]
        cross_value = sp_value[i]
        break

    if diff[i] * diff[i + 1] < 0:
        # i년과 i+1년 사이에서 교차
        x1, x2 = years[i], years[i + 1]
        y1, y2 = diff[i], diff[i + 1]

        cross_year = x1 - y1 * (x2 - x1) / (y2 - y1)

        cross_house_gross = house_price_initial * (1 + house_return) ** cross_year
        cross_remaining_loan = loan_initial * max(
            (loan_years - cross_year) / loan_years,
            0
        )
        cross_value = cross_house_gross - cross_remaining_loan
        break

# ==========================================
# 5. 그래프 시각화
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

def plot_comparison(lang='ko'):
    if lang == 'ko':
        title = '서울 아파트 (실거주) vs S&P500 (자산 증식) 성과 비교 (30년)'
        xlabel = '투자 기간 (년)'
        ylabel = '자산 가치 (억 원)'
        label_house_net = "서울 주택 순자산: 주택 가치 - 남은 대출"
        label_sp = "S&P500 ETF: 4억 × (1.10)^n"
        label_house_gross = "서울 주택 전체 가격"
        text_cross = "약 {:.1f}년 후 역전\n약 {:.1f}억"
        text_start = "시작: 자기자본 4억"
        text_house_30 = "30년 후 주택 순자산\n약 {:.1f}억"
        text_sp_30 = "30년 후 ETF\n약 {:.1f}억"
        text_assumptions = "가정: 서울 주택 연 6%, S&P500 ETF 연 10%, 주택은 10억 중 4억 자기자본·6억 대출, 대출 원금은 30년 균등 상환"
        save_name = "plots/4.5_real_estate_vs_sp500_comparison.png"
    else:
        title = 'Performance Comparison: Seoul Apartment (Residence) vs. S&P 500 (Growth) (30 Years)'
        xlabel = 'Investment Period (Years)'
        ylabel = 'Asset Value (100M KRW)'
        label_house_net = "Seoul Real Estate Net Assets: House Value - Remaining Loan"
        label_sp = "S&P 500 ETF: 400M × (1.10)^n"
        label_house_gross = "Total Price of Seoul Real Estate"
        text_cross = "Crossover after approx {:.1f} years\nApprox {:.1f} (100M KRW)"
        text_start = "Start: 400M KRW Equity"
        text_house_30 = "Net Assets after 30yr\nApprox {:.1f} (100M KRW)"
        text_sp_30 = "S&P 500 ETF after 30yr\nApprox {:.1f} (100M KRW)"
        text_assumptions = "Assumptions: Seoul Housing +6%/yr, S&P 500 +10%/yr, 400M Equity/600M Loan, 30yr Loan Repayment"
        save_name = "plots/4.5_real_estate_vs_sp500_comparison_EN.png"

    plt.figure(figsize=(10, 7))

    plt.plot(
        years,
        house_net_value,
        linewidth=2.8,
        label=label_house_net
    )

    plt.plot(
        years,
        sp_value,
        linewidth=2.8,
        label=label_sp
    )

    plt.plot(
        years,
        house_gross_value,
        linewidth=1.8,
        linestyle="--",
        alpha=0.5,
        label=label_house_gross
    )

    # 역전 시점 표시
    if cross_year is not None:
        plt.scatter(
            cross_year,
            cross_value,
            s=80,
            zorder=5
        )

        plt.text(
            cross_year + 0.5,
            cross_value,
            text_cross.format(cross_year, cross_value),
            fontsize=12,
            va="center",
            bbox=dict(
                facecolor="white",
                edgecolor="none",
                alpha=0.8,
                pad=4
            )
        )

    # 시작점 표시
    plt.scatter([0, 0], [house_net_value[0], sp_value[0]], s=60)

    plt.text(
        0.5,
        house_net_value[0] + 1.0,
        text_start,
        fontsize=12,
        va="bottom",
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.8,
            pad=3
        )
    )

    # 30년 상환 완료 표시
    plt.scatter(
        30,
        house_net_value[-1],
        s=70,
        zorder=5
    )

    plt.text(
        30 - 0.5,
        house_net_value[-1],
        text_house_30.format(house_net_value[-1]),
        fontsize=12,
        ha="right",
        va="center",
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.8,
            pad=3
        )
    )

    plt.scatter(
        30,
        sp_value[-1],
        s=70,
        zorder=5
    )

    plt.text(
        30 - 0.5,
        sp_value[-1],
        text_sp_30.format(sp_value[-1]),
        fontsize=12,
        ha="right",
        va="center",
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.8,
            pad=3
        )
    )

    # 제목과 축
    plt.title(
        title,
        fontsize=20,
        pad=20
    )

    plt.xlabel(xlabel, fontsize=16, labelpad=15)
    plt.ylabel(ylabel, fontsize=16, labelpad=15)

    plt.xlim(-3, 33)
    plt.xticks(np.arange(0, 31, 5), fontsize=12)
    plt.yticks(fontsize=12)

    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)

    plt.figtext(
        0.5,
        0.01,
        text_assumptions,
        ha="center",
        fontsize=12
    )

    plt.tight_layout(rect=[0, 0.04, 1, 1])

    plt.savefig(save_name, dpi=300, bbox_inches="tight")
    plt.show()

# 두 버전 모두 생성
plot_comparison('ko')
plot_comparison('en')
