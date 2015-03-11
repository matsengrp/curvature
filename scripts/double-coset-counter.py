gap.eval("""
Read("scripts/double-coset-counter.g");
""")


# Groups and cosets

def new_dc_counter(g, u, v):
    return gap.function_call('NewDCCounter', [gap(g), gap(u), gap(v)])

def add_dc_counter(dcc, r, time):
    return gap.function_call('AddDCCounter', [dcc, gap(r), time])

def show_dc_counter(dcc):
    return gap.function_call('ShowDCCounter', dcc)
