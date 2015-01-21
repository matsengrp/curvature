#!/bin/sh
set -e
set -u

test -z $1 && exit 1

# walk=lazy_unif
walk=unif_prior_mh
mkdir -p results-rspr/$walk

n_leaves=$1
split_size=50
slurm_config="-c 4 -n 1"

# Prepare vars and split file.
out_path="results-rspr/$walk/ricci$n_leaves.mat"
splitargs="-a 4 -l $split_size tangle/rooted-symmetric/tangle$n_leaves.idx"
files=$(split $splitargs --filter="echo \$FILE")
# Apparently split doesn't actually split when given the --filter flag, so we run it again.
split $splitargs

# Run!
for i in $files
do
    export SLURM_JOB_NAME=ricci-$i
    cmd="./ricci-tangle.py --walk $walk --graph rspr/graph_$n_leaves.sobj --out $out_path-$i $i"
    echo $cmd
    echo "#!/bin/sh" > $i.sh
    echo $cmd >> $i.sh
    sbatch $slurm_config $i.sh
done

# Wait until done.
while test 0 -ne $(squeue -u matsen -h | wc -l)
do
    squeue -h -u matsen | wc -l
    sleep 5
done

rm results-rspr/$out_path
touch results-rspr/$out_path
for i in $files
do
    cat $out_path-$i >> results-rspr/$out_path
done
