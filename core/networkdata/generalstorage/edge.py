class EdgeData:
    ''' A class representing the data belonging to an edge of the graph,
        including edge weight and user data.
    '''

    def __init__(self, weight: float, user_data = None):
        #weight for this edge
        self.weight = weight
        #spot for user data
        self.user_data = user_data
