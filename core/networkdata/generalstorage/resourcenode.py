from .node import Node

class ResourceNode(Node):
    ''' A typechecking class which represents
        a resource node.
    '''

    def __init__(self, id: str, user_data = None):
        super().__init__(id, user_data)