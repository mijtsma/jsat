import json
from enum import IntEnum
import os.path
from typing import Callable, Any, Tuple

from core.utils.defaultutils import DefaultUtils
import core.networkdata as nd

class JSONEncoder:
    ''' A class for encoding graph data into a correctly-formatted .json file
        from a NetworkModel object.
    '''

    @staticmethod
    def encode(
        file_path: str,
        model: nd.NetworkModel,
        n_user_data_func: Callable[[Any],Any] = DefaultUtils.user_encode,
        a_user_data_func: Callable[[Any],Any] = DefaultUtils.user_encode,
        e_user_data_func: Callable[[Any],Any] = DefaultUtils.user_encode,
    ):
        ''' Parses the json at the given file path and returns the 
            corresponding NetworkModel. Throws exceptions for issues 
            accessing files.
        '''
        #form dict skeleton
        data_to_encode = JSONEncoder.__create_json_skeleton()
        #put nodes
        JSONEncoder.__put_nodes(
            model,
            data_to_encode["GraphData"]["Nodes"],
            n_user_data_func
        )
        #put agents
        JSONEncoder.__put_agents(
            model,
            data_to_encode["GraphData"]["Agents"],
            a_user_data_func
        )
        #put edges
        JSONEncoder.__put_edges(
            model,
            data_to_encode["GraphData"]["Edges"],
            e_user_data_func
        )
        #put dict into json
        try:
            with open(file_path, 'w') as file:
                json.dump(data_to_encode, file, indent = 4)
        except IOError as e:
            raise Exception("Could not open file at " + file_path + "!")
    

    @staticmethod
    def __create_json_skeleton() -> dict:
        ''' Creates a dictionary containing the skeleton structure
            of the JSON standard.
        '''
        skeleton: dict = {
            "GraphData": {
                "Nodes": {},
                "Agents": {},
                "Edges": []
            }
        }
        return skeleton
    
    @staticmethod
    def __put_nodes(
        model: nd.NetworkModel,
        node_dict: dict[str, dict[str, Any]],
        n_user_data_func: Callable[[Any],Any]
    ):
        ''' Puts node data from model into node_dict following the JSON 
            standard
        '''
        for node_id in model.get_node_ids():
            node: nd.Node = model.get_node(node_id)
            node_dict[node_id]={
                "Type": (type(node).__name__)
            }
            if node.user_data is not None:
                user_data =  n_user_data_func(node.user_data)
                node_dict[node_id]["UserData"] = user_data

    @staticmethod
    def __put_agents(
        model: nd.NetworkModel,
        agent_dict: dict[str, dict[str, Any]],
        a_user_data_func: Callable[[Any],Any]
    ):
        ''' Puts agent data from model into agent_dict following the JSON 
            standard
        '''

        for agent_id, agent in model.agents.items():
            agent_dict[agent_id] = {}
            for alloc_type, node_dict in agent.nodes.items():
                type_name: str = alloc_type.name
                JSONEncoder.__encode_allocation_type(
                    agent_dict[agent_id],
                    type_name,
                    node_dict
                )
            if agent.user_data is not None:
                user_data =  a_user_data_func(agent.user_data)
                agent_dict[agent_id]["UserData"] = user_data

    @staticmethod
    def __encode_allocation_type(
        alloc_dict: dict[str, Any],
        alloc_type: str,
        node_dict: dict[type, dict[str, nd.ActionNode]]
    ):
        ''' Helper method for __put_agents which handles encoding 
            allocation data.
        '''
        id_array: list[str] = []
        for type_dict in node_dict.values():
            for node_id in type_dict.keys():
                id_array.append(node_id)
        alloc_dict[alloc_type] = id_array

    @staticmethod
    def __put_edges(
        model: nd.NetworkModel,
        edge_list: list[dict[str, Any]],
        e_user_data_func: Callable[[Any],Any]
    ):
        ''' Puts edge data from model into edge_dict following the JSON 
            standard
        '''
        for edge_pair in model.get_edge_ids():
            edge: nd.EdgeData = model.get_edge(edge_pair[0], edge_pair[1])
            edge_dict = {
                "Source": edge_pair[0],
                "Target": edge_pair[1],
                "Weight": edge.weight,
            }
            if edge.user_data is not None:
                user_data =  e_user_data_func(edge.user_data)
                edge_dict["UserData"] = user_data
            edge_list.append(edge_dict)

