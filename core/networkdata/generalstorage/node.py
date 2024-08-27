from __future__ import annotations

class Node:
    ''' A class which represents a single node in a directed teamwork network
        graph. Inherited by more specific node categories for typechecking
        and/or additional functionality.
    '''

    def __init__(self, id: str, user_data = None):
        #id string for this node
        self.id: str = id
        #space for user data
        self.user_data = user_data

    


