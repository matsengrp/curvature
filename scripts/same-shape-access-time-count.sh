set -eu

rw_path=/shared/silo_researcher/Matsen_F/MatsenGrp/working/cwhidden/random_walks

# type="*-equal"

# size=5
# type=123_45-1v5c

size=6
type=123_456-1v5c


for ntangle in $(awk '{if($8 == $9) print NR}' annotated-rspr/ricci${size}.mat); do
    sedcmd="sed -n ${ntangle}p ../../tangle/rooted-symmetric/tangle${size}.idx"
    outdir=${size}-taxon-access-distn/${type}
    mkdir -p $outdir
    ./access-time-count.py --tp "$($sedcmd)" \
        $rw_path/${size}-taxa/${type}/run[1-9]/uniq_trees_T \
        -o $outdir/${ntangle}.tab &

    while test $(ps -u matsen | grep python | wc -l) -gt 13; do
        sleep 5;
    done
done
