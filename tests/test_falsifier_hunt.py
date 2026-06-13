"""Test del Ciclo 6 — caccia al falsificatore / completezza del dizionario μ_R.

Fatti ESATTI riprodotti (n=3, 256 funzioni). La narrazione in tre stadi:
  NAIVE (B_n, no support)   -> 8 split, sembra falsificatore;
  B_n± , no support         -> 1 solo split residuo: la coppia (24,30);
  CORRECT (B_n±, +support)  -> 0 split: P_Σ == P_orbit±, collasso COMPLETO.
Entrambe le chiusure (negazione-output, support-size) sono NECESSARIE.
"""

import pytest

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.meta_complexity.falsifier_hunt import (
    average_sensitivity,
    cofactor_cost_profile,
    comm_matrix,
    cost_orbit,
    cover_number_label,
    dictionary_vector,
    fourier_fingerprint,
    frac_cover_label,
    gstar_label,
    hunt,
    named_separators,
    orbit_canon,
    real_degree,
    support_folded,
)
from pnp_lab.meta_complexity.strata_graph import (
    negate_input,
    orbit_B,
    permute_inputs,
)


# tutti i generatori che devono essere B_n±-invarianti (premessa logica del test)
_BN_PM_INVARIANTS = (
    gstar_label, cover_number_label, frac_cover_label,
    fourier_fingerprint, cofactor_cost_profile,
)
_SCALAR_BN_PM = (support_folded, average_sensitivity, real_degree)


# --------------------------------------------------------------------------- #
#  Mattoni: matrice di comunicazione, support, gruppo, G★                     #
# --------------------------------------------------------------------------- #

def test_comm_matrix_shape_and_values():
    # f = AND delle 2 var su n=2: tt=0b1000 (1 solo all'input 3=11)
    M = comm_matrix(0b1000, 2, (0,))
    assert M == ((0, 0), (0, 1))  # riga=Alice(x0), col=Bob(x1); 1 solo in (1,1)


def test_support_folded_basic():
    # 24=0b00011000 ha 2 uni; 30=0b00011110 ha 4 uni (n=3, 2^3=8 input)
    assert support_folded(24, 3) == 2
    assert support_folded(30, 3) == 4
    assert support_folded(0, 3) == 0
    assert support_folded(255, 3) == 0  # costante-1: min(8,0)=0


def test_cost_orbit_includes_output_negation():
    n = 3
    full = (1 << (1 << n)) - 1
    o_plus = cost_orbit(0, n, output_negation=True)
    o_only = cost_orbit(0, n, output_negation=False)
    assert full in o_plus          # ¬(cost-0) sta nell'orbita ±
    assert full not in o_only      # ma non in quella solo-B_n
    assert o_only <= o_plus


def test_gstar_label_is_Bn_invariant():
    # gstar_label deve essere costante sull'orbita B_n (perm + negazione input)
    n, tt = 3, 0b00011000
    base = gstar_label(tt, n)
    assert gstar_label(permute_inputs(tt, n, (1, 0, 2)), n) == base
    assert gstar_label(negate_input(tt, n, 1), n) == base


@pytest.mark.parametrize("inv", _BN_PM_INVARIANTS + _SCALAR_BN_PM)
def test_all_generators_are_Bn_pm_invariant(inv):
    """REGRESSIONE: ogni generatore (anche i forti cover-LP) DEVE essere invariante
    sotto TUTTO B_n± — incluse permutazione, negazione input E negazione output.
    Le misure cover-LP fallivano la negazione output prima del ``_output_fold``."""
    n = 3
    full = (1 << (1 << n)) - 1
    for tt in (0b00011000, 0b00010110, 0b01101001, 1, 0):
        base = inv(tt, n)
        assert inv(permute_inputs(tt, n, (2, 0, 1)), n) == base
        assert inv(negate_input(tt, n, 0), n) == base
        assert inv(tt ^ full, n) == base   # negazione OUTPUT (la piega critica)


# --------------------------------------------------------------------------- #
#  P_orbit raffina SEMPRE P_Σ (ogni generatore è invariante sul gruppo)       #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("on,sup", [(False, False), (True, False), (True, True)])
def test_orbit_refines_sigma(on, sup):
    """In ogni configurazione, due funzioni nella STESSA orbita hanno lo STESSO
    vettore-dizionario (mai INCOMPARABILE): è la premessa logica del test."""
    n = 3
    ct = min_formula_sizes(n, 60)
    by_orbit = {}
    for tt in ct.cost:
        by_orbit.setdefault(orbit_canon(tt, n, on), []).append(tt)
    for members in by_orbit.values():
        vecs = {dictionary_vector(tt, n, ct, sup) for tt in members}
        assert len(vecs) == 1


# --------------------------------------------------------------------------- #
#  La narrazione in tre stadi su n=3 (i numeri esatti del ciclo)              #
# --------------------------------------------------------------------------- #

def test_stage_naive_finds_phantom_falsifiers():
    r = hunt(3, output_negation=False, include_support=False)
    assert r.num_funcs == 256
    assert r.num_orbits == 22
    assert r.num_sigma_classes == 13
    assert len(r.splits) == 8
    assert r.verdict == "FALSIFIER_CANDIDATE"


def test_stage_correct_group_leaves_single_split():
    r = hunt(3, output_negation=True, include_support=False)
    assert r.num_orbits == 14            # 22 -> 14 chiudendo sotto negazione-output
    assert r.num_sigma_classes == 13
    assert len(r.splits) == 1
    w = r.splits[0]
    assert w.example_pair == (24, 30)
    # la coppia non è separata da NESSUN generatore nominato (senza support)
    ct = min_formula_sizes(3, 60)
    assert named_separators(24, 30, 3, ct, include_support=False) == []


def test_stage_closed_dictionary_completes_collapse():
    r = hunt(3)  # default = B_n±, +support (la configurazione corretta)
    assert r.output_negation is True and r.include_support is True
    assert r.num_orbits == 14
    assert r.num_sigma_classes == 14     # |P_Σ| == |P_orbit±|
    assert r.relation == "COINCIDE"
    assert len(r.splits) == 0
    assert r.verdict == "COLLAPSE_HARDENED"
    # support-size separa proprio la coppia (24,30) che era sopravvissuta
    ct = min_formula_sizes(3, 60)
    assert named_separators(24, 30, 3, ct) == ["support_folded"]


def test_strong_dictionary_still_completes_on_n3():
    """Con i generatori forti, su n=3 P_orbit± raffina ancora P_Σ e il collasso
    resta completo (0 split): i forti non rompono l'invarianza (regressione del bug)."""
    r = hunt(3, strong=True)
    assert r.num_sigma_classes <= r.num_orbits   # orbita raffina sigma (premessa)
    assert len(r.splits) == 0
    assert r.verdict == "COLLAPSE_HARDENED"


def test_both_closures_are_necessary():
    """Nessuna delle due chiusure da sola basta: serve B_n± E support insieme."""
    only_group = hunt(3, output_negation=True, include_support=False)
    only_supp = hunt(3, output_negation=False, include_support=True)
    both = hunt(3, output_negation=True, include_support=True)
    assert len(only_group.splits) > 0     # B_n± da solo: resta (24,30)
    assert len(only_supp.splits) > 0      # support da solo: restano coppie ¬f
    assert len(both.splits) == 0          # insieme: completo


# --------------------------------------------------------------------------- #
#  Il caso decisivo n=4 — su tabella di costi (lento) e sulla coppia (veloce)  #
# --------------------------------------------------------------------------- #

# Numeri ESATTI riprodotti su n=4 (vedi docs/falsifier-hunt.md). La coppia
# (2025, 5742) è l'UNICO split residuo del dizionario STRONG a 11 generatori,
# uccisa dal 12° (cofactor_cost_profile). Questi valori NON richiedono la tabella
# dei costi a n=4 (il cofattore usa solo la tabella a n=3) → test veloce.
_PAIR = (2025, 5742)
_COFACTOR_2025 = ((2, 7), (2, 7), (5, 5), (5, 5))
_COFACTOR_5742 = ((4, 5), (4, 5), (4, 7), (4, 7))


def test_cofactor_kills_the_lone_n4_split_fast():
    """Il 12° generatore separa la coppia (2025,5742) — il falsificatore-candidato.
    NON richiede la tabella a n=4: il cofattore è una funzione a 3 variabili."""
    f, g = _PAIR
    assert cofactor_cost_profile(f, 4) == _COFACTOR_2025
    assert cofactor_cost_profile(g, 4) == _COFACTOR_5742
    assert cofactor_cost_profile(f, 4) != cofactor_cost_profile(g, 4)


def test_naive_cofactor_would_over_refine():
    """GUARDIA anti-bug (a n=3, veloce): leggere i costi dei cofattori (n-1)-var sulla
    tabella a n var misura il costo dell'EMBEDDING ``g ∧ ¬xi``, che NON è
    B_n±-invariante → spezza dentro le orbite (è il bug che a n=4 produsse
    |P_Σ|=243>222 e #splits=0 VACUO). Mostriamo: il cofattore CORRETTO (tabella n-1) è
    invariante sotto negazione-output su TUTTE le 256 funzioni, l'INGENUO no."""
    n = 3
    N = 1 << n
    full = (1 << N) - 1
    ct_naive = min_formula_sizes(n, 60)     # tabella a n var = quella SBAGLIATA

    def naive(tt):
        prof = []
        for i in range(n):
            tt0 = tt1 = 0
            pos = 0
            for x in range(N):
                if ((x >> i) & 1) == 0:
                    tt0 |= ((tt >> x) & 1) << pos
                    tt1 |= ((tt >> (x | (1 << i))) & 1) << pos
                    pos += 1
            prof.append(tuple(sorted((ct_naive.cost[tt0], ct_naive.cost[tt1]))))
        return tuple(sorted(prof))

    # CORRETTO: invariante sotto negazione-output su tutte le 256 funzioni
    for tt in range(1 << N):
        assert cofactor_cost_profile(tt, n) == cofactor_cost_profile(tt ^ full, n)
    # INGENUO: rompe l'invarianza-output per almeno una funzione (in realtà molte)
    assert any(naive(tt) != naive(tt ^ full) for tt in range(1 << N))


@pytest.mark.slow
@pytest.mark.timeout(3600)
def test_n4_strong_collapse_complete():
    """n=4 esaustivo (65536 funzioni): col dizionario STRONG a 12 generatori il
    collasso è COMPLETO — P_Σ == P_orbit± == 222, nessuno split, nessun
    falsificatore fuori-dizionario. (Costruisce la tabella dei costi a n=4: lento.)
    """
    r = hunt(4, strong=True)
    assert r.num_funcs == 65536
    assert r.num_orbits == 222
    assert r.num_sigma_classes == 222          # P_Σ == P_orbit± (legittimo, <=222)
    assert r.num_sigma_classes <= r.num_orbits  # orbita raffina sigma: niente over-refine
    assert len(r.splits) == 0
    assert r.relation == "COINCIDE"
    assert r.verdict == "COLLAPSE_HARDENED"
