#!/usr/bin/env sage

# Given a tangle .idx file and a file with as many lines as there are vertices
# in the graph (`in_graph_info_path`), gives a two-column tsv with the row
# corresponding to t1 and the row of corresponding to t2 in the given graph.

import csv
import sys

(in_tangle_path, in_graph_info_path, out_tangle_info_path) = sys.argv[1:]

with open(in_tangle_path, 'r') as in_tangles, \
     open(in_graph_info_path, 'r') as in_graph_info, \
     open(out_tangle_info_path, 'w') as out_tangle_info:

    in_tangles = csv.reader(in_tangles, delimiter='\t')
    graph_info = [d.rstrip() for d in in_graph_info]

    for row in in_tangles:
        infos = map(lambda i: graph_info[i], [int(row[0]), int(row[1])])
        out_tangle_info.write('\t'.join(infos)+'\n')
