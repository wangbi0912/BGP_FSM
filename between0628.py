#按照排序生成49对(98个节点)点对点通信
#计算其通信最短路径经过的边的个数



import json
from networkx.algorithms import swap
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
source = []
target = []
betweeness = []

#by wb 210705
#加入边缘node
betweeness1 = []

count = 0
topo = np.zeros((212, 212))
graph = 'graph.json'
with open(graph) as gr:
    dict1 = json.load(gr)
    for i in range(dict1['property']['n_links']):
        source.append(dict1['links'][i]['source'])
        target.append(dict1['links'][i]['target'])
        topo[source[i]][target[i]] = 1
    for i in range(dict1['property']['n_nodes']):
        if  dict1['nodes'][i]['degree'] > 1:
            tup = (i,dict1['nodes'][i]['degree'])
            betweeness.append(tup)
    
    #by wb 210705
    for i in range(dict1['property']['n_nodes']):
        if  dict1['nodes'][i]['degree'] == 1:
            tup = (i,dict1['nodes'][i]['degree'])
            betweeness1.append(tup)
betweeness1.remove((42,1))
betweeness1.remove((45,1))
betweeness1.remove((46,1))
betweeness1.remove((118,1))
betweeness1.remove((119,1))
betweeness1.remove((122,1))
betweeness1.remove((123,1))
betweeness1.remove((128,1))


sortedList = sorted(betweeness,key = lambda s: s[1],reverse = True)
sortedList.remove((41,2))
G = nx.Graph()
for i in range(len(topo)):
    for j in range(len(topo)):
        G.add_node(i)
        if topo[i][j]:
            G.add_edge(i,j)
#nx.draw_networkx(G)
#plt.show()

sortedNode = []
for i in range(98):
    sortedNode.append(sortedList[i][0])
random.shuffle(sortedNode)

t_source = []
t_target = []
for i in range(49):     #49对点对点（度>=2）
    t_source.append(sortedNode[i])
    t_target.append(sortedNode[i+49])

#by wb 210705
for i in range(20):     #20对点对点（度==2）
    t_source.append(betweeness1[i][0])
    t_target.append(betweeness1[i+49][0])

#print(t_source)
#print(t_target)

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
    f1.write("**.HA" +str(t_source[i])+ ".app[0].messageLength = 1024 bytes\n")
    f1.write("**.HA" +str(t_source[i])+ ".app[0].sendInterval = 3 ms\n")
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