#!/usr/bin/env python3
from Parser import readGraphFile
from Prim import *
from multiprocessing import Pool, cpu_count
from random import shuffle
import sys

multi = True
debug = False

if len(sys.argv) > 1:
    with open(sys.argv[1],'r+b') as f:
        numVertices, edgesIter = readGraphFile(f)
else:
    numVertices, edgesIter = readGraphFile(sys.stdin)

edgesIter = edgesIter
totalW, MST,nonTreeEdges = Prim(numVertices,edgesIter)
out = []
MSTAdjLi = makeNonWAdjLi(MST,numVertices)
NonTreeEdgesAdjLi = makeAdjLi(numVertices,nonTreeEdges)


def minIfDropped(dwdudv):
    dw,du,dv = dwdudv[0],dwdudv[1],dwdudv[2]
    component = findSmallerComponent(du,dv,MSTAdjLi)
    nw,nu,nv = connectComponents(component,NonTreeEdgesAdjLi,dw)
    newW = totalW-dw + nw
    return (du,dv,newW)

if multi:
    # Shuffle array, so that the load is split
    # More evenly between the processes.
    shuffle(MST)
    with Pool(processes=cpu_count()) as pool:
        out = pool.map(minIfDropped,MST)
else:
    out = list(map(minIfDropped,MST))

out.sort()
lo = len(out)
if not debug:
    print(totalW)
    for i in range(lo):
        u,v,w = out[i]
        outstr = "%d %d %d" % out[i]
        print(outstr)
