import json
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

source = []
target = []
degree = []


link = [[]]        
count = 0
topo = np.zeros((212,212))


f = open("E:\\py\\create\\network.ned", "w")
graph = 'graph.json'


with open(graph) as gr:
    dict1 = json.load(gr)
    nodeNum = dict1['property']['n_nodes']              #节点数
    for i in range(dict1['property']['n_nodes']):
        degree.append(dict1['nodes'][i]['degree'])
    # betweeness_n1_index = [i for i, x in enumerate(betweeness) if x == 1]
    for i in range(dict1['property']['n_links']):
        source.append(dict1['links'][i]['source'])
        target.append(dict1['links'][i]['target'])   
        topo[source[i]][target[i]] = 1

    
G = nx.Graph()
for i in range(len(topo)):
    for j in range(len(topo)):
        if topo[i][j] :
            G.add_edge(i,j)

nx.draw(G,pos = nx.spring_layout(G),
        node_size = 30, 
        with_label = False,
        edgelist=None,
        width=1.0,
        edge_color='k',
        style='solid',
        alpha=1.0,
        edge_cmap=None,
        edge_vmin=None,
        edge_vmax=None,)

plt.show()
