import streamlit as st
from data_loader import load_weather_data, load_disaster_data
from utils import plot_line_chart, plot_pie_chart, plot_histogram
from model import run_monte_carlo

st.title("🌍 SDGs‑13 기후변화 피해 예측 (몬테카를로 시뮬레이션)")

weather_df = load_weather_data()
disaster_df = load_disaster_data()

region_cols = [c for c in weather_df.columns if c.lower() != "date"]
region = st.selectbox("지역 선택", region_cols)

mean_temp = st.slider("예상 기온 상승(°C)", 1.0, 4.0, 2.0, 0.1)
std_temp = st.slider("기온 상승 표준편차", 0.1, 1.0, 0.3, 0.1)
iterations = st.slider("시뮬레이션 반복 횟수", 100, 5000, 1000, 100)

if st.button("시뮬레이션 실행"):
    mask = disaster_df["region"] == region
    base_damage = float(disaster_df.loc[mask, "damage_amount_hundred_million_won"].mean())
    if not base_damage or pd.isna(base_damage):
        st.warning(f"{region}의 피해 데이터가 없어 기본값 0 사용")
        base_damage = 0.0

    damages = run_monte_carlo(base_damage, mean_temp, std_temp, iterations)
    st.success(f"예측 평균 피해액: {damages.mean():.2f} 억 원")
    
    plot_histogram(damages, "예측 피해액 분포")
    plot_line_chart(weather_df, "date", region, f"{region} 일별 기온")
    plot_pie_chart(
        disaster_df.groupby("region")["damage_amount_hundred_million_won"].sum(),
        "📊 지역별 누적 피해 비율"
    )
