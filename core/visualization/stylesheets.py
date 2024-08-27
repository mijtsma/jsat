class Stylesheets:
    ''' A class which returns various preset dash cytoscape stylesheets.
    '''
    @staticmethod
    def standard_stylesheet() -> list[dict]:
        ''' Stylesheet for standard graph with no grouping.
        '''
        return [
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'mid-target-arrow-shape': 'triangle-backcurve',
                'arrow-scale': '3'
            }
        },
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-outline-color': 'white',
                'text-outline-width': '2',
                'font-size': '25',
                'font-family': 'Times New Roman, serif'
            }
        },
        {
            'selector': '.resource',
            'style': {
                'shape': 'ellipse',
                'background-color': 'black'
            }
        },
        {
            'selector': '.action',
            'style': {
                'shape': 'rectangle',
                'background-color': 'black'
            }
        },
        {
            'selector': '.org',
            'style': {
                'line-style': 'dashed'
            }
        },
        {
            'selector': '.ame',
            'style': {
                'line-style': 'solid'
            }
        }
    ]

    @staticmethod
    def layered_stylesheet() -> list[dict]:
        ''' Stylesheet for graph with layered node type grouping.
        '''
        sheet = Stylesheets.standard_stylesheet()
        sheet.extend([
            {
                'selector': '.group',
                'style': {
                    'text-halign': 'left',
                    'text-valign':'center',
                    'text-margin-x': '-10'
                }
            }
        ])
        return sheet


