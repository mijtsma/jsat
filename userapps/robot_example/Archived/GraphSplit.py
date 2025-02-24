### Archived because this just provides a simple example of the graph splitting logic

import networkx as nx
import matplotlib.pyplot as plt

def split_graph(nodes, connections, node_assignments):
    # Create the original graph
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(connections)
    
    # Separate nodes by type
    human_nodes = sorted([n for n in nodes if node_assignments[n] == 'human'])
    robot_nodes = sorted([n for n in nodes if node_assignments[n] == 'robot'])
    
    human_graph = nx.DiGraph()
    robot_graph = nx.DiGraph()
    
    # Add nodes to each graph
    human_graph.add_nodes_from(human_nodes)
    robot_graph.add_nodes_from(robot_nodes)
    
    # Function to find the closest preceding node of the same type
    def find_previous_node(node, same_type_nodes):
        idx = same_type_nodes.index(node)
        return same_type_nodes[idx - 1] if idx > 0 else None
    
    # Add edges based on the original graph, following the connection rule
    for u, v in connections:
        if node_assignments[u] == node_assignments[v]:
            if node_assignments[u] == 'human':
                human_graph.add_edge(u, v)
            else:
                robot_graph.add_edge(u, v)
        else:
            # Handle lost connections
            if node_assignments[v] == 'human':
                prev_human = find_previous_node(v, human_nodes)
                if prev_human:
                    human_graph.add_edge(prev_human, v)
            else:
                prev_robot = find_previous_node(v, robot_nodes)
                if prev_robot:
                    robot_graph.add_edge(prev_robot, v)
    
    # Remove edges where no lower-numbered node exists in the same type
    def clean_edges(graph, nodes_of_type):
        for node in graph.nodes():
            incoming_edges = list(graph.in_edges(node))
            for u, _ in incoming_edges:
                if u not in nodes_of_type[:nodes_of_type.index(node)]:
                    graph.remove_edge(u, node)
    
    # Clean the human and robot graphs
    clean_edges(human_graph, human_nodes)
    clean_edges(robot_graph, robot_nodes)
    
    return G, human_graph, robot_graph

def plot_graph(G, node_assignments, title="Graph"):
    # Define node color based on their type
    node_colors = ['lightblue' if node_assignments[node] == 'human' else 'lightgreen' for node in G.nodes()]
    
    pos = nx.spring_layout(G)  # Layout for better visualization
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=12, font_weight="bold", edge_color="gray")
    plt.title(title)
    plt.show()

# Input Data
nodes = [1, 2, 3, 4, 5, 6]
connections = [(1, 2), (2, 4), (4, 6), (3, 5), (2, 5), (5, 6)]  # Directed edges
node_assignments = {1: 'human', 2: 'robot', 3: 'robot', 4: 'human', 5: 'robot', 6: 'human'}
#### Add in an ability to label each node, "TMP" or "RPP", etc ####


# Split the graph
full_graph, human_graph, robot_graph = split_graph(nodes, connections, node_assignments)

# Visualize the original graph and the two split graphs with color-coded nodes
plot_graph(full_graph, node_assignments, "Original Full Graph")
plot_graph(human_graph, node_assignments, "Human Graph")
plot_graph(robot_graph, node_assignments, "Robot Graph")
