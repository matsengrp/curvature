#!/usr/bin/env sage

import argparse
import gzip
import os
from sage.all import load
load(os.path.dirname(os.path.realpath(__file__))+'/load-deps.py')
load(os.path.dirname(os.path.realpath(__file__))+'/tangle-counter.py')

parser = argparse.ArgumentParser(description='Find commute times per tangle',
                                 prog='tangle-time-count.py')

parser.add_argument('tracefiles', nargs='+')
parser.add_argument(
    '-n',
    help='Number of leaves',
    required=True)
parser.add_argument('-o', help='Out path', required=True)

args = parser.parse_args()

tc = TangleCounter(int(args.n))

with gzip.GzipFile(args.o, mode='wb', mtime=0.) as fout:
    for trace in args.tracefiles:
        print trace
        # Forget if we saw it in another trace file.
        last_seen = {to_newick(t): None for t in tc.trees}
        with gzip.open(trace, 'r') as fin:
            for l in fin:
                (idx, curr) = l.split()
                idx = int(idx)
                if 0 == idx % 100:
                    print str(idx)
                for (prev, when) in last_seen.items():
                    if when is not None:
                        # idx - last_seen[prev] is the number of steps
                        # between the last time we saw prev and the current
                        # index.
                        tc.add_newick_pair_observation(
                            prev, curr, idx - last_seen[prev])
                last_seen[curr] = idx
            for (t1_idx, t2_idx), l in tc.count_d.items():
                for (coset, counter) in l:
                    newicks = to_newick_pair(
                        tc.trees[t1_idx], tc.trees[t2_idx], coset)
                    for (time, count) in counter.items():
                        fout.write(
                            '\t'.join([newicks, str(time), str(count)])+'\n')
