from sage.all import Graph


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
