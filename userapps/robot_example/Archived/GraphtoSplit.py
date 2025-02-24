### Archived as could not figure out a way to visualize with this format

### Add the directory containing the 'core' package to the Python path
import sys
import os
import networkx as nx
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from core import networkdata as nd
from core.parsing.jsonparser import JSONParser
from core.utils.defaultallocation import DefaultAllocation
from core.calculation.basicstats import BasicStats
from cytoapp.cytoscapeapp import CytoscapeApp
from core.visualization.tikzlayer import LayeredTikzVisualizer

disaster_graph: nd.NetworkModel = nd.NetworkModel()
a1: nd.DistributedWorkFunction = nd.DistributedWorkFunction("BLM", precedence=1)
a2: nd.DistributedWorkFunction = nd.DistributedWorkFunction("TMP", precedence=2)
a3: nd.DistributedWorkFunction = nd.DistributedWorkFunction("IC", precedence=3)
a4: nd.DistributedWorkFunction = nd.DistributedWorkFunction("LAA", precedence=4)
a5: nd.DistributedWorkFunction = nd.DistributedWorkFunction("RM", precedence=5)
a6: nd.DistributedWorkFunction = nd.DistributedWorkFunction("REV", precedence=6)
a7: nd.DistributedWorkFunction = nd.DistributedWorkFunction("OLL", precedence=7)
a8: nd.DistributedWorkFunction = nd.DistributedWorkFunction("NWS", precedence=8)
a9: nd.DistributedWorkFunction = nd.DistributedWorkFunction("RPP", precedence=9)

### Create the agents in the model
human: nd.Agent = nd.Agent("Human")
robot: nd.Agent = nd.Agent("Robot")

### Assign the agents functions
## Human functions
human.add_action(a3, DefaultAllocation.Authority)
human.add_action(a5, DefaultAllocation.Authority)
human.add_action(a6, DefaultAllocation.Authority)
human.add_action(a9, DefaultAllocation.Authority)
## Robot functions
robot.add_action(a1, DefaultAllocation.Authority)
robot.add_action(a2, DefaultAllocation.Authority)
robot.add_action(a4, DefaultAllocation.Authority)
robot.add_action(a7, DefaultAllocation.Authority)
robot.add_action(a8, DefaultAllocation.Authority)

### Add nodes to graph
disaster_graph.add_node(a1)
disaster_graph.add_node(a2)
disaster_graph.add_node(a3)
disaster_graph.add_node(a4)
disaster_graph.add_node(a5)
disaster_graph.add_node(a6)
disaster_graph.add_node(a7)
disaster_graph.add_node(a8)
disaster_graph.add_node(a9)
### Add agents to graph
disaster_graph.add_agent(human)
disaster_graph.add_agent(robot)
### Add edges to graph
disaster_graph.add_edge(a1.id, a9.id)
disaster_graph.add_edge(a2.id, a9.id)
disaster_graph.add_edge(a8.id, a9.id)
disaster_graph.add_edge(a7.id, a9.id)
disaster_graph.add_edge(a3.id, a7.id)
disaster_graph.add_edge(a6.id, a8.id)
disaster_graph.add_edge(a5.id, a6.id)
disaster_graph.add_edge(a4.id, a6.id)
disaster_graph.add_edge(a3.id, a4.id)
disaster_graph.add_edge(a3.id, a6.id)

print(BasicStats.number_of_nodes(disaster_graph))
