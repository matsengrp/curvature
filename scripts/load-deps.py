# This loads all of the common dependencies.

from sage.all import gap
import os

wd = os.path.dirname(os.path.realpath(__file__))

sources = [wd+'/../gricci/'+f for f in [
    'all-hail-sage/nb-fun.py',
    'all-hail-sage/tree-fun.py',
    'code.py']] + [
    wd+'/../tangle/tangle-fun.py'
    ]

for source in sources:
    load(source)

gap.eval("""
Read("{}/../tangle/tangle-fun.g");
""".format(wd))
