# JSAT Documentation

## Outline:

- JSON file format, creating nodes, edges
- The script file
= Highlighting nodes for strategies in the script file

# Part 1: The data folder, Where the nodes and edge relationships of the network are created
- First, navigate to the data folder in jsat, then to your project. In this case we are looking at NSFCareerProj, and then RevisedWMC folder. 
 
- The Revised WMC folder contains json files, which will contain our edge and node relationships that define the graph that will be generated by running the script. 
- In “GraphData” we have two sections, one for creating nodes and one for creating edges, which are the relationships/connections between the nodes. We need to define both to create the network. 
- Nodes are given a name that will be displayed on the network (usually abbreviated), assigned a node type, and then a note can be given for the entire name

 ``` JSON
"Nodes": {
    "OST": {
        "Type": "BaseEnvironmentResource",
        "UserData": "ObservedSubsystemTemperatures"
    },
    "RS": {
        "Type": "BaseEnvironmentResource",
        "UserData": "RobotState"
    },
    "GL": {
        "Type": "BaseEnvironmentResource",
        "UserData": "GoalLocation"
    }
}
```


## Node example
- “OST” will the displayed abbreviated name, the “Type” is a Base EnvironmentResource, and “UserData” is the full name ObservedSubsystemTemperatures
- After defining all the nodes in the network, then we can define the edges that connect them. The edges in our network are directed, meaning that they point from one node to another (in one direction)

 ``` JSON
 "Edges": [
    {
        "Source": "BLM",
        "Target": "OBL",
        "UserData": {
            "QOS": ""
        }
    },
    {
        "Source": "OBL",
        "Target": "RPP",
        "UserData": {
            "QOS": ""
        }
    }
]
```

- Each edge has a “Source” node and a “Target” node that is the node to which the arrow is pointing. It is possible for a source node to be pointing at several target nodes. However, one must make sure to only connect functions to resources, as connections cannot be made between nodes of the same type (this violates the logic of the network)
- “UserData” is present if you wish to give a name to the label, but we have decided to omit this for our example
- “QOS” defines the Quality of Service of an edge relationship, which defines how often a resource needs to be updated by performing its associated function 
o	Example: If the QOS = 45 seconds, then if a resource hasn’t been updated in 50 seconds, then the resource in that relationship is out-of-date. If the resource was updated 30 seconds ago, then the quality of that resource is still up-to-date 

## Part 2: The script file and generating the network

``` Python
''' The folder containing the JSON data.
'''
directory: str = "data/"

''' The JSON files in the given folder
'''
data_sets: list[str] = [
    "robot_example",
]
```
 
- First make sure that the directory is set to the folder where your data is located, in this case it is the folder we previously discussed “RevisedWMC” where are json files are located
- In “data_sets” you can list multiple json data files if you want to be able to run different configurations easily, just ensure that one json folder is uncommented, in our case “Run4”
- 

''' # Main network
''' main_net = data_dict["robot_example"]
```
