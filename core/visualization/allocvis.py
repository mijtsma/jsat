import networkx as nx
from typing import Tuple

import core.networkdata as nd
from core.visualization.stylesheets import Stylesheets
from core.utils.visutils import VisualizationUtils as vu
from core.utils.colorgen import ColorGenerator as cg

class AllocationVisualizer:
    ''' A class which visualizes a NetworkModel as a dash cytoscape graph
        with groups based on a specified type of action-agent allocation.
    '''

    ''' Prevents app from breaking with multiple datasets containing 
        matching node ids
    '''
    __visualization_id = 0

    __AGENT_BG_OPACITY: float = 0.1

    @staticmethod
    def __vis_specifier_string() -> str:
        ''' Returns the string added to the front of every cytoscape
            id: important for the case of multiple visualizations on the
            same data.
        '''
        return str(AllocationVisualizer.__visualization_id) + "_allocation_"

    @staticmethod
    def visualize(
        model: nd.NetworkModel, 
        alloc_type = 1
    ) -> Tuple[list[dict],list[dict]]:
        ''' Takes a network model and enum value (by default the direct
            assignment entry) and returns the stylesheet and elememts 
            sections of a dash cytoscape graph with allocation categories.
        ''' 
        elements: list[dict] = []
        stylesheet: list[dict] = Stylesheets.standard_stylesheet()
        AllocationVisualizer.__add_nodes_and_groups(
            model, 
            elements, 
            stylesheet,
            alloc_type
        )
        AllocationVisualizer.__add_edges(model, elements, alloc_type)
        AllocationVisualizer.__visualization_id += 1
        return (elements, stylesheet)

    @staticmethod
    def __add_nodes_and_groups(
        model: nd.NetworkModel, 
        elements: list[dict], 
        stylesheet: list[dict],
        alloc_type
    ):
        ''' Adds node and parent node elements to the dash cytoscape app.
        '''
        nodes = model.get_node_ids()
        agent_groups = []
        for node_id in nodes:
            element = {}
            vu.add_node_basics(
                element,
                model.get_node(node_id),
                AllocationVisualizer.__vis_specifier_string()
            )
            AllocationVisualizer.__put_in_groups(
                model.get_node(node_id),
                element, 
                elements,
                stylesheet,
                agent_groups,
                alloc_type
            )
            elements.append(element)
    
    @staticmethod
    def __put_in_groups(
        node: nd.Node, 
        element: dict, 
        elements: list[dict], 
        stylesheet: list[dict],
        agent_groups: list[str],
        alloc_type
    ):
        ''' Puts the specified element corresponding to the given node
            into its proper cytoscape parent node(s). If they are not 
            present, it adds them. Requires the element to already have
            a data object.
        '''
        if not issubclass (node.__class__, nd.ActionNode):
            return
        agent_group_id = ""
        agent_group_label = ""
        for agent_id in node.agents[alloc_type]:
            if agent_group_id == "":
                agent_group_id = agent_id
                agent_group_label = agent_id
            else:
                agent_group_id = agent_group_id + "_and_" + agent_id
                agent_group_label = agent_group_label + " and " + agent_id
        if agent_group_id == "":
            agent_group_id = "None"
            agent_group_label = "None"
        element['data']['parent'] = agent_group_id
        if agent_group_id in agent_groups:
            return
        agent_group_data = {}
        agent_group_data['id'] = agent_group_id
        agent_group_data['label'] = agent_group_label
        agent_group = {}
        agent_group['data'] = agent_group_data
        agent_group['classes'] = agent_group_id
        elements.append(agent_group)
        style = {}
        style['background-opacity'] = AllocationVisualizer.__AGENT_BG_OPACITY
        style['background-color'] = cg.get_color(agent_group_id)
        style_element = {}
        style_element['selector'] = "."+agent_group_id
        style_element['style'] = style
        stylesheet.append(style_element)
        agent_groups.append(agent_group_id)     
    
    @staticmethod
    def __add_edges(model: nd.NetworkModel, elements: list[dict], alloc_type):
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
                AllocationVisualizer.__vis_specifier_string()
            )
            elements.append(element)