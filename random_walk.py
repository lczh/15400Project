import networkx as nx
import numpy as np
import scipy as sp
from treeCrossLine import gen_graph, gen_matrix
import sys

def take_step(transition_matrix, prob):
    return transition_matrix @ prob

if __name__ == "__main__":
    tree = int(sys.argv[1])
    path = int(sys.argv[2])
    G = gen_graph(tree, path)
    transition = gen_matrix(G)
    p = np.zeros(tree * path, dtype = int)
    p[0] = 1
    for i in range(100):
        p = take_step(transition, p)
    print(p)
