class TreeAdjLi(object):
    T = None
    droppedComponents = None
    vertices = None
    def __init__(self,MST,numVertices):
        """
        Use: G = adjLi(MST,numVertices)
        Pre: MST is a list representing a graph with less than numVertices
            vertices of the form (w,u,v), where 0 < u < v < numVertices
        Post: G is an adjacency list of the graph that MST represents.
        """
        self.numVertices = numVertices
        self.T = [set() for _ in range(numVertices)]
        for (w,u,v) in MST:
            self.add(u,v)
        #self.droppedComponents = dict()
        #self.vertices = set(range(len(self.T)))
        #self.ranks = [len(self.T[u]) for u in range(numVertices)]
        

    def drop(self,u,v):
        """
        Use: adjLi.drop(u,v)
        Pre: u and v are vertices in the adjLi
        Post:the edge u,v has been added to the adjacency list.
        """
        self.T[u].discard(v)
        self.T[v].discard(u)

    def add(self,u,v):
        """
        Use: adjLi.add(u,v)
        Pre: u and v are vertices in the adjLi
        Post:the edge u,v has been added to the adjacency list.
        """
        self.T[u].add(v)
        self.T[v].add(u)
        
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
                unvisitedFromU.update(self.T[visitingFromCu])
                componentContainingU.add(visitingFromCu)
            visitingFromCv = unvisitedFromV.pop()
            if visitingFromCv not in componentContainingV:
                unvisitedFromV.update(self.T[visitingFromCv])
                componentContainingV.add(visitingFromCv)
        return componentContainingU if unvisitedFromV else componentContainingV
   

    def _findSmallerComponent(self,du,dv):
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

    def rank(self,v):
        return self.ranks[v]

    def compo(self,v,edgeToDrop):
        """
        edge to drop is du,dv, and v is one of du or dv.
        """

        (du,dv) = edgeToDrop
        u = du if dv == v else dv
        #Memoize
        if (v,edgeToDrop) in self.droppedComponents:
            return self.droppedComponents[(v,edgeToDrop)]

        components = []
        for nu in self.T[v]:
            if nu == u:
                continue
            edge = (v,nu) if v < nu else (nu,v)
            components.append(self.compo(nu,edge)) 
        compv = set([v])
        compv.update(*components)
        compu = self.vertices - compv
        self.droppedComponents[(u,edgeToDrop)] = compu
        self.droppedComponents[(v,edgeToDrop)] = compv
        return compv
        
        
            
            
    def findSmallerComponents(self,edgeList):
        """
        Use:  comps = findSmallerComponents(edgeList)
        Pre: edgeList is the list of the edges in this tree
        Post: comps[i] is the smaller component of the 
             two components that we'd get if we dropped edgeList[i]
        """
        components = []
        for (w,u,v) in edgeList:
            #edge = (u,v)
            #compu = self.compo(u,edge)
            #compv = self.compo(v,edge)
            #comp =  compu if len(compu) < len(compv) else compv
            comp = self._findSmallerComponent(u,v)
            components.append(comp)
        return components
        
