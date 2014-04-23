from heapq import *

   
def makeAdjLi(numVertices,edges):
    """
    Use: adjLi = makeAdjLi(numVertices, edges)
    Pre: numVertices is the number of vertices in a simple undirected connected graph,
         whose edges are in the list edges on the form (w,u,v),
    Post: adjLi is a list of length numVertices, whose entries are such 
        that adjLi[u] is a set of the edges in edges that have u as an edge.
    
    """
    adjLi = [ set() for _ in range(numVertices)]
    for (w,u,v) in edges:
        adjLi[u].add((w,u,v))
        adjLi[v].add((w,u,v))
    return adjLi

def findSmallerComponent(u,v,adjLi):
    """
    Use: component = _bfsComponent(u,v,adjLi)
    Pre: u and v are nodes in the adacencyList adjLi
    Post: component is the smaller component of the components
         that contain u and v.
    """

    #This could be paralellized, but in practice it was slower :(
    #We search from both ends, terminating
    #When we reach the end of either.
    componentContainingU, componentContainingV = set(),set()
    #Unvistied u and v
    unvisitedFromU,unvisitedFromV = set([u]), set([v])

    # Do one round first
    visitingFromCu = unvisitedFromU.pop()
    if visitingFromCu not in componentContainingU:
        unvisitedFromU.update(adjLi[visitingFromCu])
        componentContainingU.add(visitingFromCu)

    visitingFromCv = unvisitedFromV.pop()
    if visitingFromCv not in componentContainingV:
        unvisitedFromV.update(adjLi[visitingFromCv])
        componentContainingV.add(visitingFromCv)

    # We are checking what happens
    # If (u,v) was not present.
    unvisitedFromU.remove(v)
    unvisitedFromV.remove(u)

    while unvisitedFromU and unvisitedFromV:
        visitingFromCu = unvisitedFromU.pop()
        if visitingFromCu not in componentContainingU:
            unvisitedFromU.update(adjLi[visitingFromCu])
            componentContainingU.add(visitingFromCu)
        visitingFromCv = unvisitedFromV.pop()
        if visitingFromCv not in componentContainingV:
            unvisitedFromV.update(adjLi[visitingFromCv])
            componentContainingV.add(visitingFromCv)
    return componentContainingU if unvisitedFromV else componentContainingV


def makeNonWAdjLi(edgeList,numVertices):
    adjLi = [set() for _ in range(numVertices)]
    for (w,u,v) in edgeList:
        adjLi[u].add(v)
        adjLi[v].add(u)
    return adjLi


def findLegalMin(tree,edgesFromTree,edgesFromTreeSet,adjLi):
    """
    Use: (w,u,v) = findLegalMin(tree, edgesFromTree, edgesFromTreeSet, adjLi
    Pre: tree is a set of vertices in a minimum spanning tree.
         edgesFromTree is a heap of edges that point away from the tree
         (i.e. have only one vertice in the tree)
         edgesFromTreeSet is a set of edges who have at some  time
         pointed away from the tree.
         adjLi is an adjacency list of a graph, but only contains
         edges which are candidate minimum legal edges to add to a tree
         and have not been looked at before.
    Post:
         (w,u,v) is the minimum legal edge that can be added to a minimum spanning tree,
         and edgesFromTreeSet, edgesFromTree and adjLi have been updated accordingly
         such that they maintain the invariant in this functions precondition.
    
    """
    (w,u,v) = heappop(edgesFromTree)
    while (u in tree) == (v in tree): #Not XOR
        #I: (w,u,v) er minnsti hugsanlega loglegi
        #leggur hingad til.

        #Hendum theim sem eru ekki loglegir
        #Ur adj list
        adjLi[u].discard((w,u,v))
        adjLi[v].discard((w,u,v))

        (w,u,v) = heappop(edgesFromTree)

    #Hendum theim sem voru med bada hnuta i listanum
    adjLi[u].discard((w,u,v))
    adjLi[v].discard((w,u,v))
    
    for edge in adjLi[u]:
        if edge not in edgesFromTreeSet:
            edgesFromTreeSet.add(edge)
            heappush(edgesFromTree,edge)
    for edge in adjLi[v]:
        if edge not in edgesFromTreeSet:
            edgesFromTreeSet.add(edge)
            heappush(edgesFromTree,edge)

    return (w,u,v)
        

def Prim(numVertices,edges):
    """
    Use: totalW, tree, nonTree = Prim(numVertices,edges)
    Pre: numVertices is the number of vertices in a simple undirected connected graph,
         whose edges are in the iterator edges in the form (w,u,v),
         where w is the weight of an edge that connects the vertices
         u and v, where u < v.
    Post:  
         tree is a list of the edges from edges that form a minimum spanning tree,
         nonTree is a list of the edges from edges that are not in the tree,
         and totalW is the total weight of the edges of the edges in the tree.
    """
    adjLi = makeAdjLi(numVertices,edges)
    tree= set([0]) #A set of the vertices in the tree
    notInTree = numVertices -1 #The number of vertices not in the tree
    totalW = 0 #Total weight of the current minimum spanning tree
    treeEdges = [] #The edges in the tree
    edgesFromTree = [edge for edge in adjLi[0]] #A heap of the edges that have only
                                                #one vertice in the tree
    heapify(edgesFromTree)
    edgesFromTreeSet = set(edgesFromTree)       #A set of edges that have
                                                #been or are in edgesFromTree
    while(notInTree != 0):
        #I: The data invariant and there are notInTree number of vertices
        #Left to be added to the tree
        (w,u,v)= findLegalMin(tree,edgesFromTree,edgesFromTreeSet, adjLi)
        tree.add(u)
        tree.add(v)
        treeEdges.append((w,u,v))
        notInTree -= 1
        totalW += w
    nonTreeEdges = edgesFromTreeSet - set(treeEdges)
    return totalW,treeEdges,list(nonTreeEdges)
        


def connectComponents(component,adjLi):
    """
    Use: (w,u,v) = connectComponents(component,adjLi)
    Pre: component is a set that contains vertices from the adjacency list adjLi
    Post: (w,u,v) is the edge with the least weight that connects the component component
        to a vertice not in the component
    """
    mw,mu,mv  = float("inf"),0,0
    for t in component:
        for (w,u,v) in adjLi[t]:
            if (u in component) != (v in component):
                if w < mw:
                    mw,mu,mv = w,u,v
    return (mw,mu,mv) 
    
    
