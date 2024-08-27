import dash
from dash import html
from dash import dcc
import dash_cytoscape as cyto

class HTMLLayout:
    ''' Storage for the HTML layout of the cytoscape app.
    '''

    @staticmethod
    def add_html_elements(dash_app: dash.Dash, data_sets: list[str]):
        ''' Adds html element layout to the given app
        '''
        dash_app.layout = html.Div([
            html.Label(
                'Visualization Options:', 
                style = {
                    'width': '33%', 
                    'display': 'inline-block'
                }, 
                id = 'vis_ops'
            ),
            html.Label(
                'Layout Options:', 
                style = {
                    'width': '33%', 
                    'display': 'inline-block'
                }, 
                id = 'lay_ops'
            ),
            html.Label(
                'Dataset:', 
                style = {
                    'width': '33%', 
                    'display': 'inline-block'
                }, 
                id = 'dat_ops'
            ),
            html.Div(
                dcc.Dropdown(
                    id = 'visualization-dropdown',
                    options = [
                        {'label': name.capitalize(), 'value': name}
                        for name in ['layered', 'standard', 'allocation']
                    ],
                    value = 'layered',
                    clearable = False
                ), style = {'width': '33%', 'display': 'inline-block'}
            ),
            html.Div(
                dcc.Dropdown(
                    id = 'layout-dropdown',
                    options = [
                        {'label': name.capitalize(), 'value': name}
                        for name in ['dagre', 'cose-bilkent', 'concentric']
                    ],
                    value = 'dagre',
                    clearable = False
                ), style = {'width': '33%', 'display': 'inline-block'}
            ),
            html.Div(
                dcc.Dropdown(
                    id = 'dataset-dropdown',
                    options = [
                        {'label': name.capitalize(), 'value': name}
                        for name in data_sets
                    ],
                    value = data_sets[0],
                    clearable = False
                ), style = {'width': '33%', 'display': 'inline-block'}
            ),
            html.Label(
                'Spacing:', 
                id = 'spacing-label'
            ),
            html.Div(
                dcc.Slider(
                    id='spacing-slider',
                    min=0,
                    max=5,
                    step=0.05,
                    value=1,
                    marks=None,
                    tooltip={
                        "always_visible": False,
                        "style": {"color": "white", "fontSize": "20px"},
                    },
                ),
            ),
            cyto.Cytoscape(
                id='cytoscape-graph',
                layout={
                    'name': 'dagre',
                    'nodeDimensionsIncludeLabels': 'true',
                    'rankDir': 'LR'
                },
                style={'width': '100%', 'height': '600px'},
                stylesheet = [],
                elements = []
            ),
            html.Div('Download graph:'),
            html.Button('as jpg', id='btn-get-jpg'),
            html.Button('as png', id='btn-get-png'),
            html.Button('as svg', id='btn-get-svg'),

            dcc.Tabs(id = 'stats', value = 'graph', children = [
                dcc.Tab(label = 'Graph Stats', value = 'graph'),
                dcc.Tab(label = 'Node Stats', value = 'node'),
                dcc.Tab(label = 'Modularity', value = 'modularity')
            ]),
            html.Div(id = 'stats-content')
            
        ])