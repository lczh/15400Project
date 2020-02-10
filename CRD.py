import numpy as np
import networkx as nx
import sys
import os
import random

class adjlist:
    def __init__(self, G):
        n = G.number_of_nodes(G)
        degrees = list(nx.degree(G))
        self.graph = [(degrees[i], None) for i in range(n)]
        for i in range(n):
            self.graph[i][1] = list(G.edges(i))

class linked_list_node:
    def __init__(self, node, label):
        self.node = node
        self.label = label
        self.next = None
        self.prev = None

class linked_list:
    def __init__(self, ll_node):
        self.head = ll_node
        self.tail = ll_node

class active_list:
    def __init__(self, node):
        start = linked_list_node(node, 0)
        self.node_list = linked_list(start)
        _list = linked_list(start)
        self.label_list = [_list]
        self.count = 1

    def get_first(self):
        return self.node_list.head.node

    def empty(self):
        return self.count == 0

    def add(self, node):
        # Adding a node with label 0 to list
        new_start = linked_list_node(node, 0)
        new_start.next = self.node_list.head
        self.node_list.head.prev = new_start
        self.node_list.head = new_start
        self.label_list[0].head = new_start
        self.count += 1

    def remove(self):
        # Remove the first node from list
        label = self.node_list.head.label
        new_start = self.node_list.head.next
        self.node_list.head = new_start
        new_start.prev = None
        if new_start.label == label:
            # New head and old head are in the same label entry
            self.label_list[label].head = new_start
        else:
            # Old head are the only node with its label, and we don't need to
            # modify the entry for new head
            self.label_list[label].head = None
            self.label_list[label].tail = None
        self.count -= 1

    def shift(self, node, orig_label):
        # Shift the first node of a certain label
        ll_list = self.label_list[orig_label]
        ll_node = ll_list.head
        # Change its position in linked list
        new_node = linked_list_node(node, orig_label + 1)
        # Deal with list head
        if self.node_list.head == ll_node:
            # Case 1: singleton
            if ll_list.tail == ll_node:
                self.node_list.head = new_node
                ll_list.head = None
                ll_list.tail = None
            # Case 2: non-singleton
            else:
                self.node_list.head = ll_node.next
                ll_list.head = ll_node.next
                ll_list.tail.next = new_node
                new_node.prev = ll_list.tail
        # General non-head case
        else:
            # Case 1: singleton
            if ll_list.tail == ll_node:
                new_node.prev = ll_node.prev
                new_node.prev.next = new_node
                ll_list.head = None
                ll_list.tail = None
            # Case 2: non-singleton
            else:
                ll_node.prev.next = ll_node.next
                ll_list.head = ll_node.next
                ll_list.tail.next = new_node
                new_node.prev = ll_list.tail
        # Shift to new entry
        if len(self.label_list) == orig_label + 1:
            # Label has not yet been recorded
            new_entry = linked_list(new_node)
            self.label_list.append(new_entry)
        else:
            next_entry = self.label_list[orig_label + 1]
            new_node.next = next_entry.head
            next_entry.head = new_node

    def print_list(self):
        print("Linked list contains nodes:")
        start = self.node_list.head
        while start:
            print("Node %s, label %d"%(start.node, start.label))
            start = start.next
        print("Linked list points to labels:")
        for i in range(len(self.label_list)):
            print("Current label %d"%i)
            start = self.label_list[i].head
            while start:
                print("Node %s, label %d"%(start.node, start.label))
                start = start.next


def init_list(list_nodes):
    # It takes a list of nodes with nonzero mass, then init
    Q = active_list(list_nodes[0])
    for i in range(1, len(list_nodes)):
        Q.add(list_nodes[i])
    return Q

def capacity_releasing_diffusion(G, start_node, cond, threshold, iters):
    # Initialize G and start_node
    G = G.to_directed()  # Turn it into a directed graph
    nx.set_node_attributes(G, 0, "mass")
    nx.set_node_attributes(G, 0, "height")
    nx.set_node_attributes(G, 0, "current")
    nx.set_edge_attributes(G, 0, "capacity")
    nx.set_edge_attributes(G, 0, "flow")
    adjG = adjlist(G)
    # Set mass of start node to its degree
    mass = G.degree[start_node] 
    G.nodes[start_node]["mass"] = mass 
    # Maintain a list of nodes with mass, initially it's just start node
    work_set = [start_node]
    for i in range(iters):
        # Initialize parameters
        for node in work_set:
            G.nodes[node]["mass"] *= 2  # Double amount of mass at start
            assert(G.nodes[node]["mass"] <= 2 * nx.degree(G.nodes[node]))
            G.nodes[node]["height"] = 0  # Set all labels to 0
            in_edges = G.in_edges(node)
            out_edges = G.out_edges(node)
            for edge in in_edges:
                G.edges[edge]["flow"] = 0
                G.edges[edge]["capacity"] = 0
            for edge in out_edges:
                G.edges[edge]["flow"] = 0
                G.edges[edge]["capacity"] = 0
        Q = init_list(work_set)  # Initialize data structure Q

        def eligible(edge):
            v, u, weights = edge
            flag1 = G.nodes[v]["height"] > G.nodes[u]["height"]
            flag2 = (weights["capacity"] - weights["flow"]) > 0
            flag3 = (G.nodes[v]["mass"] - G.degree[v]) > 0
            flag4 = (2 * G.degree[u] - G.nodes[u]["mass"]) > 0
            return flag1 and flag2 and flag3 and flag4

        def push_relabel(v):
            deg, edgelist = adjG[v]
            index = G.nodes[v]["current"]
            edge = edgelist[index]
            _, u, weights = edge
            if eligible(edge):
                push(edge)
                return 0
            else:
                if index < deg:
                    G.nodes[v]["current"] += 1
                    return -1
                else:  # index == deg, do Relabel
                    G.nodes[v]["height"] += 1
                    G.nodes[v]["current"] = 0
                    return 1

        def push(edge):
            v, u, weights = edge
            exv = G.nodes[v]["mass"] - G.degree[v]
            rm = weights["capacity"] - weights["flow"]
            exu = 2 * G.degree[u] - G.nodes[u]["mass"]
            amount = min(min(exv, rm), exu)
            G.edges[edge]["flow"] += amount
            G.edges[u, v]["flow"] -= amount
            G.nodes[v]["mass"] -= amount
            G.nodes[u]["mass"] += amount

        while not Q.empty():
            v = Q.get_first()
            rv = push_relabel(v)
            if rv == 0:  # Push
                if G.nodes[v]["mass"] == G.degree[v]:
                    Q.remove()
                if G.nodes[u]["mass"] >= G.degree[u]:
                    Q.add(u)
            else if rv == 1:
                




'''if __name__ == "__main__":
    L = [str(i) for i in range(10)]
    Q = active_list(L[0])
    for i in range(1, 3):
        Q.add(L[i])
    Q.print_list()
    for i in range(1, 3):
        Q.remove()
    Q.print_list()
    for i in range(4, 8):
        Q.add(L[i])
    for i in range(4, 8):
        Q.shift(L[7], i - 4)
        Q.print_list() '''
