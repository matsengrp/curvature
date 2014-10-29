#!/bin/sh
set -e
set -u

test -z $1 && exit 1

n_leaves=$1
split_size=20
slurm_config="-c 4 -n 1 -w gizmof[1-180]"
slurm_config="-c 8 -n 1"

# Prepare vars and split file.
out_path="ricci$n_leaves.mat"
splitargs="-l $split_size tangles/tangle$n_leaves.idx"
files=$(split $splitargs --filter="echo \$FILE")
# Apparently split doesn't actually split when given the --filter flag, so we run it again.
split $splitargs

# Run!
for i in $files
do
    export SLURM_JOB_NAME=ricci-$i
    cmd="./ricci-tangle.py --matrix matrices/matrix_$n_leaves --out $out_path-$i $i"
    echo $cmd
    echo "#!/bin/sh" > $i.sh
    echo $cmd >> $i.sh
    sbatch $slurm_config $i.sh
done

# Wait until done.
while test 0 -ne $(squeue -u matsen -h | wc -l)
do
    squeue -u matsen
    sleep 5
done

rm results/$out_path
touch results/$out_path
for i in $files
do
    cat $out_path-$i >> results/$out_path
done
