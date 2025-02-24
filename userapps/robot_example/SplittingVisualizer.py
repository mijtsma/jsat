import networkx as nx
import matplotlib.pyplot as plt

def split_graph(nodes, connections, node_assignments, node_labels):
    # Create the original graph with node attributes
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node, assignment=node_assignments[node], label=node_labels[node])
    
    G.add_edges_from(connections)
    
    # Separate nodes by type
    human_nodes = sorted([n for n in nodes if node_assignments[n] == 'human'])
    robot_nodes = sorted([n for n in nodes if node_assignments[n] == 'robot'])
    
    # Create subgraphs
    human_graph = nx.DiGraph()
    robot_graph = nx.DiGraph()
    
    for node in human_nodes:
        human_graph.add_node(node, assignment=node_assignments[node], label=node_labels[node])
    for node in robot_nodes:
        robot_graph.add_node(node, assignment=node_assignments[node], label=node_labels[node])
    
    # Process nodes in order and enforce the new rule
    for node in sorted(nodes):  # Process nodes in precedence order
        if list(G.successors(node)):  # If the node had outgoing edges in the original graph
            valid_human_targets = [t for t in human_nodes if G.in_degree(t) > 0 and t > node]
            valid_robot_targets = [t for t in robot_nodes if G.in_degree(t) > 0 and t > node]
            
            if node in human_nodes and valid_human_targets:
                human_graph.add_edge(node, valid_human_targets[0])  # Connect to the next valid human node
            if node in robot_nodes and valid_robot_targets:
                robot_graph.add_edge(node, valid_robot_targets[0])  # Connect to the next valid robot node
    
    return G, human_graph, robot_graph

def plot_graph(G, title="Graph", pos=None):
    """Plots the graph while keeping node IDs and labels consistent."""
    labels = nx.get_node_attributes(G, "label")  # Retrieve stored node labels
    node_colors = ["lightblue" if data["assignment"] == "human" else "lightgreen" for _, data in G.nodes(data=True)]
    
    if pos is None:
        pos = nx.spring_layout(G)  # Generate layout only once for consistency
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=500, node_color=node_colors,
            font_size=12, font_weight="bold", edge_color="gray")
    
    plt.title(title)
    plt.show()

# Input Data
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
connections = [(1,8), (2, 8), (7, 8), (6, 8), (3, 6), (5, 7), (4,5), (3,4)]  # Directed edges
node_assignments = {1: 'human', 2: 'robot', 3: 'robot', 4: 'robot', 5: 'robot', 6: 'human', 7:'human', 8:'robot'}  # Custom assignments
node_labels = {1: 'BLM', 2: 'TMP', 3: 'IC', 4: 'LAA', 5: 'REV', 6:'OLL', 7:'NWS', 8:'RPP'}  # Custom labels

# Split the graph while keeping node IDs and labels
full_graph, human_graph, robot_graph = split_graph(nodes, connections, node_assignments, node_labels)

# Generate a consistent position layout
pos = nx.spring_layout(full_graph)

# Plot graphs with consistent IDs, labels, and positions
plot_graph(full_graph, "Original Full Graph", pos)
plot_graph(human_graph, "Human Graph", pos)
plot_graph(robot_graph, "Robot Graph", pos)
