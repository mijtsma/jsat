import os.path
from dash import html
from typing import FrozenSet

from core import networkdata as nd
from core.visualization.standardvis import StandardVisualizer
from core.visualization.layervis import LayeredVisualizer
from core.visualization.allocvis import AllocationVisualizer
from core.calculation.basicstats import BasicStats

class DataHandler:
    ''' Class which handles NetworkData operations for the cytoscape app.
        Methods can be overriden to display different information.
    '''

    def __init__(self, model: nd.NetworkModel):
        self.model: nd.NetworkModel = model
        self.visualizations: dict[str, list[dict]]
        self.stylesheets: dict[str, list[dict]]
        self.d_centrality: dict[str, float]
        self.e_centrality: dict[str, float]
        self.c_centrality: dict[str, float]
        self.clustering: dict[str, float]
        self.layer_modularity: float
        self.alloc_modularity: float
        self.generated_communities: list[frozenset[str]]
        self.__create_visualizations()
        self.__calculate_stats()
        self.current_node = None

    def get_graph_stats_text(self) -> list[html.P]:
        ''' Returns the text displayed under the Graph Stats tab using
            data stored in self.
        '''
        return[
            html.P(
                "Number of nodes: " + 
                str(BasicStats.number_of_nodes(self.model))
            ),
            html.P(
                "Number of edges: " + 
                str(BasicStats.number_of_edges(self.model)) 
            )
        ]
    
    def set_node(self, node_id: str):
        ''' Sets self.current_node to the given id if it is present in
            self.model.
        '''
        if self.model.has_node(node_id):
            self.current_node = node_id

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
                "Name: " + node_id
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

    def get_modularity_text(self, current_vis: str) -> list[html.P]:
        ''' Returns the text displayed under the modularity tab based on
            the graph visualization currently selected.
        '''
        match current_vis:
            case 'layered':
                return self.__get_layer_modularity_text()
            case 'standard':
                return self.__get_standard_modularity_text()
            case 'allocation':
                return self.__get_allocation_modularity_text()
            case _:
                return [html.P("Modularity default case!")]

    def __get_layer_modularity_text(self) -> list[html.P]:
        ''' Returns text displaying the modularity of self.model based on node
            type.
        '''
        return[
            html.P("Modularity based on layers: "),
            html.P(self.layer_modularity)
        ]

    def __get_standard_modularity_text(self) -> list[html.P]:
        ''' Returns text displaying generated modular communities based on
            the data in self.model
        '''
        result: list[html.P] = []
        result.append(html.P("Generated Communities: "))
        c: frozenset[str]
        for c in self.generated_communities: 
            c_str: str = str(c)
            result.append(html.P(c_str[10:len(c_str)-1]))
        return result

    def __get_allocation_modularity_text(self) -> list[html.P]:
        ''' Returns text displaying the modularity of self.model based on 
            allocation.
        '''
        return[
            html.P("Modularity based on allocation: "),
            html.P(self.alloc_modularity)
        ]
        
    def __create_visualizations(self):
        ''' Creates visualizations and stylesheets from self.model for access 
            by the app.
        '''
        model = self.model
        standard_elements, standard_style = StandardVisualizer.visualize(model)
        layered_elements, layered_style = LayeredVisualizer.visualize(model)
        alloc_elements, alloc_style = AllocationVisualizer.visualize(model)
        self.visualizations = {
            'layered': layered_elements,
            'standard': standard_elements,
            'allocation': alloc_elements
        }
        self.stylesheets = {
            'layered': layered_style,
            'standard': standard_style,
            'allocation': alloc_style,
        }

    def __calculate_stats(self):
        ''' Calculates varoious stats about self.model for use in the app.
        '''
        self.d_centrality = BasicStats.degree_centrality(self.model)
        self.e_centrality = BasicStats.eigenvector_centrality(self.model)
        self.c_centrality = BasicStats.closeness_centrality(self.model)
        self.clustering = BasicStats.clustering_coefficients(self.model)
        self.layer_modularity = BasicStats.layer_modularity(self.model)
        self.alloc_modularity = BasicStats.allocation_modularity(
            self.model, 
            1
        )
        self.generated_communities = BasicStats.find_communities(self.model)



