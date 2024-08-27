from dash import html

from core import networkdata as nd
from cytoapp.datahandler import DataHandler

class MultiDataHandler:
    ''' Class which handles NetworkData operations across multiple data sets
        for the cytoscape app.
    '''

    def __init__(
        self, 
        models: dict[str, nd.NetworkModel],
        handler_type: type[DataHandler] = DataHandler,
        *handler_additional_parameters
    ):
        # print(*handler_additional_parameters)

        self.handlers: dict[str, handler_type] = {}
        for name in models:
            self.handlers[name] = handler_type(
                models[name],
                *handler_additional_parameters
            )
        
    def get_graph_stats_text(self, file_name: str) -> list[html.P]:
        ''' Returns the text displayed under the Graph Stats tab using
            data stored in the specified handler's model.
        '''
        return self.handlers[file_name].get_graph_stats_text()

    def set_node(self, node_id: str, file_name: str):
        ''' Sets the current node in the specified handler's model to the 
            given id if it is present in that model.
        '''
        return self.handlers[file_name].set_node(node_id)

    def get_node_stats_text(self, file_name: str) -> list[html.P]:
        ''' Returns the text displayed under the Node Stats tab using
            data stored in the specified handler's model.
        '''
        return self.handlers[file_name].get_node_stats_text()

    def get_modularity_text(
        self, 
        current_vis: str, 
        file_name: str
    ) -> list[html.P]:
        ''' Returns the text displayed under the modularity tab based on
            the graph visualization currently selected and the specified
            handler's model.
        '''
        return self.handlers[file_name].get_modularity_text(current_vis)