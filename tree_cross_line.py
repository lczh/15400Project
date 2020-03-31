import networkx as nx
import numpy as np
import scipy as sp
import sys

def gen_graph(tree_size, path_len):
    T = nx.full_rary_tree(2, tree_size)
    P = nx.path_graph(path_len)
    return nx.convert_node_labels_to_integers(nx.cartesian_product(T, P))

def gen_matrix(G):
    L = nx.laplacian_matrix(G).A
    A = nx.adjacency_matrix(G).A
    I = np.identity(A.shape[0])
    D = L + A
    return (A @ np.linalg.inv(D) + I) / 2

def gen_diag(G):
    L = nx.laplacian_matrix(G).A
    A = nx.adjacency_matrix(G).A
    D = L + A
    return np.diag(D)

