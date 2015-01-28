#!/bin/sh
set -e
set -u

test -z $1 && exit 1

# walk=lurw
walk=upmh
mkdir -p results-rspr/$walk

n_leaves=$1

idx_path="tangle/rooted-symmetric/tangle$n_leaves.idx"
out_path="results-rspr/$walk/ricci$n_leaves.mat"

./ricci-tangle.py --walk $walk --graph rspr/graph_$n_leaves.sobj --out $out_path $idx_path
