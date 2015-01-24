#!/usr/bin/env python
'''
Suggested use:
./commute-time-detail.py --tp \
    "$(sed -n 60p ../../tangle/rooted-symmetric/tangle5.idx)" <mcmc-trace-files>
'''

import argparse
import collections
import re

parser = argparse.ArgumentParser(description='Find commute times',
                                 prog='gen-tangles.py')

parser.add_argument('tracefiles', nargs='+')
parser.add_argument(
    '--tp',
    help='A pair of trees of interest. \
    String is trimmed between first open paren and last semicolon.',
    required=True)
parser.add_argument('-o', help='Out path', required=True)

args = parser.parse_args()
tp_str = args.tp
tp_str = re.sub('^[^(]*', '', tp_str)
tp_str = re.sub(';[^;]*$', '', tp_str)

# The states of interest to us.
interesting = [s.rstrip(';') for s in tp_str.split()]
(s1, s2) = interesting
print "Searching for: " + str(interesting)

transitions = {}
for a in interesting:
    transitions[a] = {}
    for b in interesting:
        transitions[a][b] = collections.Counter()

with open(args.o, 'w') as fout:
    for trace in args.tracefiles:
        print trace
        # Forget if we saw it in another trace file.
        last_seen = {s: None for s in interesting}
        with open(trace, 'r') as fin:
            for l in fin:
                (_, idx, _, curr) = l.split()
                idx = int(idx)
                if curr in interesting:
                    for prev in interesting:
                        if last_seen[prev] is not None:
                            # idx - last_seen[prev] is the number of steps
                            # between the last time we saw prev and the current
                            # index.
                            transitions[prev][curr][idx - last_seen[prev]] += 1
                    last_seen[curr] = idx
    print 'count\tfrom\tto'
    for a in interesting:
        for b in interesting:
            for time, freq in transitions[a][b].items():
                fout.write('\t'.join([a, b, str(time), str(freq)])+'\n')
            print "\t".join([str(sum(transitions[a][b].values())), a, b])
