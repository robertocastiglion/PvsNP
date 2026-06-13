"""Direzione A, ciclo 1 — geometria dello spazio delle soluzioni (OGP minuscolo).

Fatti ESATTI su n=3 (256 funzioni). Risultato chiave: a n=3 la chiave-scalare
(cost, |orbita B_n±|, N_min) è GIÀ iniettiva sulle 14 orbite (14 classi == |P_orbit±|),
quindi il test di H-A è VACUO/sotto-soglia a n=3 — serve n=4 (slow/separato) per
decidere. La geometria è però B_n±-invariante e K2-canonica (ordinato↔non-ordinato).
"""

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.meta_complexity.solution_geometry import (
    analyze,
    geometry,
    n_min_ordered,
    n_min_unordered,
    optimal_splits,
    optimal_splits_via_dp,
    reach,
)
import pytest

from pnp_lab.circuits.circuit import AND, OR
from pnp_lab.meta_complexity.falsifier_hunt import cofactor_cost_profile
from pnp_lab.meta_complexity.strata_graph import negate_input, permute_inputs


def _ctx(n=3):
    ct = min_formula_sizes(n, 60)
    splits = optimal_splits(ct)
    rc = reach(ct, splits)
    return ct, splits, rc


def test_optimal_splits_are_valid():
    """Ogni split (op,a,b) di t calcola davvero t ed è ottimo (additività esatta)."""
    ct, splits, _ = _ctx()
    for t, sp in splits.items():
        for op, a, b in sp:
            val = AND(a, b) if op == "and" else OR(a, b)
            assert val == t
            assert ct.cost[a] + ct.cost[b] + 1 == ct.cost[t]
        if ct.cost[t] > 0:
            assert sp, f"funzione non-letterale {t} senza split ottimi"


def test_reach_contains_self_and_children():
    ct, splits, rc = _ctx()
    for t in ct.cost:
        assert t in rc[t]
        for _, a, b in splits[t]:
            assert rc[a] <= rc[t] and rc[b] <= rc[t]


def test_n_min_literals_are_one():
    ct, splits, _ = _ctx()
    nm = n_min_ordered(ct, splits)
    for t in ct.cost:
        if ct.cost[t] == 0:
            assert nm[t] == 1


def test_n_min_unordered_le_ordered():
    """Il conteggio AC-quozientato non supera mai quello ordinato."""
    ct, splits, _ = _ctx()
    no, nu = n_min_ordered(ct, splits), n_min_unordered(ct, splits)
    for t in ct.cost:
        assert nu[t] <= no[t]


def test_geometry_is_Bn_invariant():
    """La geometria (definita su FUNZIONI) è costante sull'orbita B_n: encoding-indep."""
    ct, splits, rc = _ctx()
    for tt in (0b00011000, 0b00010110, 0b01101001, 1):
        base = geometry(tt, ct, splits, rc).as_tuple()
        assert geometry(permute_inputs(tt, 3, (2, 0, 1)), ct, splits, rc).as_tuple() == base
        assert geometry(negate_input(tt, 3, 0), ct, splits, rc).as_tuple() == base


def test_dp_builder_matches_oN2_on_n3():
    """Il builder DP (usato per n=4) coincide con lo scan O(N²) di riferimento su n=3:
    stesso cost-table e stesso insieme di split ottimi per ogni funzione."""
    ct = min_formula_sizes(3, 60)
    ref = optimal_splits(ct)
    cost_dp, splits_dp = optimal_splits_via_dp(3, 60)
    assert cost_dp == ct.cost
    for t in ct.cost:
        assert set(splits_dp.get(t, [])) == set(ref[t])


def test_n3_is_below_threshold_collapse():
    """A n=3 (cost,|orbita|,N_min) ha 14 classi == |P_orbit±|=14: già iniettiva sulle
    orbite → nessuno spazio per la geometria. K1 scatta (collasso) ma il test è VACUO;
    K2 canonico. Il caso decisivo è n=4 (vedi run_solution_geometry.py --n4)."""
    r = analyze(3)
    assert r.num_funcs == 256
    assert r.num_scalar_classes == 14        # == |P_orbit±| a n=3
    assert r.num_geo_classes == 14           # la geometria NON raffina
    assert r.separated == []
    assert r.k1_collapses is True
    assert r.k2_canonical is True
    assert r.verdict.startswith("COLLAPSE")


# Le coppie a n=4 che la geometria separa a parità di chiave-scalare (run decisivo,
# _geometry_n4.out). L'ADVERSARY le ha uccise: stanno in orbite DIVERSE e il dizionario
# del Ciclo 6 (orbit-completo a n=4, |P_Σ|=222) le separa già — il cofactor_cost_profile
# ∈ σ(cost) da solo separa tutte. La geometria NON esce da σ(cost) → RESTATEMENT.
_N4_GEOMETRY_PAIRS = [
    (27, 427), (30, 1654), (111, 287), (283, 494), (300, 875), (303, 983),
    (367, 415), (425, 961), (429, 430), (982, 2017), (985, 990), (1716, 6042),
]


def test_n4_geometry_separation_is_sigma_cost_restatement_fast():
    """KILL (veloce, niente tabella n=4): ogni coppia separata dalla geometria a n=4 è
    GIÀ separata dal cofactor_cost_profile (raffinamento di cost del Ciclo 6, ∈ σ(cost)).
    Quindi la geometria è dominata da σ(cost): contenuto NON nuovo, RESTATEMENT."""
    for f, g in _N4_GEOMETRY_PAIRS:
        assert cofactor_cost_profile(f, 4) != cofactor_cost_profile(g, 4)


@pytest.mark.slow
@pytest.mark.timeout(3600)
def test_n4_analyze_verdict_is_restatement():
    """n=4 esaustivo (lento, costruisce cost+split DP). La geometria raffina la chiave-
    scalare fino a 222 == |P_orbit±|, ma ogni coppia separata è in σ(cost)
    (cofactor_cost_profile) → verdetto RESTATEMENT, non contenuto fuori-dizionario."""
    r = analyze(4)
    assert r.num_funcs == 65536
    assert r.num_geo_classes == 222          # == |P_orbit±| a n=4
    assert len(r.separated) > 0              # la geometria SEPARA (K1 debole non scatta)
    assert r.k2_canonical is True
    assert r.sigma_cost_dominated is True    # ADVERSARY: tutto in σ(cost)
    assert r.verdict.startswith("RESTATEMENT")
