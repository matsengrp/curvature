#!/usr/bin/env python

# Gather together all the results into a binary pickle.

import gzip
import pandas as pd
import pickle
import sys

(ricci_path, tangle_nwk_path, tangle_deg_path, out_pickle_gz_path) = \
    sys.argv[1:]

all_data = pd.concat([
    pd.read_table(path, names=col_names, header=None)
    for (path, col_names) in [
        (ricci_path, ['dist', 'kappa_Q', 'kappa_R']),
        (tangle_nwk_path, ['t1_nwk', 't2_nwk']),
        (tangle_deg_path, ['t1_deg', 't2_deg']),
        ]], axis=1)

all_data['avg_deg'] = (all_data['t1_deg'] + all_data['t2_deg'])/2

pickle.dump(all_data, gzip.open(out_pickle_gz_path, 'wb'))
