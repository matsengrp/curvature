#!/usr/bin/env sage

import gzip
import sys
from sage.all import *

(in_fname, out_fname) = sys.argv[1:]

with gzip.open(in_fname, 'r') as f:
    def tuple_generator():
        for line in f:
            yield tuple(map(int, line.rstrip().split(',')))
    adj_graph = Graph(tuple_generator())
    sage.structure.sage_object.save(
        adj_graph,
        filename=out_fname)
