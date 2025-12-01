# ================================ #
#            REQUIREMENTS          #
# ================================ #
import sys
import os
import itertools
import webbrowser
# Add project root to module search path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
)
from core import networkdata as nd
from core.parsing.jsonparser import JSONParser
from core.parsing.jsonencoder import JSONEncoder
from cytoapp.cytoscapeapp import CytoscapeApp
from userapps.robot_example.roverdatahandler import RoverDataHandler
from core.visualization.tikzlayer import LayeredTikzVisualizer as l

# ================================ #
#         Setup Python             #
# ================================ #

#  Add the following to terminal to create virtual environment (venv):
#  python3 -m venv .venv
#  source .venv/bin/activate

# ================================ #
#         CONFIGURATION            #
# ================================ #

### STEP 1: Define where your data is located
DATA_DIR = "data/"
DATASET = "toy_arch2"

# STEP 2: Define agents for the system
Cook = nd.Agent("Cook")
Assistant = nd.Agent("Assistant")

agent_lookup = {
    "Cook": Cook,
    "Assistant": Assistant
}

# ================================ #
#       DEFINE ARCHITECTURE        #
# ================================ #

### STEP 3: Define the architecture by assinging functions in .json data file to agents

##### Architecture 1: The Cook does everything ######
# agent_assignments = {
#     "Cook": [
#         "IngredientPreparing",
#         "HeatAdjusting",
#         "IngredientCombining",
#         "ToolFetching",
#         "IngredientUnpacking",
#         "ItemsMoving",
#     ],
#     "Assistant": []
# }

##### Architecture 2: Cook splits original work with Assistant 50/50, creating new coordination functions ######
##### Uncomment only one agent_assignments block at a time ######
agent_assignments = {
    "Cook": [
        "IngredientPreparing",
        "HeatAdjusting",
        "IngredientCombining",
        "Asking for tool",
        "Asking for ingredient",
        "Directing items",
    ],
    "Assistant": [
        "ToolFetching",
        "IngredientUnpacking",
        "ItemsMoving",
    ],
}

# ================================ #
#     USER DATA PARSING / ENCODE   #
# ================================ #

class UserData:
    def __init__(self, QOS=1_000_000):
        self.QOS = QOS

def custom_user_parse(raw):
    """Parses UserData objects from JSON."""
    qos = raw.get("QOS")
    qos = float(qos) if qos not in ("", None) else 1_000_000
    return UserData(qos)

def custom_user_encode(user_data):
    return {"QOS": user_data.QOS}

# ================================ #
#          LOAD THE DATA           #
# ================================ #

data_dict = {
    DATASET: JSONParser.parse(
        os.path.join(DATA_DIR, f"{DATASET}.json"),
        e_user_data_func=custom_user_parse,
    )
}
main_net = data_dict[DATASET]

# # ================================ #
# #    ASSIGN AUTHORITY/RESPONSIB.   #
# # ================================ #

for agent_name, node_list in agent_assignments.items():
    agent = agent_lookup[agent_name]
    for node_id in node_list:
        try:
            node = main_net.get_node(node_id)
            agent.add_action(node, agent.allocation_types.Authority)
            agent.add_action(node, agent.allocation_types.Responsibility)
        except Exception as e:
            print(f"Warning: Could not assign {node_id} to {agent_name}: {e}")

# ================================ #
#     VISUALIZATION + APP START    #
# ================================ #

# TikZ output
l.visualize(main_net, "tikzout3.tex")

# Cytoscape App
app = CytoscapeApp(data_dict, RoverDataHandler)
webbrowser.open_new("http://127.0.0.1:8050")
app.run()