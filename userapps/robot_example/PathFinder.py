import networkx as nx
import matplotlib.pyplot as plt
import itertools

def find_paths_to_target(graph, source, target):
    """Find all paths from a specific source node to the target node."""
    return list(nx.all_simple_paths(graph, source=source, target=target))

# Create a simple graph
G = nx.DiGraph()  # Use nx.Graph() for an undirected graph
edges = [(1, 2), (2, 3), (3, 4), (1, 5), (5, 4), (2, 6), (6, 4)]
G.add_edges_from(edges)

# Define source and target nodes
source_node = 1
target_node = 4

# Find paths
paths = find_paths_to_target(G, source_node, target_node)

# Generate distinct colors for each path
colors = itertools.cycle(["red", "blue", "green", "purple", "orange", "cyan", "magenta"])

# Visualize the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=700, font_size=10)

# Highlight each path with a different color
for path, color in zip(paths, colors):
    edges_in_path = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color=color, width=2)
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color=color, node_size=700)

plt.show()

# Output the paths
for path in paths:
    print(" -> ".join(map(str, path)))
