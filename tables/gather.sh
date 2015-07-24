set -eu

tmp=$(mktemp)
tmp2=$(mktemp)

for c in delta1 mean-access; do
    csvcut -c1 ../analysis/5-walks-200K/rspr/$c*csv | sed 's#""#variable#' > $c.csv
    for w in ../analysis/5-walks-200K ../analysis/6-walks-50K ../analysis/7-walks-5K; do
        ntaxa=$(echo $w | sed -e "s/-.*//" -e "s#.*/##")
        csvcut -c3 $w/rspr/$c*csv | sed "s/p-value/$ntaxa taxa/" > $tmp
        paste -d, $c.csv $tmp > $tmp2
        cp $tmp2 $c.csv
    done
done

