
rw_path=/shared/silo_researcher/Matsen_F/MatsenGrp/working/cwhidden/random_walks

for ntangle in 7 14 66 68 69; do
    sedcmd="sed -n ${ntangle}p ../../tangle/rooted-symmetric/tangle5.idx"
    ./commute-time-detail.py --tp "$($sedcmd)" $rw_path/5-taxa/123_45-1v5c/run1/uniq_trees_T -o runs/run1.${ntangle}.tab
done

#123_456-1v5c.tre
