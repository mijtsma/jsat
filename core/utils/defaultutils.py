from core.networkdata.generalstorage import EdgeData

class DefaultUtils:
    ''' Utility functions relating to default settings.
    '''

    @staticmethod
    def default_edge() -> EdgeData:
        ''' Returns a default instance of EdgeData
        '''
        result: EdgeData = EdgeData(1)
        return result

    @staticmethod
    def user_parse(user_data):
        ''' The default behavior for parsing user data. These types of
            functions recieve the data tied to the "UserData" entries in
            JSON files and return what user_data within the network model
            elements should be set to.
        '''
        return user_data
    
    @staticmethod
    def user_encode(user_data):
        ''' The default behavior for encoding user data. These types of
            functions recieve the data tied to the user_data entries in
            network model elements and return what the "UserData" field in
            the JSON file should contain.
        '''
        return user_data
