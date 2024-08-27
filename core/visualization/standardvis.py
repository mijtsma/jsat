import networkx as nx
from typing import Tuple

import core.networkdata as nd
from core.visualization.stylesheets import Stylesheets
from core.utils.visutils import VisualizationUtils as vu

class StandardVisualizer:
    ''' A class which visualizes a NetworkModel as a dash cytoscape graph
        without categories.
    '''
    
    ''' Prevents app from breaking with multiple datasets containing 
        matching node ids
    '''
    __visualization_id = 0

    @staticmethod
    def vis_specifier_string() -> str:
        ''' Returns the string added to the front of every cytoscape
            id: important for the case of multiple visualizations on the
            same data.
        '''
        return str(StandardVisualizer.__visualization_id) + "_standard_"

    @staticmethod
    def visualize(model: nd.NetworkModel) -> Tuple[list[dict],list[dict]]:
        ''' Takes a network model and returns the stylesheet and elememts 
            sections of a dash cytoscape graph for the standard visualization.
        ''' 
        result: Tuple[list[dict], list[dict]]
        result = (StandardVisualizer.get_elements(model),
            Stylesheets.standard_stylesheet())
        StandardVisualizer.__visualization_id += 1
        return result

    @staticmethod
    def get_elements(model: nd.NetworkModel) -> list[dict]:
        ''' Takes a network model and returns the elememts 
            sections of a dash cytoscape graph.
        ''' 
        elements: list[dict] = []
        StandardVisualizer.__add_nodes(model, elements)
        StandardVisualizer.__add_edges(model, elements)
        return elements

    @staticmethod
    def __add_nodes(model: nd.NetworkModel, elements: list[dict]):
        ''' Adds the nodes from the given model to the elements array in
            dash cytoscape format.
        '''
        nodes = model.get_node_ids()
        for node_id in nodes:
            element = {}
            vu.add_node_basics(
                element, 
                model.get_node(node_id),
                StandardVisualizer.vis_specifier_string()
            )
            elements.append(element)

    @staticmethod
    def __add_edges(model: nd.NetworkModel, elements: list[dict]):
        ''' Adds the edges from the given model to the elements array in
            dash cytoscape format.
        '''
        edges = model.get_edge_ids()
        for edge_ids in edges:
            element = {}
            vu.add_edge_basics(
                element, 
                model.get_node(edge_ids[0]),
                model.get_node(edge_ids[1]),
                StandardVisualizer.vis_specifier_string()
            )
            elements.append(element)


            

