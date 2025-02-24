import networkx as nx
import matplotlib.pyplot as plt
import itertools

def find_paths_to_target(graph, source, target):
    """Find all paths from a specific source node to the target node."""
    return list(nx.all_simple_paths(graph, source=source, target=target))

# Input Data
nodes = [1, 2, 3, 4, 5, 6, 7, 8]
connections = [(1, 8), (2, 8), (7, 8), (6, 8), (3, 6), (5, 7), (4, 5), (3, 4)]  # Directed edges
node_assignments = {1: 'human', 2: 'robot', 3: 'robot', 4: 'robot', 5: 'robot', 6: 'human', 7: 'human', 8: 'robot'}  
node_labels = {1: 'BLM', 2: 'TMP', 3: 'IC', 4: 'LAA', 5: 'REV', 6: 'OLL', 7: 'NWS', 8: 'RPP'}  

# Create directed graph and add nodes and edges
G = nx.DiGraph()
G.add_edges_from(connections)

# Define source and target nodes
source_node = 3  # Change as needed
target_node = 8  # Change as needed

# Find paths
paths = find_paths_to_target(G, source_node, target_node)

# Generate distinct colors for each path
colors = itertools.cycle(["red", "blue", "green", "purple", "orange", "cyan", "magenta"])

# Layout positions (fixed for consistency across plots)
pos = nx.spring_layout(G)

# Loop through each path and create a separate plot
for i, (path, color) in enumerate(zip(paths, colors), start=1):
    plt.figure(figsize=(6, 4))
    plt.title(f"Path {i}: {' → '.join(node_labels[n] for n in path)}", fontsize=10)
    
    # Draw full graph in black
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_color='lightgray', edge_color='black', node_size=700, font_size=10)

    # Highlight the current path
    edges_in_path = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color=color, width=2)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color=color, node_size=700)

    plt.show()

    # Print the path in the console
    print(f"\033[1;{31 + (i % 7)}m{' → '.join(node_labels[n] for n in path)}\033[0m")  # Colored console output
