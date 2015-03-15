
# Fill empty spaces in list with zeroes. Modifies in place.
ZeroFill := function(l)
    local i;
    for i in [1..Length(l)] do
        if not IsBound(l[i]) then
            l[i] := 0;
        fi;
    od;
end;;

# For some reason DisplayString was just returning '<object>' so I wrote this.
# See https://github.com/gap-system/gap/issues/29
MyPrintToString := function(obj)
    local str, out;
    str := "";;
    out := OutputTextString( str, true );;
    PrintTo(out, obj);
    CloseStream(out);
    return str;
end;;

# inverse_same determines if we consider the inverse of the double coset to be
# the same as the original.
NewDCCounter := function(g, u, v, inverse_same)
    if inverse_same and u <> v then
      Error("\n\
To consider the inverse to be the same, \
need identical subgroups forming the double coset.");
    fi;
    return rec(
        g := g,
        u := u,
        v := v,
        inverse_same := inverse_same,
        max_idx := 0,
        dc_number := [],
        t := RightTransversal(g, u),
        counts := []);
end;;

NewDCCounterExemplar := function(g, coset, inverse_same)
    return NewDCCounter(g, LeftActingGroup(coset), RightActingGroup(coset), inverse_same);
end;;

# Get the representatives corresponding to all right cosets within the same
# double coset, via orbit of right coset (dcc.u, elt) under dcc.v by right
# multiplication.
DCCAllRightCosetRepresentatives := function(dcc, elt)
    return Orbit(dcc.v, CanonicalRightCosetElement(dcc.u, elt),
        function(pnt, s)
            return CanonicalRightCosetElement(dcc.u, pnt*s);
        end);
end;;

# r is a representative of the double coset to add.
AddDCCounterRepresentative := function(dcc, r, time)
    local dcn, i, o, p;
    p := PositionCanonical(dcc.t, r); # Number of the right coset for the element.
    if IsBound(dcc.dc_number[p]) then
        dcn := dcc.dc_number[p];
        if IsBound(dcc.counts[dcn][time]) then
            dcc.counts[dcn][time] := dcc.counts[dcn][time] + 1;
        else
            dcc.counts[dcn][time] := 1;
        fi;
    else
        dcc.max_idx := dcc.max_idx + 1;
        dcc.counts[dcc.max_idx] := [];
        dcc.counts[dcc.max_idx][time] := 1;
        dcc.dc_number[p] := dcc.max_idx;
        if dcc.inverse_same then
            o := Union(DCCAllRightCosetRepresentatives(dcc, dcc.t[p]),
                       DCCAllRightCosetRepresentatives(dcc, Inverse(dcc.t[p]))
                       );
        else
            o := DCCAllRightCosetRepresentatives(dcc, dcc.t[p]);
        fi;
        for i in o do
            dcc.dc_number[PositionCanonical(dcc.t, i)] := dcc.max_idx;
        od;
    fi;
end;;

AddDCCounter:= function(dcc, coset, time)
    AddDCCounterRepresentative(dcc, Representative(coset), time);
end;;

ShowDCCounter := function(dcc)
    local dcn, pos;
    for dcn in [1..dcc.max_idx] do
        pos := Position(dcc.dc_number, dcn);
        Display(dcc.t[pos]);
        ZeroFill(dcc.counts[dcn]);
        Display(dcc.counts[dcn]);
    od;
end;;

DCCounterTable := function(dcc)
    local dc, dcn, tab, pos;
    tab := [];
    for dcn in [1..dcc.max_idx] do
        pos := Position(dcc.dc_number, dcn);
        ZeroFill(dcc.counts[dcn]);
        dc := DoubleCoset(dcc.u, dcc.t[pos], dcc.v);
        tab[dcn] := [MyPrintToString(dc), dcc.counts[dcn]];
    od;
    return tab;
end;;


###### Read("double-coset-counter.g");

# mdcc := NewDCCounter(
#     SymmetricGroup(4),
#     Subgroup(SymmetricGroup(4), [(3,4)]),
#     Subgroup(SymmetricGroup(4), [(3,4)]), false);
# AddDCCounterRepresentative(mdcc, (1,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounterRepresentative(mdcc, (1,2,3), 5); mdcc; ShowDCCounter(mdcc);
# AddDCCounterRepresentative(mdcc, (1,3,2), 5); mdcc; ShowDCCounter(mdcc);
#
# mdcc := NewDCCounter(
#     SymmetricGroup(4),
#     Subgroup(SymmetricGroup(4), [(3,4)]),
#     Subgroup(SymmetricGroup(4), [(3,4)]), true);
# AddDCCounterRepresentative(mdcc, (1,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounterRepresentative(mdcc, (1,2,3), 5); mdcc; ShowDCCounter(mdcc);
# AddDCCounterRepresentative(mdcc, (1,3,2), 5); mdcc; ShowDCCounter(mdcc);
#
# mdcc := NewDCCounter(
#     SymmetricGroup(4),
#     Subgroup(SymmetricGroup(4), [(1,3)]),
#     Subgroup(SymmetricGroup(4), [(3,4)]), false);
# AddDCCounterRepresentative(mdcc, (1,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounterRepresentative(mdcc, (1,2,3), 5); mdcc; ShowDCCounter(mdcc);
# AddDCCounterRepresentative(mdcc, (1,3,2), 5); mdcc; ShowDCCounter(mdcc);
#
# AddDCCounterRepresentative(mdcc, (2,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounterRepresentative(mdcc, (1,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounterRepresentative(mdcc, (2,3,4), 4); mdcc; ShowDCCounter(mdcc);
