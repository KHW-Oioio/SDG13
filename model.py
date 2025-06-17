# model.py
import numpy as np
import pandas as pd
import networkx as nx

def run_monte_carlo(base_damage=100, mean_temp=2.0, std_temp=0.3, iterations=1000):
    np.random.seed(42)
    temp_increases = np.random.normal(loc=mean_temp, scale=std_temp, size=iterations)
    damage_results = base_damage * (1 + 0.2 * temp_increases)
    return damage_results

def build_graph(disaster_df):
    G = nx.Graph()
    for _, row in disaster_df.iterrows():
        region = row["region"]
        damage = row["damage_amount_hundred_million_won"]
        G.add_node(region, damage=damage)
    for i, r1 in enumerate(disaster_df["region"]):
        for j, r2 in enumerate(disaster_df["region"]):
            if i < j:
                G.add_edge(r1, r2, weight=np.random.rand())
    return G

def get_top_regions(disaster_df, top_n=5):
    grouped = disaster_df.groupby("region")["damage_amount_hundred_million_won"].sum()
    return grouped.sort_values(ascending=False).head(top_n)
