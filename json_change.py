import json

input_json_file = 'graph.json'
output_json_file = 'graph_change.json'

file_in = open(input_json_file, "r")
file_out = open(output_json_file, "w")

# load数据到变量json_data
json_data = json.load(file_in)

#print(json_data)

for i in range(json_data['property']['n_links']):
    json_data['links'][i]['betweenness'] = 1

file_out.write(json.dumps(json_data, indent=4))
file_in.close()
file_out.close()
 
