# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 18:31:13 2019

@author: z
"""

import numpy as np
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

#印度村庄人脉网络
A1 = np.loadtxt("adj_allVillageRelationships_vilno_1.csv",delimiter=",")
A2 = np.loadtxt("adj_allVillageRelationships_vilno_2.csv",delimiter=",")

G1 = nx.Graph(A1)
G2 = nx.Graph(A2)

def basic_net_stats(G):
    degree_sequence = [d for n,d in G.degree()]    
    print("Nunber of nodes: %d" % G.number_of_nodes())
    print("Nunber of edges: %d" % G.number_of_edges())
    print("Average degree: %.2f" % np.mean(degree_sequence))
    
basic_net_stats(G1)
basic_net_stats(G2)

#最大连接组件
gen = nx.connected_component_subgraphs(G1)

G1_LCC = max(nx.connected_component_subgraphs(G1),key=len)
G2_LCC = max(nx.connected_component_subgraphs(G2),key=len)

plt.figure()
nx.draw(G1_LCC,node_size=20,node_color="red",edge_color="gray")
len(G1_LCC)/len(G1)

plt.figure()
nx.draw(G2_LCC,node_size=20,node_color="green",edge_color="gray")
len(G2_LCC)/len(G2)
