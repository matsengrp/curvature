from sage.all import Graph, matrix, SymmetricGroup
from sage.plot.graphics import GraphicsArray


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


def n_leaves(t):
    """
    Note that this is the number of leaf edges, so the number of leaves of a
    rooted tree is this number minus 1.
    """
    return len(leaf_edges(t))


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


def equivalence_class_representatives(criterion, things):
    (map_to_class, _) = equivalence_classes(criterion, things)
    return list(things[i] for i in list(set(map_to_class)))


def leaf_autom_group(t):
    """
    The automorphism group of the leaf nodes of a tree rooted at 0, as a
    subgroup of the symmetric group.
    Like everything here, assumes that the first n nodes are leaves.
    # list((to_newick(t), leaf_autom_group(t)) for t in t_list)
    """
    n = n_leaves(t)-1
    G = SymmetricGroup(n)
    # Only take graph automorphisms that don't move 0.
    Gp = t.automorphism_group(partition=[[0], range(1, t.order())])
    return G.subgroup(
        filter(
            # Just take the movement of the leaves, not the internals.
            lambda tup: all(i <= n for i in tup),
            g.cycle_tuples()) for g in Gp.gens())
