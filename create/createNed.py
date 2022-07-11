import json
from networkx.algorithms.centrality import betweenness
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

source = []
target = []
bet = []
degree = []

A = [0] * 300
link = [[]]        
count = 0
topo = np.zeros((212,212))


f = open("E:\\py\\create\\network.ned", "w")
graph = 'E:\\py\\create\\graph_change0708.json'


with open(graph) as gr:
    dict1 = json.load(gr)
    nodeNum = dict1['property']['n_nodes']              #节点数
    for i in range(dict1['property']['n_nodes']):
        degree.append(dict1['nodes'][i]['degree'])
    # betweeness_n1_index = [i for i, x in enumerate(betweeness) if x == 1]
    for i in range(dict1['property']['n_links']):
        source.append(dict1['links'][i]['source'])
        target.append(dict1['links'][i]['target'])  
        bet.append(dict1['links'][i]['betweenness']) 
        topo[source[i]][target[i]] = 1

    
G = nx.Graph()
for i in range(len(topo)):
    for j in range(len(topo)):
        if topo[i][j] :
            G.add_edge(i,j)
nx.draw_networkx(G)
plt.show()
pos = nx.spring_layout(G)
for i in pos.keys(): 
    pos[i][0] = (pos[i][0] + 1) * 2000
    pos[i][1] = (pos[i][1] + 1) * 2000


#生成ned头文件
f.write("package inet.examples.bgpv4.BgpAndOspf;\n")
f.write("import inet.common.misc.ThruputMeteringChannel;\n")
f.write("import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;\n")
f.write("import inet.node.bgp.BgpRouter;\n")
f.write("import inet.node.ethernet.EtherSwitch;\n")
f.write("import inet.node.inet.StandardHost;\n")
f.write("import inet.node.ospfv2.OspfRouter;\n")
f.write("import inet.visualizer.integrated.IntegratedCanvasVisualizer;\n")
f.write("import inet.common.scenario.ScenarioManager;\n")
f.write("\n")
f.write("network BgpNetwork\n")
f.write("{\n")

f.write("\ttypes:\n")


#
link_exist = [0]*1000
for i in range(dict1['property']['n_links']):
    if(link_exist[bet[i]] != 0):
        continue
    link_exist[bet[i]] = 1
    if(bet[i] != 0):
        f.write("\t\tchannel LINK_" + str(bet[i]) + " extends ThruputMeteringChannel\n")
        f.write("\t\t{\n")
        f.write("\t\t\tparameters:\n")
        f.write("\t\t\t\tdelay = 50us;\n")
        f.write("\t\t\t\tdatarate = " + str(bet[i] * 10) + "Mbps;\n")
        f.write("\t\t\t\tdisplayAsTooltip = true;\n")
        f.write("\t\t\t\tthruputDisplayFormat = \"#N\";\n")
        f.write("\t\t}\n")
    else:
        f.write("\t\tchannel LINK_" + str(bet[i]) + " extends ThruputMeteringChannel\n")
        f.write("\t\t{\n")
        f.write("\t\t\tparameters:\n")
        f.write("\t\t\t\tdelay = 50us;\n")
        f.write("\t\t\t\tdatarate = 10Mbps;\n")
        f.write("\t\t\t\tdisplayAsTooltip = true;\n")
        f.write("\t\t\t\tthruputDisplayFormat = \"#N\";\n")
        f.write("\t\t}\n")


f.write("\tsubmodules:\n")
f.write("\t\tvisualizer: IntegratedCanvasVisualizer {\n")
f.write("\t\t\tparameters:\n")
f.write("\t\t\t\t@display(\"p=100,100;is=s\");\n")
f.write("\t\t}\n")
f.write("\t\tconfigurator: Ipv4NetworkConfigurator {\n")
f.write("\t\t\tparameters:\n")
f.write("\t\t\t\t@display(\"p=100,200;is=s\");\n")
f.write("\t\t\t\tconfig = xmldoc(\"IPv4Config.xml\");\n")
f.write("\t\t\t\taddStaticRoutes = false;\n")
f.write("\t\t\t\taddDefaultRoutes = false;\n")
f.write("\t\t\t\taddSubnetRoutes = false;\n")
f.write("\t\t}\n")
#

for i in pos.keys():
    f.write("\t\tA"+str(i)+":BgpRouter{\n")
    f.write("\t\t\tparameters:\n")
    f.write("\t\t\t\t@display(\"p="+str(pos[i][0])+","+str(pos[i][1])+"\");\n")
    f.write("\t\t\tgates:\n")
    f.write("\t\t\t\tpppg["+str(degree[i])+"];\n")
    f.write("\t\t\t\tethg[1];\n")
    f.write("\t\t}\n")

for i in pos.keys():
    f.write("\t\tHA"+str(i)+": StandardHost {\n")
    f.write("\t\t\tparameters:\n")
    f.write("\t\t\t\t@display(\"p="+str(pos[i][0]+30)+","+str(pos[i][1]+30)+";i=device/pc\");\n")
    f.write("\t\t\tgates:\n")
    f.write("\t\t\t\tethg[1];\n")
    f.write("\t\t}\n")
for i in pos.keys():
    f.write("\t\tPA"+str(i)+": EtherSwitch {\n")
    f.write("\t\t\tparameters:\n")
    f.write("\t\t\t\t@display(\"p="+str(pos[i][0]+15)+","+str(pos[i][1]+15)+"\");\n")
    f.write("\t\t\tgates:\n")
    f.write("\t\t\t\tethg[2];\n")
    f.write("\t\t}\n")

f.write("\tconnections:\n")
for i in range(len(source)):
    f.write("\t\tA" + str(source[i]) + ".pppg[" + str(A[source[i]]) + "] <--> " + "LINK_" + str(bet[i]) + " <--> A" + str(target[i]) + ".pppg[" + str(A[target[i]]) + "];\n")
    A[source[i]] += 1
    A[target[i]] += 1

for i in range(nodeNum):
    f.write("\t\tA" + str(i) + ".ethg[0] <--> LINK_100 <--> PA" + str(i) + ".ethg[0];\n")
    f.write("\t\tPA" + str(i) + ".ethg[1] <--> LINK_100 <--> HA" + str(i) + ".ethg[0];\n")


f.write("}\n")