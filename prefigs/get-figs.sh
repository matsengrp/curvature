for i in ../analysis/6-walks-50K/rspr/upmh/scatter*svg ../analysis/7-walks-5K/rspr/upmh/scatter7.svg; do
    cp $i rspr-upmh-$(basename $i)
done
