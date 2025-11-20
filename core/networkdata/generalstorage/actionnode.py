from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Dict,Union, List

if TYPE_CHECKING:
    from .agent import Agent

from .node import Node
from core.utils.defaultallocation import DefaultAllocation

class ActionNode(Node):
    ''' A class of node which has a field for
        an agent.
    '''

    def __init__(
        self, 
        id: str, 
        user_data = None,
        allocation_types: IntEnum = DefaultAllocation
    ):
        super().__init__(id, user_data)
        self.allocation_types = allocation_types
        self.agents: dict[allocation_types, dict[str, Agent]] = {}
        for t in allocation_types:
            self.agents[t] = {}

    def has_authorized_agent(self) -> bool:
        ''' Returns whether there is a current authorized agent (enum value 1).
        '''
        return list(self.agents[self.allocation_types(1)].values()) != []

    def get_authorized_agent(self, return_list: bool = False) -> Union[Agent, List[Agent]]:
        ''' Returns the current authorized agent (enum value 1). If multiple
            are assigned, returns the first in the dict.values() list unless
            return_list is true, in which case returns a list of all authorized agents.
            Requires there to be an authorized agent.
        '''
        if not self.has_authorized_agent():
            raise Exception("No authorized agent found for ActionNode " + self.id)
        if return_list:
            return list(self.agents[self.allocation_types(1)].values())
        else:
            return list(self.agents[self.allocation_types(1)].values())[0]

    def has_responsible_agent(self) -> bool:
        ''' Returns whether there is a current responsible agent (enum value 2).
        '''
        return list(self.agents[self.allocation_types(2)].values()) != []

    def get_responsible_agent(self, return_list: bool = False) -> Union[Agent, List[Agent]]:
        ''' Returns the current responsible agent (enum value 2). If multiple
            are assigned, returns the first in the dict.values() list unless
            return_list is true, in which case returns a list of all responsible agents.
            Requires there to be a responsible agent.
        '''
        if not self.has_responsible_agent():
            raise Exception("No responsible agent found for ActionNode " + self.id)
        if return_list:
            return list(self.agents[self.allocation_types(2)].values())
        else:
            return list(self.agents[self.allocation_types(2)].values())[0]

    def add_agent(self, agent: Agent, alloc_type):
        ''' Method which links a specified Agent to this ActionNode with the 
            given allocation type. Requires allocation type to be in the
            enum provided at initialization for the agent and the action.
        '''
        self.__check_alloc_in_enum(alloc_type)
        self.agents[alloc_type][agent.id] = agent
        if not agent.has_action(self, alloc_type):
            agent.add_action(self, alloc_type)

    def has_agent(self, agent: Agent, alloc_type) -> bool:
        ''' Returns true if the given agent is present with the given
            alloction type, false otherwise. Requires alloc_type to be
            present in self.allocation_types.
        '''
        self.__check_alloc_in_enum(alloc_type)
        return agent.id in self.agents[alloc_type]


    def __check_alloc_in_enum(self, alloc_type):
        ''' Raises an exception if alloc_type is not in self.allocation_types
        '''
        if alloc_type not in self.allocation_types:
            raise Exception("Value " + alloc_type + " not in " +
                            self.allocation_types +"!")