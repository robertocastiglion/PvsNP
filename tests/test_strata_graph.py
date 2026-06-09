"""Test ESATTI per strata_graph (Ciclo 5, meta-complessità).

I numeri qui sono MISURATI su n=3 (256 funzioni, esaustivo in secondi), non
inventati. Confermano:
  - killer-1: down_degree_negation ≡ 0 ovunque (input-negation è automorfismo);
  - i valori di cost/strati coerenti con il Modulo 6 / MCSP;
  - per la mossa GENUINA output-flip: |{d_flip}| per strato e la relazione tra
    la partizione-per-d_flip e {sensitivity, block_sensitivity, gf2_degree,
    orbita-B_n}.
"""

import pytest

from pnp_lab.circuits import parity_table
from pnp_lab.meta_complexity.strata_graph import (
    analyze,
    block_sensitivity,
    down_degree_flip,
    down_degree_negation,
    flip_output,
    gf2_degree,
    negate_input,
    orbit_B,
    sensitivity,
    strata,
)
from pnp_lab.circuits import min_formula_sizes


# --------------------------------------------------------------------------- #
#  Mosse elementari                                                           #
# --------------------------------------------------------------------------- #

def test_negate_input_e_involuzione():
    n = 3
    ct = min_formula_sizes(n)
    for tt in list(ct.cost)[:20]:
        for i in range(n):
            assert negate_input(negate_input(tt, n, i), n, i) == tt


def test_flip_output_e_involuzione():
    for tt in range(0, 256, 7):
        for k in range(8):
            assert flip_output(flip_output(tt, k), k) == tt


# --------------------------------------------------------------------------- #
#  killer-1: input-negation è automorfismo del costo (atteso d_negation ≡ 0)  #
# --------------------------------------------------------------------------- #

def test_killer1_negation_down_degree_zero_n3():
    n = 3
    ct = min_formula_sizes(n)
    for tt in ct.cost:
        assert down_degree_negation(ct, tt, n) == 0
    # corollario diretto: il costo è INVARIANTE sotto negazione di ogni input
    for tt in ct.cost:
        for i in range(n):
            assert ct.cost[negate_input(tt, n, i)] == ct.cost[tt]


# --------------------------------------------------------------------------- #
#  Strati di MCSP-size coerenti col Modulo 6                                   #
# --------------------------------------------------------------------------- #

def test_strati_n3_dimensioni_esatte():
    n = 3
    ct = min_formula_sizes(n)
    assert ct.complete
    assert ct.num_functions == 256
    assert ct.max_cost == 9
    st = strata(ct)
    # {cost: #funzioni} misurato esattamente su n=3
    sizes = {c: len(v) for c, v in st.items()}
    assert sizes == {0: 6, 1: 26, 2: 64, 3: 30, 4: 80, 5: 32, 7: 16, 9: 2}
    # somma = tutte le funzioni
    assert sum(sizes.values()) == 256


# --------------------------------------------------------------------------- #
#  Invarianti classici su casi noti                                           #
# --------------------------------------------------------------------------- #

def test_invarianti_parita_n3():
    n = 3
    p = parity_table(n)
    assert gf2_degree(p, n) == 1          # x0⊕x1⊕x2 ha grado GF(2) = 1
    assert sensitivity(p, n) == 3         # ogni bit è sensibile ovunque
    assert block_sensitivity(p, n) == 3
    assert len(orbit_B(p, n)) == 2        # parità e la sua negazione


def test_invarianti_and3_n3():
    n = 3
    andf = 1 << 7                          # x0 ∧ x1 ∧ x2 (acceso solo su 111)
    assert gf2_degree(andf, n) == 3
    assert sensitivity(andf, n) == 3
    assert block_sensitivity(andf, n) == 3
    assert len(orbit_B(andf, n)) == 8      # 8 AND di letterali


# --------------------------------------------------------------------------- #
#  La mossa GENUINA: |{d_flip}| per strato e relazioni di partizione (n=3)     #
# --------------------------------------------------------------------------- #

def test_dflip_valori_per_strato_n3():
    """Valori MISURATI di d_flip per ciascuno strato di costo su n=3."""
    n = 3
    _, reps = analyze(n)
    by_cost = {r.cost: r for r in reps}
    expected = {
        0: [0],
        1: [0],
        2: [3, 4],
        3: [0, 4],
        4: [4, 6],
        5: [6, 8],
        7: [7],
        9: [8],
    }
    assert {c: r.dflip_values for c, r in by_cost.items()} == expected


def test_dflip_relazioni_partizione_n3():
    """Negli strati con |{d_flip}|>=2, relazione partizione-d_flip vs invarianti.

    Valori MISURATI esattamente su n=3. Mostrano che d_flip NON coincide
    uniformemente con nessun invariante classico: la relazione DIPENDE dallo
    strato (a volte RAFFINA, a volte COINCIDE, a volte è RAFFINATA/INCOMPARABILE).
    """
    n = 3
    _, reps = analyze(n)
    rel = {
        r.cost: (
            r.rel_sensitivity,
            r.rel_block_sensitivity,
            r.rel_gf2_degree,
            r.rel_orbit,
        )
        for r in reps
        if r.num_dflip_values >= 2
    }
    assert rel == {
        2: ("COINCIDE", "COINCIDE", "RAFFINA", "RAFFINATA"),
        3: ("RAFFINA", "RAFFINA", "COINCIDE", "COINCIDE"),
        4: ("COINCIDE", "COINCIDE", "INCOMPARABILE", "RAFFINATA"),
        5: ("RAFFINA", "RAFFINA", "RAFFINA", "RAFFINATA"),
    }


def test_dflip_non_e_funzione_del_costo_n3():
    """d_flip varia DENTRO uno strato (non è una funzione di cost): 4 strati su 8
    hanno |{d_flip}|>=2. Quindi NON scatta il killer 'd = funzione(cost)'."""
    n = 3
    _, reps = analyze(n)
    multi = [r.cost for r in reps if r.num_dflip_values >= 2]
    assert multi == [2, 3, 4, 5]


# --------------------------------------------------------------------------- #
#  n=4 — esaustivo, marcato slow                                              #
# --------------------------------------------------------------------------- #

@pytest.mark.slow
@pytest.mark.timeout(2400)
def test_killer1_negation_zero_n4():
    """killer-1 su n=4 (65536 funzioni): input-negation è automorfismo del costo.

    Lento: il collo è ``min_formula_sizes(4)`` (DP esaustiva sulle 65536 funzioni);
    il down_degree_negation è invece trascurabile. Marcato slow.
    """
    n = 4
    ct = min_formula_sizes(n)
    assert ct.complete
    assert ct.num_functions == 65536
    assert ct.max_cost == 15
    for tt in ct.cost:
        assert down_degree_negation(ct, tt, n) == 0


@pytest.mark.slow
@pytest.mark.timeout(3600)
def test_dflip_n4_misure_complete():
    """Analisi completa n=4 — ESAUSTIVA e MOLTO lenta (~35 min, misurata).

    Registra i numeri VERI di d_flip per strato e le relazioni di partizione.
    Killer-1 confermato (neg_nonzero=0). Su n=4 la partizione-per-d_flip è quasi
    ovunque INCOMPARABILE con sensitivity/block_sensitivity/gf2_degree e sempre
    RAFFINATA rispetto all'orbita-B_4: d_flip NON è nessun invariante classico.
    """
    n = 4
    ct, reps = analyze(n)
    assert ct.max_cost == 15 and len(ct.cost) == 65536
    by_cost = {r.cost: r for r in reps}
    # valori di d_flip per strato (misurati esattamente)
    assert by_cost[3].dflip_values == [0, 3, 4, 5]
    assert by_cost[8].dflip_values == [3, 4, 5, 6, 7, 8, 9, 10]
    assert by_cost[9].dflip_values == [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16]
    assert by_cost[15].dflip_values == [0, 10, 14]
    # relazioni: orbita-B_4 sempre RAFFINATA (più fine di d_flip)
    for c in range(3, 16):
        assert by_cost[c].rel_orbit == "RAFFINATA"
    # negli strati 4..11 d_flip è INCOMPARABILE con tutti gli invarianti scalari
    for c in range(4, 12):
        assert by_cost[c].rel_sensitivity == "INCOMPARABILE"
        assert by_cost[c].rel_block_sensitivity == "INCOMPARABILE"
        assert by_cost[c].rel_gf2_degree == "INCOMPARABILE"
