# This loads all of the common dependencies.

import os

wd = os.path.dirname(os.path.realpath(__file__))

sources = [wd+'/../gricci/'+f for f in [
    'all-hail-sage/nb-fun.py',
    'all-hail-sage/tree-fun.py',
    'code.py']]

for source in sources:
    load(source)
