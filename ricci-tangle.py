#!/usr/bin/env sage

import time
from multiprocessing import Pool
from sys import stdout
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
        row = list(line)
        t1_idx = int(row[0])
        t2_idx = int(row[1])
        if t1_idx == t2_idx:
            row.extend([0, "-"])
        else:
            calc = ric_unif_rw(adj_graph, source=t1_idx, target=t2_idx)
            row.extend([calc.dist, calc.ric])
        return row

    def process_line_status(line):
        stdout.write("*")
        stdout.flush()
        return process_line(line)

    p = Pool(processes=8)

    with open(idx_fname, 'rb') as csvfile:
        lines = list(csv.reader(csvfile, delimiter='\t', quotechar="'"))
        print "There are {} tangles to process.".format(len(lines))
        print "|"+"-"*(len(lines)-2)+"|"
        results = p.map(process_line_status, lines)
        print ""
        with open("ricci"+str(n)+".mat", "w") as f_out:
            for r in results:
                f_out.write("\t".join(str(e) for e in r)+"\n")

    print "{}\t{}".format(n, time.time() - old_time)
