
rw_path=/shared/silo_researcher/Matsen_F/MatsenGrp/working/cwhidden/random_walks

for ntangle in 7 14 66 68 69; do
    sedcmd="sed -n ${ntangle}p ../../tangle/rooted-symmetric/tangle5.idx"
    ./access-time-count.py --tp "$($sedcmd)" $rw_path/5-taxa/123_45-1v5c/run[1-9]/uniq_trees_T -o 5-taxon-access-distn/run1.${ntangle}.tab
done

#123_456-1v5c.tre
