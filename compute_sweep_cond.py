import networkx as nx
import math
import numpy as np
import sys

# Should input a normalized vector by its degree
def compute_cond(G, normalized):
    indices = list(enumerate(normalized))
    indices = sorted(indices, key = lambda x : x[1], reverse = True)
    B = set(list(G.nodes))
    A = set()
    min_cond = sys.maxsize
    min_set = None
    volA = 0
    volB = nx.volume(G, G)
    cross = 0
    prev = None
    for tup in indices:
        vertex = tup[0]
        val = tup[1]
        if prev == None:
            prev = val
        else:
            if prev == val:
                A.add(vertex)
                B.remove(vertex)
                if len(B) == 0: break
                d = nx.degree(G, vertex)
                volA += d
                volB -= d
                vol = min(volA, volB)
                for u in G.neighbors(vertex):
                    if u in A:
                        cross -= 1
                    else:
                        cross += 1
            else:
                A.add(vertex)
                B.remove(vertex)
                if len(B) == 0: break
                d = nx.degree(G, vertex)
                volA += d
                volB -= d
                vol = min(volA, volB)
                for u in G.neighbors(vertex):
                    if u in A:
                        cross -= 1
                    else:
                        cross += 1
                cond = cross / vol
                if cond < min_cond:
                    min_cond = cond
                    min_set = A.copy()
            prev = val
    return (min_cond, min_set)
