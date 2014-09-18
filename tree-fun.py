from sage.all import Graph, matrix
from itertools import combinations


def plot_tree(t):
    return t.plot(layout='tree', tree_root=0, tree_orientation="down")


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
    We assume that the tree was made by enumerate_rooted_trees, so that the
    leaf indices are all smaller than any internal node.
    """
    m = t.copy()
    m.allow_multiple_edges(True)
    for (u, v, _) in leaf_edges(m):
        # min(u, v) is the leaf number; we add the (leaf number + 1) edges to a
        # leaf edge so that it gets distinguished from other leaf edges.
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
    identity = {i: i for i in range(treel[0].order())}
    for test_i in range(len(treel)):
        # Begin search.
        for found_i in found:
            (is_same, cert) = criterion(treel[found_i], treel[test_i])
            if is_same:
                map_to_class.append(found_i)  # This maps test_i to found_i.
                certs.append(cert)
                break  # We are done searching.
        else:  # Else statement for the for loop (!).
            found.append(test_i)
            map_to_class.append(test_i)  # Isomorphic to self, of course.
            certs.append(identity)
    return (map_to_class, certs)


def compose_dicts(d1, d2):
    """
    First apply d2 then d1.
    """
    return {k: d1[v] for k, v in d2.items()}


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
    pairs = list(combinations(range(len(trees)), 2))
    # Surprisingly, we have to define this iterator before we put the pairs
    # into the graph.
    pair_pairs = combinations(pairs, 2)
    g = Graph()
    g.add_vertices(pairs)
    equivs = []

    def test_equivalence((a1, a2), (b1, b2)):
        if classif[a1] == classif[b1]:
            # a1 and b1 are in the same class. Furthermore, trees[a1] (resp.
            # trees[b1]) is obtained by applying cert[a1] (resp. cert[b1]) to
            # trees[classif[a1]].
            # That is, trees[a1] is obtained by applying cert[a1] o
            # cert[b1]^{-1} to trees[b1].
            certs_b1_inv = {v: k for k, v in certs[b1].items()}
            # trans = compose_dicts(certs[a1], certs_b1_inv)
            trans = {k: certs[a1][v] for k, v in certs_b1_inv.items()}
            assert(llt_is_isomorphic(trees[a1],
                   trees[b1].relabel(trans, inplace=False)))
            trans_b2 = trees[b2].relabel(trans, inplace=False)
            if llt_is_isomorphic(trees[a2], trans_b2):
                print to_newick(trees[a1])
                print to_newick(trees[b1])
                print to_newick(trees[a2])
                print to_newick(trees[b2])
                print trans.values()
                print trans.keys()
                print ""
                # It is! So the pair is isomorphic.
                return True
        return False

    for ((a1, a2), (b1, b2)) in pair_pairs:
        if (test_equivalence((a1, a2), (b1, b2)) or
           test_equivalence((a1, a2), (b2, b1))):
            g.add_edge((a1, a2), (b1, b2))

    return (g, equivs)
