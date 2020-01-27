import numpy as np
import networkx as nx
import sys
import os
import random

class linked_list_node:
    def __init__(self, node, label):
        self.node = node
        self.label = label
        self.next = None
        self.prev = None

class linked_list:
    def __init__(self):
        self.head = None

class active_list:
    def __init__(self, node):
        self.node_list = linked_list()
        start = linked_list_node(node, 0)
        self.node_list.head = start
        self.label_list = [start]
    def add(self, node):
        # Adding a node with label 0 to list
        new_start = linked_list_node(node, 0)
        new_start.next = self.node_list.head
        self.node_list.head.prev = new_start
        self.node_list.head = new_start.next
        label_ptr = self.label_list[0]
        self.label_list[0] = new_start
    def remove(self):
        # Remove the first node from list
        new_start = self.node_list.head.next
        new_start.prev = None
        if new_start.label == 0:
            # If the label is 0, then we can simply make it to be the new header
            # of label list
            self.label_list[0] = new_start
        else:
            # If it's nonzero, then the first entry of label list becomes None
            self.label_list[0] = None
    def shift(self, node, orig_label):
        # Shift the first node of a certain label
        ll_node = self.label_list[orig_label]
        # Change its position in linked list
        ll_node.prev.next = ll_node.next
        new_node = linked_list_node(node, orig_label + 1)
        if len(self.label_list) == orig_label:
            # Higher label has not yet existed
            # TO DO: add a tail pointer for each linked list
            # TO DO: correctly setup shift operation


def capacity_releasing_diffusion(G, start_node, cond, threshold, iters):
    # Initialize G and start_node
    nx.set_node_attributes(G, 0, "mass")
    nx.set_node_attributes(G, 0, "height")
    nx.set_edge_attributes(G, 0, "capacity")
    # Set mass of start node to its degree
    G.nodes[start_node]["mass"] = nx.degree(G.nodes[start_node])
    # Maintain a list of active nodes
    Q = linked_list()

    for i in range(iters):
        for node in active:
            G.nodes[node]["mass"] *= 2  # Double amount of mass at start

