import networkx as nx
from typing import Tuple, Dict

from core.networkdata import Agent
from core.networkdata.generalstorage import Node, Agent, ActionNode, EdgeData
from core.utils.defaultutils import DefaultUtils

class NetworkModel:
    ''' A data class which stores the data relating to a teamwork network.
    '''
    agents: dict[str, Agent]

    def __init__(self):
        #agent storage
        self.agents: dict[str, Agent] = {}
        #graph storage
        self.__graph: nx.DiGraph = nx.DiGraph()

    def get_graph(self) -> nx.DiGraph:
        ''' WARNING: Use this method carefully!!!!!
            Returns the networkx graph used by the model to the user.
            This can be useful for computing various metrics through networkx.
            However, dicrectly modifying this graph, rather than through this
            class's methods, may create unexpected behavior related to agent 
            desynchronization.
        '''
        return self.__graph

    def add_node(self, node: Node):
        ''' Adds the specified node to the network.
        '''
        self.__graph.add_node(node.id, data=node)

    def has_node(self, node_id: str) -> bool:
        ''' Returns whether the node with the specified ID is in the network.
        '''
        return self.__graph.has_node(node_id)

    def get_node(self, node_id: str) -> Node:
        ''' Returns the node with the specified ID. Requires the node to be
            in the network.
        '''
        if not self.has_node(node_id):
            raise Exception("Node not in graph!")
        #node present
        return self.__graph.nodes[node_id]["data"]

    def remove_node(self, node_id: str):
        ''' Remodves the node with the specified ID from the network, along
            with its relationships. Requires the node to be present in the 
            graph.
        '''
        if not self.has_node(node_id):
            raise Exception("Node not in graph!")
        #node present
        data: Node = self.get_node(node_id)
        self.__graph.remove_node(node_id)
        #remove from agents
        if not isinstance(data, ActionNode):
            return
        agent: Agent
        for agent in self.agents.values():
            for alloc_type in agent.allocation_types:
                agent.try_remove_action(node_id, alloc_type)

    def get_node_ids(self) -> list[str]:
        ''' Returns a list containing all IDs of the nodes in the graph.
        '''
        return self.__graph.nodes

    def add_edge(
            self, 
            parent_id: str, 
            child_id: str, 
            edge: EdgeData = None
        ):
        ''' Adds the specified directed edge to the network. Requires both
            nodes to be present in the graph to preserve expected attributes.
        '''
        if not (self.has_node(parent_id)): 
            raise Exception("No parent node " + parent_id + "!")
        if not (self.has_node(child_id)):
            raise Exception("No child node " + child_id + "!")
        if edge is None:
            edge = DefaultUtils.default_edge()
        self.__graph.add_edge(parent_id, child_id, data = edge)
    
    def has_edge(self, parent_id: str, child_id: str) -> bool:
        ''' Returns whether the edge with the specified parent and child IDs 
            is in the network.
        '''
        return self.__graph.has_edge(parent_id, child_id)

    def get_edge(self, parent_id: str, child_id: str) -> EdgeData:
        ''' Returns the node with the specified ID. Requires the node to be
            in the network.
        '''
        if not self.has_edge(parent_id, child_id):
            raise Exception("Edge not in graph!")
        #node present
        return self.__graph[parent_id][child_id]["data"]

    def remove_edge(self, parent_id: str, child_id: str):
        ''' Removes an edge between the specified parent and child. Requires
            the edge to exist.
        '''
        if not self.has_edge(parent_id, child_id):
            raise Exception("Edge not in graph!")
        self.__graph.remove_edge(parent_id, child_id)

    def add_agent(self, agent: Agent):
        ''' Adds the specified agent to the network.
        '''
        self.agents.update({agent.id: agent})

    def has_agent(self, agent_id: str) -> bool:
        ''' Returns whether the agent with the specified ID is in the network.
        '''
        return agent_id in self.agents

    def get_agent(self, agent_id: str) -> Agent:
        ''' Returns the agent with the specified ID. Requires the agent to
            be in the network.
        '''
        if not self.has_agent(agent_id):
            raise Exception("Agent not in graph!")
        #agent present
        return self.agents[agent_id]

    def swap_node_agent(self, node_id: str, agent_id: str) -> str:
        ''' Swaps the authorized agent of the specified action node to the 
            specified agent and returns the ID of the old agent. Throws an
            exception if the node or agent aren't in the network, or if the
            node is not an action node.
        '''
        if not self.has_node(node_id):
            raise Exception("Node not in graph!")
        if not self.has_agent(agent_id):
            raise Exception("Agent not in graph!") 
        swap_node: Node = self.get_node(node_id)
        if not isinstance(swap_node, ActionNode):
            raise Exception("Node not ActionNode!")
        old_agent: Agent = swap_node.get_authorized_agent()
        old_agent.try_remove_action(swap_node.id, old_agent.allocation_types(1))
        new_agent: Agent = self.get_agent(agent_id)
        new_agent.add_action(swap_node, new_agent.allocation_types(1))

    def get_edge_ids(self) -> list[Tuple[str, str]]:
        ''' Returns a list containing all node ID pairs corresponding to
            the edges in the graph.
        '''
        return self.__graph.edges

