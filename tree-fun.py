from sage.all import Graph, matrix
from itertools import combinations


def _enumerate_rooted_trees(n_leaves, start_internal):
    """
    Tree enumeration with internal nodes starting at some value.
    """
    assert(n_leaves > 0)
    if n_leaves == 1:
        g = Graph()
        g.add_vertices([0, 1])
        g.add_edge(0, 1)
        return [g]
    else:
        l = []
        for g in _enumerate_rooted_trees(n_leaves-1, start_internal+1):
            for (u, v, _) in g.edges():
                h = g.copy()
                h.delete_edge(u, v)
                new_leaf = h.add_vertex()
                # One more internal node, starting with start_internal.
                h.add_vertex(start_internal)
                h.add_edges([(u, start_internal),
                             (v, start_internal),
                             (new_leaf, start_internal)])
                l.append(h)
        return l


def enumerate_rooted_trees(n_leaves):
    """
    Construct all the rooted (with leaf 0), bifurcating, leaf-labeled
    phylogenetic trees.
    """
    return _enumerate_rooted_trees(n_leaves, n_leaves + 1)


def tree_reduce(t, f_internal, f_leaf):
    """
    Assume that t is rooted at 0 and recur down through the rest of the tree.
    """
    # Imagine arrow pointing from src to dst. That is where the subtree starts.
    def aux(src, dst):
        n = t.neighbors(dst)
        n.remove(src)
        if n == []:  # Leaf.
            return f_leaf(dst)
        else:  # Internal node.
            [left, right] = n
            return f_internal(aux(dst, left), aux(dst, right))
    [internal_root] = t.neighbors(0)
    return aux(0, internal_root)


def to_newick(t):
    return tree_reduce(t, lambda a, b: '('+a+','+b+')', str)+";"


def duplicate_zero_edge(t):
    """
    Return a tree that is the same as the input except with the edge to zero
    doubled up.
    """
    m = t.copy()
    m.allow_multiple_edges(True)
    [internal_root] = t.neighbors(0)
    m.add_edge(0, internal_root)
    return m


def rooted_is_isomorphic(t1, t2):
    """
    Are the two trees isomporphic if we give special status to the root?
    """
    return duplicate_zero_edge(t1).is_isomorphic(duplicate_zero_edge(t2),
                                                 certify=True)


def leaf_edges(t):
    """
    Find all the edges corresponding to leaves in t.
    Here the "edge to the root" will count as a leaf.
    """
    return [(u, v, l) for (u, v, l) in t.edges()
            if t.degree(u) == 1 or t.degree(v) == 1]


def multiedge_leaf_edges(t):
    """
    Make a tree such that graph isomorphism is equivalent to leaf-labeled
    (labeled by the leaf vertex numbers) isomorphism.
    """
    m = t.copy()
    m.allow_multiple_edges(True)
    for (u, v, _) in leaf_edges(m):
        for _ in range(min(u, v) + 1):
            m.add_edge(u, v)
    return m


def llt_is_isomorphic(t1, t2, certificate=False):
    """
    Return if trees are leaf-labeled (labeled by the leaf vertex numbers)
    isomorphic.
    """
    return multiedge_leaf_edges(t1).is_isomorphic(multiedge_leaf_edges(t2),
                                                  certificate)


def llt_isomorphism_matrix(l):
    n = len(l)
    return matrix(n, n, lambda i, j: int(llt_is_isomorphic(l[i], l[j])))


def classify_shapes(criterion, treel):
    """
    Given a criterion for isomporphism and a tree list, return an array such
    that the ith entry is the first appearance of that tree's equivalence class
    under the criterion.
    """
    found = []
    map_to_class = []
    certs = []
    for ti in range(len(treel)):
        # Begin search.
        for tj in found:
            (is_same, cert) = criterion(treel[ti], treel[tj])
            if is_same:
                map_to_class.append(tj)
                certs.append(cert)
                break  # We are done searching.
        else:  # Else statement for the for loop (!).
            found.append(ti)
            map_to_class.append(ti)  # Isomorphic to self
            certs.append(None)
    return (map_to_class, certs)


def pair_equivalence_graph(trees, classif, certs):
    """
    Which pairs are equivalent under leaf-labeled isomorphism?
    """
    # In this function we need the observation that the "certificate" returned
    # in g.is_isomorphic(h) maps from g's vertices to h's:
    # g = Graph(); g.add_vertices([0,1]); g.add_edge(0,1)
    # h = Graph(); h.add_vertices([3,4]); h.add_edge(3,4)
    # g.is_isomorphic(h, certify=True)
    # (True, {0: 3, 1: 4})
    pairs = combinations(range(len(trees)), 2)
    # Surprisingly, we have to define this iterator before we put the pairs
    # into the graph.
    pair_pairs = combinations(pairs, 2)
    g = Graph()
    g.add_vertices(pairs)
    for ((o1, o2), (n1, n2)) in pair_pairs:
        print [to_newick(trees[i]) for i in [o1, o2, n1, n2]]
        relabeled_t = trees[o2].relabel(certs[n1], inplace=False)
        if llt_is_isomorphic(relabeled_t, trees[n2]):
            # Relabeled tree is equivalent!
            # We also know that n1 is equivalent to o1 by definition of
            # classif, etc, so we know that the pair is equivalent by
            # certs[n1].
            g.add_edge((o1, o2), (n1, n2))
            print "EQUIV\n"
        print "not equiv\n"
    return g
