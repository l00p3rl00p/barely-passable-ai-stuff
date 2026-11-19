"""Three positions, one identity. Original sources are never modified."""
import ast
import json
import hashlib
import math
from pathlib import Path
import networkx as nx

class KnowledgePositions:
    def __init__(self, model_name='all-MiniLM-L6-v2', encoder=None):
        self.graph = nx.MultiDiGraph()
        self.model_name = model_name
        self.encoder = encoder
        self._chat_cache = {}

    def _embed(self, text):
        if self.encoder is None:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer(self.model_name)
        return [float(x) for x in self.encoder.encode(text, normalize_embeddings=True)]

    def add(self, source, text, *, version, position, kind='text', node_id=None, defer_embedding=False, entity_type=None, cluster_id=None):
        """Store a source-backed span. Position uses 1-based lines, UTF-8 byte columns for Python."""
        if not text.strip() or not source or not version or not position:
            raise ValueError('source, version, position and nonempty text are required')
        identity = json.dumps([source, version, position, kind], sort_keys=True)
        node_id = node_id or hashlib.sha256(identity.encode()).hexdigest()
        if node_id in self.graph:
            existing = self.graph.nodes[node_id]
            if existing['source'] != source or existing['version'] != version or existing['position'] != position or existing['kind'] != kind or existing['content_hash'] != hashlib.sha256(text.encode()).hexdigest():
                raise ValueError('node identity collision')
            return node_id
        # Unknown is a positional state, not a numeric vector or similarity score.
        vector = None if defer_embedding else self._embed(text)
        self.graph.add_node(node_id, source=source, version=version, position=position,
                            kind=kind, content_hash=hashlib.sha256(text.encode()).hexdigest(),
                            entity_type=entity_type or kind, vector=vector,
                            vector_status='unknown' if vector is None else 'known',
                            embedding_model=self.model_name, status='current', status_history=[],
                            enrichment={}, enrichment_touches=1,
                            enrichment_touch_limit=3, enrichment_frozen=False,
                            enrichment_cluster=cluster_id)
        if cluster_id is not None:
            budgets = self.graph.graph.setdefault('enrichment_budgets', {})
            state = budgets.get(cluster_id)
            if state is None:
                budgets[cluster_id] = {'touches': 1, 'limit': 3, 'frozen': False,
                                       'source_versions': {source: version},
                                       'members': [node_id]}
            else:
                versions = state.setdefault('source_versions', {})
                # A verified new source version begins a new enrichment epoch.
                if source in versions and versions[source] != version:
                    state.update(touches=1, frozen=False)
                versions[source] = version
                members = state.setdefault('members', [])
                if node_id not in members:
                    members.append(node_id)
        self.invalidate_cache()
        return node_id

    # Reuse one location vocabulary across AST, DOM, structured documents and readers.
    # Native structure first; stable anchors second; source spans third.
    # A model-supplied clue is provisional regardless of how precise it sounds.
    LOCATION_METHODS = ('native_structure', 'stable_anchor', 'source_span',
                        'observed_locator')

    def register_location_method(self, name, *, source_kind, description, verification):
        """Persist a novel locator convention for other consumers of this graph.

        Only a descriptive, provisional method is registered here. Actual source
        verification is separate; never promote a novel convention by assertion.
        """
        import re
        if not isinstance(name, str) or not re.fullmatch(r'custom:[a-z][a-z0-9_-]{1,47}', name):
            raise ValueError('Novel method name must use custom:<short-slug>')
        if not all(isinstance(v, str) and 0 < len(v.strip()) <= 240
                   for v in (source_kind, description, verification)):
            raise ValueError('Provide brief, nonsecret source kind, method and verification rule')
        item = {'source_kind': source_kind.strip(), 'description': description.strip(),
                'verification': verification.strip(), 'status': 'provisional'}
        registry = self.graph.graph.setdefault('location_methods', {})
        if name in registry:
            if registry[name] != item:
                raise ValueError('Location convention conflict: use existing registry identity')
            return False
        registry[name] = item
        self.invalidate_cache()
        return True

    def location_method_catalog(self):
        """Shared canonical order plus any provisional, graph-stored novel methods."""
        return {'preferred': list(self.LOCATION_METHODS),
                'custom': dict(self.graph.graph.get('location_methods', {}))}

    def record_item_position(self, node_id, *, path=None, basis='observation',
                             precision='locator_only', sibling_index=None,
                             source_version=None, coordinates=None, method=None):
        """Maintain source-relative position, independently of identity and vectors.

        Readers/parsers supply verified structure or spans; agents can submit
        provisional observations through this SAME method. No LLM is needed to
        maintain coordinates, and no source content or embedding is modified.
        """
        if node_id not in self.graph:
            raise KeyError(node_id)
        if path is not None and (not isinstance(path, (list, tuple)) or not path
                                 or any(not isinstance(v, str) or not v.strip() for v in path)):
            raise ValueError('path, when supplied, must contain structural selectors')
        if coordinates is None:
            coordinates = {}
        if not isinstance(coordinates, dict) or any(
                not isinstance(k, str) or not k or not isinstance(v, (str, int, float, bool, type(None)))
                for k, v in coordinates.items()):
            raise ValueError('coordinates must be a flat map of ordinary scalar values')
        if path is None and not coordinates:
            raise ValueError('Supply an actual structural path or coordinate')
        if basis not in ('parser', 'reader', 'observation'):
            raise ValueError('basis must be parser, reader or observation')
        verified = basis in ('parser', 'reader') and precision == 'parsed'
        if precision not in ('parsed', 'locator_only') or (
                precision == 'parsed' and not verified):
            raise ValueError('Only a deterministic reader/parser may report parsed precision')
        if sibling_index is not None and (
                type(sibling_index) is not int or sibling_index < 0):
            raise ValueError('sibling_index must be a nonnegative integer')
        node = self.graph.nodes[node_id]
        if source_version is not None and source_version != node['version']:
            raise ValueError('Location belongs to a different source version')
        if method is None:
            if not verified:
                method = 'observed_locator'
            elif path is not None:
                method = 'native_structure'
            elif 'anchor' in coordinates or 'id' in coordinates:
                method = 'stable_anchor'
            else:
                method = 'source_span'
        if method not in self.LOCATION_METHODS:
            if method not in self.graph.graph.get('location_methods', {}):
                raise ValueError('Register any novel method before using it')
            if verified:
                raise ValueError('Novel methods remain provisional until a verified adapter exists')
        elif verified and method == 'observed_locator':
            raise ValueError('Verified reader must use a verified location method')
        elif not verified and method != 'observed_locator':
            raise ValueError('An observation cannot claim a verified method')
        # Existing precise locations cannot be erased by later model observations.
        old = node.get('item_location')
        if old and old.get('source_version') == node['version']:
            if old.get('precision') == 'parsed' and not verified:
                return False
            if verified and old.get('precision') == 'parsed':
                if (path is not None and old.get('method') == 'native_structure'
                        and old.get('path') is not None
                        and list(path) != old['path']):
                    raise ValueError('Conflicting verified structural path in same source version')
                for key, value in coordinates.items():
                    if key in old.get('coordinates', {}) and old['coordinates'][key] != value:
                        raise ValueError('Conflicting verified coordinate in same source version')
                coordinates = {**old.get('coordinates', {}), **coordinates}
                rank = {name: len(self.LOCATION_METHODS)-i
                        for i, name in enumerate(self.LOCATION_METHODS)}
                if rank.get(old.get('method'), 0) > rank.get(method, 0):
                    method = old['method']
                    basis = old['basis']
                    path = old.get('path')
                    sibling_index = old.get('sibling_index')
                elif path is None:
                    path = old.get('path')
                    sibling_index = old.get('sibling_index')
        loc = {'path': list(path) if path is not None else None,
               'parent_path': list(path[:-1]) if path is not None else None,
               'depth': len(path)-1 if path is not None else None,
               'sibling_index': sibling_index, 'coordinates': dict(coordinates),
               'source_version': node['version'], 'method': method,
               'basis': basis, 'precision': precision}
        if old == loc:
            return False
        node['item_location'] = loc
        self.invalidate_cache()
        return True

    def positioned_embedding_input(self, node_id, original_text):
        """Optional, source-hash-verified positional text; NO automatic re-embedding."""
        node = self.graph.nodes[node_id]
        if hashlib.sha256(original_text.encode('utf-8')).hexdigest() != node['content_hash']:
            raise ValueError('Original text does not match the recorded content hash')
        loc = node.get('item_location')
        if not loc:
            return original_text
        locator = (' > '.join(loc['path']) if loc.get('path')
                   else json.dumps(loc.get('coordinates', {}), sort_keys=True))
        return 'Position within source: ' + locator + '\nOriginal text:\n' + original_text

    def fill_vector(self, node_id, text):
        """Resolve a deferred vector without changing source identity or graph edges."""
        d = self.graph.nodes[node_id]
        if hashlib.sha256(text.encode()).hexdigest() != d['content_hash']:
            raise ValueError('Content does not match the recorded source span')
        if d.get('embedding_model') != self.model_name:
            raise ValueError('Embedding model mismatch')
        if d.get('vector') is None:
            d['vector'] = self._embed(text)
            d['vector_status'] = 'known'
            self.invalidate_cache()
        return d['vector']
    def enrichment_state(self, node_id, *, cluster_id=None):
        """Return the hard mutation budget for a node or explicit cluster."""
        if node_id not in self.graph:
            raise KeyError(node_id)
        node = self.graph.nodes[node_id]
        if cluster_id is None:
            return {'scope': 'node', 'id': node_id,
                    'touches': int(node.get('enrichment_touches', 1)),
                    'limit': int(node.get('enrichment_touch_limit', 3)),
                    'frozen': bool(node.get('enrichment_frozen', False))}
        state = self.graph.graph.get('enrichment_budgets', {}).get(cluster_id)
        if state is None:
            raise KeyError(cluster_id)
        return {'scope': 'cluster', 'id': cluster_id,
                'touches': int(state['touches']), 'limit': int(state['limit']),
                'frozen': bool(state['frozen'])}

    def enrich_node(self, node_id, updates, *, cluster_id=None, source_version=None):
        """Apply one semantic enrichment touch; the third touch freezes payload mutation.

        Initial admission is touch 1. Touches 2 and 3 may update the explicit
        enrichment payload. After touch 3, new knowledge must grow outward
        through relationships/new nodes rather than inflating this payload.
        Relationship writes remain legal because they do not mutate the frozen
        node payload. A new verified source version creates a new node identity
        and therefore a fresh node budget; cluster epochs reset only when add()
        observes a changed version for an existing cluster source.
        """
        if node_id not in self.graph:
            raise KeyError(node_id)
        if not isinstance(updates, dict) or not updates:
            raise ValueError('updates must be a nonempty mapping')
        node = self.graph.nodes[node_id]
        if node.get('status', 'current') != 'current':
            raise ValueError('Only current knowledge can be enriched')
        if source_version is not None and source_version != node.get('version'):
            raise ValueError('Enrichment belongs to a different source version')
        touches = int(node.get('enrichment_touches', 1))
        limit = int(node.get('enrichment_touch_limit', 3))
        if node.get('enrichment_frozen') or touches >= limit:
            raise ValueError('Enrichment mutation budget exhausted; add outward relationships/new knowledge instead')
        cluster_id = cluster_id if cluster_id is not None else node.get('enrichment_cluster')
        cluster = None
        if cluster_id is not None:
            budgets = self.graph.graph.setdefault('enrichment_budgets', {})
            cluster = budgets.get(cluster_id)
            if cluster is None:
                cluster = budgets[cluster_id] = {
                    'touches': 1, 'limit': 3, 'frozen': False,
                    'source_versions': {node['source']: node['version']},
                    'members': [node_id]}
            if cluster.get('frozen') or int(cluster.get('touches', 1)) >= int(cluster.get('limit', 3)):
                raise ValueError('Cluster enrichment mutation budget exhausted; link outward instead')
        payload = dict(node.get('enrichment', {}))
        payload.update(updates)
        node['enrichment'] = payload
        touches += 1
        node['enrichment_touches'] = touches
        node['enrichment_frozen'] = touches >= limit
        if cluster is not None:
            cluster['touches'] = int(cluster.get('touches', 1)) + 1
            cluster['frozen'] = cluster['touches'] >= int(cluster.get('limit', 3))
        self.invalidate_cache()
        return self.enrichment_state(node_id, cluster_id=cluster_id) if cluster_id is not None else self.enrichment_state(node_id)

    def link(self, source_id, target_id, relation, *, evidence=None, weight=None, cost=None, qualification=None):
        if source_id not in self.graph or target_id not in self.graph:
            raise KeyError('Both endpoints must already exist')
        attrs = {'relation': relation, 'evidence': evidence}
        if qualification is not None: attrs['qualification'] = qualification
        if cost is not None:
            cost = float(cost)
            if not math.isfinite(cost) or cost < 0: raise ValueError('Cost must be finite and nonnegative')
            attrs['cost'] = cost
        if weight is not None:
            attrs['weight'] = float(weight)
        key = hashlib.sha256(json.dumps([relation, evidence], sort_keys=True).encode()).hexdigest()
        self.graph.add_edge(source_id, target_id, key=key, **attrs)
        self.invalidate_cache()
        if relation.lower() in ('derived_from','depends_on','requires') and self.graph.nodes[target_id].get('status','current') != 'current':
            self.invalidate(source_id, 'dependency requires review')
        return key

    def ingest_python(self, path, *, defer_embedding=False):
        """Parse Python spans and structural paths; defer vectors for cheap indexing."""
        import tokenize
        p = Path(path).resolve()
        raw = p.read_bytes()
        import io
        encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
        text = raw.decode(encoding)
        version = hashlib.sha256(raw).hexdigest()
        tree = ast.parse(text, filename=str(p))
        ids = []
        def visit(node, parent=None, path=('Module',), sibling_index=None):
            current = parent
            if getattr(node, 'lineno', None) is not None and getattr(node, 'end_lineno', None) is not None:
                segment = ast.get_source_segment(text, node)
                if segment and segment.strip():
                    pos = {k: getattr(node,k) for k in ('lineno','end_lineno','col_offset','end_col_offset')}
                    pos['unit'] = 'python_utf8_columns'
                    current = self.add(str(p), segment, version=version, position=pos,
                                       kind=type(node).__name__, defer_embedding=defer_embedding)
                    # Structural path is metadata, not part of the node ID or its text hash.
                    self.record_item_position(current, path=path, basis='parser',
                                              precision='parsed', sibling_index=sibling_index,
                                              source_version=version)
                    ids.append(current)
                    if parent and parent != current:
                        self.link(parent, current, 'contains')
            # Reuse native AST fields to capture hierarchy and exact sibling order.
            for field, value in ast.iter_fields(node):
                if isinstance(value, list):
                    for index, child in enumerate(value):
                        if isinstance(child, ast.AST):
                            visit(child, current, path + (f'{field}[{index}]:{type(child).__name__}',), index)
                elif isinstance(value, ast.AST):
                    visit(value, current, path + (f'{field}:{type(value).__name__}',))
        visit(tree)
        return ids

    # Discoverable conveniences, not an exhaustive graph language. Agents can
    # calculate other structures via derive_graph or ordinary NetworkX calls.
    GRAPH_VIEWS = ('directed', 'undirected', 'weighted', 'multigraph', 'tree',
                   'forest', 'dag', 'bipartite', 'similarity', 'neighborhood')

    def graph_view(self, kind='directed', *, name=None, **options):
        """Named, native graph calculated from captured knowledge; never persisted."""
        view = self._graph_view(kind, **options)
        view.graph.update(name=name or kind, view_kind=kind,
                          relations=options.get('relations'), derived=True,
                          parameters=dict(options))
        return view

    def derive_graph(self, name, transform, *, source='multigraph', **options):
        """Apply an investigator-selected NetworkX transformation to a detached view."""
        if not name or not callable(transform):
            raise ValueError('A name and callable transform are required')
        result = transform(self.graph_view(source, **options))
        if not isinstance(result, nx.Graph):
            raise TypeError('Transformation must return a NetworkX graph')
        result.graph.update(name=name, view_kind='custom', source_view=source, derived=True,
                            parameters=dict(options))
        return result

    def _graph_view(self, kind='directed', *, relations=None, root=None,
                   include_historical=False, unit_cost=False, threshold=0.25,
                   model=None, partition=None, radius=1):
        """Native graph copies with source-edge references. No invented facts."""
        import math
        import numpy as np
        from copy import deepcopy
        # Work on detached copies so a derived graph cannot mutate source evidence.
        active = [n for n,d in self.graph.nodes(data=True)
                  if include_historical or d.get('status','current') == 'current']
        selected = set(active)
        allowed = None if relations is None else {r.lower() for r in relations}
        g = nx.MultiDiGraph()
        g.add_nodes_from((n,deepcopy(self.graph.nodes[n])) for n in active)
        for a,b,k,d in self.graph.edges(keys=True,data=True):
            if a in selected and b in selected and (allowed is None or d['relation'].lower() in allowed):
                g.add_edge(a,b,key=k,**deepcopy(d))
        if kind == 'multigraph':
            return g
        # Collapse parallel edges only in a derived view; keep original edge IDs.
        # Minimum explicit cost is the selected aggregation for weighted paths.
        def simple(directed=True, weighted=False):
            out = nx.DiGraph() if directed else nx.Graph()
            out.add_nodes_from(g.nodes(data=True))
            for a,b,k,d in g.edges(keys=True,data=True):
                cost = d.get('cost')
                if weighted:
                    if cost is None and unit_cost: cost = 1.0
                    if cost is None or not math.isfinite(cost) or cost < 0:
                        raise ValueError('Weighted view requires finite nonnegative edge costs or unit_cost=True')
                ref = (a,b,k)
                if out.has_edge(a,b):
                    out[a][b]['original_edges'].append(ref)
                    if weighted: out[a][b]['cost'] = min(out[a][b]['cost'],cost)
                else:
                    attrs = {'original_edges':[ref]}
                    if weighted: attrs['cost'] = cost
                    out.add_edge(a,b,**attrs)
            return out
        if kind == 'neighborhood':
            if root not in g or not isinstance(radius,int) or radius < 0: raise ValueError('Choose an existing root and nonnegative integer radius')
            return nx.ego_graph(simple(False), root, radius=radius)
        if kind == 'condensation': return nx.condensation(simple())
        if kind == 'directed': return simple()
        if kind == 'undirected': return simple(False)
        if kind == 'weighted': return simple(False,True)
        # A precedence DAG uses only explicit ordering/dependency relations.
        # A real dependency cycle is an error, not an edge to silently delete.
        if kind == 'dag':
            d = nx.DiGraph(); d.add_nodes_from(g.nodes(data=True))
            for a,b,k,e in g.edges(keys=True,data=True):
                r = e['relation'].lower()
                if r in ('requires','depends_on','derived_from'): a,b = b,a
                elif r != 'precedes': continue
                if not d.has_edge(a,b): d.add_edge(a,b,original_edges=[])
                d[a][b]['original_edges'].append((b,a,k) if r != 'precedes' else (a,b,k))
            if not nx.is_directed_acyclic_graph(d):
                raise nx.NetworkXUnfeasible('Precedence graph contains a cycle; inspect dependency evidence')
            return d
        # A rooted traversal tree and spanning forest are derived structures;
        # they do not assert that the source knowledge is a hierarchy.
        if kind in ('tree','forest'):
            u = simple(False)
            if kind == 'tree':
                if root not in u: raise ValueError('Choose an existing root')
                tree = nx.bfs_tree(u,root)
                nx.set_node_attributes(tree,{n:dict(u.nodes[n]) for n in tree})
                for a,b in tree.edges: tree[a][b].update(u[a][b])
                return tree
            return nx.minimum_spanning_tree(simple(False,True),weight='cost')
        if kind == 'bipartite':
            h = nx.Graph()
            if partition is not None:
                left,right = map(set,partition)
                if left & right or not (left|right) <= selected:
                    raise ValueError('Partitions must be disjoint known nodes')
                h.add_nodes_from((n,{**g.nodes[n],'bipartite':0}) for n in left)
                h.add_nodes_from((n,{**g.nodes[n],'bipartite':1}) for n in right)
                for a,b,k in g.edges(keys=True):
                    if (a in left and b in right) or (b in left and a in right):
                        if not h.has_edge(a,b): h.add_edge(a,b,original_edges=[])
                        h[a][b]['original_edges'].append((a,b,k))
                return h
            # Incidence partitions original references from actual edge records.
            # These temporary incidence nodes do not become new knowledge.
            h.add_nodes_from((n,{**g.nodes[n],'bipartite':0}) for n in g)
            for a,b,k,d in g.edges(keys=True,data=True):
                eid = ('edge',a,b,k)
                h.add_node(eid,bipartite=1,relation=d['relation'],original_edge=(a,b,k))
                h.add_edge(a,eid); h.add_edge(b,eid)
            return h
        if kind == 'similarity':
            if not -1 <= threshold <= 1: raise ValueError('Invalid cosine threshold')
            # Keep unknown/incompatible vectors as isolated nodes. Computed
            # similarity edges are candidates, never factual dependencies.
            h = nx.Graph(); model = model or self.model_name
            h.add_nodes_from(g.nodes(data=True)); vectors = {}
            for n,d in g.nodes(data=True):
                if d.get('embedding_model') != model or d.get('vector') is None or d.get('vector_status') == 'unknown': continue
                v = np.asarray(d['vector'],dtype=float)
                if v.ndim != 1 or not np.isfinite(v).all(): raise ValueError('Invalid vector')
                norm = np.linalg.norm(v)
                if norm: vectors[n] = v/norm
            ids = list(vectors)
            for i,a in enumerate(ids):
                for b in ids[i+1:]:
                    if vectors[a].shape != vectors[b].shape: raise ValueError('Incompatible vector dimensions')
                    s = float(np.clip(vectors[a] @ vectors[b],-1,1))
                    if s >= threshold: h.add_edge(a,b,similarity=s,cost=1-s,qualification='candidate')
            return h
        raise ValueError('Unknown graph view: '+kind)

    def core_algorithms(self, root, target, *, relations=None):
        """Run the ten core algorithms, naming each selected input view."""
        # The algorithms declare their input views; unit cost is explicit.
        d = self.graph_view('directed',relations=relations)
        u = self.graph_view('undirected',relations=relations)
        w = self.graph_view('weighted',relations=relations,unit_cost=True)
        if root not in d or target not in d: raise ValueError('Choose current nodes')
        uf = nx.utils.UnionFind(u.nodes)
        for a,b in u.edges: uf.union(a,b)
        try: cycle = nx.find_cycle(d)
        except nx.NetworkXNoCycle: cycle = []
        try: order = list(nx.topological_sort(self.graph_view('dag',relations=relations)))
        except nx.NetworkXUnfeasible: order = None
        forest = nx.minimum_spanning_tree(w,weight='cost')
        return dict(views={'dfs':'directed','bfs':'directed','topological_sort':'dag',
                           'union_find':'undirected','cycle':'directed',
                           'connected_components':'undirected','bipartite':'undirected',
                           'flood_fill':'undirected','minimum_spanning_forest':'weighted',
                           'shortest_path':'weighted'}, dfs=list(nx.dfs_preorder_nodes(d,root)),
                    bfs=list(nx.bfs_tree(d,root)),topological_sort=order,
                    union_find=[list(s) for s in uf.to_sets()],cycle=cycle,
                    connected_components=[list(s) for s in nx.connected_components(u)],
                    bipartite=nx.is_bipartite(u),flood_fill=list(nx.node_connected_component(u,root)),
                    minimum_spanning_forest=list(forest.edges(data=True)),
                    shortest_path=nx.shortest_path(w,root,target,weight='cost') if nx.has_path(w,root,target) else None)

    RETRIEVAL_PROFILES = {
        'conservative': {'alpha': 0.55, 'score_ratio': 0.20},
        'balanced': {'alpha': 0.75, 'score_ratio': 0.08},
        'aggressive': {'alpha': 0.90, 'score_ratio': 0.02},
    }

    def chat_context(self, root, *, relations=None, direction='both',
                     retrieval='ppr', profile='balanced', radius=None):
        """Return a graph-theoretically bounded working context.

        Default retrieval uses Personalized PageRank / random-walk-with-restart
        attenuation from root. Profile is the normal dial: conservative,
        balanced, or aggressive. No fixed hop depth is imposed. Callers may
        explicitly request retrieval='ego' with a nonnegative radius when an
        ego-graph radius is genuinely the desired algorithm. The other bucket
        retains one-edge boundary references without loading payloads.
        """
        from copy import deepcopy
        if direction not in ('both', 'out', 'in'):
            raise ValueError('direction must be both, out or in')
        if root not in self.graph or self.graph.nodes[root].get('status','current') != 'current':
            raise ValueError('Choose a current root')
        if retrieval not in ('ppr', 'ego'):
            raise ValueError('retrieval must be ppr or ego')
        if profile not in self.RETRIEVAL_PROFILES:
            raise ValueError('profile must be conservative, balanced or aggressive')
        if retrieval == 'ego' and (not isinstance(radius, int) or radius < 0):
            raise ValueError('ego retrieval requires a nonnegative integer radius')
        allowed = None if relations is None else frozenset(r.lower() for r in relations)
        key = (root, None if allowed is None else tuple(sorted(allowed)), direction,
               retrieval, profile, radius)
        if key in self._chat_cache:
            return deepcopy(self._chat_cache[key])

        def adjacent(n):
            edges = []
            if direction in ('both','out'):
                edges.extend((b,a,b,k,d) for a,b,k,d in self.graph.out_edges(n,keys=True,data=True))
            if direction in ('both','in'):
                edges.extend((a,a,b,k,d) for a,b,k,d in self.graph.in_edges(n,keys=True,data=True))
            return [(v,a,b,k,d) for v,a,b,k,d in edges
                    if self.graph.nodes[v].get('status','current') == 'current'
                    and (allowed is None or d['relation'].lower() in allowed)]

        current = [n for n,d in self.graph.nodes(data=True)
                   if d.get('status','current') == 'current']
        h = nx.Graph() if direction == 'both' else nx.DiGraph()
        h.add_nodes_from(current)
        for a,b,k,d in self.graph.edges(keys=True,data=True):
            if a not in h or b not in h or (allowed is not None and d['relation'].lower() not in allowed):
                continue
            if direction == 'both':
                h.add_edge(a,b)
            elif direction == 'out':
                h.add_edge(a,b)
            else:
                h.add_edge(b,a)

        scores = {root: 1.0}
        if retrieval == 'ego':
            selected = set(nx.ego_graph(h, root, radius=radius).nodes)
            policy = {'algorithm':'ego_graph', 'radius':radius, 'profile':profile}
        else:
            cfg = self.RETRIEVAL_PROFILES[profile]
            scores = nx.pagerank(h, alpha=cfg['alpha'],
                                 personalization={root: 1.0},
                                 dangling={root: 1.0})
            root_score = scores.get(root, 0.0)
            threshold = root_score * cfg['score_ratio']
            selected = {n for n,s in scores.items() if s >= threshold and s > 0}
            selected.add(root)
            policy = {'algorithm':'personalized_pagerank',
                      'profile':profile, 'alpha':cfg['alpha'],
                      'score_ratio':cfg['score_ratio'],
                      'absolute_threshold':threshold}

        sub = h.subgraph(selected)
        lengths = nx.single_source_shortest_path_length(sub, root) if root in sub else {root:0}
        levels = []
        for depth in range(max(lengths.values(), default=0)+1):
            levels.append(sorted(n for n,d in lengths.items() if d == depth))
        outside = {}
        for n in selected:
            for v,a,b,k,d in adjacent(n):
                if v not in selected:
                    outside.setdefault(v,set()).add((a,b,k))
        result = {'root':root, 'depth':max(lengths.values(), default=0),
                  'levels':levels, 'nodes':sorted(selected),
                  'edges':sorted({(a,b,k) for n in selected for v,a,b,k,d in adjacent(n)
                                  if v in selected}),
                  'retrieval':policy,
                  'scores':{n:scores[n] for n in sorted(selected) if n in scores},
                  'other':{'label':'other','boundary_refs':[
                      {'node_id':v,'edge_refs':sorted(refs)} for v,refs in sorted(outside.items())],
                      'count':len(outside), 'deeper_contents':'not loaded'}}
        if len(self._chat_cache) >= 32:
            self._chat_cache.clear()
        self._chat_cache[key] = deepcopy(result)
        return result
    def invalidate_cache(self):
        """Discard derived chat results. Original source evidence stays intact."""
        self._chat_cache.clear()

    def neighbors(self, node_id):
        return {'incoming': list(self.graph.in_edges(node_id, keys=True, data=True)),
                'outgoing': list(self.graph.out_edges(node_id, keys=True, data=True))}

    def _dependency_graph(self):
        """Dependent -> prerequisite. Similarity and containment never cascade."""
        g = nx.DiGraph()
        g.add_nodes_from(self.graph.nodes)
        g.add_edges_from((a,b) for a,b,d in self.graph.edges(data=True)
                         if d.get('relation', '').lower() in ('derived_from','depends_on','requires'))
        return g

    def _record_status(self, node_id, status, reason):
        d = self.graph.nodes[node_id]
        if d.get('status','current') == status:
            return
        d.setdefault('status_history', []).append({'status':status,'reason':reason})
        d['status'] = status
        self.invalidate_cache()

    def invalidate(self, node_id, reason, *, deprecate=False):
        """Mark explicit dependents stale, retaining all evidence and history."""
        if node_id not in self.graph or not reason:
            raise ValueError('Existing node and reason required')
        affected = sorted(nx.ancestors(self._dependency_graph(), node_id))
        if deprecate or self.graph.nodes[node_id].get('status') != 'deprecated':
            self._record_status(node_id, 'deprecated' if deprecate else 'stale', reason)
        for n in affected:
            if self.graph.nodes[n].get('status') != 'deprecated':
                self._record_status(n, 'stale', reason)
        return affected

    def mark_source_changed(self, source, new_version):
        """Caller supplies a verified new source version; no automatic file scan."""
        self.invalidate_cache()
        affected = set()
        for n,d in list(self.graph.nodes(data=True)):
            if d.get('source') == source:
                d['observed_source_version'] = new_version
                if d.get('version') != new_version:
                    affected.add(n)
                    affected.update(self.invalidate(n, 'source version changed'))
        return sorted(affected)

    def deprecate(self, node_id, reason, replacement_id=None):
        if replacement_id is not None:
            if replacement_id == node_id or replacement_id not in self.graph:
                raise ValueError('Replacement must be another existing node')
            if self.graph.nodes[replacement_id].get('status','current') != 'current':
                raise ValueError('Replacement must be current')
            self.link(node_id, replacement_id, 'superseded_by', evidence={'reason':reason})
        return self.invalidate(node_id, reason, deprecate=True)

    def revalidate(self, node_id, evidence):
        """Explicit review; cannot silently revive deprecated or dependent stale nodes."""
        d = self.graph.nodes[node_id]
        if not evidence or d.get('status') == 'deprecated':
            raise ValueError('Explicit evidence required; deprecated nodes stay historical')
        if d.get('observed_source_version', d['version']) != d['version']:
            raise ValueError('Source version no longer matches; ingest the new version')
        g = self._dependency_graph()
        if any(self.graph.nodes[n].get('status','current') != 'current'
               for n in nx.descendants(g,node_id)):
            raise ValueError('A prerequisite still requires review')
        self._record_status(node_id, 'current', evidence)

    def search(self, text, limit=5, *, include_historical=False):
        import numpy as np
        q = np.asarray(self._embed(text))
        scores = []
        for nid, data in self.graph.nodes(data=True):
            if not include_historical and data.get('status','current') != 'current':
                continue
            if data.get('vector') is None or data.get('vector_status') == 'unknown':
                continue
            if data['embedding_model'] != self.model_name:
                continue
            v = np.asarray(data['vector'])
            denom = np.linalg.norm(q)*np.linalg.norm(v)
            if denom:
                scores.append((nid, float(np.dot(q,v)/denom)))
        return sorted(scores, key=lambda x: (-x[1], x[0]))[:limit]

    def save(self, path):
        p = Path(path)
        payload = {'schema_version': 1, 'model': self.model_name,
                   'nodes': [{'id': n, **d} for n,d in self.graph.nodes(data=True)],
                   'edges': [{'source': a,'target': b,'key': k, **d} for a,b,k,d in self.graph.edges(keys=True,data=True)]}
        if self.graph.graph.get('location_methods'):
            payload['location_methods'] = self.graph.graph['location_methods']
        if self.graph.graph.get('enrichment_budgets'):
            payload['enrichment_budgets'] = self.graph.graph['enrichment_budgets']
        temp = p.with_name(p.name+'.tmp')
        temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
        temp.replace(p)

    @classmethod
    def load(cls, path, encoder=None):
        data = json.loads(Path(path).read_text(encoding='utf-8'))
        if data['schema_version'] != 1:
            raise ValueError('Unsupported schema version')
        obj = cls(data['model'], encoder)
        obj.graph.graph['location_methods'] = dict(data.get('location_methods', {}))
        obj.graph.graph['enrichment_budgets'] = dict(data.get('enrichment_budgets', {}))
        for node in data['nodes']:
            node = dict(node); nid = node.pop('id')
            node.setdefault('status','current')
            node.setdefault('status_history', [])
            node.setdefault('vector_status', 'unknown' if node.get('vector') is None else 'known')
            node.setdefault('entity_type',node.get('kind','text'))
            node.setdefault('enrichment', {})
            node.setdefault('enrichment_touches', 1)
            node.setdefault('enrichment_touch_limit', 3)
            node.setdefault('enrichment_frozen',
                            node['enrichment_touches'] >= node['enrichment_touch_limit'])
            node.setdefault('enrichment_cluster', None)
            obj.graph.add_node(nid, **node)
        for edge in data['edges']:
            edge = dict(edge); a=edge.pop('source'); b=edge.pop('target'); k=edge.pop('key')
            if a not in obj.graph or b not in obj.graph: raise ValueError('Dangling edge')
            obj.graph.add_edge(a,b,key=k,**edge)
        return obj
