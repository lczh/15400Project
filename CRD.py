import numpy as np
import networkx as nx
import sys
import os
import random
import math
import matplotlib.pyplot as plt

class adjlist:
    def __init__(self, G):
        n = G.number_of_nodes()
        self.graph = [[G.degree[i] // 2, None] for i in range(n)]
        for i in range(n):
            self.graph[i][1] = list(nx.edges(G, i))

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
        if active_list.empty(self):
            self.node_list.head = new_start
        else:
            new_start.next = self.node_list.head
            self.node_list.head.prev = new_start
            self.node_list.head = new_start
        self.label_list[0].head = new_start
        if self.label_list[0].tail == None:
            self.label_list[0].tail = new_start
        self.count += 1

    def remove(self):
        # Remove the first node from list
        label = self.node_list.head.label
        new_start = self.node_list.head.next
        if new_start == None:
            # Reach the end of list
            self.node_list.head = None
            self.label_list[label].head = None
            self.label_list[label].tail = None
            self.count -= 1
            return
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
            if next_entry.head == None:  # Empty entry
                next_entry.head = new_node
                next_entry.tail = new_node
                if orig_label + 1 < len(self.label_list) - 1:
                    next_next_entry = self.label_list[orig_label + 2]
                    new_node.next = next_next_entry.head
            else:
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
            while start != None:
                if start.label != i: break
                print("Node %s, label %d"%(start.node, start.label))
                start = start.next


def init_list(list_nodes):
    # It takes a list of nodes with nonzero mass, then init
    list_nodes = list(list_nodes)
    Q = active_list(list_nodes[0])
    for i in range(1, len(list_nodes)):
        Q.add(list_nodes[i])
    return Q

def compute_conductance(G, volG, S):
    # Compute conductance of cut S, G is the original graph, S is a collection
    # of nodes

    # Step 1: compute volume of S, compare with volume of G - S
    vol = 0
    cut_edges = 0
    for node in S:
        vol += G.graph[node][0]
        edges = G.graph[node][1]
        for edge in edges:
            _, u = edge
            if u not in S:
                cut_edges += 1
    vol = min(vol, volG - vol)
    return 1 if vol == 0 else cut_edges / vol

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
    mass = adjG.graph[start_node][0]
    G.nodes[start_node]["mass"] = mass 
    # Maintain a list of nodes with mass, initially it's just start node
    work_set = {start_node}
    mass_set = {start_node}
    C = 1 / cond

    def CRD_inner(mass):
        for node in work_set:
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
        height = math.floor(3 * math.log2(mass) / cond)
            
        def eligible(edge):
            v, u = edge
            flag1 = G.nodes[v]["height"] > G.nodes[u]["height"]
            flag2 = (G.edges[edge]["capacity"] - G.edges[edge]["flow"]) > 0
            flag3 = (G.nodes[v]["mass"] - adjG.graph[v][0]) > 0
            flag4 = (2 * adjG.graph[u][0] - G.nodes[u]["mass"]) > 0
            return flag1 and flag2 and flag3 and flag4

        def push_relabel(v):
            deg, edgelist = adjG.graph[v][0], adjG.graph[v][1]
            index = G.nodes[v]["current"]
            if index == deg:
                G.nodes[v]["height"] += 1
                G.nodes[v]["current"] = 0
                for edge in nx.edges(G, v):
                    G.edges[edge]["capacity"] = min(G.nodes[v]["height"], C)
                return 1
            edge = edgelist[index]
            _, u = edge
            if eligible(edge):
                push(edge)
                return 0
            elif index < deg:
                G.nodes[v]["current"] += 1
                return -1

        def push(edge):
            v, u = edge
            exv = G.nodes[v]["mass"] - adjG.graph[v][0]
            rm = G.edges[edge]["capacity"] - G.edges[edge]["flow"]
            exu = 2 * adjG.graph[u][0] - G.nodes[u]["mass"]
            amount = min(min(exv, rm), exu)
            G.edges[edge]["flow"] += amount
            G.edges[u, v]["flow"] -= amount
            G.nodes[v]["mass"] -= amount
            G.nodes[u]["mass"] += amount

        while not Q.empty():
            v = Q.get_first()
            rv = push_relabel(v)
            if rv == 0:  # Push
                currIdx = G.nodes[v]["current"]
                edgelist = adjG.graph[v][1]
                e = edgelist[currIdx]
                _, u = e
                mass_set.add(u)
                if G.nodes[v]["mass"] == adjG.graph[v][0]:
                    Q.remove()
                if G.nodes[u]["mass"] >= adjG.graph[u][0] and u not in work_set:
                    Q.add(u)
                    work_set.add(u)
            elif rv == 1:  # Relabel
                if G.nodes[v]["height"] <  height:  # Not reach max height yet
                    Q.shift(v, G.nodes[v]["height"] - 1)
                else:
                    Q.remove()

    cut1 = None
    for i in range(iters + 1):
        # Initialize parameters
        for node in mass_set:
            G.nodes[node]["mass"] *= 2  # Double amount of mass at start
        CRD_inner(2 * mass)
        mass = 0
        for node in mass_set:
            G.nodes[node]["mass"] = min(adjG.graph[node][0], G.nodes[node]["mass"])
            mass += G.nodes[node]["mass"]
        if mass <= threshold * (2**i * 2 * adjG.graph[start_node][0]):
            cut1 = work_set.copy()
            for node in mass_set:
                G.nodes[node]["mass"] *= 2  # Double amount of mass at start
            CRD_inner(2 * mass)
            break
    if cut1 == None:
        cut1 = work_set.copy()
    # Run an extra iteration, get the best level cut
    print("Iterations:%d"%i)
    S = set() 
    height = math.floor(3 * math.log2(2 * mass) / cond)
    volG = 0
    min_cond = sys.maxsize
    min_height = -1
    for node in G.nodes:
        volG += adjG.graph[node][0]
    work_set_cond = compute_conductance(adjG, volG, cut1)
    for i in range(1, height + 1):
        for node in work_set:
            if G.nodes[node]["height"] == i:
                S.add(node)
        conductance = compute_conductance(adjG, volG, S)
        if conductance <= min_cond:
            min_cond = conductance
            min_height = i
    cut2 = set() 
    for node in work_set:
        if G.nodes[node]["height"] <= min_height:
            cut2.add(node)
    return (cut1, cut2, work_set_cond, min_cond)

def tree_line_graph(n):
    # n**1/3 should be integer
    tree_nodes = int(np.cbrt(n))**2
    copies = n // tree_nodes

if __name__ == "__main__":
    G = nx.path_graph(20) 
    G = nx.convert_node_labels_to_integers(G)
    nx.draw(G)
    plt.show()
    cut1, cut2, cond1, cond2 = capacity_releasing_diffusion(G, 0, 0.5, 0.5, 20)
    H1 = G.subgraph(cut1)
    nx.draw(H1)
    plt.show()
    H2 = G.subgraph(cut2)
    nx.draw(H2)
    plt.show()
    print(cut1, cut2, cond1, cond2)
