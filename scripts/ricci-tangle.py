#!/usr/bin/env sage

import argparse
import csv
import os
import sys
from multiprocessing import Pool
from sage.all import load, RR
load(os.path.dirname(os.path.realpath(__file__))+'/load-deps.py')

parser = argparse.ArgumentParser(description='ricci curvature of tangles',
                                 prog='ricci-tangle.py')

parser.add_argument('idx_path',
                    type=str, help='Path to .idx file.')
parser.add_argument('--graph', dest='graph_path',
                    type=str, help='Path to graph in SAGE object format.')
parser.add_argument('--out', dest='out_path',
                    type=str, help='Output path.')
parser.add_argument('--walk', choices=['lurw', 'upmh'],
                    default='lurw', help='What random walk to use.')
args = parser.parse_args()
assert(os.path.exists(args.idx_path))
assert(os.path.exists(args.graph_path))
g = load(args.graph_path)


def process_line(line):
    row = list(line)
    t1_idx = int(row[0])
    t2_idx = int(row[1])
    if t1_idx == t2_idx:
        return [0, '-', 'nan']
    else:
        calc = ricci(args.walk, g, source=t1_idx, target=t2_idx)
        return [calc.dist, calc.ric, RR(calc.ric)]


def process_line_status(line):
    sys.stdout.write("*")
    sys.stdout.flush()
    return process_line(line)


p = Pool(processes=4)

with open(args.idx_path, 'rb') as csvfile:
    lines = list(csv.reader(csvfile, delimiter='\t', quotechar="'"))
    print "|"+"-"*(len(lines)-2)+"|\n"
    results = p.map(process_line_status, lines)
    print "\nsucceeded on {}\n".format(args.idx_path)
    with open(args.out_path, 'w') as f_out:
        for r in results:
            f_out.write("\t".join(str(e) for e in r)+"\n")
