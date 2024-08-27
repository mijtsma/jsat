import dash
from dash import  ctx
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_cytoscape as cyto

from core import networkdata as nd
from cytoapp.layoutsettings import LayoutSettings
from cytoapp.datahandler import DataHandler
from cytoapp.multidatahandler import MultiDataHandler
from cytoapp.htmllayout import HTMLLayout

class CytoscapeApp:
    
    def __init__(
        self,
        data: dict[str: nd.NetworkModel],
        handler_type: type[DataHandler] = DataHandler,
        *handler_additional_parameters
    ):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        cyto.load_extra_layouts()

        # print(*handler_additional_parameters)
        self.data: MultiDataHandler = MultiDataHandler(
            data,
            handler_type,
            *handler_additional_parameters
        )
        
        
        self.app: dash.Dash = dash.Dash(
            __name__, 
            external_stylesheets = external_stylesheets
        )

        HTMLLayout.add_html_elements(self.app, list(data.keys()))
        self.__add_callbacks()

    def run(self):
        ''' Launches self.app, a dash app
        '''
        self.app.run_server(debug=False)

    def __add_callbacks(self):
        ''' Adds dash callbacks to self.app
        '''
        self.app.callback(Output('cytoscape-graph', 'layout'),
              Input('layout-dropdown', 'value'),
              Input('spacing-slider', 'value'),
              State('visualization-dropdown', 'value'))(self.__change_layout)

        self.app.callback(Output('cytoscape-graph', 'elements'),
              Output('cytoscape-graph', 'stylesheet'),
              Input('visualization-dropdown', 'value'),
              Input('dataset-dropdown', 'value'))(self.__change_graph)

        self.app.callback(Output('cytoscape-graph', 'generateImage'),
              Input('btn-get-jpg', 'n_clicks'),
              Input('btn-get-png', 'n_clicks'),
              Input('btn-get-svg', 'n_clicks'))(self.__save_graph)

        self.app.callback(Output('stats-content', 'children'),
              Input('stats', 'value'),
              Input('dataset-dropdown', 'value'),
              State('visualization-dropdown', 'value'))(self.__display_stats)

        self.app.callback(
            Output('stats-content', 'children', allow_duplicate=True),
              Input('visualization-dropdown', 'value'),
              State('stats', 'value'),
              State('stats-content', 'children'),
              State('dataset-dropdown', 'value'),
              prevent_initial_call = True)(self.__adjust_modularity)

        self.app.callback(
              Output('stats-content', 'children', allow_duplicate=True),
              Input('cytoscape-graph', 'tapNodeData'),
              State('stats', 'value'),
              State('stats-content', 'children'),
              State('dataset-dropdown', 'value'),
              prevent_initial_call = True)(self.__node_clicked)



    ''' All below functions are callback functions.
    '''

    def __change_layout(self, layout, spacingFactor, visVal):
        return LayoutSettings.get_layout_spacing_factor(
            layout, 
            spacingFactor,
            visVal
        )

    def __change_graph(self, value, dataset):
        return (self.data.handlers[dataset].visualizations[value],
         self.data.handlers[dataset].stylesheets[value])
            
    def __save_graph(self, jpg_clicks, png_clicks, svg_clicks):
        if ctx.triggered:
            if (ctx.triggered_id == 'btn-get-jpg' or 
                ctx.triggered_id == 'btn-get-png' or
                ctx.triggered_id == 'btn-get-svg'):
                return {
                    'type': (ctx.triggered_id.split("-")[-1]),
                    'action': 'download'
                }
        return {}

    def __display_stats(self, tab, dataset, dropdown):
        return_val = "Something went wrong!"
        match tab:
            case 'graph':
                return_val = self.data.get_graph_stats_text(dataset)
            case 'node':
                return_val = self.data.get_node_stats_text(dataset)
            case 'modularity':
                return_val = self.data.get_modularity_text(dropdown, dataset)
        return return_val


    def __adjust_modularity(self, dropdown, tab, current_content, dataset):
        if tab != 'modularity':
            return current_content
        return self.data.get_modularity_text(dropdown, dataset)


    def __node_clicked(self, node, tab, current_content, dataset):
        self.data.set_node(node['label'], dataset)
        if tab != 'node':
            return current_content
        else:
            return self.data.get_node_stats_text(dataset)
    


