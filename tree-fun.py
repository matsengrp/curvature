from sage.all import Graph, matrix
from sage.plot.graphics import GraphicsArray
from itertools import combinations


def plot_tree(t):
    return t.plot(layout='tree', tree_root=0, tree_orientation="down")


def plot_tree_list(l):
    return GraphicsArray([plot_tree(t) for t in l])


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


def indexed_tree_list(to):
    """
    Return a list of trees up to `to-1` such that the ith element in the list
    is a list of trees with i leaves.
    """
    return [[]] + [enumerate_rooted_trees(i) for i in range(1, to)]


def tree_reduce(t, f_internal, f_leaf):
    """
    Assume that t is rooted at 0 and recur down through the rest of the tree
    using the supplied functions.
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
        # leaf edge so that it gets distinguished from other leaf edges. Thus
        # edge 0 will be doubled, edge 1 will be tripled, etc.
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


def equivalence_classes(criterion, things):
    """
    Given a criterion for isomporphism (returning a boolean and a certificate)
    and a list of things, return an array such that the ith entry is the first
    appearance of the ith thing's equivalence class under the criterion, as
    well as the certificates that show the isomorphism.
    """
    found = []
    map_to_class = []
    certs = []
    identity = {i: i for i in range(things[0].order())}
    for test_i in range(len(things)):
        # Begin search.
        for found_i in found:
            (is_same, cert) = criterion(things[found_i], things[test_i])
            if is_same:
                map_to_class.append(found_i)  # This maps test_i to found_i.
                certs.append(cert)
                break  # We are done searching.
        else:  # Else statement for the for loop (!).
            found.append(test_i)
            map_to_class.append(test_i)  # Isomorphic to self, of course.
            certs.append(identity)
    return (map_to_class, certs)


def pair_equivalence_graph(trees, classif, certs):
    """
    Fix whether we are talking about rooted or unrooted (labeled) bifurcating
    phylogenetic trees. Let $T_n$ be the set of trees on $n$ taxa. Let $S_n =
    T_n \odot T_n$, the set of unordered pairs of $n$-taxon trees. The
    permutation group $\Sigma_n$ acts on $T_n$ and $S_n$ by permuting leaf
    labels. Let $\bar T_n$ and $\bar S_n$ be the resulting sets of equivalence
    classes.

    We would like to find representatives and sizes of each equivalence class
    in $S_n$. This represents all of the, say, SPR "problems": relabeling of
    both trees doesn't matter, and SPRs can easily be reversed to solve the
    "backwards" problem.
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

    def test_equivalence((a1, a2), (b1, b2)):
        if classif[a1] == classif[b1]:
            # a1 and b1 are in the same class. Furthermore, trees[a1] (resp.
            # trees[b1]) is obtained by applying certs[a1] (resp. certs[b1]) to
            # trees[classif[a1]].
            # That is, trees[a1] is obtained by applying certs[a1] o
            # certs[b1]^{-1} to trees[b1].
            certs_b1_inv = {v: k for k, v in certs[b1].items()}
            # Make trans, which first applies certs[b1]^{-1} then certs[a1]
            trans = {k: certs[a1][v] for k, v in certs_b1_inv.items()}
            # Make sure that trans changes trees[b1] to trees[a1] as it should.
            assert(llt_is_isomorphic(trees[a1],
                   trees[b1].relabel(trans, inplace=False)))
            trans_b2 = trees[b2].relabel(trans, inplace=False)
            if llt_is_isomorphic(trees[a2], trans_b2):
                return True
        return False

    # We have to try both flips of the indices because we are investigating the
    # symmetric product.
    for ((a1, a2), (b1, b2)) in pair_pairs:
        if (test_equivalence((a1, a2), (b1, b2)) or
           test_equivalence((a1, a2), (b2, b1))):
            g.add_edge((a1, a2), (b1, b2))

    return g


def rooted_pair_equivalence_graph(trees):
    (classif, certs) = equivalence_classes(rooted_is_isomorphic, trees)
    return pair_equivalence_graph(trees, classif, certs)


def favorite_node(g):
    """
    We favor the center of g that has maximum degree.
    """
    centers = g.center()
    center_degrees = [g.degree(c) for c in centers]
    return centers[center_degrees.index(max(center_degrees))]


def pair_representatives(trees, peg):
    """
    Get index of representative (favorite) nodes from each component of the
    supplied pair equivalence graph.
    """
    return [favorite_node(g) for g in peg.connected_components_subgraphs()]
