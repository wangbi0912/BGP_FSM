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


f = open("E:\\py\\create\\OSPFConfig.xml", "w")
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

#OSPFConfig
f.write("<?xml version=\"1.0\"?>\n")
f.write("<OSPFASConfig xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"OSPF.xsd\">\n")

f.write("\n")

for i in range(nodeNum):
    f.write("\t<Area id=\"0.0.0." + str(i + 1) + "\">\n")
    f.write("\t\t<AddressRange address=\"172." + str(i + 10) + ".4.0\" mask=\"255.255.255.0\" status=\"Advertise\" />\n")
    f.write("\t</Area>\n")
    f.write("\n")

for i in range(nodeNum):
    f.write("\t<Router name=\"A" + str(i) + "\" RFC1583Compatible=\"true\">\n")
    f.write("\t\t<BroadcastInterface ifName=\"eth0\" areaID=\"0.0.0." + str(i + 1) + "\" interfaceOutputCost=\"10\" routerPriority=\"1\" />\n")
    f.write("\t</Router>\n")
    f.write("\n")

f.write("</OSPFASConfig>\n")
