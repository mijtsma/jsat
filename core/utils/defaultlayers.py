from core.networkdata import nodetypes as nt
from core.networkdata.generalstorage.node import Node

class DefaultLayers:
    ''' A class which defines default layers for nodes in the model.
    '''

    @staticmethod
    def layers_dict() -> dict[str: Node]:
        ''' Returns a dictionary that maps strings used in a JSON file
            to implementations of node.
        '''
        return {
            'BaseEnvironmentResource': nt.BaseEnvironmentResource,
            'DistributedWorkFunction': nt.DistributedWorkFunction,
            'CoordinationGroundingResource': nt.CoordinationGroundingResource,
            'SynchronyFunction': nt.SynchronyFunction
        }




