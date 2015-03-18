#!/usr/bin/env python

import argparse
import gzip
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import pickle
import seaborn as sns

sns.set_style('ticks')
mpl.rcParams.update({
    'font.size': 32, 'font.family': 'Lato',
    'font.weight': 600, 'axes.labelweight': 600})

parser = argparse.ArgumentParser(
    description='plot curvature results',
    prog='plot.py')

parser.add_argument('access', type=str, help='Access times, gzipped.')
parser.add_argument('tangles', type=str, help='Tanglegram idx file.')
parser.add_argument('degrees', type=str, help='Degrees file.')
parser.add_argument('curvatures', type=str, help='Tangle curvatures.')
parser.add_argument('--prefix', required=True,
                    type=str, help='Prefix of plot paths for saving.')

args = parser.parse_args()
for p in [args.access, args.tangles, args.degrees, args.curvatures]:
    assert(os.path.exists(p))

access = pd.read_table(gzip.open(args.access),
                        names=['tangle', 'time', 'count'], header=False)
tangle = pd.read_table(args.tangles,
                       names=['t1_idx', 't2_idx', 't1_nwk', 't2_nwk', 'coset'])
degrees = pd.read_table(args.degrees,
                       names=['t1_deg', 't2_deg'])
curvatures = pd.read_table(args.curvatures,
                       names=['dist', 'kappa_str', 'kappa'])

catted = pd.concat([tangle, degrees, curvatures], axis=1)
catted['mean_access'] = \
    pd.Series(sum(adf['time']*adf['count']) / sum(adf['count'])
              for (tangle_num, adf) in access.groupby('tangle'))
catted['tangle'] = catted.index

t1_degs = catted['t1_deg'].unique()
t2_degs = catted['t2_deg'].unique()

def subplots():
    return plt.subplots(
        len(t1_degs), len(t2_degs),
        sharex=True,
        sharey=True,
        figsize=(4*len(t1_degs), 4*len(t1_degs)),
        squeeze=False)  # Always return an array of axs, even if 1x1.
e_fig, e_axs = subplots()
d_fig, d_axs = subplots()

for (t1_deg, t2_deg, dist), group in catted.groupby(['t1_deg','t2_deg', 'dist']):
    i = np.where(t1_degs == t1_deg)[0][0]
    j = np.where(t2_degs == t2_deg)[0][0]
    p = group['mean_access'].plot(
        ax=e_axs[i][j], kind='hist', stacked=True, bins=25)
    p.grid(b=None)

    norm = mpl.colors.Normalize(group['kappa'].min(), group['kappa'].max())
    m = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.winter)

    for (idx, _) in group.iterrows():
        kappa = group['kappa'][idx]
        sub_d = access[access['tangle'] == idx]
        d_axs[i][j].plot(sub_d['time'], sub_d['count'], color=m.cmap(kappa), label=kappa)
        d_axs[i][j].legend()

sns.despine()
# sns.despine(offset=10, trim=True)

e_fig.savefig(args.prefix+'-expected.svg')
d_fig.savefig(args.prefix+'-distribution.svg')
