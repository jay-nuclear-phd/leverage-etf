import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path


# =========================
# 1. 한글 폰트 설정
# =========================
def set_korean_font():
    font_candidates = [
        # Linux / WSL
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKkr-Regular.otf",

        # Windows
        "C:/Windows/Fonts/malgun.ttf",

        # macOS
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/AppleGothic.ttf",
    ]

    for font_path in font_candidates:
        if Path(font_path).exists():
            fm.fontManager.addfont(font_path)
            font_name = fm.FontProperties(fname=font_path).get_name()
            plt.rcParams["font.family"] = font_name
            plt.rcParams["axes.unicode_minus"] = False
            print(f"사용 폰트: {font_name}")
            return

    print("한글 폰트를 찾지 못했습니다.")
    print("WSL/Linux라면 아래 명령어로 폰트를 설치하세요:")
    print("sudo apt update && sudo apt install -y fonts-nanum")


set_korean_font()


# =========================
# 2. 데이터 생성
# =========================
# 연수익률 1% ~ 20%
rates_percent = np.linspace(1, 20, 300)
rates_decimal = rates_percent / 100

# 실제 복리 공식으로 계산한 2배 달성 기간
# 2 = (1 + r)^t
# t = log(2) / log(1 + r)
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


# =========================
# 3. 그래프 그리기
# =========================
fig, axes = plt.subplots(
    nrows=2,
    ncols=1,
    figsize=(10, 10),
    sharex=True
)


# -------------------------
# 첫 번째 그래프
# 실제 복리 계산 vs 72의 법칙
# -------------------------
axes[0].plot(
    rates_percent,
    actual_years,
    linewidth=2.5,
    label="실제 복리 계산"
)

axes[0].plot(
    rates_percent,
    rule72_years,
    linewidth=2,
    linestyle="--",
    label="72의 법칙 근사"
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
        f"{r}% → {y:.1f}년",
        fontsize=10
    )

axes[0].set_title("연수익률에 따른 자산 2배 달성 기간", fontsize=16, pad=15)
axes[0].set_ylabel("자산이 2배가 되는 기간 (년)", fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].legend(fontsize=11)
axes[0].set_ylim(0, 75)


# -------------------------
# 두 번째 그래프
# 실제 계산에서 연수익률 × 기간이 얼마인지
# -------------------------
axes[1].plot(
    rates_percent,
    actual_products,
    linewidth=2.5,
    label="실제 복리 기준: 연수익률 × 기간"
)

axes[1].axhline(
    72,
    linestyle="--",
    linewidth=1.5,
    label="72의 법칙 기준선"
)

axes[1].scatter(
    highlight_rates,
    highlight_products,
    s=60,
    zorder=3
)

for i, (r, p, y) in enumerate(zip(highlight_rates, highlight_products, highlight_actual_years)):
    label = f"{r}% × {y:.1f}년 = {p:.1f}"

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

axes[1].set_title("실제 복리 계산에서 연수익률 × 기간", fontsize=16, pad=15)
axes[1].set_xlabel("연수익률 (%)", fontsize=12)
axes[1].set_ylabel("연수익률 × 기간", fontsize=12)
axes[1].grid(True, alpha=0.3)
axes[1].legend(fontsize=11)


# =========================
# 4. 전체 설정
# =========================
axes[1].set_xlim(0, 20)
axes[1].set_xticks(np.arange(0, 21, 2))


fig.text(
    0.5,
    0.02,
    "실제 공식: 자산 2배 달성 기간 = log(2) ÷ log(1 + 연수익률)",
    ha="center",
    fontsize=12
)

plt.tight_layout(rect=[0, 0.04, 1, 0.95])

# 책 삽입용 고해상도 저장
plt.savefig("rule_of_72_vs_actual_compound.png", dpi=300, bbox_inches="tight")

# plt.show()