#!/usr/bin/env sage

# Calculates degrees of graphs.

import sys
from sage.all import *

(in_graph_sobj_fname, out_degrees_fname) = sys.argv[1:]

g = load(in_graph_sobj_fname)

with open(out_degrees_fname, 'w') as out:
    for d in g.degree():
        out.write(str(d)+'\n')
