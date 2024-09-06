from core import networkdata as nd
from core.parsing.jsonparser import JSONParser
from core.parsing.jsonencoder import JSONEncoder
from cytoapp.cytoscapeapp import CytoscapeApp
from userapps.rovercase.roverdatahandler import RoverDataHandler
import itertools
import copy
import webbrowser
from core.visualization.tikzstandard import StandardTikzVisualizer as s
from core.visualization.tikzlayer import LayeredTikzVisualizer as l
### HRT Metrics Script

''' The folder containing the JSON data.
'''
directory: str = "data/NSFCareerProj/RevisedWMC/"

''' The JSON files in the given folder
'''
data_sets: list[str] = [
    # "Run1",
    # "Run2",
    # "Run3",
    "Run4",
    # "Run5",
    # "Run6"#,
]


# Define a dictionary with edges as keys and lists of QOS values as values
edge_qos_values = {
    # "PP_NWS": [30, 31, 42, 43],
    # ("PP", "NWS"): [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 130, 150, 180, 210, 240, 270],
    ("PP", "NWS"): [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
    # ("PP", "NWS"): [1, 2, 3, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 200, 240, 320],
    # ("Confirmation-BLM", "BLM"): [0, 20, 30, 40, 50, 60, 80]
    # ("confirmation", ""): [0]
    ("confirmation", ""): [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
}

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
main_net = data_dict["Run4"]

# Define roles for both human and operator (is there a way to do this through the JSON?)
operator: nd.Agent = nd.Agent("Operator")
rover: nd.Agent = nd.Agent("Robot")

operator.add_action(main_net.get_node("LAA"), operator.allocation_types.Authority)
operator.add_action(main_net.get_node("OLL"), operator.allocation_types.Authority)
operator.add_action(main_net.get_node("CAM"), operator.allocation_types.Authority)
operator.add_action(main_net.get_node("REV"), operator.allocation_types.Authority)
# Obstacle size estimation?

rover.add_action(main_net.get_node("BLM"), rover.allocation_types.Authority)
rover.add_action(main_net.get_node("TMP"), rover.allocation_types.Authority)
rover.add_action(main_net.get_node("RPP"), rover.allocation_types.Authority)
rover.add_action(main_net.get_node("NWS"), rover.allocation_types.Authority)
rover.add_action(main_net.get_node("IC"), rover.allocation_types.Authority)
rover.add_action(main_net.get_node("RM"), rover.allocation_types.Authority) # Remove this function?

# Responsibility
operator.add_action(main_net.get_node("BLM"), operator.allocation_types.Responsibility)
operator.add_action(main_net.get_node("TMP"), operator.allocation_types.Responsibility)
operator.add_action(main_net.get_node("RPP"), operator.allocation_types.Responsibility)
operator.add_action(main_net.get_node("NWS"), operator.allocation_types.Responsibility)
operator.add_action(main_net.get_node("IC"), operator.allocation_types.Responsibility)
operator.add_action(main_net.get_node("RM"), operator.allocation_types.Responsibility) # Remove this function?


# # Identify the shared resources
# shared_resources = []

# # Loop over all nodes in the graph
# for node_id in main_net.get_graph().nodes():
    
#     node = main_net.get_node(node_id)
    
#     # Check if BaseEnvironmentResource
#     if issubclass (node.__class__, nd.BaseEnvironmentResource):

#         # Get all neighboring nodes (actionNodes)
#         functions_that_set = main_net.get_graph().predecessors(node_id)
#         functions_that_get = main_net.get_graph().successors(node_id)

#         # A list of all function pairs that are connected through this resources
#         interdependent_functions = list(itertools.product(functions_that_get,functions_that_set))

#         # For each pair, check whether roles is the same
#         for pair in interdependent_functions:
#             agent_setting = main_net.get_node(pair[0]).get_authorized_agent()
#             agent_getting = main_net.get_node(pair[1]).get_authorized_agent()

#             if agent_setting.id != agent_getting.id:
#                 shared_resources.append((node_id,pair))


# # For each of the shared resources, do something!
# # Current rule: When an information resource is shared between agents at the taskwork level, 
# # then a function must be created at the teamwork level to show the relaying of information, 
# # such that a shared awareness is formed at the social organizational level. 
# for element in shared_resources:

#     # print("There is a shared resource",element[0],"between ", element[1][0], "and", element[1][1])

#     # Create a shared resources node and a teamwork function node
#     soc_org_node = main_net.add_node(nd.Node("shared_"+element[0])) # TODO: Specify the node type/class
#     teamwork_node = main_net.add_node(nd.ActionNode("sharing_"+element[0]))

#     # Add edge going from teamwork node to shared_resource node
#     main_net.add_edge("sharing_"+element[0],"shared_"+element[0])

#     # Add edge going from original resource to the teamwork node
#     main_net.add_edge(element[0],"sharing_"+element[0])

#     # Add QOS to each edge (making an assumption that this needs to updated always but can change!)
#     user_data = lambda: None
#     user_data.QOS = 0
#     # main_net.get_edge("sharing_"+element[0],"shared_"+element[0]).user_data = user_data # No QOS needed--because is set relationship
#     main_net.get_edge(element[0],"sharing_"+element[0]).user_data = user_data


# Identify the shared resources
shared_actions = []

# Loop over all nodes in the graph
for node_id in main_net.get_graph().nodes():
    
    node = main_net.get_node(node_id)
    
    # Check if DistributedWorkFunction
    if issubclass (node.__class__, nd.DistributedWorkFunction):

        # Get all neighboring nodes (actionNodes)
        authorized_agent = node.get_authorized_agent()
        # responsible_agent = node.get_responsible_agent()

        # For each pair, check whether roles is the same
        if authorized_agent != operator:
            shared_actions.append(node_id)

# For each of the shared action, do something!
# Current rule: When authority-responsibility mismatch, create a confirmation resources and an a confirmation
# action that is allocated to the operator
for node_id in shared_actions:

    if node_id == "RM":
        continue

    # Create a coordination resource and a teamwork function node
    soc_org_node = main_net.add_node(nd.CoordinationGroundingResource("Confirmation-"+node_id)) # TODO: Specify the node type/class
    main_net.get_node("Confirmation-"+node_id).user_data = "Confirmation-"+node_id # Need to fill these for WMC parsing
    teamwork_node = main_net.add_node(nd.SynchronyFunction("Confirming-"+node_id))
    main_net.get_node("Confirming-"+node_id).user_data = "Confirming-"+node_id # Need to fill these for WMC parsing

    # Add edge going from teamwork node to coordination resource
    main_net.add_edge("Confirming-"+node_id,"Confirmation-"+node_id)
    main_net.get_edge("Confirming-"+node_id,"Confirmation-"+node_id).user_data = UserData(100000)

    # Add edges going from coordination resource to original node
    main_net.add_edge("Confirmation-"+node_id,node_id)

    # Add edge going from work domain resources set by shared action to teamwork node
    for wd_resource in main_net.get_graph().successors(node_id):
        main_net.add_edge(wd_resource,"Confirming-"+node_id)
        
        # Add QOS to each edge (making an assumption that this needs to updated always but can change!)
        main_net.get_edge(wd_resource,"Confirming-"+node_id).user_data = UserData(1000000)

    # Allocate authority and responsibility to human
    operator.add_action(main_net.get_node("Confirming-"+node_id), operator.allocation_types.Authority)
    operator.add_action(main_net.get_node("Confirming-"+node_id), operator.allocation_types.Responsibility)

    # Add QOS to each edge (making an assumption that this needs to updated always but can change!)
    main_net.get_edge("Confirmation-"+node_id,node_id).user_data = UserData(0)


# We want to write this new graph to an output JSON file.
# Create a custom encoder for the user data that should fill the QOS
def custom_user_encode(user_data):

    user_data = {
                "QOS": user_data.QOS,
            }
    
    return user_data


# Create all combinations of QOS values for the edges
qos_combinations = list(itertools.product(*edge_qos_values.values()))

# Loop over each combination to create copies of the main_net with these QOS values
for qos_combo in qos_combinations:
    # Create a deep copy of the main_net to modify
    temp_net = copy.deepcopy(main_net)
    
    # Set the QOS values for the edges in the temp_net
    for edge, qos_value in zip(edge_qos_values.keys(), qos_combo):
        if edge[0] == "confirmation":
            confirmation_nodes = [node for node in temp_net.get_node_ids() if node.startswith("Confirmation-")]
            for full_node_id in confirmation_nodes:
                node_id_after_dash = full_node_id.split("-", 1)[1]
                print(full_node_id,node_id_after_dash)
                temp_net.get_edge(full_node_id, node_id_after_dash).user_data = UserData(qos_value)
        else:
            print(edge[0])
            temp_net.get_edge(*edge).user_data = UserData(qos_value)
    
    # Write the data to a JSON file using the JSONEncoder and custom_user_encode
    # The file name includes the QOS values for identification
    file_name = "data/NSFCareerProj/ForWMCreading/PPtoNWS_{}_conf_{}.json".format(*qos_combo)
    JSONEncoder.encode(file_name, temp_net, e_user_data_func=custom_user_encode)



# Manually set the QOS for NWP to RM to 0. This is necessary because WMC schedules NWS but for 
# the network analysis, this edge must be triggered
main_net.get_edge("NWP","RM").user_data = UserData(0)


# Now add attributes that represent when each BaseEnvironmentResource and OrgResource was last updated
for node_id in main_net.get_node_ids():
    
    node = main_net.get_node(node_id)
    
    # Check if BaseEnvironmentResource
    if issubclass (node.__class__, nd.BaseEnvironmentResource) or issubclass (node.__class__, nd.CoordinationGroundingResource):
        
        user_data = lambda: None # Lambda function that we can add attributes to, could use to set last_update_time to zero.
        user_data.last_update_time = 0#-1000000 # Something really small so that it updates the first time we run it.
        node.user_data = user_data

# Check that previous is actually working
# for node_id in main_net.get_node_ids():
    
#     node = main_net.get_node(node_id)
    
#     # Check if BaseEnvironmentResource
#     if issubclass (node.__class__, nd.BaseEnvironmentResource) or issubclass (node.__class__, nd.CoordinationGroundingResource):
        
#         print(node.user_data.last_update_time)

# Check that QOS is loaded properly
# for edge_id in main_net.get_edge_ids():
    
#     edge = main_net.get_edge(edge_id[0],edge_id[1])
    
#     print(edge.user_data.QOS)

# Now we can do some funky things with the QOS requirements...
# First want to find edges that need updating based on when resources were last updated.
current_time = 32 #Needs something different here

out_of_bound_edges = []

# Identify which edges are out of QOS bound
for edge_id in main_net.get_edge_ids():
    
    edge = main_net.get_edge(edge_id[0],edge_id[1])
    
    # Check if the target is a function node
    target_node = main_net.get_node(edge_id[1])
    if issubclass (target_node.__class__, nd.ActionNode):
        
        # Check when resource was last updated
        source_node = main_net.get_node(edge_id[0])
        last_update_time = source_node.user_data.last_update_time
        QOS = edge.user_data.QOS

        if float(current_time) - float(last_update_time) > float(QOS):
            print("QOS for",source_node.id,"to",target_node.id,"is out of bounds with QOS",float(QOS),"and last update time",last_update_time)

            out_of_bound_edges.append(edge_id)

# This function is used to identify functional nodes are predependencies for a target function
# based on QOS bounds and when resources were last updated.
# This function takes in a node id of a FUNCTION node that is the target
# It returns a list of function and resource nodes that need to be updated/executed to abide by QOS requirements
def add_predecessors_to_strategy(node_id, out_of_bound_edges, strategy_list, main_net):

    # Get the node handle
    node = main_net.get_node(node_id)

    # If this node is not yet in the strategy, add it!
    if node not in strategy_list:
        strategy_list.append(node)

    # Now loop over all incoming edges
    for pred_node_id in main_net.get_graph().predecessors(node_id):

        # And check whether it is within QOS bound
        if (pred_node_id, node_id) in out_of_bound_edges:

            # If out of QOS bound, need to add to our strategy (in need for an update)
            strategy_list.append(main_net.get_node(pred_node_id))

            # We need to add each of the functions that is linked to set this predecessor node
            # and perform the same check to see if we need to add their predecessors
            for pred_pred_node_id in main_net.get_graph().predecessors(pred_node_id):

                if main_net.get_node(pred_pred_node_id) not in strategy_list:
                    add_predecessors_to_strategy(pred_pred_node_id, out_of_bound_edges, strategy_list, main_net)

    return strategy_list

# Identify the strategy
strategy_list = add_predecessors_to_strategy('RM', out_of_bound_edges, [], main_net)

# Identify edges to highlight (that are connecting the nodes in the strategy)
connecting_edges = []
for node in strategy_list:
    for neighbor in main_net.get_graph().neighbors(node.id):
        if main_net.get_node(neighbor) in strategy_list:
            edge = (node.id, neighbor) if (node.id, neighbor) in main_net.get_edge_ids() else (neighbor, node.id)
            if edge not in connecting_edges:
                connecting_edges.append(edge)

# Identify all incoming edges for every node in the strategy_list
connecting_edges = []
for node in strategy_list:
    print(node.id)
    for incoming_edge in main_net.get_graph().in_edges(node.id):
        if incoming_edge not in connecting_edges:
            connecting_edges.append(incoming_edge)

# Let's output as a TikZ graph
l.visualize(main_net, "tikzout3.tex")

''' Alter networks after they have been read 
    from JSON.
'''
app = CytoscapeApp(data_dict, RoverDataHandler)
# app = CytoscapeApp(data_dict, RoverDataHandler, connecting_edges)
# Type in the edges you wish to highlight in format ("node1", "node2") as seen in examples below
# Strategy without updating PP for NWS
# app = CytoscapeApp(data_dict, RoverDataHandler, [("GL", "RM"),("GL", "NWS"),("TM", "NWS"), ("Confirmation-NWS", "NWS"), ("NWS", "NWP"), ("NWP", "Confirming-NWS"), ("Confirming-NWS", "Confirmation-NWS"), ("NWP", "RM"), ("PP", "NWS"), ("PP", "RM")])
# Fully highlighted
# app = CytoscapeApp(data_dict, RoverDataHandler, [("GL", "RM"),("GL", "NWS"),("TM", "NWS"), ("NWS", "NWP"), ("NWP", "RM"), ("PP", "NWS"), ("PP", "RM"),("TM", "LAA"), ("CIMG", "LAA"), ("LAA", "RS"), ("RS", "CAM"), ("OS", "CAM"), ("CAM","CA"),("CA","IC"),("CA","OLL"),
#                                                    ("CIMG","OLL"), ("OLL", "OL"), ("OL", "RPP"),("RS","RPP"),("RS","IC"),("OS","RPP"),("TM","RPP"),("GL","RPP"),("RPP","PP"),("IC","CIMG"),("OST","RPP"),("OBL","RPP"),("TMP","OST"),("BLM","OBL"),
#                                                    ("Confirmation-NWS", "NWS"),("NWP", "Confirming-NWS"),("Confirming-NWS", "Confirmation-NWS"),("CIMG", "Confirming-IC"),("Confirming-IC", "IC"),("Confirming-IC","Confirmation-IC"),("Confirmation-IC","IC"),("PP","Confirming-RPP"),("Confirming-RPP","Confirmation-RPP"),("Confirmation-RPP","RPP"),
#                                                    ("OBL","Confirming-BLM"),("Confirming-BLM","Confirmation-BLM"),("Confirmation-BLM","BLM"),("OST","Confirming-TMP"),("Confirming-TMP","Confirmation-TMP"),
#                                                    ("Confirmation-TMP","TMP")])
# app = CytoscapeApp(data_dict,RoverDataHandler)
webbrowser.open_new("http://127.0.0.1:8050")
app.run()