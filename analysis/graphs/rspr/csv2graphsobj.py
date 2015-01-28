#!/usr/bin/env sage

from sage.all import *
load("../gricci/nb-fun.py")

for i in range(3,8):
    print i
    adj_graph = Graph(matrix_of_csv("matrix_{}".format(i)))
    sage.structure.sage_object.save(
        adj_graph,
        filename=("graph_{}.sobj".format(i)))

