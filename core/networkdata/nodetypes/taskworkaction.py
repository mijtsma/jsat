from enum import IntEnum

from core.networkdata.generalstorage import ActionNode, Agent
from core.utils.defaultallocation import DefaultAllocation

class DistributedWorkFunction(ActionNode):
    ''' A typechecking class which represents
        a taskwork action node.
    '''

    def __init__(
        self, 
        id: str,  
        user_data = None,
        allocation_types: IntEnum = DefaultAllocation
    ):
        super().__init__(id, user_data, allocation_types)
