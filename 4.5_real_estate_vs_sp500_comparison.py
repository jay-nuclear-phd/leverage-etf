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
# 2. 기본 가정
# =========================
years = np.arange(0, 31)  # 0년 ~ 30년

house_price_initial = 10  # 주택 가격 10억
house_return = 0.06       # 서울 주택 연 6%

loan_initial = 6          # 대출 6억
loan_years = 30           # 30년 원금 균등 상환

sp_initial = 4            # S&P500 ETF 투자금 4억
sp_return = 0.10          # S&P500 ETF 연 10%


# =========================
# 3. 자산 가치 계산
# =========================
house_gross_value = house_price_initial * (1 + house_return) ** years

remaining_loan = loan_initial * np.maximum(
    (loan_years - years) / loan_years,
    0
)

house_net_value = house_gross_value - remaining_loan
sp_value = sp_initial * (1 + sp_return) ** years


# =========================
# 4. 두 자산의 역전 시점 계산
# =========================
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


# =========================
# 5. 그래프 그리기
# =========================
plt.figure(figsize=(11, 7))

plt.plot(
    years,
    house_net_value,
    linewidth=2.8,
    label="서울 주택 순자산: 주택 가치 - 남은 대출"
)

plt.plot(
    years,
    sp_value,
    linewidth=2.8,
    label="S&P500 ETF: 4억 × (1.10)^n"
)

plt.plot(
    years,
    house_gross_value,
    linewidth=1.8,
    linestyle="--",
    alpha=0.5,
    label="서울 주택 전체 가격"
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
        f"약 {cross_year:.1f}년 후 역전\n약 {cross_value:.1f}억",
        fontsize=11,
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
    "시작: 자기자본 4억",
    fontsize=10,
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
    f"30년 후 주택 순자산\n약 {house_net_value[-1]:.1f}억",
    fontsize=10,
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
    f"30년 후 ETF\n약 {sp_value[-1]:.1f}억",
    fontsize=10,
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
    "서울 주택 순자산과 S&P500 ETF 투자 비교",
    fontsize=18,
    pad=18
)

plt.xlabel("투자 기간 (년)", fontsize=13)
plt.ylabel("자산 가치 (억 원)", fontsize=13)

plt.xlim(-3, 33)
plt.xticks(np.arange(0, 31, 5))

plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)

plt.figtext(
    0.5,
    0.01,
    "가정: 서울 주택 연 6%, S&P500 ETF 연 10%, 주택은 10억 중 4억 자기자본·6억 대출, 대출 원금은 30년 균등 상환",
    ha="center",
    fontsize=10.5
)

plt.tight_layout(rect=[0, 0.04, 1, 1])

plt.savefig("real_estate_vs_sp500_comparison.png", dpi=300, bbox_inches="tight")

plt.show()
