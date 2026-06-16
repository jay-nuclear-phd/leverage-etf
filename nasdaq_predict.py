import matplotlib.pyplot as plt
import pandas as pd

# 1. 엑셀 파일의 특정 시트('Daily, Close') 불러오기
file_path = "NASDAQCOM.xlsx"
df = pd.read_excel(file_path, sheet_name="Daily, Close")

# 2. 데이터 전처리
# 날짜 컬럼을 datetime 형식으로 변환하고 날짜순 정렬
df["observation_date"] = pd.to_datetime(df["observation_date"])
df = df.sort_values("observation_date").reset_index(drop=True)

# 결측치(휴장일 등으로 인해 비어있거나 '.'으로 채워진 값) 처리
df["NASDAQCOM"] = pd.to_numeric(df["NASDAQCOM"], errors="coerce")
# 주말/휴일로 비어있는 종가는 '직전 거래일의 종가'로 채워줍니다 (Forward Fill)
df["NASDAQCOM"] = df["NASDAQCOM"].ffill()

# 혹시 첫 행이 결측치인 경우 데이터에서 제외
df = df.dropna(subset=["NASDAQCOM"]).reset_index(drop=True)

# 3. 일일 변동률(수익률) 계산 및 레버리지 배수 적용
# 전일 대비 당일의 변동 비율 계산 (예: +1.5% -> 0.015)
df["NASDAQ_Return"] = df["NASDAQCOM"].pct_change().fillna(0)

# 가상 QLD(2배)와 TQQQ(3배)의 일일 변동률
df["QLD_Return"] = df["NASDAQ_Return"] * 2
df["TQQQ_Return"] = df["NASDAQ_Return"] * 3

# 4. 일일 복리 누적 수익률 계산 (시작점 기준가를 100으로 통일)
# (1 + 변동률)을 계속 곱해나가는 누적곱(cumprod) 방식입니다.
df["NASDAQ_Sim"] = 100 * (1 + df["NASDAQ_Return"]).cumprod()
df["QLD_Sim"] = 100 * (1 + df["QLD_Return"]).cumprod()
df["TQQQ_Sim"] = 100 * (1 + df["TQQQ_Return"]).cumprod()

# 5. 그래프 시각화
plt.figure(figsize=(14, 7))

# 각 지수의 가상 움직임 그래프 그리기
plt.plot(
    df["observation_date"],
    df["NASDAQ_Sim"],
    label="NASDAQ Composite (1x)",
    color="gray",
    alpha=0.7,
)
plt.plot(
    df["observation_date"], df["QLD_Sim"], label="Virtual QLD (2x)", color="orange"
)
plt.plot(
    df["observation_date"], df["TQQQ_Sim"], label="Virtual TQQQ (3x)", color="red"
)

# 그래프 제목 및 축 설정
plt.title(
    "NASDAQ vs Virtual QLD vs Virtual TQQQ (Since 1971, Base=100)",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Value (Log Scale)", fontsize=12)

# ⚠️ 아주 중요: 1971년부터 3배 복리를 적용하면 자산 스케일이 비현실적으로 커집니다.
# 이를 한 화면에 왜곡 없이 보기 위해 Y축을 반드시 '로그 스케일(Log Scale)'로 설정해야 합니다.
plt.yscale("log")

# 격자(Grid) 및 범례(Legend) 추가
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend(fontsize=11)
plt.tight_layout()

plt.show()

# 계산이 잘 되었는지 마지막 5행 데이터 확인용 출력
print(df[["observation_date", "NASDAQ_Sim", "QLD_Sim", "TQQQ_Sim"]].tail())

df.to_csv("NASDAQ_simulation.csv", index=False, encoding="utf-8-sig")