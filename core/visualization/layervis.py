import networkx as nx
from typing import Tuple

import core.networkdata as nd
from core.visualization.stylesheets import Stylesheets
from core.utils.visutils import VisualizationUtils as vu
from core.utils.colorgen import ColorGenerator as cg

class LayeredVisualizer:
    ''' A class which visualizes a NetworkModel as a dash cytoscape graph
        with layers based on node type.
    '''

    ''' Prevents app from breaking with multiple datasets containing 
        matching node ids
    '''
    __visualization_id = 0

    __agent_bg_opacity: float = 0.5

    @staticmethod
    def vis_specifier_string() -> str:
        ''' Returns the string added to the front of every cytoscape
            id: important for the case of multiple visualizations on the
            same data.
        '''
        return str(LayeredVisualizer.__visualization_id) + "_layered_"

    @staticmethod
    def visualize(model: nd.NetworkModel) -> Tuple[list[dict],list[dict]]:
        ''' Takes a network model and returns the stylesheet and elememts 
            sections of a dash cytoscape graph with layer categories.
        ''' 
        elements: list[dict] = []
        stylesheet: list[dict] = Stylesheets.layered_stylesheet()
        LayeredVisualizer.__add_nodes_and_groups(model, elements, stylesheet)
        LayeredVisualizer.__add_edges(model, elements)
        LayeredVisualizer.__visualization_id += 1
        return (elements, stylesheet)

    @staticmethod
    def __add_nodes_and_groups(
        model: nd.NetworkModel, 
        elements: list[dict], 
        stylesheet: list[dict]
    ):
        ''' Adds node and parent node elements to the dash cytoscape app.
        '''
        nodes = model.get_node_ids()
        agent_groups = []
        node_layers = []
        agent_styles = []
        for node_id in nodes:
            element = {}
            vu.add_node_basics(
                element,
                model.get_node(node_id),
                LayeredVisualizer.vis_specifier_string()
            )
            LayeredVisualizer.__put_in_groups(
                model.get_node(node_id),
                element, 
                elements,
                stylesheet,
                agent_groups,
                node_layers,
                agent_styles
            )
            elements.append(element)

    @staticmethod
    def __put_in_groups(
        node: nd.Node, 
        element: dict, 
        elements: list[dict], 
        stylesheet: list[dict],
        agent_groups: list[str],
        node_layers: list[str],
        agent_styles: list[str]
    ):
        ''' Puts the specified element corresponding to the given node
            into its proper cytoscape parent node(s). If they are not 
            present, it adds them. Requires the element to already have
            a data object.
        '''
        if (LayeredVisualizer.__belongs_in_agent_group(node)):
            LayeredVisualizer.__handle_agent_grouping(
                node, 
                element, 
                elements, 
                stylesheet, 
                agent_groups,
                agent_styles
            )
        else:
            element['data']['parent'] = node.__class__.__name__
        if node.__class__.__name__ in node_layers:
            return
        data = {}
        data['id'] = node.__class__.__name__
        data['label'] = node.__class__.__name__
        group_element = {}
        group_element['data'] = data
        group_element['classes'] = 'group'
        elements.append(group_element)
        node_layers.append(node.__class__.__name__)
        
    @staticmethod
    def __belongs_in_agent_group(node: nd.Node) -> bool:
        return (issubclass (node.__class__, nd.ActionNode) 
            and node.has_authorized_agent())

    @staticmethod
    def __handle_agent_grouping(
        node: nd.Node, 
        element: dict, 
        elements: list[dict], 
        stylesheet: list[dict],
        agent_groups: list[str],
        agent_styles: list[str]
    ):
        node_agent = node.get_authorized_agent()
        agent_group_id = node_agent.id + node.__class__.__name__
        element['data']['parent'] = agent_group_id
        if agent_group_id in agent_groups:
            return
        agent_group_data = {}
        agent_group_data['id'] = agent_group_id
        agent_group_data['label'] = node_agent.id
        agent_group_data['parent'] = node.__class__.__name__
        agent_group = {}
        agent_group['data'] = agent_group_data
        agent_group['classes'] = node_agent.id
        elements.append(agent_group)
        agent_groups.append(agent_group_id)
        if node_agent.id in agent_styles:
            return
        style = {}
        style['background-opacity'] = LayeredVisualizer.__agent_bg_opacity
        style['background-color'] = cg.get_color(node_agent.id)
        style_element = {}
        style_element['selector'] = "."+node_agent.id
        style_element['style'] = style
        stylesheet.append(style_element)
        agent_styles.append(node_agent.id)
        
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
                LayeredVisualizer.vis_specifier_string()
            )
            elements.append(element)