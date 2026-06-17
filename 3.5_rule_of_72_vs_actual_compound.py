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
# 2. 데이터 생성
# ==========================================
# 연수익률 1% ~ 20%
rates_percent = np.linspace(1, 20, 300)
rates_decimal = rates_percent / 100

# 실제 복리 공식으로 계산한 2배 달성 기간
# 2 = (1 + r)^t -> t = log(2) / log(1 + r)
actual_years = np.log(2) / np.log(1 + rates_decimal)

# 72의 법칙으로 계산한 근사 기간
rule72_years = 72 / rates_percent

# 실제 복리 기준으로 계산했을 때 연수익률(%) × 기간
actual_products = rates_percent * actual_years

# 강조할 대표 수익률
highlight_rates = np.array([3, 5, 7, 10, 12, 15])
highlight_decimal = highlight_rates / 100

highlight_actual_years = np.log(2) / np.log(1 + highlight_decimal)
highlight_rule72_years = 72 / highlight_rates
highlight_products = highlight_rates * highlight_actual_years

# ==========================================
# 3. 그래프 시각화
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

def plot_rule_72(lang='ko'):
    if lang == 'ko':
        xlabel = '연수익률 (%)'
        ylabel1 = '원금 2배 도달까지 걸리는 시간 (년)'
        ylabel2 = '연수익률 × 기간'
        title_main = '72의 법칙 vs 실제 복리 계산 비교'
        title1 = '연수익률에 따른 자산 2배 달성 기간'
        title2 = '실제 복리 계산에서 연수익률 × 기간'
        label_actual = '실제 복리 계산'
        label_rule72 = '72의 법칙 근사'
        label_actual_product = '실제 복리 기준: 연수익률 × 기간'
        label_rule72_line = '72의 법칙 기준선'
        anno_suffix = '년'
        caption = "실제 공식: 자산 2배 달성 기간 = log(2) ÷ log(1 + 연수익률)"
        save_name = "plots/3.5_rule_of_72_vs_actual_compound.png"
    else:
        xlabel = 'Annual Return (%)'
        ylabel1 = 'Time to Double Principal (Years)'
        ylabel2 = 'Annual Return × Duration'
        title_main = 'Rule of 72 vs. Actual Compound Interest Comparison'
        title1 = 'Time to Double Assets by Annual Return'
        title2 = 'Annual Return × Duration in Actual Compound Calculation'
        label_actual = 'Actual Compound Interest'
        label_rule72 = 'Rule of 72 Approximation'
        label_actual_product = 'Actual Compound Basis: Annual Return × Duration'
        label_rule72_line = 'Rule of 72 Baseline'
        anno_suffix = 'yr'
        caption = "Actual Formula: Time to Double Assets = log(2) ÷ log(1 + Annual Return)"
        save_name = "plots/3.5_rule_of_72_vs_actual_compound_EN.png"

    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(10, 10),
        sharex=True
    )

    # -------------------------
    # 첫 번째 그래프: 실제 복리 vs 72의 법칙
    # -------------------------
    axes[0].plot(
        rates_percent,
        actual_years,
        linewidth=2.5,
        label=label_actual
    )

    axes[0].plot(
        rates_percent,
        rule72_years,
        linewidth=2,
        linestyle="--",
        label=label_rule72
    )

    axes[0].scatter(
        highlight_rates,
        highlight_actual_years,
        s=60,
        zorder=3
    )

    for r, y in zip(highlight_rates, highlight_actual_years):
        axes[0].text(
            r + 0.25,
            y + 0.7,
            f"{r}% → {y:.1f}{anno_suffix}",
            fontsize=10
        )

    axes[0].set_title(title1, fontsize=20, pad=20)
    axes[0].set_ylabel(ylabel1, fontsize=16, labelpad=15)
    axes[0].tick_params(axis='both', which='major', labelsize=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(fontsize=12)
    axes[0].set_ylim(0, 75)

    # -------------------------
    # 두 번째 그래프: 연수익률 × 기간 분석
    # -------------------------
    axes[1].plot(
        rates_percent,
        actual_products,
        linewidth=2.5,
        label=label_actual_product
    )

    axes[1].axhline(
        72,
        linestyle="--",
        linewidth=1.5,
        label=label_rule72_line
    )

    axes[1].scatter(
        highlight_rates,
        highlight_products,
        s=60,
        zorder=3
    )

    for i, (r, p, y) in enumerate(zip(highlight_rates, highlight_products, highlight_actual_years)):
        label = f"{r}% × {y:.1f}{anno_suffix} = {p:.1f}"

        if i < 3:
            # 앞의 3개 포인트: 오른쪽 위로 이동
            x_offset = 0.4
            ha = "right"
        else:
            # 뒤의 3개 포인트: 왼쪽 위로 이동
            x_offset = -0.20
            ha = "right"

        axes[1].text(
            r + x_offset,
            p + 0.35,
            label,
            fontsize=10,
            ha=ha,
            va="bottom"
        )

    axes[1].set_title(title2, fontsize=20, pad=20)
    axes[1].set_xlabel(xlabel, fontsize=16, labelpad=15)
    axes[1].set_ylabel(ylabel2, fontsize=16, labelpad=15)
    axes[1].tick_params(axis='both', which='major', labelsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(fontsize=12)

    axes[1].set_xlim(0, 20)
    axes[1].set_xticks(np.arange(0, 21, 2))

    fig.text(
        0.5,
        0.02,
        caption,
        ha="center",
        fontsize=12
    )

    plt.tight_layout(rect=[0, 0.04, 1, 0.95])

    # 고해상도 저장
    plt.savefig(save_name, dpi=300, bbox_inches="tight")
    plt.show()

# 두 버전 모두 생성
plot_rule_72('ko')
plot_rule_72('en')