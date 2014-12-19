
rw_path=/shared/silo_researcher/Matsen_F/MatsenGrp/working/cwhidden/random_walks

#for ntangle in 7 14 66 68 69; do
#    sedcmd="sed -n ${ntangle}p ../../tangle/rooted-symmetric/tangle5.idx"
#    ./access-time-count.py --tp "$($sedcmd)" $rw_path/5-taxa/123_45-equal/run[1-9]/uniq_trees_T -o 5-taxon-access-distn/equal/${ntangle}.tab
#    ./access-time-count.py --tp "$($sedcmd)" $rw_path/5-taxa/123_45-1v5c/run[1-9]/uniq_trees_T -o 5-taxon-access-distn/123_45-1v5c/${ntangle}.tab
#done

for ntangle in 662 665 795; do
    sedcmd="sed -n ${ntangle}p ../../tangle/rooted-symmetric/tangle6.idx"
    ./access-time-count.py --tp "$($sedcmd)" $rw_path/6-taxa/123_456-equal/run[1-9]/uniq_trees_T -o 6-taxon-access-distn/equal/${ntangle}.tab
    #./access-time-count.py --tp "$($sedcmd)" $rw_path/6-taxa/123_456-1v5c/run[1-9]/uniq_trees_T -o 6-taxon-access-distn/123_456-1v5c/${ntangle}.tab
done

