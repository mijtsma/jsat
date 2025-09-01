import copy
from typing import Callable

class LayoutSettings:
    ''' A class containing options for various graph layouts.
    '''    

    ''' Default COSE ideal spacing.
    '''
    __COSE_IDEAL_SPACING = 100

    ''' Default layered COSE ideal spacing.
    '''
    __COSE_LAYER_SPACING = 100

    @staticmethod
    def get_layout_spacing_factor(
        layout: str, 
        factor: float,
        visualization: str
    ) -> dict[str: str]:
        result = LayoutSettings.get_layout(layout)
        match layout:
            case 'dagre':
                result['spacingFactor'] = str(factor)
            case 'cose-bilkent':
                if(visualization != 'layered'):
                    #TODO: make spacing adjustment work for this case without freezing
                    spacing: float = LayoutSettings.__COSE_IDEAL_SPACING * factor
                    result['idealEdgeLength'] = str(int(spacing))
                    
            case 'concentric':
                result['minNodeSpacing'] = str(int(factor))
                result['spacingFactor'] = str(factor)
            case 'preset':
                result['spacingFactor'] = str(factor)
        return result

    @staticmethod
    def get_layout(layout: str) -> dict[str: str]:
        return LayoutSettings.__func_map[layout]()

    @staticmethod
    def dagre_layout():
        return {
            'name': 'dagre',
            'nodeDimensionsIncludeLabels': 'true',
            'rankDir': 'LR',
            'animate': True,
            'fit': True,
            'spacingFactor': 0.6
        }

    @staticmethod
    def cose_bilkent_layout():
        return {
            'name': 'cose-bilkent',
            'nodeDimensionsIncludeLabels': 'true',
            'animate': True,
            'fit': True
        }

    @staticmethod
    def concentric_layout():
        return {
            'name': 'concentric',
            'nodeDimensionsIncludeLabels': 'true',
            'animate': True,
            'fit': True,
            'spacingFactor': 0.57,
            # 'concentric': lambda node: node.data('degree'),  # Assumes nodes have a 'degree' attribute
        }

    @staticmethod
    def preset_layout():
        return {
            'name': 'preset',
            'nodeDimensionsIncludeLabels': 'true'
            # 'animate': True,
            # "animationDuration": 5,
            # 'fit': True,
        }
    
    @staticmethod
    def grid_layout():
        return {
            'name': 'grid',
            'nodeDimensionsIncludeLabels': 'true',
            'animate': True,
            'fit': True
        }
    
    @staticmethod
    def cola_layout():
        return {
            'name': 'cola',
            'nodeDimensionsIncludeLabels': 'true',
            'animate': True,
            'fit': True
        }
    
    @staticmethod
    def klay_layout():
        return {
            'name': 'klay',
            'nodeDimensionsIncludeLabels': 'true',
            'animate': True,
            'fit': True
        }
    
    @staticmethod
    def spread_layout():
        return {
            'name': 'spread',
            'nodeDimensionsIncludeLabels': 'true',
            'animate': True,
            'fit': True
        }
    
    @staticmethod
    def euler_layout():
        return {
            'name': 'euler',
            'nodeDimensionsIncludeLabels': 'true',
            'animate': True,
            'fit': True
        }
    
    @staticmethod
    def breadthfirst_layout():
        return {
            'name': 'breadthfirst',
            'nodeDimensionsIncludeLabels': 'true',
            'animate': True,
            'fit': True
        }
    
    __func_map: dict[str: Callable[[], dict[str:str]]] = {
            'dagre': dagre_layout,
            'cose-bilkent': cose_bilkent_layout,
            'concentric': concentric_layout,
            'preset': preset_layout,
            'grid': grid_layout,
            'cola': cola_layout,
            'klay': klay_layout,
            'spread': spread_layout,
            'euler': euler_layout,
            'breadthfirst': breadthfirst_layout
    }
    