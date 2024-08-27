import json
import os.path
import csv

''' Messy file for converting rover data to json standard
''' 

data_set = "3_2"

resource_filepath = "data/JSON/Rover/OldRoverData/InformationResources_Defense" + data_set + ".csv"
action_filepath = "data/JSON/Rover/OldRoverData/Taskwork_Defense" + data_set + ".csv"
edge_filepath = "data/JSON/Rover/OldRoverData/InfoDependencies_Defense" + data_set + ".csv"
out_file_path = "data/JSON/Rover/Rover" + data_set + ".json"

data: dict = {
    "GraphData":{
        "Nodes":{},
        "Edges":[],
        "Agents":{}
    }
}

converted_strs: dict[str,str] = {}

nodes: dict = data["GraphData"]["Nodes"]

with open(resource_filepath, 'r') as resource_file:
    datareader = csv.reader(resource_file)
    for row in datareader:
        name = row[1]
        converted_strs[name] = "".join(ch for ch in name if ch.isupper())
        if "Commands" in name or "Confirmation" in name:
            nodes[converted_strs[name]] = {
                "Type": "CoordinationGroundingResource",
                "UserData": name
            }
        else:
            nodes[converted_strs[name]] = {
                "Type": "BaseEnvironmentResource",
                "UserData": name
            }

with open(action_filepath, 'r') as action_file:
    datareader = csv.reader(action_file)
    for row in datareader:
        name = row[1]
        converted_strs[name] = "".join(ch for ch in name if ch.isupper())
        if (name.startswith("Monitoring") or 
            name.startswith("Confirm") or
            name.startswith("Command")):
            nodes[converted_strs[name]] = {
                "Type": "SynchronyFunction",
                "UserData": name
            }
        else:
            nodes[converted_strs[name]] = {
                "Type": "DistributedWorkFunction",
                "UserData": name
            }

edges: list = data["GraphData"]["Edges"]

with open(edge_filepath, 'r') as edge_file:
    datareader = csv.reader(edge_file)
    for row in datareader:
        node_names = [row[0], row[1]]
        correct_names = []
        for name in node_names:
            correct_name = ""
            index = 10
            if index + 10 < len(name) and name[index:index+10] == "RoverModel":
                index += 10
            else:
                correct_name += name[10].upper()
                index += 1
            while index < len(name):
                if name[index] == "-":
                    index = index + 11
                    continue
                if name[index] == "_":
                    correct_name += name[index+1].upper()
                    index = index + 2
                    continue
                correct_name += name[index]
                index = index + 1
            correct_names.append(correct_name)
        if row[2] == "get":
            to_add = {
                "Source": converted_strs[correct_names[1]],
                "Target": converted_strs[correct_names[0]]
            }
            edges.append(to_add)
        elif row[2] == "set":
            to_add = {
                "Source": converted_strs[correct_names[0]],
                "Target": converted_strs[correct_names[1]]
            }
            edges.append(to_add)

json_obj = json.dumps(data, indent=4)

with open(out_file_path, 'w') as file:
    file.write(json_obj)
    