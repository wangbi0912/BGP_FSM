#Random
#随机选取50个source和50个target，计算其通信最短路径经过的边的个数



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
#nx.draw_networkx(G)
#plt.show()
random_source = []
random_target = []
t_source1 = random.sample(range(0, 40), 25)
t_source2 = random.sample(range(47, 117), 25)
t_source = t_source1 + t_source2
t_target = random.sample(range(129, 211), 50)
#print(t_source)
#print(t_target)

#shortest_path = np.zeros((50,10))
shortest_path = []
for i in range(len(t_source)):
    path = nx.dijkstra_path(G, source=t_source[i], target=t_target[i])
    for j in range(len(path) - 1):
        shortest_path.append([path[j],path[j+1]])
    
    #print(path)

for i in range(len(shortest_path)):
    if shortest_path[i][0] > shortest_path[i][1]:
        shortest_path[i][0], shortest_path[i][1] = shortest_path[i][1], shortest_path[i][0]
print(shortest_path)
np_spath = np.array(shortest_path)
np_spath = np_spath[np.lexsort(np_spath[:,::-1].T)] #按照首列排序

np_spath = np_spath.tolist()

map = {}
for i in np_spath:
        s = str(i)
        if s in map.keys():
            map[s] = map[s] + 1
        else:
            map[s] = 1

test = []

i = 0
for key in map.keys():
        test.append([np_spath[i][0],np_spath[i][1],map[key]])
        i = i + map[key]
print(test)
#   test[i][0]:source
#   test[i][1]:target
#   test[i][2]:vbetween

# UDP traffic generation parameters
f1 = open("udp_traffic.txt","w")
for i in range(len(t_source)):
    f1.write("**.HA" +str(t_source[i])+ ".numApps = 1\n")
    f1.write("**.HA" +str(t_source[i])+ ".app[*].typename = \"UdpBasicApp\"\n")
    f1.write("**.HA" +str(t_source[i])+ ".app[0].startTime = 100s\n")
    f1.write("**.HA" +str(t_source[i])+ ".app[0].localPort = 1234\n")
    f1.write("**.HA" +str(t_source[i])+ ".app[0].destPort = 5678\n")
    f1.write("**.HA" +str(t_source[i])+ ".app[0].messageLength = 128 bytes\n")
    f1.write("**.HA" +str(t_source[i])+ ".app[0].sendInterval = 2 ms\n")
    f1.write("**.HA" +str(t_source[i])+ ".app[0].destAddresses = \"172." + str(t_target[i] + 10) + ".4.1\"\n")
    f1.write("\n")
    f1.write("**.HA" +str(t_target[i])+ ".numApps = 1\n")
    f1.write("**.HA" +str(t_target[i])+ ".app[*].typename = \"UdpSink\"\n")
    f1.write("**.HA" +str(t_target[i])+ ".app[0].localPort = 5678\n")
    f1.write("\n")

f2 = open("vbetween.txt","w")
for i in range(len(test)):
    f2.write("source:"+str(test[i][0])+"\n")
    f2.write("target:"+str(test[i][1])+"\n")
    f2.write("vbetween:"+str(test[i][2])+"\n")
    f2.write("\n")