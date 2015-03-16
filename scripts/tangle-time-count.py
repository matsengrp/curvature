#!/usr/bin/env sage

import argparse
import gzip
import os
from sage.all import load, gap
wd = os.path.dirname(os.path.realpath(__file__))
load(wd+'/load-deps.py')
load(wd+'/tangle-counter.py')

parser = argparse.ArgumentParser(description='Find commute times per tangle',
                                 prog='tangle-time-count.py')

parser.add_argument('tracefiles', nargs='+')
parser.add_argument(
    '-n',
    help='Number of leaves',
    required=True)
parser.add_argument('--oaccess', help='Access out path', required=True)
parser.add_argument('--otangle', help='Tangle out path', required=True)
parser.add_argument('--asymmetric', action='store_true',
                    help='Generate tangles without exchange symmetry.')

args = parser.parse_args()

tc = TangleCounter(int(args.n), not args.asymmetric)

with gzip.GzipFile(args.oaccess, mode='wb', mtime=0.) as walk_out, \
    open(args.otangle, mode='w') as tangle_out:
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
            for (tangle_idx, (s1_idx, s2_idx)) in enumerate(tc.count_d.keys()):
                for (coset, counts) in tc.get_counts(s1_idx, s2_idx):
                    (t1n, t2n) = to_newick_pair(
                        tc.trees[s1_idx], tc.trees[s2_idx], coset).split()
                    t1_idx = tc.dn_trees[t1n]
                    t2_idx = tc.dn_trees[t2n]
                    for time, count in enumerate(counts):
                        walk_out.write(
                            '\t'.join(map(str, [tangle_idx, time, count]))+'\n')
                    # Note that this does not correspond to the tangle.idxs in
                    # the tangle repo. But that's fine here.
                    tangle_out.write("\t".join([str(o) for o in [
                        t1_idx, t2_idx,
                        t1n, t2n,
                        "".join(str(coset).split())  # Cosets with no whitespace.
                        ]])+"\n")
