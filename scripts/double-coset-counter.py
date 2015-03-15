# Groups and cosets

wd = os.path.dirname(os.path.realpath(__file__))
gap.eval("""
Read("{}/double-coset-counter.g");
""".format(wd))

# Note: I don't know why, but `sg.libgap(True)` gives a gap `true`,
# while just `gap(True)` gives 1.
def new_dc_counter(g, u, v, inverse_same=False):
    return gap.function_call(
        'NewDCCounter',
        [gap(g), gap(u), gap(v), sg.libgap(inverse_same)])

def new_dc_counter_exemplar(g, coset, inverse_same=False):
    return gap.function_call(
        'NewDCCounterExemplar',
        [gap(g), coset, sg.libgap(inverse_same)])

def add_dc_counter(dcc, coset, time):
    return gap.function_call('AddDCCounter', [dcc, coset, time])

def dc_counter_table(dcc):
    tab = gap.function_call('DCCounterTable', dcc)
    return [[gap.eval(coset_str), counts]
        for (coset_str, counts) in tab.sage()]
