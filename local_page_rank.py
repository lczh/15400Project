import networkx as nx
import numpy as np

# We adapt the Laplacian solver way to compute local pagerank
def LPR_compute(G, alpha, i):
    H = G.copy(as_view = False)
    H = nx.convert_node_labels_to_integers(H)
    n = len(list(H.nodes))
    # Add an extra ground node
    H.add_node(n)
    weights = []
    beta = alpha / (1 - alpha)
    for i in range(n):
        d = H.degree[i]
        weights.append((i, n, beta * d))
    H.add_weighted_edges_from(weights)
    L = nx.laplacian_matrix(H).A
    miu = np.zeros(n + 1)
    miu[i] = beta
    miu[-1] = -beta
    try:
        x = np.linalg.solve(L, miu)
    except np.linalg.LinAlgError:
        x = np.linalg.lstsq(L, miu)
    return x


