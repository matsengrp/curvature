rw_path=/shared/silo_researcher/Matsen_F/MatsenGrp/working/cwhidden/random_walks
size=5

for ntangle in $(awk '{if($8 == $9) print NR}' annotated-rspr/ricci${size}.mat); do
    sedcmd="sed -n ${ntangle}p ../../tangle/rooted-symmetric/tangle${size}.idx"
    ./access-time-count.py --tp "$($sedcmd)" $rw_path/${size}-taxa/*-equal/run[1-9]/uniq_trees_T -o ${size}-taxon-access-distn/equal/${ntangle}.tab
done
