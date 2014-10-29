#!/usr/bin/env sage

from sage.all import *
load("../gricci/nb-fun.py")

for i in range(7,8):
    print i
    matrix_path = "matrix_{}".format(i)
    adj_graph = Graph(matrix_of_csv(matrix_path))
    sage.structure.sage_object.save(
        adj_graph,
        filename=(matrix_path+".sobj"))

