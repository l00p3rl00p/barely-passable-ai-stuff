"""Run native graph/vector operations on an existing Knowledge Positions graph.

Usage: python core_operations.py GRAPH.json [--start ID] [--target ID]
No graph modifications are persisted.
"""
import argparse
import json
from pathlib import Path
import networkx as nx
import numpy as np
from knowledge_positions import KnowledgePositions


def analyze(graph, start=None, target=None, threshold=0.25):
    active = [n for n, d in graph.nodes(data=True) if d.get('status', 'current') == 'current']
    g = graph.subgraph(active).copy()
    if not g:
        raise ValueError('No current nodes')
    start = start or next(iter(g))
    target = target or list(g)[-1]
    if start not in g or target not in g:
        raise ValueError('Start and target must be current nodes')
    label = lambda n: g.nodes[n].get('locator', {}).get('key', n)
    labels = lambda ns: [label(n) for n in ns]
    # Explicit undirected projection; unit cost is a demonstration, not confidence.
    u = nx.Graph(g)
    nx.set_edge_attributes(u, 1.0, 'cost')
    uf = nx.utils.UnionFind(g.nodes)
    for a, b in u.edges:
        uf.union(a, b)
    deps = nx.DiGraph()
    deps.add_nodes_from(g)
    deps.add_edges_from((b, a) for a, b, d in g.edges(data=True)
                        if d.get('relation', '').lower() in {'requires', 'depends_on', 'derived_from'})
    try:
        cycle = [[label(a), label(b)] for a, b, *_ in nx.find_cycle(g)]
    except nx.NetworkXNoCycle:
        cycle = []
    try:
        dependency_order = labels(nx.topological_sort(deps))
    except nx.NetworkXUnfeasible:
        dependency_order = None
    forest = nx.minimum_spanning_tree(u, weight='cost')
    model = g.nodes[start]['embedding_model']
    compatible = [n for n in g if g.nodes[n].get('embedding_model') == model
                  and g.nodes[n].get('vector') is not None
                  and g.nodes[n].get('vector_status') != 'unknown']
    X = np.asarray([g.nodes[n]['vector'] for n in compatible], dtype=float).reshape(len(compatible), -1) if compatible else np.empty((0, 0))
    if X.ndim != 2 or not np.isfinite(X).all():
        raise ValueError('Incompatible or nonfinite vectors')
    norms = np.linalg.norm(X, axis=1)
    X = X[norms > 0]
    compatible = [n for n, norm in zip(compatible, norms) if norm > 0]
    if len(X):
        X = X / np.linalg.norm(X, axis=1, keepdims=True)
    q = X[compatible.index(start)] if start in compatible else None
    scores = X @ q if q is not None else []
    ranks = sorted([(n, float(s)) for n, s in zip(compatible, scores) if n != start],
                   key=lambda v: (-v[1], v[0]))
    sim = nx.Graph()
    sim.add_nodes_from(compatible)
    for i, a in enumerate(compatible):
        for j in range(i+1, len(compatible)):
            score = float(X[i] @ X[j])
            if score >= threshold:
                sim.add_edge(a, compatible[j], similarity=score)
    centroid = X.mean(axis=0) if len(X) else None
    return {
        'projection': 'current nodes; directed navigation plus explicit undirected unit-cost and prerequisite-first dependency views',
        'nodes': len(g), 'edges': g.number_of_edges(), 'start': label(start), 'target': label(target),
        'dfs': labels(nx.dfs_preorder_nodes(g, start)),
        'bfs': labels(nx.bfs_tree(g, start)),
        'topological_dependency_order': dependency_order,
        'union_find_groups': [labels(s) for s in uf.to_sets()],
        'directed_cycle': cycle,
        'connected_components': [labels(s) for s in nx.connected_components(u)],
        'strong_components': [labels(s) for s in nx.strongly_connected_components(g)],
        'bipartite': nx.is_bipartite(u),
        'flood_fill': labels(nx.node_connected_component(u, start)),
        'minimum_spanning_forest': {'edges': [[label(a), label(b)] for a, b in forest.edges],
                                    'unit_cost': forest.size(weight='cost')},
        'shortest_path': labels(nx.shortest_path(u, start, target, weight='cost')) if nx.has_path(u, start, target) else None,
        'vector': {'model': model, 'start_vector_status': 'known' if q is not None else 'unknown_or_zero', 'dimensions': X.shape[1], 'compatible_nonzero_vectors': len(X),
                   'top_k_cosine': [{'node': label(n), 'cosine': s, 'cosine_distance': 1-s,
                                     'unit_euclidean': float(np.linalg.norm(q-X[compatible.index(n)]))}
                                    for n,s in ranks[:5]],
                   'centroid_norm': float(np.linalg.norm(centroid)) if centroid is not None else None, 'similarity_threshold': threshold,
                   'similarity_edges': sim.number_of_edges(),
                   'candidate_groups': [labels(s) for s in nx.connected_components(sim)]}
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('graph', type=Path)
    p.add_argument('--start')
    p.add_argument('--target')
    p.add_argument('--threshold', type=float, default=0.25)
    a = p.parse_args()
    if not -1 <= a.threshold <= 1:
        raise ValueError('Cosine threshold must be in [-1,1]')
    k = KnowledgePositions.load(a.graph)
    print(json.dumps(analyze(k.graph, a.start, a.target, a.threshold), indent=2))
