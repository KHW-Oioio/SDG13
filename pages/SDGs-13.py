# pages/SDGs-13.py
import streamlit as st
import pandas as pd
from data_loader import load_weather_data, load_disaster_data
from utils import plot_line_chart, plot_pie_chart
from model import run_monte_carlo

st.title("SDGs‑13 몬테카를로 시뮬레이션 대시보드")

weather_df = load_weather_data()
disaster_df = load_disaster_data()  # ← 이미 소문자·공백 제거됨

# 1) 지역 리스트 추출 (weather_df 기준)
region_cols = [c for c in weather_df.columns if c.lower() != "date"]
region = st.selectbox("지역 선택", region_cols)

# 2) 파라미터 입력
mean_temp = st.slider("예상 기온 상승(°C)", 1.0, 4.0, 2.0, 0.1)
std_temp = st.slider("기온 상승 표준편차", 0.1, 1.0, 0.3, 0.1)
iterations = st.slider("시뮬레이션 반복 횟수", 100, 5000, 1000, 100)

# 3) 실행 버튼
if st.button("시뮬레이션 실행"):

    # 🔑 Boolean 인덱싱 (칼럼명은 이미 소문자)
    mask = disaster_df["region"] == region
    base_damage = float(disaster_df.loc[mask, "damage_amount_hundred_million_won"].mean())

    if pd.isna(base_damage):
        st.warning(f"{region}의 피해 데이터가 없어 기본값 0을 사용합니다.")
        base_damage = 0.0

    damages = run_monte_carlo(
        base_damage=base_damage,
        mean_temp=mean_temp,
        std_temp=std_temp,
        iterations=iterations,
    )

    st.success(f"예측 평균 피해액: {damages.mean():.2f} 억 원")
    plot_line_chart(weather_df, "date", region, f"{region} 일별 기온")
    plot_pie_chart(
        disaster_df.groupby("region")["damage_amount_hundred_million_won"].sum(),
        "지역별 누적 피해액 비율",
    )
