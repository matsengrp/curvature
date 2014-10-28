#!/usr/bin/env sage

import argparse
import math
import time
import sys
from multiprocessing import Pool
from sage.all import *
load("tree-fun.py")
load("gricci/code.py")
load("gricci/nb-fun.py")
load("../tangle-fun.py")


parser = argparse.ArgumentParser(description='ricci curvature of tangles',
                                 prog='ricci-tangle.py')

parser.add_argument('--size', dest='n',
                    type=int, help='Number of leaves.')
parser.add_argument('--n-batches', dest='n_batches',
                    type=int, help='Number of batches.')
parser.add_argument('--batch', dest='batch', default=None,
                    type=int, help='Which batch, zero indexed.')

arguments = parser.parse_args()
n = arguments.n
n_batches = arguments.n_batches
batch = arguments.batch

assert(n is not None)
assert(n_batches is not None)
assert(batch is not None)

idx_fname = "tangles/tangle{}.idx".format(n)
matrix_fname = "matrices/matrix_{}".format(n)
assert(os.path.exists(idx_fname))
assert(os.path.exists(matrix_fname))
adj_graph = Graph(matrix_of_csv(matrix_fname))
assert(batch >= 0)
assert(batch < n_batches)


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
    sys.stdout.write("*")
    sys.stdout.flush()
    return process_line(line)


def chunks(l, n_chunks):
    """ Yield successive n-sized chunks from l.
    http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
    """
    for i in xrange(0, len(l), n_chunks):
        yield l[i:i+n_chunks]


p = Pool(processes=8)

with open(idx_fname, 'rb') as csvfile:
    lines = list(csv.reader(csvfile, delimiter='\t', quotechar="'"))
    batch_size = int(len(lines) / n_batches)+1
    batch_start = range(0, len(lines), batch_size)[batch]
    batch_end_plus_one = min((batch+1)*batch_size, len(lines))
    print "Processing {} to {}.".format(batch_start, batch_end_plus_one)
    lines = lines[batch_start:batch_end_plus_one]
    print "|"+"-"*(len(lines)-2)+"|"
    results = p.map(process_line_status, lines)
    print ""
    out_fname = "ricci{}.{}-of-{}.mat".format(n, batch, n_batches)
    with open(out_fname, "w") as f_out:
        for r in results:
            f_out.write("\t".join(str(e) for e in r)+"\n")
