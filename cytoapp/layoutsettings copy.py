from typing import Callable

class LayoutSettings:
    ''' A class containing options for various graph layouts.
    '''    

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
            'spacingFactor': 0.57
        }

    __func_map: dict[str: Callable[[], dict[str:str]]] = {
            'dagre': dagre_layout,
            'cose-bilkent': cose_bilkent_layout,
            'concentric': concentric_layout
    }
    