fname=$1

s1=$(mktemp)
cut -f 3 $fname | nw_topology -IL - | nw_order -c n - > $s1
s2=$(mktemp)
cut -f 4 $fname | nw_topology -IL - | nw_order -c n - > $s2

paste $fname $s1 $s2 > annotated-rspr/$(basename $1)
