from typing import Tuple
import networkx as nx

import core.networkdata as nd

class VisualizationUtils:
    ''' A class for common cytoscape visualization operations.
    '''
    @staticmethod
    def add_node_basics(
        element: dict, 
        node: nd.Node,
        vis_id: str
    ):
        ''' Adds all basic visualization elements of a node to a dash
            cytoscape element.
        '''
        if not 'data' in element:
            element['data'] = {}
        element['data']['id'] = vis_id + node.id
        element['data']['label']  = node.id
        if issubclass (node.__class__, nd.ActionNode):
            element['classes'] = 'action'
        else:
            element['classes'] = 'resource'

    @staticmethod
    def add_edge_basics(
        element: dict, 
        source: nd.Node, 
        target: nd.Node,
        vis_id: str
    ):
        ''' Adds all basic visualization elements of an edge to a dash
            cytoscape element.
        '''
        data = {}
        data['source'] = vis_id + source.id
        data['target'] = vis_id + target.id
        element['data'] = data
        source_type: type = type(source)
        target_type: type = type(target)
        if source_type is target_type:
            element['classes'] = 'org'
        else:
            element['classes'] = 'ame'
