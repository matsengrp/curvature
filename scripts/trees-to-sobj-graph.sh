set -eu

if [ $# -ne 2 ]
then
  echo 'usage: $0 graph_type tree_list'
  exit 1
fi

binary=$(dirname $0)/"../spr_neighbors/spr_dense_graph"

graph_type=$1
tree_list=$2
out_name=$(basename $tree_list .tre)-$graph_type.csv

case $graph_type in
    rspr)
        flag=""
        ;;
    nni)
        flag="--nni"
        ;;
    *)
        echo "$graph_type not known!"
        exit 1
        ;;
esac

cat $tree_list | $binary $flag > $out_name
gzip $out_name
