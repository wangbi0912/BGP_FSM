#对节点的度进行排序、计算个数
import json
from networkx.algorithms import swap
from networkx.algorithms.centrality import degree_alg
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

degree = []
count = 0
topo = np.zeros((212, 212))
graph = 'graph.json'
with open(graph) as gr:
    dict1 = json.load(gr)
    
    for i in range(dict1['property']['n_nodes']):
        # 43个度 > 3的节点
        # 61个度 > 2的节点
        degree.append(dict1['nodes'][i]['degree'])

sorted_degree = sorted(degree)
print(sorted_degree)