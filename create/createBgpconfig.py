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


f = open("E:\\py\\create\\BGPConfig.xml", "w")
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
nx.draw_networkx(G)
#plt.show()
pos = nx.spring_layout(G)
for i in pos.keys(): 
    pos[i][0] = (pos[i][0] + 1) * 2000
    pos[i][1] = (pos[i][1] + 1) * 2000

f.write("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>\n")
f.write("<BGPConfig xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n")
f.write("\t\t  xsi:schemaLocation=\"BGP.xsd\">\n")
f.write("\n")
f.write("\t<TimerParams>\n")
f.write("\t\t<connectRetryTime> 120 </connectRetryTime>\n")
f.write("\t\t<holdTime> 180 </holdTime>\n")
f.write("\t\t<keepAliveTime> 60 </keepAliveTime>\n")
f.write("\t\t<startDelay> 15 </startDelay>\n")
f.write("\t<TimerParams>\n")
f.write("\n")
f.write("\n")

for i in range(nodeNum):
    f.write("\t<AS id=\"" + str(60010 + i) +"\">\n")
    f.write("\t\t<Router interAddr=\"172."+ str(10 + i) + ".4.255\"/> <!--router A" + str(i) +"-->\n")
    f.write("\t</AS>\n")
    f.write("\n")

for i in range(len(source)):
    f.write("\t<Session id=\"1\">\n")
    if(i < 246):
        f.write("\t\t<Router exterAddr=\"10.10." + str(i + 10) + ".1\" > </Router> <!--Router A" + str(source[i]) + "-->\n")
        f.write("\t\t<Router exterAddr=\"10.10." + str(i + 10) + ".2\" > </Router> <!--Router A" + str(target[i]) + "-->\n")
    else:
        f.write("\t\t<Router exterAddr=\"10.11." + str(i - 236) + ".1\" > </Router> <!--Router A" + str(source[i]) + "-->\n")
        f.write("\t\t<Router exterAddr=\"10.11." + str(i - 236) + ".2\" > </Router> <!--Router A" + str(target[i]) + "-->\n")
    f.write("\t</Session>\n")


f.write("\n")
f.write("</BGPConfig>\n")