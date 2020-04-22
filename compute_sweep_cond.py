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
    for tup in indices:
        vertex = tup[0]
        A.add(vertex)
        B.remove(vertex)
        if len(B) == 0: break
        cond = nx.cuts.conductance(G, A, B)
        if cond < min_cond:
            min_cond = cond
            min_set = A.copy()
    return (min_cond, min_set)
