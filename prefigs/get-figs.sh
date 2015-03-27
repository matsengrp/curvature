for graph in nni rspr; do
    for i in ../analysis/6-walks-50K/$graph/upmh/scatter*svg; do
        cp $i $graph-upmh-$(basename $i)
    done
done
