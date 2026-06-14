"""Module 21 (Local-Consistency Width) — test ESATTI di w*(Gamma) su D={0,1,2}.

Regime esatto-PER-ISTANZA su campione: ogni is_sat e` enumerazione completa <=729, ogni
kk1_consistent e` un punto fisso esatto, ogni w* e` un MIN esatto sulla batteria CONGELATA.
Fissa i NUMERI del campione (rigenerabili) e l'esito dei 4 predicati-killer.
"""

import pytest

from pnp_lab.csp.local_consistency3 import (
    CSP,
    analyze_consistency,
    is_sat,
    kk1_consistent,
    tractable_catalog,
    w_star,
    T,
)
from pnp_lab.csp.polymorphism3 import CATALOG


# --------------------------------------------------------------------------- #
#  Sanity is_sat                                                              #
# --------------------------------------------------------------------------- #

def test_is_sat_known_sat():
    # x0 <= x1 con leq: soddisfacibile (es. 0,0).
    leq = CATALOG["leq"]
    phi = CSP(2, (((0, 1), leq),))
    assert is_sat(phi) is True


def test_is_sat_known_unsat():
    # Ciclo di disuguaglianza stretta su 3 var: x0<x1<x2<x0 -> impossibile.
    lt = CATALOG["lt"]
    phi = CSP(3, (((0, 1), lt), ((1, 2), lt), ((2, 0), lt)))
    assert is_sat(phi) is False


# --------------------------------------------------------------------------- #
#  Soundness: SAT => (k,k+1)-consistente per ogni k testato                    #
# --------------------------------------------------------------------------- #

def test_soundness_sat_implies_consistent():
    """Per ogni Gamma trattabile e ogni istanza SAT della batteria, kk1_consistent deve
    essere True per ogni k in {1,2,3}: un modello totale non viene mai cancellato."""
    for name, R in tractable_catalog().items():
        for inst_name, phi in T(R):
            if is_sat(phi):
                for k in (1, 2, 3):
                    assert kk1_consistent(phi, k) is True, (name, inst_name, k)


# --------------------------------------------------------------------------- #
#  GAP esibito: UNSAT ma 1-consistente, scoperto solo da k=2                   #
# --------------------------------------------------------------------------- #

def test_exhibited_gap_cycle4_on_C3():
    """Testimone ESATTO che w* puo` essere > 1. Relazione C3 = {(0,1),(1,2),(2,0)} (il
    grafo "+1 mod 3"). Ciclo su 4 variabili: x0 C3 x1 C3 x2 C3 x3 C3 x0.

    Calcolo A MANO. Ogni arco impone x_{i+1} = x_i + 1 (mod 3). Lungo il ciclo di
    lunghezza 4 la somma degli incrementi e` 4 ≡ 1 (mod 3) != 0, quindi x0 = x0 + 1 (mod 3)
    -> CONTRADDIZIONE globale -> UNSAT. MA: ogni singolo arco e` soddisfacibile e ogni
    dominio di variabile resta {0,1,2} pieno (arc-consistency non propaga nulla lungo un
    ciclo) -> 1-consistente. La (2,3)-consistency invece confronta coppie e scopre la
    contraddizione -> NON 2-consistente.
    """
    C3 = CATALOG["cycle3"]
    phi = CSP(4, (((0, 1), C3), ((1, 2), C3), ((2, 3), C3), ((3, 0), C3)))
    assert is_sat(phi) is False
    assert kk1_consistent(phi, 1) is True    # 1-consistente
    assert kk1_consistent(phi, 2) is False   # ma NON 2-consistente
    # quindi w* per C3 e` > 1 (k=1 sbaglia su questa istanza)


def test_cycle3_on_C3_is_sat_and_consistent():
    """Controprova: il ciclo di lunghezza 3 su C3 e` SAT (3 ≡ 0 mod 3): es. 0->1->2->0."""
    C3 = CATALOG["cycle3"]
    phi = CSP(3, (((0, 1), C3), ((1, 2), C3), ((2, 0), C3)))
    assert is_sat(phi) is True
    assert kk1_consistent(phi, 1) is True
    assert kk1_consistent(phi, 2) is True


# --------------------------------------------------------------------------- #
#  NUMERI congelati del campione (rigenerabili: py examples/run_local_consistency3.py)
# --------------------------------------------------------------------------- #

# (g, sym_profile, has_majority, n_pol_slice, w*)
EXPECTED_W = {
    "between":   (8, (2, 3), True,  8,  1),
    "cycle3":    (3, (2,),   False, 3,  2),
    "eq012":     (7, (2, 3), True,  27, 1),
    "impl01":    (18, (2, 3), True, 18, 1),
    "leq":       (8, (2, 3), True,  8,  1),
    "lt":        (9, (2, 3), True,  9,  1),
    "min_graph": (1, (2, 3), False, 1,  1),
}


def test_sample_numbers_frozen():
    rep = analyze_consistency()
    got = {
        r.name: (r.g_value, r.sym_profile, r.has_majority, r.n_pol_slice, r.w)
        for r in rep.rows
    }
    assert got == EXPECTED_W


# --------------------------------------------------------------------------- #
#  I 4 predicati-killer (numeri esatti, NESSUNA interpretazione)               #
# --------------------------------------------------------------------------- #

def test_killer_predicates():
    rep = analyze_consistency()

    # K-bw23 (PRINCIPALE): max w* finito <= 2 -> range {1,2}.
    assert rep.w_star_range == (1, 2)
    assert rep.k_bw23_holds is True

    # w1_tracks_majority: w*=1 <=> ha_majority? NO -> min_graph ha w*=1 senza maggioranza
    # (e` un semilattice: width-1 SENZA near-unanimity). Predicato FALSO.
    assert rep.w1_tracks_majority is False

    # K-Pol-slice: w* funzione esatta di (g, profilo, |Pol-slice|)? Sul campione SI`
    # (nessuna collisione di triple con w* diverso).
    assert rep.k_polslice_collapses is True

    # Separazione H: coppia stesso-g stesso-profilo ma w* diverso? NESSUNA sul campione.
    sep, witnesses = rep.h_separates
    assert sep is False
    assert witnesses == []


def test_min_graph_w1_without_majority():
    """ISOLATO: il semilattice min_graph ha w*=1 ma NON ha la maggioranza ternaria.
    E` la ragione per cui w1_tracks_majority e` False (w*=1 e` width-1, piu` ampio di
    near-unanimity)."""
    rep = analyze_consistency()
    row = next(r for r in rep.rows if r.name == "min_graph")
    assert row.w == 1
    assert row.has_majority is False


# --------------------------------------------------------------------------- #
#  w_star None fuori batteria                                                  #
# --------------------------------------------------------------------------- #

def test_w_star_none_when_empty_battery():
    # Relazione unaria: la batteria binaria/ternaria non si applica -> batteria vuota.
    unary = frozenset({(0,), (1,)})
    assert w_star(unary) is None
