set -eu

slurm_config="-c 4 -n 1"

for out in ~/tmp/*/*out; do
    echo "checking $out ..."
    grep succeeded $out || {
        name=$(echo $out | sed 's/.out//')
        sbatch $slurm_config -e ${name}.err -o ${name}.out ${name}.sh || {
            echo "$name submission failed"
            exit
        }
        sleep 1
    }
done
