# curvature

[FOCS Example](http://arxiv.org/abs/1406.0242v2)

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
