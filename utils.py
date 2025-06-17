# utils.py

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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

def plot_heatmap(data, title):
    fig, ax = plt.subplots()
    sns.heatmap(data, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax)
    ax.set_title(title)
    st.pyplot(fig)
