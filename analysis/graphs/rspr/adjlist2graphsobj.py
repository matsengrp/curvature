#!/usr/bin/env sage

from sage.all import *
load("../gricci/nb-fun.py")

for i in range(8, 9):
    print i
    with open(("adj_list_{}".format(i)), 'r') as f:
        def tuple_generator():
            for line in f:
                line.rstrip("\n")
                yield tuple(line.split(","))
        adj_graph = Graph(tuple_generator())
        sage.structure.sage_object.save(
            adj_graph,
            filename=("graph_{}.sobj".format(i)))
