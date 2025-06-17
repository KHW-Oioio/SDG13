# File: app.py
import streamlit as st
from data_loader import load_weather_data, load_disaster_data
from model import build_graph, run_monte_carlo, get_top_regions
from utils import plot_line_chart, plot_pie_chart, plot_heatmap

st.set_page_config(page_title="EcoRisk MC", layout="wide")

st.title("EcoRisk MC: 기후 리스크 예측 대시보드")
st.markdown("""
Monte Carlo 시뮬레이션 기반의 재난 위험 예측 및 시각화 웹앱입니다. SDG 13(기후 행동)을 지원합니다.
""")

# Sidebar: 사용자 입력
st.sidebar.header("입력 파라미터")
region = st.sidebar.selectbox("지역(시/도)", load_weather_data().columns.drop('date'))
start_date, end_date = st.sidebar.date_input("기간 선택", ["2022-01-01", "2022-12-31"])
n_iter = st.sidebar.slider("시뮬레이션 반복 횟수(n)", min_value=100, max_value=5000, value=1000, step=100)

if st.sidebar.button("시뮬레이션 실행"):
    # 데이터 수집
    st.info("데이터 수집 중...")
    weather_df = load_weather_data(start_date, end_date)
    disaster_df = load_disaster_data()

    # 그래프 구축
    st.info("그래프 모델 구축 중...")
    G = build_graph(weather_df)

    # 몬테카를로 시뮬레이션
    st.info(f"몬테카를로 시뮬레이션 ({n_iter}회) 실행 중...")
    results = run_monte_carlo(G, weather_df, disaster_df, n_iter)

    # 상위 위험 지역 추출
    st.success("결과 정렬 중...")
    top_regions = get_top_regions(results, top_n=5)

    # 시각화
    st.header("시뮬레이션 결과 시각화")
    st.subheader("연도별 예측 피해액 추이")
    st.pyplot(plot_line_chart(results))

    st.subheader("상위 5개 위험 지역 비율")
    st.pyplot(plot_pie_chart(top_regions))

    st.subheader("위험도 히트맵")
    st.pyplot(plot_heatmap(G, results))

    # 리포트 다운로드
    csv = results.to_csv(index=False).encode('utf-8')
    st.download_button("CSV 다운로드", data=csv, file_name="ecorisk_results.csv", mime="text/csv")


# File: data_loader.py
import pandas as pd

def load_weather_data(start=None, end=None):
    df = pd.read_csv('data/weather.csv', parse_dates=['date'])
    if start and end:
        df = df[(df['date'] >= pd.to_datetime(start)) & (df['date'] <= pd.to_datetime(end))]
    return df.set_index('date')


def load_disaster_data():
    return pd.read_csv('data/disaster.csv')

# File: model.py
import networkx as nx
import numpy as np
import heapq

def build_graph(weather_df):
    G = nx.Graph()
    regions = weather_df.columns.drop('date') if 'date' in weather_df.columns else weather_df.columns
    for r in regions:
        G.add_node(r)
    # 엣지 생성 예시: 인접 행정구역 간 연결
    # for u, v, dist in edges:
    #     G.add_edge(u, v, weight=dist)
    return G


def run_monte_carlo(G, weather_df, disaster_df, n_iter):
    results = []
    for i in range(n_iter):
        sampled = np.random.choice(weather_df.values.flatten(), size=len(G.nodes()))
        damage = {r: alpha*val**beta + np.random.normal(0,1) for r, val in zip(G.nodes(), sampled)}
        results.append(damage)
    return pd.DataFrame(results)


def get_top_regions(results_df, top_n=5):
    mean_damage = results_df.mean()
    return mean_damage.nlargest(top_n)

# File: utils.py
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

def plot_line_chart(results_df):
    fig, ax = plt.subplots()
    results_df.mean().plot(ax=ax)
    ax.set_xlabel('Region')
    ax.set_ylabel('Average Damage')
    return fig


def plot_pie_chart(top_series):
    fig, ax = plt.subplots()
    ax.pie(top_series.values, labels=top_series.index, autopct='%1.1f%%')
    return fig


def plot_heatmap(G, results_df):
    fig, ax = plt.subplots()
    values = results_df.mean().reindex(G.nodes())
    nx.draw_networkx(G, pos=nx.spring_layout(G), node_size=values*1000, with_labels=True, ax=ax)
    return fig
