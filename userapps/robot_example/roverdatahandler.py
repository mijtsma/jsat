import os.path
from dash import html
from typing import FrozenSet

from core import networkdata as nd
from cytoapp.datahandler import DataHandler
from core.calculation.basicstats import BasicStats

class RoverDataHandler(DataHandler):
    ''' Class which handles NetworkData operations for the cytoscape app.
        Overrides node stats to get full node name from userdata when
        clicking on node.
    '''

    def __init__(
        self, 
        model: nd.NetworkModel,
        highlighted_edges: [[str,str]] = [],
    ):
        # print(highlighted_edges)
        super().__init__(model)
        self.__update_stylesheets()
        self.__update_visualizations(highlighted_edges)

    def get_node_stats_text(self) -> list[html.P]:
        ''' Returns the text displayed under the Node Stats tab using
            data stored in self.
        '''
        if self.current_node == None:
            return[
                html.P("No node selected!")
            ]
        node_id = self.current_node
        return[
            html.P(
                "Name: " + self.model.get_node(node_id).user_data
            ),
            html.P(
                "Degree: " + str(BasicStats.degree(self.model, node_id))
            ),
            html.P(
                "Degree Centrality: " + str(self.d_centrality[node_id])
            ),
            html.P(
                "Eigenvector Centrality: " + str(self.e_centrality[node_id])
            ),
            html.P(
                "Closeness Centrality: " + str(self.c_centrality[node_id])
            ),
            html.P(
                "Clustering Coefficient: " + str(self.clustering[node_id])
            )
        ]

    def __update_stylesheets(self):
        highlight_style: dict = {
            'selector': '.highlighted',
            'style': {
                'line-color': 'black',
                'mid-target-arrow-color': 'black',
                'width': 6,
                'label': 'data(label)',  # Accessing the label property of the edge object
                'text-rotation': 'autorotate',
                'font-size': '22px',
                'text-margin-y': '-15px'
            }
        }
        for stylesheet in self.stylesheets.values():
            stylesheet.append(highlight_style)
        return

    def __update_visualizations(
        self,
        highlighted_edges: [(str,str)]
    ):
        for visualization in self.visualizations.values():
            node_dict = {}
            edge_dict = {}
            for element in visualization:
                self.__rectify_vis_element(element, node_dict, edge_dict)
            for edge in highlighted_edges:
                self.__highlight_edge(edge, edge_dict)
        return
            

    def __rectify_vis_element(self, element, node_dict, edge_dict):
        if 'id' in element['data']:
            node_dict[element['data']['id']] = element
        elif 'source' in element['data']:
            source_name = element['data']['source'].rsplit("_", 1)[1]
            target_name = element['data']['target'].rsplit("_", 1)[1]
            edge_dict[(source_name, target_name)] = element

            if self.model.has_edge(source_name, target_name):
                edge_object = self.model.get_edge(source_name, target_name)
                if edge_object and hasattr(edge_object.user_data, 'QOS'):
                    target_node = self.model.get_node(target_name)
                    # if isinstance(target_node, nd.ActionNode):
                    #     element['data']['label'] = edge_object.user_data.QOS

    def __highlight_edge(self, edge, edge_dict):
        if not edge in edge_dict:
            return
        class_str = ""
        if 'classes' in edge_dict[edge]:
            class_str = class_str + edge_dict[edge]['classes']
        if len(class_str) > 0:
            class_str = class_str + " "
        class_str = class_str + "highlighted"
        edge_dict[edge]['classes'] = class_str





