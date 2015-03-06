def trees_shapes_autos_dn_ttsn(n):
    trees = enumerate_rooted_trees(n)
    # So that we can recognize trees after acting on t2 by mu^{-1}.
    # `dn` is short for a dictionary keyed on Newick strings.
    dn_trees = {to_newick(trees[i]): i for i in range(len(trees))}
    shapes = []
    # Using Newick representation of shape is much faster than
    # searching for isomorphic trees.
    dn_shapes = OrderedDict()
    tree_to_shape_num = {}
    for i in range(len(trees)):
        newick_shape_i = to_newick_shape(trees[i])
        if newick_shape_i in dn_shapes:
            dn_shapes[newick_shape_i] = dn_shapes[newick_shape_i] + [i]
        else:
            shapes.append(trees[i])
            dn_shapes[newick_shape_i] = [i]
        tree_to_shape_num[i] = dn_shapes.keys().index(newick_shape_i)
    shape_autos = [leaf_autom_group(s) for s in shapes]
    return (trees, shapes, shape_autos, dn_trees, tree_to_shape_num)


def newick_factorization_dict(n):
    trees = enumerate_rooted_trees(n)
    fS = sg.SymmetricGroup(n)
    dn_trees = {to_newick(trees[i]): i for i in range(len(trees))}
    factorization_d = OrderedDict()
    shapes = []
    dn_shapes = OrderedDict()
    for i in range(len(trees)):
        newick_shape_i = to_newick_shape(trees[i])
        if newick_shape_i in dn_shapes:
            dn_shapes[newick_shape_i] = dn_shapes[newick_shape_i] + [i]
            # This is the _tree_ index of the shape.
            idx_tree = dn_shapes[newick_shape_i][0]
            (check, cert) = rooted_is_isomorphic(trees[idx_tree], trees[i])
            assert(check)
            # cert is a dictionary mapping all nodes to each other.
            # Recall that 0 is the root node, and nodes > n are internal nodes.
            isom = fS(Permutation(cert.values()[1:n+1]))
        else:
            shapes.append(trees[i])
            dn_shapes[newick_shape_i] = [i]
            idx_tree = i
            isom = fS.identity()
        tree_to_shape = {}
        factorization_d[to_newick(trees[i])] = (idx_tree, isom)
    return factorization_d


class TangleCounter:
    def __init__(self, n):
        self.nfd = newick_factorization_dict(n)
        (_, _, self.shape_autos, _, self.ttsn) = trees_shapes_autos_dn_ttsn(n)

    # Define an "ntangle" to be a triple of (idx_tree1, idx_tree2, coset)
    # WRT the `sigma_1 * inverse(sigma_2)` term below,
    # recall that the element in the middle of the double coset gets applied to the first tree to get the right tangle.
    # sigma_1 maps us from leaves of first tree to "middle" leaves, and sigma_2 maps us from "middle" leaves to leaves of second tree.
    # Thus sigma_1 * inverse(sigma_2) gives us the map to apply to the first tree to get correct tangle when also using identity map for second tree.
    def newick_pair_to_ntangle(self, n1, n2):
        (idx_tree1, sigma_1) = self.nfd[n1]
        (idx_tree2, sigma_2) = self.nfd[n2]
        if idx_tree1 > idx_tree2:
            # Tangles start with lowest shape index, so flip.
            tmp = (idx_tree1, sigma_1)
            (idx_tree1, sigma_1) = (idx_tree2, sigma_2)
            (idx_tree2, sigma_2) = tmp
        coset = double_coset(
            self.shape_autos[self.ttsn[idx_tree1]],
            sigma_1 * inverse(sigma_2),
            self.shape_autos[self.ttsn[idx_tree2]])
        return (idx_tree1, idx_tree2, coset)


