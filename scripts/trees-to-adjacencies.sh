set -eu

if [ $# -ne 3 ]
then
  echo 'usage: $0 graph_type tree_list out_name'
  exit 1
fi

binary=$(dirname $0)/"../spr_neighbors/spr_dense_graph"

graph_type=$1
tree_list=$2
out_name=$3

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

tmp=$(mktemp)

cat $tree_list | $binary $flag > $tmp
gzip $tmp
mv $tmp.gz $out_name
