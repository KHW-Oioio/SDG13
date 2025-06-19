# pages/SDGs-13.py
import streamlit as st
import pandas as pd
from data_loader import load_weather_data, load_disaster_data
from utils import plot_line_chart, plot_pie_chart
from model import run_monte_carlo

st.title("SDGs‑13 몬테카를로 시뮬레이션 대시보드")

# --- 1. 데이터 로딩 ------------------------
weather_df = load_weather_data()
disaster_df = load_disaster_data()

# --- 2. 지역 리스트 안전 추출 -------------
region_cols = [c for c in weather_df.columns if c != "date"]
region = st.selectbox("지역 선택", region_cols)

# --- 3. 시뮬레이션 파라미터 ----------------
mean_temp = st.slider("예상 기온 상승(°C)", 1.0, 4.0, 2.0, 0.1)
std_temp = st.slider("기온 상승 표준편차", 0.1, 1.0, 0.3, 0.1)
iterations = st.slider("시뮬레이션 반복 횟수", 100, 5000, 1000, 100)

# --- 4. 시뮬레이션 실행 --------------------
if st.button("시뮬레이션 실행"):
    damages = run_monte_carlo(
        base_damage=float(disaster_df.query("region == @region")["damage_amount_hundred_million_won"].mean()),
        mean_temp=mean_temp,
        std_temp=std_temp,
        iterations=iterations,
    )
    st.success(f"예측 평균 피해액: {damages.mean():.2f} 억 원")

    # --- 5. 결과 시각화 --------------------
    plot_line_chart(weather_df, "date", region, f"{region} 일별 기온")
    plot_pie_chart(
        disaster_df.groupby("region")["damage_amount_hundred_million_won"].sum(),
        "지역별 누적 피해액 비율",
    )

