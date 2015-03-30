# curvature

This is the code and TeX for the paper "Ricci-Ollivier curvature of two random walks on the rooted phylogenetic Subtree-Prune-Regraft graph" by Chris Whidden and Erick Matsen.


## Software dependencies

In addition to [sage](http://sagemath.org/), we depend on the following python packages,

* `scons`
* `matplotlib`
* `seaborn`
* `pandas`


## Running analyses

Edit the `SConstruct` file in `analysis` according to needs, and then type `scons` on the command line to run the analyses.

Additional plotting and regression is performed in the IPython notebook `analysis/plot-and-regress.ipynb`.


## Handy commands

    git pull --recurse-submodules
    git submodule update --recursive
