from core import networkdata as nd
from core.parsing.jsonparser import JSONParser
from core.utils.defaultallocation import DefaultAllocation
from core.calculation.basicstats import BasicStats
from cytoapp.cytoscapeapp import CytoscapeApp
from core.visualization.tikzlayer import LayeredTikzVisualizer

### HRT Metrics Script Example

''' To start, you will need to put data into a NetworkModel. Network 
    models are made out of Nodes, Edges, and Agents. One easy way 
    to get a NetworkModel is to run an existing .json file through the 
    parser, like so:
'''
example_model: nd.NetworkModel = JSONParser.parse("data/JSON/example.json")

''' You can also build a NetworkModel manually. Below is an example of a
    simple network model built manually.
'''
basic_model: nd.NetworkModel = nd.NetworkModel()
r1: nd.BaseEnvironmentResource = nd.BaseEnvironmentResource("R1")
r2: nd.BaseEnvironmentResource = nd.BaseEnvironmentResource("R2")
a1: nd.DistributedWorkFunction = nd.DistributedWorkFunction("A1")
agent: nd.Agent = nd.Agent("Agent")
agent.add_action(a1, DefaultAllocation.Authority)
basic_model.add_node(r1)
basic_model.add_node(r2)
basic_model.add_node(a1)
basic_model.add_agent(agent)
basic_model.add_edge(r1.id, a1.id)
basic_model.add_edge(a1.id, r2.id)

''' You can calculate various statistics about the networks you create,
    for example:
'''
print()
print("Basic Model Nodes:")
print(BasicStats.number_of_nodes(basic_model))
print()
print("Example Model Layer Modularity:")
print(BasicStats.layer_modularity(example_model))
print()

''' You can generate .tex files containing tikz figures:
'''
LayeredTikzVisualizer.visualize(example_model, "cytoapp/tikz/out.tex")

''' If you want, you can alter networks after they have been read 
    from JSON.
'''
v10: nd.CoordinationGroundingResource = nd.CoordinationGroundingResource("v10")
example_model.add_node(v10)

''' You can pass your models into a dash cytoscape app to generate
    interactive visualizations:
'''
app = CytoscapeApp(
    {
        "Example Data": example_model,
        "Basic Data": basic_model
    },  
)
app.run()

''' If you would like a more practical example of a script, check out
    userapps/cadencehagenauer/rover.

    The core is designed to be highly customizable. It supports custom node
    types, allocation types, and user data parsing through optional
    parameters and inheritance.

    Since the NetworkModel is based on Networkx, it is very simple to
    calculate a plethora of graph statistics beyond those in BasicStats.
    Be warned that directly modifying the Networkx graph could cause
    node-agent synchronization issues.

    Feel free to use existing core or cytoapp code as a template for your own
    apps if you really want to get into the customization.
'''

    



