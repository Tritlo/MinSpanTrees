#!/usr/bin/env python3
from Parser import readGraphFile
from Prim import *
from multiprocessing import Pool
import sys


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
    dw,du,dv = dwdudv[0],dwdudv[1],dwdudv[2] #Dropped 
    #component = findSmallerComponent(du,dv,MSTAdjLi.T)
    component = findSmallerComponent(du,dv,MSTAdjLi)
    nw,nu,nv = connectComponents(component,NonTreeEdgesAdjLi)
    newW = totalW-dw + nw
    return (du,dv,newW)

with Pool(processes=16) as pool:
    out = pool.map(minIfDropped,MST)

#out = list(map(minIfDropped,MST))

out.sort()
lo = len(out)
#printOut = False
#if printOut:
print(totalW)
for i in range(lo):
    u,v,w = out[i]
    outstr = "%d %d %d" % out[i]
    print(outstr)
