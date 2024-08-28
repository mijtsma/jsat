from core.networkdata.generalstorage import ResourceNode

class BaseEnvironmentResource(ResourceNode):
    ''' A typechecking class which represents
        a work domain resource node.
    '''

    def __init__(self, id: str, user_data = None):
        super().__init__(id, user_data)