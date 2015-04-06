# curvature

This is the text and code for the paper [Ricci-Ollivier curvature of the rooted phylogenetic Subtree-Prune-Regraft graph](http://arxiv.org/abs/1504.00304) by Chris Whidden and Erick Matsen.


## Software dependencies

In addition to [Sage](http://sagemath.org/), we depend on the following python packages:

* `scons`
* `matplotlib`
* `seaborn`
* `pandas`


## Running analyses

Edit the `SConstruct` file in `analysis` according to needs, and then type `scons` on the command line in the `analysis` directory to run the analyses.

Additional plotting and regression is performed in the IPython notebook `analysis/plot-and-regress.ipynb`.


## Handy commands

    git pull --recurse-submodules
    git submodule update --recursive
