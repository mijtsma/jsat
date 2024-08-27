import networkx as nx
from typing import Tuple, Type

import core.networkdata as nd
from .eagle import EagleModularity

class BasicStats:
    ''' A class for calculating various simple statistics of a NetworkModel.
    '''

    EIGENVECTOR_DEFAULT_MAX_ITER: int = 5000
    EIGENVECTOR_DEFAULT_TOL: float = 1.0e-6

    @staticmethod
    def number_of_nodes(model: nd.NetworkModel) -> int:
        ''' Calculates the number of nodes in the given NetworkModel.
        '''
        return model.get_graph().number_of_nodes()

    @staticmethod
    def number_of_edges(model: nd.NetworkModel) -> int:
        ''' Calculates the number of edges in the given NetworkModel.
        '''
        return model.get_graph().number_of_edges()

    @staticmethod
    def degree(model: nd.NetworkModel, node_id: str) -> int:
        ''' Calculates the degree of the node with the given id in the
            given NetworkModel.
        '''
        return model.get_graph().degree(node_id)

    @staticmethod
    def degree_centrality(model: nd.NetworkModel) -> dict[str, float]:
        ''' Calculates the degree centrality of all nodes in the graph
            and returns a dictionary from node ids to centrality values
            between 0 and 1 (provided no multigraphs or self-loops).
        '''
        return nx.degree_centrality(model.get_graph())

    @staticmethod
    def eigenvector_centrality(
        model: nd.NetworkModel,
        iterations: int = EIGENVECTOR_DEFAULT_MAX_ITER,
        tolerance: float = EIGENVECTOR_DEFAULT_TOL
    ) -> dict[str, float]:
        ''' Calculates the eigenvector centrality of all nodes in the graph
            and returns a dictionary from node ids to centrality values.
            In the case of an PowerIterationFailedConvergence error, increase
            the number of iterations or increase the tolerance.
        '''
        return nx.eigenvector_centrality(
            model.get_graph(),
            iterations,
            tolerance
        )

    @staticmethod
    def closeness_centrality(model: nd.NetworkModel) -> dict[str, float]:
        ''' Calculates the closeness centrality of all nodes in the graph
            and returns a dictionary from node ids to centrality values.
        '''
        return nx.closeness_centrality(model.get_graph())

    @staticmethod
    def find_cycle(model: nd.NetworkModel) -> list[Tuple[str,str]]:
        ''' Finds a cycle in the current graph and returns a list of
            edges in that cycle. Returns an empty list if no cycle is
            found.
        '''
        result: list[Tuple[str,str]] = []
        try:
            result = nx.find_cycle(model.get_graph())
        finally:
            return result

    @staticmethod
    def cycle_basis(model: nd.NetworkModel) -> list[list[str]]: 
        ''' Finds a basis for the cycles in the given NetworkModel
            and returns a list of cycle list, each containing the ids of the
            node in the cycle.
        '''
        return nx.cycle_basis(model.get_graph())

    @staticmethod
    def clustering_coefficients(
        model: nd.NetworkModel,
        nodes = None
    ) -> dict[str, float]:
        ''' Calculates the clustering coefficient of all nodes in the graph
            or for the specified node string(s), and returns a dictionary
            from node ids to clustering values.
        '''
        return nx.clustering(model.get_graph(), nodes)

    @staticmethod
    def find_communities(model: nd.NetworkModel) -> list[frozenset[str]]:
        ''' Finds a list of community sets of the given model using
            greedy modularity maximization
        '''
        return nx.community.greedy_modularity_communities(model.get_graph())

    @staticmethod
    def layer_modularity(model: nd.NetworkModel) -> float:
        ''' Returns the modularity of the given model with partitions
            based on node type.
        '''
        layers: dict[Type, list[str]] = {}
        for node_id in model.get_node_ids(): 
            node_type: Type = type(model.get_node(node_id))
            if node_type in layers:
                layers[node_type].append(node_id)
            else:
                layers[node_type] = [node_id]
        return nx.community.modularity(model.get_graph(), layers.values())

    @staticmethod
    def allocation_modularity(model: nd.NetworkModel, alloc_type) -> float:
        ''' Returns the modularity of the given model with partitions
            based on the specified allocation type.
        '''
        communities: dict[str, list[str]] = {}
        for agent_id in model.agents:
            communities[agent_id] = []
        non_allocated_actions: list[str] = []
        non_actions: list[str] = []
        for node_id in model.get_node_ids():
            node = model.get_node(node_id)
            if (not isinstance(node, nd.ActionNode)):
                non_actions.append(node_id)
                continue
            if(alloc_type not in node.agents or 
            len(node.agents[alloc_type]) == 0):
                non_allocated_actions.append(node_id)
                continue
            for agent_id in node.agents[alloc_type]:
                communities[agent_id].append(node_id)
        result = list(communities.values())
        result.append(non_allocated_actions)
        result.append(non_actions)
        return EagleModularity.eagle_modularity(
            model.get_graph(), 
            result
        )



    