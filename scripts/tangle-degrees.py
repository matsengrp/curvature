#!/usr/bin/env sage

# Calculates degrees of tangles, resulting in a two-column tsv with the degree
# of t1 and the degree of t2 in the given graph.

import csv
import sys

(in_tangle_fname, in_graph_degrees_fname, out_tangle_degrees_fname) = sys.argv[1:]

with open(in_tangle_fname, 'r') as in_tangles, \
     open(in_graph_degrees_fname, 'r') as in_graph_degrees, \
     open(out_tangle_degrees_fname, 'w') as out_tangle_degrees:

    in_tangles = csv.reader(in_tangles, delimiter='\t')
    graph_degrees = [d.rstrip() for d in in_graph_degrees]

    for row in in_tangles:
        degs = map(lambda i: graph_degrees[i], [int(row[0]), int(row[1])])
        out_tangle_degrees.write('\t'.join(degs)+'\n')
