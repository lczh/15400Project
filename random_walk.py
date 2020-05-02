import networkx as nx
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from tree_cross_line import gen_graph, gen_matrix, gen_diag
import sys
from compute_sweep_cond import compute_cond

def take_step(transition_matrix, prob):
    return transition_matrix.dot(prob)

# Perform random walk for iters steps, find lowest conductance sweepcut
def find_cut(tree, path, iters, start, epsilon):
    G = gen_graph(tree, path)
    trans = gen_matrix(G)
    p = np.zeros(tree * path, dtype = float)
    p[start] = 1
    d = gen_diag(G)
    min_cond = 1
    min_set = None
    for i in range(iters):
        p = take_step(trans, p)
        normalized = list(np.divide(p, d))
        (cond, S) = compute_cond(G, normalized)
        if cond < min_cond: 
            min_cond = cond
            min_set = S
    return (min_cond, min_set)

def get_set(S, n, i):
    A = []
    base_val = i * n
    upper = base_val + n
    for elt in S:
        if elt >= base_val and elt < upper:
            A.append(elt - base_val)
    return A

def analyze(A, n):
    '''
    Input: a set of vertices in a tree, n indicates the max number of vertices
    in that tree
    '''
    levels = int(math.log2(n)) + 1
    output = [ [] for i in range(levels)]
    for num in A:
        level = int(math.log2(num + 1))
        output[level].append(num)
    return output


