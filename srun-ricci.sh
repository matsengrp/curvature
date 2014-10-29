#!/bin/sh
set -e
set -u

n_leaves=5
split_size=15
slurm_config="-c 4 -n 1 -w gizmof[1-180]"

out_path="results/ricci$n_leaves.mat"
files=$(split -l $split_size tangles/tangle$n_leaves.idx --filter="echo \$FILE")


for i in $files; do
    export SLURM_JOB_NAME=ricci-$i
    cmd="srun $slurm_config ./ricci-tangle.py --matrix matrices/matrix_$n_leaves --out $out_path-$i $i"
    echo $cmd
    $cmd
done


