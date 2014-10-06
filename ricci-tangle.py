#!/usr/bin/env sage

import time
from sage.all import *
load("tree-fun.py")
load("gricci/code.py")
load("gricci/nb-fun.py")
load("../tangle-fun.py")

for n in (int(a) for a in sys.argv[1:]):
    old_time = time.time()
    idx_fname = "tangles/tangle{}.idx".format(n)
    matrix_fname = "matrices/matrix_{}".format(n)
    print idx_fname
    assert(os.path.exists(idx_fname))
    assert(os.path.exists(matrix_fname))
    adj_graph = Graph(matrix_of_csv(matrix_fname))

    def process_line(line):
        row = list(int(x) for x in line)
        t1_idx = row[0]
        t2_idx = row[1]
        if t1_idx == t2_idx:
            row.append("-")
        else:
            row.append(ric_unif_rw(adj_graph, source=row[0], target=row[1]).ric)
        return row

    with open(idx_fname, 'rb') as csvfile:
        idx_reader = csv.reader(csvfile, delimiter='\t', quotechar="'")
        results = list(process_line(line) for line in idx_reader)
        results.sort(key=lambda r: r[3])
        with open("ricci"+str(n)+".mat", "w") as f_out:
            for r in results:
                f_out.write("\t".join(str(e) for e in r)+"\n")

    print "{}\t{}".format(n, time.time() - old_time)
