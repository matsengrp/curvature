#!/bin/sh

if [ $# -ne 2 ]
then
  echo "usage: $0 walk n_leaves"
  exit
fi

walk=$1
n_leaves=$2

if [ $walk != "lurw" ] && [ $walk != "upmh" ]
then
  echo '`walk` must be either "lurw" or "upmh"'
  exit
fi

mkdir -p results-rspr/$walk


idx_path="tangle/rooted-symmetric/tangle$n_leaves.idx"
out_path="results-rspr/$walk/ricci$n_leaves.mat"

./ricci-tangle.py --walk $walk --graph rspr/graph_$n_leaves.sobj --out $out_path $idx_path
