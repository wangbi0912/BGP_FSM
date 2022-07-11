import json

import numpy as np
import re
import matplotlib.pyplot as plt
import networkx as nx
transmissionState = 'transmission.json'
graph = 'graph.json'
topo = np.zeros((212, 212))
source = []
target = []
change = []
txState = {}
numbers = {}  # 存放非正常结束路由器的端口号与路由器号
target_host = []#存放非正常结束路由器链路另一端路由器号
count = 0
line = []
row = []
change_row = []
list2 = []

# 根据value查找key


def get_keys(d, value):
    return [k for k, v in d.items() if v == value]


def is_odd(n):
    return n % 2 == 1



# 打开json，读取端点结束传输时间
with open(transmissionState) as ts:
    dict0 = json.load(ts)
    for i in range(len(dict0['General-0-20210714-16:48:32-11814']['vectors'])):
        endtime = dict0['General-0-20210714-16:48:32-11814']['vectors'][i]['time'][-1]
        host = dict0['General-0-20210611-15:14:34-176316']['vectors'][i]['module']
        txState[host] = endtime


# 查找非正常结束传输的端口，存入change
for key, value in txState.items():
    if value < 1900:
        change.append(key)
# list1 = []
# list1.append('BgpNetwork.A0.ppp[0].ppp')
# list1.append('BgpNetwork.A1.ppp[1].ppp')
# list1.append('BgpNetwork.A2.ppp[1].ppp')
# list1.append('BgpNetwork.A5.ppp[0].ppp')  # 测试用例
# 提取出非正常结束传输端口的路由器号和端口号
host_string = ",".join(change)
host_number_string = re.findall(r"\d+", host_string)
host_number = list(map(int, host_number_string))
for i in range(len(host_number)):
    if is_odd(i):
        numbers['post_number'+str(int(i/2))] = host_number[i]
    else:
        numbers['host_number'+str(int(i/2))] = host_number[i]


# 打开graph。json，将网络链接信息存在矩阵中
# 获取非正常结束路由器链路另一端路由器号
with open(graph) as gr:
    dict1 = json.load(gr)
    for i in range(dict1['property']['n_links']):
        source.append(dict1['links'][i]['source'])
        target.append(dict1['links'][i]['target'])
        topo[source[i]][target[i]] = 1
    not_zero = np.nonzero(topo)
    line = not_zero[0].tolist()
    row = not_zero[1].tolist()
    for i in range(len(line)):
        list2.append((line[i],row[i]))
    for i in range(len(numbers)//2):
        change_row.append(line.index(numbers['host_number'+str(i)])+numbers['post_number'+str(i)])
    # for i in range(len(change_row)-1,-1,-1):
    #     list2.pop(change_row[i])
# 修改拓扑
for i in range(len(change_row)):
    topo[numbers['host_number'+str(i)]][row[change_row[i]]] = 0

# 生成连通子图
G = nx.Graph()
for i in range(len(topo)):
    for j in range(len(topo)):
        G.add_node(i)#去掉这一行就是端口运行状态，孤立节点不画
        if topo[i][j]:
            G.add_edge(i,j)
nx.draw_circular(G)
plt.show()
largest_graphy = max(nx.connected_components(G),key = len)
print(largest_graphy)