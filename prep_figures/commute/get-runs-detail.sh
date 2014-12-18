
#for ntangle in 7 14 66 68; do
for ntangle in 69; do
    sedcmd="sed -n ${ntangle}p ../../tangle/rooted-symmetric/tangle5.idx"
    ./commute-time-detail.py --tp "$($sedcmd)" ~/curvature-paths/123_45-1v5c/run1-uniq_trees_T-col -o run1.${ntangle}.tab
done
