import numpy as np
import networkx as nx
import pandas as pd

def run_monte_carlo(base_damage=100, mean_temp=2.0, std_temp=0.3, iterations=1000):
    np.random.seed(42)
    temp_increases = np.random.normal(loc=mean_temp, scale=std_temp, size=iterations)
    damage_results = base_damage * (1 + 0.2 * temp_increases)
    return damage_results

def build_graph(disaster_df):
    G = nx.Graph()
    for _, row in disaster_df.iterrows():
        G.add_node(row["region"], damage=row["damage_amount_hundred_million_won"])
    return G

def get_top_regions(disaster_df, top_n=5):
    grouped = disaster_df.groupby("region")["damage_amount_hundred_million_won"].sum()
    return grouped.sort_values(ascending=False).head(top_n)
