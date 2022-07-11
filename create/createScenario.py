import json
import random
from numpy.lib.utils import source

link = []           #[[souece, target, betweenness], [souece, target, betweenness]...]

f = open("E:\\py\\create\\scenario.xml", "w")
graph = 'E:\\py\\create\\graph_change0708.json'

pppg = [0] * 300
source = []
target = []
betweenness = []

with open(graph) as gr:
    dict1 = json.load(gr)
    for i in range(dict1['property']['n_links']):
        source.append(dict1['links'][i]['source'])
        target.append(dict1['links'][i]['target'])
        betweenness.append(dict1['links'][i]['betweenness'])   



for i in range(len(source)):
    link.append([source[i], target[i], betweenness[i], pppg[source[i]], pppg[target[i]]])
    pppg[source[i]] += 1
    pppg[target[i]] += 1

link_sorted = sorted(link,key=(lambda link:link[2]),reverse=True)
#print(link_sorted)

f.write("<scenario>\n")


time = 200
start_time = 110     #仿真时长为2000s，间隔设置为200s，初始时间为110s
mode = 0                #mode = 0 策略仿真, mode = 1 随机仿真


#随机生成数组
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list



if(mode == 1):
#策略选择
    for i in range(5):
        f.write("\t<at t=\"" + str(start_time) + "\">\n")
        f.write("\t\t<set-channel-param src-module=\"A" + str(link_sorted[i][0]) + "\" src-gate=\"pppg[" + str(link_sorted[i][3]) + "]\" dest-gate=\"A" + str(link_sorted[i][1]) + "\" par=\"datarate\" value=\"10bps\"/>\n")
        f.write("\t\t<set-channel-param src-module=\"A" + str(link_sorted[i][1]) + "\" src-gate=\"pppg[" + str(link_sorted[i][4]) + "]\" dest-gate=\"A" + str(link_sorted[i][0]) + "\" par=\"datarate\" value=\"10bps\"/>\n")
        f.write("\t</at>\n")
        start_time = start_time + time
else:
    random_list = random_int_list(0, 200, 5)
    for i in range(5):
        f.write("\t<at t=\"" + str(start_time) + "\">\n")
        f.write("\t\t<set-channel-param src-module=\"A" + str(link_sorted[random_list[i]][0]) + "\" src-gate=\"pppg[" + str(link_sorted[random_list[i]][3]) + "]\" dest-gate=\"A" + str(link_sorted[random_list[i]][1]) + "\" par=\"datarate\" value=\"10bps\"/>\n")
        f.write("\t\t<set-channel-param src-module=\"A" + str(link_sorted[random_list[i]][1]) + "\" src-gate=\"pppg[" + str(link_sorted[random_list[i]][4]) + "]\" dest-gate=\"A" + str(link_sorted[random_list[i]][0]) + "\" par=\"datarate\" value=\"10bps\"/>\n")
        f.write("\t</at>\n")
        start_time = start_time + time


f.write("</scenario>\n")    
