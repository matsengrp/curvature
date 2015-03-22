set -eu

rw_path=/shared/silo_researcher/Matsen_F/MatsenGrp/working/cwhidden/random_walks

# size=5
# type=123_45-equal

size=6
type=123_456-equal
# type=123_456-1v5c


tangle_file=../../tangle/rooted-symmetric/tangle${size}.idx

for ntangle in $(seq $(wc -l $tangle_file | cut -f 1 -d' ')); do # loop over all tangles (yes, self-defeating)
    sedcmd="sed -n ${ntangle}p $tangle_file"
    outdir=${size}-taxon-access-distn/${type}
    mkdir -p $outdir
    ./access-time-count.py --tp "$($sedcmd)" \
        $rw_path/${size}-taxa/${type}/run[1-9]/uniq_trees_T \
        -o $outdir/${ntangle}.tab &

    while test $(ps -u matsen | grep python | wc -l) -gt 12; do
        sleep 5;
    done
done


