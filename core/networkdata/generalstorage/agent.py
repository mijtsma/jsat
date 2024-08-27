from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .actionnode import ActionNode

from core.utils.defaultallocation import DefaultAllocation

class Agent:
    ''' A class representing a single agent. Can
        be assigned ActionNodes.
    '''

    def __init__(
        self,
        id: str,
        user_data = None,
        allocation_types: IntEnum = DefaultAllocation
    ):
        self.id: str = id
        self.allocation_types = allocation_types
        self.nodes: dict[allocation_types, dict[type, dict[str, ActionNode]]]
        self.nodes = {}
        for t in allocation_types:
            self.nodes[t] = {}
        self.user_data = user_data

    def add_action(
        self, 
        action: ActionNode, 
        alloc_type
    ):
        ''' Method which links a specified ActionNode to this agent with the 
            given allocation type. Requires allocation type to be in the
            enum provided at initialization for the agent and the action.
        '''
        self.__check_alloc_in_enum(alloc_type)
        current_nodes: dict[type, dict[str, ActionNode]] 
        current_nodes = self.nodes[alloc_type]
        action_type: type = type(action)
        if action_type in current_nodes:
            current_nodes[action_type][action.id] = action
        else:
            current_nodes.update({action_type: {action.id: action}})
        if not action.has_agent(self, alloc_type):
            action.add_agent(self, alloc_type)

    def has_action(self, action: ActionNode, alloc_type) -> bool:
        ''' Returns true if the given action is present with the given
            alloction type, false otherwise. Requires alloc_type to be
            present in self.allocation_types.
        '''
        self.__check_alloc_in_enum(alloc_type) 
        action_type: type = type(action)
        if not action_type in self.nodes[alloc_type]:
            return False
        return action.id in self.nodes[alloc_type][action_type]

    def get_actions(self, alloc_type) -> list:
        ''' Method which returns a list of all ActionNode IDs in the specified
            categoty associated with this agent. Requires allocation type to
            be in the enum provided at initialization.
        '''
        self.__check_alloc_in_enum(alloc_type)
        ans: list = []
        for d in self.nodes[alloc_type].values():
            ans = ans + list(d.keys())
        return ans

    def try_remove_action(
        self,
        action_id: str,
        alloc_type
    ):
        ''' Method which removes the ActionNode specified by the ID from the
            specified category of this agent, if it is present. Requires 
            allocation type to be in the enum provided at initialization.
        '''
        self.__check_alloc_in_enum(alloc_type)
        d: dict[str, ActionNode]
        for d in self.nodes[alloc_type].values():
            if action_id in d:
                del d[action_id]
    
    def __check_alloc_in_enum(self, alloc_type):
        ''' Raises an exception if alloc_type is not in self.allocation_types
        '''
        if alloc_type not in self.allocation_types:
            raise Exception("Value " + alloc_type + " not in " +
                            self.allocation_types +"!")



    
