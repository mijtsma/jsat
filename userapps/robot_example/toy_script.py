import sys
import os

# Add the project root to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from core import networkdata as nd
from core.parsing.jsonparser import JSONParser
from core.parsing.jsonencoder import JSONEncoder
from cytoapp.cytoscapeapp import CytoscapeApp
from userapps.robot_example.roverdatahandler import RoverDataHandler
import itertools
import copy
import webbrowser
from core.visualization.tikzstandard import StandardTikzVisualizer as s
from core.visualization.tikzlayer import LayeredTikzVisualizer as l
### HRT Metrics Script

''' The folder containing the JSON data.
'''
directory: str = "data/"
''' The JSON files in the given folder
'''

###### The only place to modify the dataset you want to visualize ######
dataset = "toy_arch2"

data_sets: list[str] = [
    dataset,
]

# Class for user data
class UserData:
    def __init__(self, QOS=1000000):  # Default value set to 1000000
        self.QOS = QOS

# Custom edge_user_data processor
def custom_user_parse(user_data):
    ''' The default behavior for parsing user data. These types of
        functions recieve the data tied to the "UserData" entries in
        JSON files and return what user_data within the network model
        elements should be set to.
    '''

    QOS = user_data["QOS"]
    # user_data = lambda: None
    if QOS != "":
        user_data = UserData(float(QOS))
    else:
        user_data = UserData(1000000) # Assumption for missing data

    return user_data

''' Store the parsed network models in a dictionary.
'''
data_dict: dict[str, nd.NetworkModel] = {}
for name in data_sets:
    data_dict[name] = JSONParser.parse(directory + name + ".json", e_user_data_func = custom_user_parse)

# Main network
main_net = data_dict[dataset]

# Define Agents
Cook = nd.Agent("Cook")
Assistant = nd.Agent("Assistant")

# Assign nodes to agents

##### Architecture 1: The cook does everything alone! ######
##### Architecture 1: The cook does everything alone! ######
# Assign nodes to agents

##### Architecture 1: The cook does everything alone! ######
##### Architecture 1: The cook does everything alone! ######
# agent_assignments = {
#     "Cook": [
#         "IngredientPreparing", 
#         "HeatAdjusting", 
#         "IngredientCombining",
#         "ToolFetching", 
#         "IngredientUnpacking", 
#         "ItemsMoving"
#     ],
#     "Assistant": []
# }

##### Architecture 2: Cook splits work with assistant ######
##### Uncomment only one agent_assignents at a time to visualize! ######
agent_assignments = {
    "Cook": [
        "IngredientPreparing", 
        "HeatAdjusting", 
        "IngredientCombining",
        "Asking for tool", 
        "Asking for ingredient", 
        "Directing items"
    ],
    "Assistant": [
        "ToolFetching", 
        "IngredientUnpacking", 
        "ItemsMoving"
    ]
}


# Map agent names to actual agent objects
agent_lookup = {
    "Cook": Cook,
    "Assistant": Assistant
}

# Assign authority and responsibility
for agent_name, node_list in agent_assignments.items():
    agent = agent_lookup[agent_name]
    for node_id in node_list:
        try:
            node = main_net.get_node(node_id)
            agent.add_action(node, agent.allocation_types.Authority)
            agent.add_action(node, agent.allocation_types.Responsibility)
        except Exception as e:
            print(f"Warning: Could not assign {node_id} to {agent_name} — {e}")

# Identify the shared resources
shared_resources = []

# Loop over all nodes in the graph
for node_id in main_net.get_graph().nodes():
    
    node = main_net.get_node(node_id)
    
    # Check if BaseEnvironmentResource
    if issubclass (node.__class__, nd.BaseEnvironmentResource):

        # Get all neighboring nodes (Function Nodes)
        functions_that_set = main_net.get_graph().predecessors(node_id)
        functions_that_get = main_net.get_graph().successors(node_id)

        # A list of all function pairs that are connected through this resources
        interdependent_functions = list(itertools.product(functions_that_get,functions_that_set))

        # For each pair, check whether roles is the same
        for pair in interdependent_functions:
            agent_setting = main_net.get_node(pair[0]).get_authorized_agent()
            agent_getting = main_net.get_node(pair[1]).get_authorized_agent()

            if agent_setting.id != agent_getting.id:
                shared_resources.append((node_id,pair))


# Identify the functions with authority-responsibility mismatches
functions_w_auth_resp_mismatch = []

# Loop over all nodes in the graph
for node_id in main_net.get_graph().nodes():
    
    node = main_net.get_node(node_id)
    
    # Check if DistributedWorkFunction
    if issubclass (node.__class__, nd.DistributedWorkFunction):

        # Get all neighboring nodes (actionNodes)
        authorized_agent = node.get_authorized_agent()
        # responsible_agent = node.get_responsible_agent()

        # For each pair, check whether roles is the same
        if authorized_agent.id != "IncidentCommand":
            functions_w_auth_resp_mismatch.append(node_id)

# We want to write this new graph to an output JSON file.
# Create a custom encoder for the user data that should fill the QOS
def custom_user_encode(user_data):

    user_data = {
                "QOS": user_data.QOS,
            }
    
    return user_data


# Let's output as a TikZ graph
l.visualize(main_net, "tikzout3.tex")

''' Alter networks after they have been read 
    from JSON.
'''
# This will generate the graph without a highlighted strategy, comment this out if you use on the highlighted strategies below
app = CytoscapeApp(data_dict, RoverDataHandler)

webbrowser.open_new("http://127.0.0.1:8050")
app.run()

