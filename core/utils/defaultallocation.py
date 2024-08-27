from enum import IntEnum

''' An enum that specifies the dimmensions of allocation of actions. By
        convention, enum element 1 (in this case Authority) is used for
        direct agent assignment.
        Used in JSON parsing and in agent/action node classes.
'''

class DefaultAllocation(IntEnum):
    Authority = 1
    Responsibility = 2
    Competency = 3
