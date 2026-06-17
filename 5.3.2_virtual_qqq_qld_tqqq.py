import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

# ==========================================
# 3. 일일 수익률 및 가상 데이터 생성
# ==========================================
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

# ==========================================
# 4. 그래프 시각화
# ==========================================
import os
os.makedirs('plots', exist_ok=True)

def plot_virtual_performance(lang='ko'):
    if lang == 'ko':
        title = "가상 QQQ, QLD, TQQQ 장기 성과 비교"
        xlabel = "연도"
        ylabel = "초기 투자금 대비 가치, 로그축"
        labels = {
            "가상 QQQ 1배": "가상 QQQ 1배",
            "가상 QLD 2배": "가상 QLD 2배",
            "가상 TQQQ 3배": "가상 TQQQ 3배"
        }
        save_name = "plots/5.3.2_virtual_qqq_qld_tqqq.png"
    else:
        title = "Long-term Performance Comparison of Virtual QQQ, QLD, TQQQ"
        xlabel = "Year"
        ylabel = "Value relative to Initial Investment, Log Scale"
        labels = {
            "가상 QQQ 1배": "Virtual QQQ 1x",
            "가상 QLD 2배": "Virtual QLD 2x",
            "가상 TQQQ 3배": "Virtual TQQQ 3x"
        }
        save_name = "plots/5.3.2_virtual_qqq_qld_tqqq_EN.png"

    plt.figure(figsize=(10, 7))

    for col in ["가상 QQQ 1배", "가상 QLD 2배", "가상 TQQQ 3배"]:
        plt.plot(df["observation_date"], df[col], linewidth=1.0, label=labels[col])

    plt.yscale("log")

    plt.title(title, fontsize=20, pad=20)

    plt.xlabel(xlabel, fontsize=16, labelpad=15)
    plt.ylabel(ylabel, fontsize=16, labelpad=15)

    ax = plt.gca()

    # x축을 날짜 대신 연도만 표시
    ax.xaxis.set_major_locator(mdates.YearLocator(base=2))   # 2년 간격 major tick
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # 더 촘촘한 보조 tick: 매년
    ax.xaxis.set_minor_locator(mdates.YearLocator(base=1))

    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)

    plt.grid(True, which="major", linestyle="--", alpha=0.35)
    plt.grid(True, which="minor", linestyle=":", alpha=0.20)

    plt.legend(fontsize=12, loc="upper left")

    plt.tight_layout()

    plt.savefig(save_name, dpi=300, bbox_inches="tight")
    plt.show()

# 두 버전 모두 생성
plot_virtual_performance('ko')
plot_virtual_performance('en')