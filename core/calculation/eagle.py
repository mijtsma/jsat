import networkx as nx

class EagleModularity:
    ''' A class for calculating the modularity of a DIRECTED networkx
        graph with overlapping communities using the EAGLE algorthm.
        https://www.sciencedirect.com/science/article/pii/S0378437108010376#b9
    '''

    @staticmethod
    def eagle_modularity(G, communities) -> float:
        ''' Parameters
            ----------
            G : NetworkX Graph

            communities : list or iterable of set of nodes
                These node sets must contain all nodes in G at least once.

            Returns
            -------
            Q : float
                The modularity of the partition.

            Evaluates the modularity of the given overlapping communities
            using the EAGLE formula, an extension of Newman's modularity.
            Currently no support for weights.
        '''

        if not isinstance(communities, list):
            communities = list(communities)

        member_numbers: dict[str, int]
        member_numbers = EagleModularity.__check_communities(G, communities)

        result: float = 0
        for community in communities:
            result += EagleModularity.__community_contribution(
                G, 
                community, 
                member_numbers
            )
        result *= 1 / (G.number_of_edges())
        return result

    @staticmethod
    def __check_communities(G, communities: list[list[str]]) -> dict[str, int]:
        ''' Checks how many communities each node of a graph is in.
            Raises an exception if a node isn't in a community.
        '''
        result: dict[str, int] = {}
        for node in G.nodes:
            result[node] = 0

        for community in communities:
            for node in community:
                result[node] += 1

        for name in result:
            if result[name] <= 0:
                raise Exception(name + " is not in any community!")
        return result

    @staticmethod
    def __community_contribution(
        G,
        community: list[str],
        member_numbers: dict[str, int]
    ) -> float:
        ''' Calculates the effect of a single community on modularity.
        '''
        contribution: float = 0
        for v in community:
            for w in community:
                member_frac = 1 / (member_numbers[v] * member_numbers[w])
                adjacent = G.number_of_edges(v,w)
                prob_frac = (G.in_degree(v) * G.out_degree(w)/ 
                (G.number_of_edges()))
                contribution += member_frac * (adjacent - prob_frac)
        return contribution

