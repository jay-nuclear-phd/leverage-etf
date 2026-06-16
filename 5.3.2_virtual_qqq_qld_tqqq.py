import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path
import matplotlib.dates as mdates

def set_korean_font():
    font_candidates = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJKkr-Regular.otf",
        "C:/Windows/Fonts/malgun.ttf",
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


set_korean_font()

df = pd.read_excel("NASDAQCOM.xlsx", sheet_name="Daily, Close")

df["observation_date"] = pd.to_datetime(df["observation_date"])
df = df.sort_values("observation_date").reset_index(drop=True)

df["NASDAQCOM"] = pd.to_numeric(df["NASDAQCOM"], errors="coerce").ffill()
df = df.dropna(subset=["NASDAQCOM"]).reset_index(drop=True)

df = df[df["observation_date"] <= pd.Timestamp("2026-06-12")].reset_index(drop=True)


df["daily_return"] = df["NASDAQCOM"].pct_change()
df = df.dropna(subset=["daily_return"]).reset_index(drop=True)


trading_days_per_year = 254

annual_expense = {
    "가상 QQQ 1배": 0.0018,
    "가상 QLD 2배": 0.0095,
    "가상 TQQQ 3배": 0.0082,
}

daily_expense = {
    k: (1 + v) ** (1 / trading_days_per_year) - 1
    for k, v in annual_expense.items()
}

df["가상 QQQ 1배"] = (1 + df["daily_return"] * 1 - daily_expense["가상 QQQ 1배"]).cumprod()
df["가상 QLD 2배"] = (1 + df["daily_return"] * 2 - daily_expense["가상 QLD 2배"]).cumprod()
df["가상 TQQQ 3배"] = (1 + df["daily_return"] * 3 - daily_expense["가상 TQQQ 3배"]).cumprod()

plt.figure(figsize=(10, 6))

for col in ["가상 QQQ 1배", "가상 QLD 2배", "가상 TQQQ 3배"]:
    plt.plot(df["observation_date"], df[col], linewidth=1.0, label=col)

plt.yscale("log")

plt.title("가상 QQQ, QLD, TQQQ 장기 성과 비교", fontsize=12, pad=10)

plt.xlabel("연도", fontsize=13)
plt.ylabel("초기 투자금 대비 가치, 로그축", fontsize=13)

ax = plt.gca()

# x축을 날짜 대신 연도만 표시
ax.xaxis.set_major_locator(mdates.YearLocator(base=2))   # 2년 간격 major tick
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# 더 촘촘한 보조 tick: 매년
ax.xaxis.set_minor_locator(mdates.YearLocator(base=1))

plt.xticks(rotation=45)

plt.grid(True, which="major", linestyle="--", alpha=0.35)
plt.grid(True, which="minor", linestyle=":", alpha=0.20)

plt.legend(fontsize=12, loc="upper left")

plt.tight_layout()

plt.savefig("virtual_qqq_qld_tqqq_log_chart.png", dpi=300, bbox_inches="tight")

plt.show()