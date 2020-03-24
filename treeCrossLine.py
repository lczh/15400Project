import networkx as nx
import numpy as np
import scipy as sp
import sys

def gen_graph(tree_size, path_len):
    T = nx.full_rary_tree(2, tree_size)
    P = nx.path_graph(path_len)
    return nx.cartesian_product(T, P)

def gen_matrix(G):
    L = nx.laplacian_matrix(G).A
    A = nx.adjacency_matrix(G).A
    D = L + A
    return A @ np.linalg.inv(D)

if __name__=="__main__":
    tree_size = int(sys.argv[1])
    path_len = int(sys.argv[2])
    G = gen_graph(tree_size, path_len)
    print(gen_matrix(G))
