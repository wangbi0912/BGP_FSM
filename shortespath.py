#将49对通信的路径打印出来
import json
from networkx.algorithms import swap
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
source = []
target = []
betweeness = []
count = 0
topo = np.zeros((212, 212))
graph = 'graph.json'

with open(graph) as gr:
    dict1 = json.load(gr)
    for i in range(dict1['property']['n_links']):
        source.append(dict1['links'][i]['source'])
        target.append(dict1['links'][i]['target'])
        topo[source[i]][target[i]] = 1

G = nx.Graph()
for i in range(len(topo)):
    for j in range(len(topo)):
        G.add_node(i)
        if topo[i][j]:
            G.add_edge(i,j)

path = nx.dijkstra_path(G, source=27, target=60)
print(path)