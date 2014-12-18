#!/usr/bin/env python

import argparse
import collections
import re
import string

parser = argparse.ArgumentParser(description='Find commute times',
                                 prog='gen-tangles.py')

parser.add_argument('tracefiles', nargs='+')
parser.add_argument('--tp', help='A pair of trees of interest. String is trimmed between first open paren and last semicolon.', required=True)

args = parser.parse_args()
tp_str = args.tp
tp_str = re.sub('^[^(]*', '', tp_str)
tp_str = re.sub(';[^;]*$', '', tp_str)

# The states of interest to us.
interesting = [s.rstrip(';') for s in tp_str.split()]
(s1, s2) = interesting

print "Searching for: " + str(interesting)


def posixify_newick(s):
    return s.translate(string.maketrans("(),", "CD_"))


for fname in args.tracefiles:
    last_seen = {s: None for s in interesting}
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
