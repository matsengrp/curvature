#!/usr/bin/env python

import argparse
import gzip
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle

parser = argparse.ArgumentParser(
    description='plot curvature results',
    prog='plot.py')

parser.add_argument('results_path',
                    type=str, help='Path to .p.gz file.')
parser.add_argument('plot_path',
                    type=str, help='Where to save plot.')

parser.add_argument('--which', choices=['hexbin', 'scatter'],
                    help='What type of plot is desired.')
parser.add_argument('--d3', action='store_true',
                    help='Save as a D3 HTML file, possibly with extras.')

args = parser.parse_args()
assert(os.path.exists(args.results_path))

mpl.rcParams.update({'font.size': 48, 'font.family': 'Lato'})

df = pickle.load(gzip.open(args.results_path, 'rb'))
df['dist_jitter'] = df['dist'] + np.random.normal(0, 0.1, size=len(df))
df['info'] = \
    df['t1_nwk']+'<br/>'+df['t2_nwk']+'<br/>avg_deg: '+map(str, df['avg_deg'])

if args.which == 'hexbin':
    p = df.plot(
        kind='hexbin',
        x='kappa_R',
        y='dist',
        gridsize=24,
        cmap=mpl.cm.gist_yarg)
elif args.which == 'scatter':
    if min(df['avg_deg']) == max(df['avg_deg']):
        p = df.plot(
            kind='scatter',
            x='kappa_R',
            y='dist_jitter',
            alpha=0.4)
    else:
        p = df.plot(
            kind='scatter',
            x='kappa_R',
            y='dist_jitter',
            alpha=0.4,
            c='avg_deg',
            cmap=plt.get_cmap('Blues'))

p.grid(b=None)
p.set_frame_on(False)

if args.d3:
    from mpld3 import fig_to_html, plugins
    plugins.connect(
        p.figure,
        plugins.PointHTMLTooltip(p.collections[0], list(df['info'])))
    with gzip.GzipFile(args.plot_path, mode='wb', mtime=0.) as f:
        f.write(fig_to_html(p.figure))
else:
    p.figure.savefig(args.plot_path)
