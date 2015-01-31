#!/usr/bin/env python

import argparse
import gzip
import matplotlib as mp
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

parser.add_argument('--which', choices=['hexbin', 'scatter'])
args = parser.parse_args()
assert(os.path.exists(args.results_path))

df = pickle.load(gzip.open(args.results_path, 'rb'))
df['dist_jitter'] = df['dist'] + np.random.normal(0, 0.1, size=len(df))

if args.which == 'hexbin':
    p = df.plot(
        kind='hexbin',
        x='kappa_R',
        y='dist',
        gridsize=24,
        cmap=mp.cm.gist_yarg)
elif args.which == 'scatter':
    if min(df['avg_deg']) == max(df['avg_deg']):
        p = df.plot(
            kind='scatter',
            x='kappa_R',
            y='dist_jitter',
            alpha=0.3)
    else:
        p = df.plot(
            kind='scatter',
            x='kappa_R',
            y='dist_jitter',
            c='avg_deg',
            alpha=0.3,
            cmap=plt.get_cmap('cool'))

p.get_figure().savefig(args.plot_path)
