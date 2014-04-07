#!/usr/bin/env python3
from Parser import readGraphFile
from Prim import *
from TreeAdjLi import TreeAdjLi
import sys


if len(sys.argv) > 1:
    with open(sys.argv[1],'r+b') as f:
        numVertices, edgesIter = readGraphFile(f)
else:
    numVertices, edgesIter = readGraphFile(sys.stdin)

edgesIter = edgesIter
totalW, MST,nonTreeEdges = Prim(numVertices,edgesIter)
print(totalW)
out = []
MSTAdjLi = TreeAdjLi(MST,numVertices)
NonTreeEdgesAdjLi = makeAdjLi(numVertices,nonTreeEdges)
ComponentsIfDropped = MSTAdjLi.findSmallerComponents(MST)
for i in range(len(MST)):
    dw,du,dv = MST[i] #Dropped 
    component = ComponentsIfDropped[i]
    nw,nu,nv = connectComponents(component,NonTreeEdgesAdjLi)
    newW = totalW-dw + nw
    out.append((du,dv, newW))

out.sort()
lo = len(out)
for i in range(lo):
    u,v,w = out[i]
    outstr = "%d %d %d" % out[i]
    print(outstr)
