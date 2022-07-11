#210708
#生成的vbetweeness直接在json文件里修改
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
for i in range(20):     #20对点对点（度==1）
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


#-----------------------写入omnet.ini---------------------------#

# UDP traffic generation parameters
f1 = open("omnetpp.ini","w")
f1.write("[General]\n")
f1.write("\n")
f1.write("description = \"Multi OSPF routing test + BGP\"\n")
f1.write("sim-time-limit = 2000s\n")

f1.write("output-scalar-file = results.sca\n")
f1.write("output-vector-file = results.vec\n")
f1.write("output-scalar-precision = 2\n")

f1.write("**.app[0].**.scalar-recording = false\n")
f1.write("**.scalar-recording = false\n")
f1.write("**.vector-recording = true\n")
#**.vector-recording-intervals = ..100, 200..300, 400..500, 600..700, 800..900, 1000..1100, 1200..1300, 1400..1500, 1600..1700, 1800..1900

# ip settings
f1.write("**.rsvp.procDelay = 1us\n")

#tcp settings
f1.write("**.tcp.typename = \"Tcp\"\n")
f1.write("**.tcp.mss = 1024\n")
f1.write("**.tcp.advertisedWindow = 14336\n")
f1.write("**.tcp.tcpAlgorithmClass = \"TcpReno\"\n")

# OSPF configuration
f1.write("**.ospfConfig = xmldoc(\"OSPFConfig.xml\")\n")

#scenariomanager
f1.write("*.scenarioManager.script = xmldoc(\"scenario.xml\")\n")

# Visualizer settings
f1.write("*.visualizer.interfaceTableVisualizer.displayInterfaceTables = true\n")

# bgp settings
f1.write("**.bgpConfig = xmldoc(\"BGPConfig.xml\")\n")

f1.write("**.bgp.redistributeOspf = \"E2\"\n")

# router setting
f1.write("**.ppp[*].ppp.queue.typename = \"DropTailQueue\"\n")
f1.write("**.ppp[*].ppp.queue.packetCapacity = 20\n")
f1.write("**.ppp[*].ppp.queue.dataCapacity = 102400b\n")

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

#f2 = open("vbetween0708.txt","w")
#for i in range(len(test)):
#    f2.write("source:"+str(test[i][0])+"\n")
#    f2.write("target:"+str(test[i][1])+"\n")
#    f2.write("vbetween:"+str(test[i][2])+"\n")
#    f2.write("\n")

for i in range(dict1['property']['n_links']):
    dict1['links'][i]['betweenness'] = 0
    for j in range(len(test)):
        if((dict1['links'][i]['source'] == test[j][0]) and (dict1['links'][i]['target'] == test[j][1])):
            dict1['links'][i]['betweenness'] = test[j][2]
            

output_json_file = 'graph_change0708.json'
file_out = open(output_json_file, "w")
file_out.write(json.dumps(dict1, indent=4))
