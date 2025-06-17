import streamlit as st
from data_loader import load_weather_data, load_disaster_data

st.set_page_config(page_title="SDGs13 기후 분석 대시보드")

st.title("🌍 SDGs 13: 기후 변화 대응 시뮬레이션")
st.markdown("기후 데이터와 재난 데이터를 분석하고, 몬테카를로 시뮬레이션을 통해 지속 가능한 정책 방향을 탐색합니다.")

st.subheader("데이터 미리 보기")
weather = load_weather_data()
disaster = load_disaster_data()

st.write("📈 Weather Data", weather.head())
st.write("🌪️ Disaster Data", disaster.head())

st.info("왼쪽 사이드바 메뉴에서 심화 분석을 진행하세요.")

