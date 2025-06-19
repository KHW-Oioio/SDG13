import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_line_chart(df, x_col, y_col, title):
    fig, ax = plt.subplots()
    ax.plot(df[x_col], df[y_col], marker='o')
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    st.pyplot(fig)

def plot_pie_chart(series, title):
    fig, ax = plt.subplots()
    ax.pie(series, labels=series.index, autopct='%1.1f%%', startangle=90)
    ax.set_title(title)
    st.pyplot(fig)

def plot_histogram(data, title):
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, color='skyblue', edgecolor='black')
    ax.set_title(title)
    ax.set_xlabel("예측 피해액")
    ax.set_ylabel("빈도")
    st.pyplot(fig)
