# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:31:13 2019

@author: z
"""

import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import bernoulli


G = nx.karate_club_graph()
nx.draw(G,with_labels=True,node_color="lightblue",edge_color="gray")

N=20
p=0.2
def er_graph(N,p):
    """"Generate an ER graph."""
    G=nx.Graph()
    G.add_nodes_from(range(N))
    for node1 in G.node():
        for node2 in G.node():
            if node1 < node2 and bernoulli.rvs(p=p):
                G.add_edge(node1,node2)
    return G

nx.draw(G,node_size=40,node_color="lightblue",edge_color="gray")

#绘制度分布图
def plot_degree_distribution(G):
    degree_sequence = [d for n,d in G.degree()]
    plt.hist(degree_sequence,histtype="step")
    plt.xlabel("Degree $k$")
    plt.ylabel("$P(k)$")
    plt.title("Degree distribution")
    
G1 = er_graph(500,0.08)
plot_degree_distribution(G1)

