# This loads all of the common dependencies.

import glob
import os

from sage.all import load

for source in glob.glob(
        os.path.dirname(os.path.realpath(__file__)) +
        '/../gricci/all-hail-sage/*.py'):
    load(source)
