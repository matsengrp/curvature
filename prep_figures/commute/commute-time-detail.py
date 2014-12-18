#!/usr/bin/env python

import argparse
import collections
import string

parser = argparse.ArgumentParser(description='Find commute times',
                                 prog='gen-tangles.py')

parser.add_argument('tracefiles', nargs='+')
parser.add_argument('--s1', action='store', help='The first state.', required=True)
parser.add_argument('--s2', action='store', help='The second state.', required=True)

args = parser.parse_args()
s1 = args.s1
s2 = args.s2

interesting = [s1, s2]


def posixify_newick(s):
    return s.translate(string.maketrans("(),;", "CD_ "))


for fname in args.tracefiles:
    last_seen = {s: 0 for s in interesting}
    transitions = {}
    for a in interesting:
        transitions[a] = {}
        for b in interesting:
            transitions[a][b] = collections.Counter()
    with open('-'.join([fname, posixify_newick(s1), posixify_newick(s2)])+'.tab', 'w') as fout:
        with open(fname, 'r') as fin:
            for l in fin:
                (_, idx, curr) = l.split()
                idx = int(idx)
                if curr in interesting:
                    for prev in interesting:
                        transitions[curr][prev][idx - last_seen[prev]] += 1
                    last_seen[curr] = idx
        for a in interesting:
            for b in interesting:
                for time, freq in transitions[a][b].items():
                    fout.write('\t'.join([a, b, str(time), str(freq)])+'\n')
