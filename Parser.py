def readGraphFile(f):
    """
    Use: (numVertices, edges) = readGraphFile(f)
    Pre: f is a file whose first line is the number of vertices in a graph
        and the following lines is a list of the edges of the graph
        on the form 
        u v w
        where u and v are edges in the graph and w is the weight of that edge
    Post: numVertices is the number of vertices in the graph,
          edges is an iterator over the edges of the graph on the form
          (w,u,v)
    """
    nVs = int(f.readline())

    rearrange = lambda s: tuple([int(s[2]),int(s[0]),int(s[1])])
    lToTuple = lambda l: rearrange(l.split())
    
    #Python 3 gerir ekki iteratora ad listum
    # fyrr en eins seint og mogulegt er.
    return nVs, map(lToTuple,f.readlines())


if __name__=="__main__":
    nv,es = readGraphFile(sys.argv[1])
    print(next(vs))
