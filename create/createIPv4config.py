import json
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

source = []
target = []
degree = []

A = [0] * 300
link = [[]]        
count = 0
topo = np.zeros((212,212))


f = open("E:\\py\\create\\IPv4Config.xml", "w")
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

#IPv4Config
f.write("<config>\n")

for i in range(len(source)):
    if(i < 246):
        f.write("\t<interface hosts='A" + str(source[i]) + "' names='ppp" + str(A[source[i]]) + "' address='10.10." + str(i + 10) +
        ".1' netmask='255.255.255.0' groups='224.0.0.1 224.0.0.2 224.0.0.5' metric='1'/>\n")
        f.write("\t<interface hosts='A" + str(target[i]) + "' names='ppp" + str(A[target[i]]) + "' address='10.10." + str(i + 10) +
        ".2' netmask='255.255.255.0' groups='224.0.0.1 224.0.0.2 224.0.0.5' metric='1'/>\n")
        A[source[i]] += 1
        A[target[i]] += 1
    else:
        f.write("\t<interface hosts='A" + str(source[i]) + "' names='ppp" + str(A[source[i]]) + "' address='10.11." + str(i - 236) +
        ".1' netmask='255.255.255.0' groups='224.0.0.1 224.0.0.2 224.0.0.5' metric='1'/>\n")
        f.write("\t<interface hosts='A" + str(target[i]) + "' names='ppp" + str(A[target[i]]) + "' address='10.11." + str(i - 236) +
        ".2' netmask='255.255.255.0' groups='224.0.0.1 224.0.0.2 224.0.0.5' metric='1'/>\n")
        A[source[i]] += 1
        A[target[i]] += 1

f.write("\n")

for i in range():
    if(i < 246):
        f.write("\t<interface hosts='A" + str(i) + "' names='eth0' address='172." + str(i + 10) + ".4.255' netmask='255.255.255.0' metric='1'/>\n")
    else:
        f.write("\t<interface hosts='A" + str(i) + "' names='eth0' address='173." + str(i - 236) + ".4.255' netmask='255.255.255.0' metric='1'/>\n")


for i in range():
    if(i < 246):
        f.write("\t<interface hosts='HA" + str(i) + "' names='eth0' address='172." + str(i + 10) + ".4.1' netmask='255.255.255.0' mtu='1500' metric='1'/>\n")
    else:
        f.write("\t<interface hosts='HA" + str(i) + "' names='eth0' address='173." + str(i -236) + ".4.1' netmask='255.255.255.0' mtu='1500' metric='1'/>\n")

f.write("\n")
f.write("\t<route hosts='H*' destination='*' netmask='*' interface='eth0'/>\n")
f.write("\t<route hosts='R*' destination='*' netmask='0.0.0.0' interface='ppp0'/>\n")
f.write("\n")

f.write("</config>\n")