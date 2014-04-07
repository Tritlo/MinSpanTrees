class TreeAdjLi(object):
    G = None
    def __init__(self,MST,numVertices):
        """
        Use: G = adjLi(MST,numVertices)
        Pre: MST is a list representing a graph with less than numVertices
            vertices of the form (w,u,v), where 0 < u < v < numVertices
        Post: G is an adjacency list of the graph that MST represents.
        """
        self.numVertices = numVertices
        self.G = [set() for _ in range(numVertices)]
        for (w,u,v) in MST:
            self.add(u,v)

    def drop(self,u,v):
        """
        Use: adjLi.drop(u,v)
        Pre: u and v are vertices in the adjLi
        Post:the edge u,v has been added to the adjacency list.
        """
        self.G[u].discard(v)
        self.G[v].discard(u)

    def add(self,u,v):
        """
        Use: adjLi.add(u,v)
        Pre: u and v are vertices in the adjLi
        Post:the edge u,v has been added to the adjacency list.
        """
        G = self.G
        G[u].add(v)
        G[v].add(u)
        
    def _bfsComponent(self,u,v):
        """
        Use: component = adjLi._bfsComponent(u,v)
        Pre: u and v are nodes in the AdjacencyList
        Post: component is the smaller component of the components
             that contain u and v.
        """
        
        #This could be paralellized, but in practice it was slower :(
        #We search from both ends, terminating
        #When we reach the end of either.
        componentContainingU, componentContainingV = set(),set()
        #Unvistied u and v
        unvisitedFromU,unvisitedFromV = set([u]), set([v])
        while unvisitedFromU and unvisitedFromV:
            visitingFromCu = unvisitedFromU.pop()
            if visitingFromCu not in componentContainingU:
                unvisitedFromU |= self.G[visitingFromCu]
                componentContainingU.add(visitingFromCu)
            visitingFromCv = unvisitedFromV.pop()
            if visitingFromCv not in componentContainingV:
                unvisitedFromV |= self.G[visitingFromCv]
                componentContainingV.add(visitingFromCv)
        return componentContainingU if unvisitedFromV else componentContainingV
   

    def findSmallerComponent(self,du,dv):
        """
        Use: component = adjLi.findSmallerComponent(du,dv)
        Pre: du and dv are nodes in the AdjacencyList
        Post: component is the smaller component of the components
             that contain du and dv if edge (du,dv) is dropped.
        """
        self.drop(du,dv)
        component = self._bfsComponent(du,dv)
        self.add(du,dv)
        return component

    def findSmallerComponents(self,edgeList):
        #Naive version
        components = []
        for (w,u,v) in edgeList:
            components.append(self.findSmallerComponent(u,v))
        return components
        
