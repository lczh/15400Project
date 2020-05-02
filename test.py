import networkx as nx
import sys
import numpy as np
import random_walk
import local_page_rank
import compute_sweep_cond
import tree_cross_line

def get_tree(S, i):
    L = []
    for node in S:
        if node % 25 == i:
            L.append(node)
    return L

def print_tree_len(S):
    for i in range(25):
        print(len(get_tree(S, i)))

def get_level(T, i):
    if i == 0:
        lower = 0
        upper = 0
    else:
        lower = 2**i - 1
        upper = 2**(i + 1) - 2
    L = []
    for node in T:
        if node >= lower and node <= upper:
            L.append(node)
    return L
