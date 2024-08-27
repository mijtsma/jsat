import json
from enum import IntEnum
import os.path
from typing import Callable, Any

from core.utils.defaultallocation import DefaultAllocation
from core.utils.defaultlayers import DefaultLayers
from core.utils.defaultutils import DefaultUtils
import core.networkdata as nd

class JSONParser:
    ''' A class for parsing graph data from a correctly-formatted .json file
        into a NetworkModel object.
    '''
    @staticmethod
    def parse(
        file_path: str,
        node_layers: dict[str, type[nd.Node]] = DefaultLayers.layers_dict(),
        action_allocation: IntEnum = DefaultAllocation,
        n_user_data_func: Callable[[Any],Any] = DefaultUtils.user_parse,
        a_user_data_func: Callable[[Any],Any] = DefaultUtils.user_parse,
        e_user_data_func: Callable[[Any],Any] = DefaultUtils.user_parse,
    ) -> nd.NetworkModel:
        ''' Parses the json at the given file path and returns the 
            corresponding NetworkModel. Throws exceptions for incorrect
            formatting and issues accessing files.
        '''
        data: dict = JSONParser.__get_graph_data(file_path)
        model: nd.NetworkModel = nd.NetworkModel()
        if "Nodes" in data:
            JSONParser.__get_nodes(
                data["Nodes"],
                model, 
                node_layers, 
                action_allocation,
                n_user_data_func
            )
        if "Agents" in data:
            JSONParser.__get_agents(
                data["Agents"],
                model, 
                action_allocation,
                a_user_data_func
            )
        if "Edges" in data:
            JSONParser.__get_edges(data["Edges"], model, e_user_data_func)
        return model

    @staticmethod
    def __get_graph_data(file_path: str)->dict:
        ''' Method which gets and returns the GraphData section from a
            json file at the specified path. Throws exceptions when
            it cannot read the json data, or if it is incorrectly formatted.
        '''
        if not os.path.isfile(file_path):
            raise Exception("Could not acccess file at " + file_path + "!")
        data: dict
        with open(file_path, 'r') as file:
            data = json.loads(file.read())
        if not "GraphData" in data:
            raise Exception("Format error: Could not find key GraphData!")
        return data["GraphData"]

    @staticmethod
    def __get_nodes(
        node_data: dict[str, dict],
        model: nd.NetworkModel,
        node_layers: dict[str, type[nd.Node]],
        action_allocation : IntEnum,
        user_data_func: Callable[[Any],Any]
    ):
        ''' Method which adds the nodes from the json-based dictionary to
            the provided NetworkModel.
        '''
        name: str
        properties: dict
        for name, properties in node_data.items():
            JSONParser.__add_node(
                model, 
                name, 
                properties, 
                node_layers, 
                action_allocation,
                user_data_func
            )
            
    @staticmethod
    def __add_node(
        model: nd.NetworkModel, 
        name: str, 
        properties: dict,
        node_layers: dict[str, type[nd.Node]],
        action_allocation : IntEnum,
        user_data_func: Callable[[Any],Any]
    ):
        ''' Method which adds the node from the json-based data entry
            the provided NetworkModel. Throws an exception if the node type
            is not found in the provided node_layers or if format issues
            are present.
        '''
        if not "Type" in properties:
            raise Exception("Format error: Type property not present in " 
                + name + "!")
        node_type: str = properties["Type"]
        if not node_type in node_layers:
            raise Exception("JSON node type not specified in given" 
                + " node_layers!")
        if issubclass(node_layers[node_type], nd.ActionNode):
            node: nd.Node = node_layers[node_type](name, None, action_allocation)
        else:
            node: nd.Node = node_layers[node_type](name)
        if "UserData" in properties:
                node.user_data = user_data_func(properties["UserData"])
        model.add_node(node)

    @staticmethod
    def __get_agents(
        agent_data: dict[str, dict],
        model: nd.NetworkModel,
        action_allocation: IntEnum,
        user_data_func: Callable[[Any],Any]
    ):
        ''' Method which adds the agents from the json-based dictionary to
            the provided NetworkModel.
        '''
        for name, properties in agent_data.items():
            agent: nd.Agent = nd.Agent(name, None, action_allocation)
            JSONParser.__allocate_actions(
                agent, 
                model, 
                properties, 
                action_allocation
            )
            if "UserData" in properties:
                agent.user_data = user_data_func(properties["UserData"])
            model.add_agent(agent)

    @staticmethod
    def __allocate_actions(
        agent: nd.Agent,
        model: nd.NetworkModel,
        properties: dict,
        action_allocation: IntEnum
    ):
        ''' Allocates all specified actionss from properties to the given agent.
        '''
        for alloc_type in action_allocation:
            if not alloc_type.name in properties:
                continue
            for node_id in properties[alloc_type.name]:
                JSONParser.__allocate_node_to_agent(
                    agent,
                    node_id,
                    model, 
                    alloc_type
                )
    
    @staticmethod
    def __allocate_node_to_agent(
        agent: nd.Agent,
        node_id: str,
        model: nd.NetworkModel, 
        alloc_type
    ):
        ''' Allocates the specified node to the given agent. Raises exceptions
            if the node is not in the model or if the node isn't an ActionNode.
        '''
        if not model.has_node(node_id):
            raise Exception("Node " + node_id + "not in JSON, cannot " +
                "allocate to " + agent.id + "!")
        action: nd.Node = model.get_node(node_id)
        if not isinstance(action, nd.ActionNode):
            raise Exception("Can't add " + action.id + " to " + agent.id +
                ", given node is not an ActionNode!")
        agent.add_action(action, alloc_type)

    @staticmethod
    def __get_edges(
        edge_data: list[dict],
        model: nd.NetworkModel,
        user_data_func: Callable[[Any],Any]  
    ):
        ''' Method which adds the edges specified in the json data
            to the given model. Raises an exception for incorrect formatting.
        '''
        entry: dict
        i: int = 0
        for entry in edge_data:
            if not "Source" in entry:
                raise Exception("Edge " + i + " missing source!")
            if not "Target" in entry:
                raise Exception("Edge " + i + " missing target!")
            edge: nd.EdgeData = DefaultUtils.default_edge()
            if "Weight" in entry:
                edge.weight = entry["Weight"]
            if "UserData" in entry:
                edge.user_data = user_data_func(entry["UserData"])
            model.add_edge(entry["Source"], entry["Target"], edge)
            i+=1
