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
directory: str = "data/"

''' The JSON files in the given folder
'''
data_sets: list[str] = [
    "robot_example",
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
main_net = data_dict["robot_example"]

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


# You can identify what resources are shared between agents as a way to identify interdependencies between agents that
# require some form of information exchange and/or coordination.

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

# One can also identify where there are mismatches in which agent is authorized to perform a function
# (i.e., is executing the work) and the agent who is responsible (i.e., accountable for the outcome, in a legal or
# organizational sense). Mismatches have implications for coordination overhead, as responsible agents need to be able
# to supervise and manage authorized agents.
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
        if authorized_agent != operator:
            functions_w_auth_resp_mismatch.append(node_id)

# For each function with an authority-responsibility mismatch, do something!
# Current rule: When authority-responsibility mismatch, create a confirmation resources and a confirmation
# function that is allocated to the operator
for node_id in functions_w_auth_resp_mismatch:

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


# Let's output as a TikZ graph
l.visualize(main_net, "tikzout3.tex")

''' Alter networks after they have been read 
    from JSON.
'''
# This will generate the graph without a highlighted strategy, comment this out if you use on the highlighted strategies below
app = CytoscapeApp(data_dict, RoverDataHandler)
# Type in the edges you wish to highlight in format ("node1", "node2") as seen in examples below
# Included are two different examples of highlighted strategies, uncomment the one you wish to visualize
# Strategy without updating PP for NWS
# app = CytoscapeApp(data_dict, RoverDataHandler, [("GL", "RM"),("GL", "NWS"),("TM", "NWS"), ("Confirmation-NWS", "NWS"), ("NWS", "NWP"), ("NWP", "Confirming-NWS"), ("Confirming-NWS", "Confirmation-NWS"), ("NWP", "RM"), ("PP", "NWS"), ("PP", "RM")])
# Fully highlighted
# app = CytoscapeApp(data_dict, RoverDataHandler, [("GL", "RM"),("GL", "NWS"),("TM", "NWS"), ("NWS", "NWP"), ("NWP", "RM"), ("PP", "NWS"), ("PP", "RM"),("TM", "LAA"), ("CIMG", "LAA"), ("LAA", "RS"), ("RS", "CAM"), ("OS", "CAM"), ("CAM","CA"),("CA","IC"),("CA","OLL"),
#                                                    ("CIMG","OLL"), ("OLL", "OL"), ("OL", "RPP"),("RS","RPP"),("RS","IC"),("OS","RPP"),("TM","RPP"),("GL","RPP"),("RPP","PP"),("IC","CIMG"),("OST","RPP"),("OBL","RPP"),("TMP","OST"),("BLM","OBL"),
#                                                    ("Confirmation-NWS", "NWS"),("NWP", "Confirming-NWS"),("Confirming-NWS", "Confirmation-NWS"),("CIMG", "Confirming-IC"),("Confirming-IC", "IC"),("Confirming-IC","Confirmation-IC"),("Confirmation-IC","IC"),("PP","Confirming-RPP"),("Confirming-RPP","Confirmation-RPP"),("Confirmation-RPP","RPP"),
#                                                    ("OBL","Confirming-BLM"),("Confirming-BLM","Confirmation-BLM"),("Confirmation-BLM","BLM"),("OST","Confirming-TMP"),("Confirming-TMP","Confirmation-TMP"),
#                                                    ("Confirmation-TMP","TMP")])
webbrowser.open_new("http://127.0.0.1:8050")
app.run()