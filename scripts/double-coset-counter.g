
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
MyPrintToString := function(obj)
    local str, out;
    str := "";;
    out := OutputTextString( str, true );;
    PrintTo(out, obj);
    CloseStream(out);
    return str;
end;;

NewDCCounter := function(g, u, v)
    return rec(
        g := g,
        u := u,
        v := v,
        max_idx := 0,
        dc_number := [],
        t := RightTransversal(g, u),
        counts := []);
end;;

NewDCCounterExemplar := function(g, coset)
    return NewDCCounter(g, LeftActingGroup(coset), RightActingGroup(coset));
end;;

AddDCCounter := function(dcc, coset, time)
    local dcn, i, o, p, r;
    r := Representative(coset);
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
        # Mark all right cosets within the same double coset, via
        # orbit of right coset (dcc.u, t[p]) under dcc.v by right multiplication.
        o := Orbit(dcc.v, CanonicalRightCosetElement(dcc.u, dcc.t[p]),
            function(pnt, s)
                return CanonicalRightCosetElement(dcc.u, pnt*s);
            end);
        for i in o do
            dcc.dc_number[PositionCanonical(dcc.t, i)] := dcc.max_idx;
        od;
    fi;
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



# mdcc := NewDCCounter(
#     SymmetricGroup(4),
#     Subgroup(SymmetricGroup(4), [(1,2,3),(1,2)]),
#     Subgroup(SymmetricGroup(4), [(3,4)]));
# AddDCCounter(mdcc, (1,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounter(mdcc, (1,4,2), 5); mdcc; ShowDCCounter(mdcc);
# AddDCCounter(mdcc, (1,2), 3); mdcc; ShowDCCounter(mdcc);
# AddDCCounter(mdcc, (1,2,3), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounter(mdcc, (2,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounter(mdcc, (1,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounter(mdcc, (1,4), 4); mdcc; ShowDCCounter(mdcc);
# AddDCCounter(mdcc, (2,3,4), 4); mdcc; ShowDCCounter(mdcc);


