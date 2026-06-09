"""Ciclo 4 (research loop): feasible interpolation MONOTONA su K4-triangolo +
comunicazione Karchmer-Wigderson (KW+) misurata in modo ESATTO.

Misuriamo tre interi INDIPENDENTI sull'istanza f = "il grafo contiene un
triangolo" su K4 (6 archi):

  S = taglia dell'interpolante MONOTONO estratto dalla refutazione dello split
      A(p,z) ∧ B(q,z) (conteggio gate distinti con structural sharing);
  P = partition number della matrice KW+ di f (rettangoli monocromatici disgiunti);
  C = D^cc = costo del miglior protocollo deterministico sulla stessa matrice.

VINCOLO DI BANCO (buco-2 del ciclo 3): lo split DEVE forzare la regola privata
a→OR / b→AND con operandi NON costanti. Il test `test_swap_breaks_semantics`
ricostruisce l'interpolante SCAMBIANDO la regola: se la semantica REGGE comunque,
l'istanza non forza la regola → fallimento di banco. Qui lo scambio DEVE rompere
`verify_interpolant`.

I numeri asseriti sono quelli MISURATI dal codice (vedi examples/run_kw_communication.py).
"""
from __future__ import annotations

from itertools import product

import pytest

from pnp_lab.feasible_interp.families import clique_triangle_K4
from pnp_lab.feasible_interp.interp import (
    dag_refute, build_interpolant, build_interpolant_swapped,
    verify_interpolant, eval_gate, _restrict_sat,
)
from pnp_lab.kw_communication.kw import (
    clique_f, minterms, maxterms, kw_plus_matrix, partition_number, dcc,
)

# Numerazione archi di K4 (la stessa dello split clique_triangle_K4):
#   indice 0..5 = archi 12,13,14,23,24,34
K4_EDGES = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
N = 6

# I tre numeri ESATTI misurati su K4-triangolo (rigenerabili con
#   py examples/run_kw_communication.py):
S_EXACT = 19          # gate distinti dell'interpolante (11 MUX + 8 AND/OR)
S_BOOL_EXACT = 8      # solo gate AND/OR
S_MUX_EXACT = 11      # MUX = pivot risolti su variabili shared
P_EXACT = 10          # partition number della matrice KW+
C_EXACT = 4           # D^cc deterministico  ->  2^C = 16

# Cap necessario: la saturazione resolution di questo split trova la clausola
# vuota dopo ~94k passi (il cap di default 20000 non basta).
REFUTE_CAP = 200000


def _triangle_f():
    return clique_f(K4_EDGES, 3)


# --------------------------------------------------------------------------- #
#  (a) minterm / maxterm di K4-triangolo                                      #
# --------------------------------------------------------------------------- #
def test_minterms_are_the_four_triangles():
    f = _triangle_f()
    mts = minterms(f, N)
    # 4 triangoli, ciascuno = esattamente 3 archi accesi
    assert len(mts) == 4
    for m in mts:
        assert sum(m) == 3
    # gli archi accesi corrispondono ai 4 triangoli di K4
    as_sets = {frozenset(i for i in range(N) if m[i]) for m in mts}
    expected = {
        frozenset({0, 1, 3}),  # archi 12,13,23  (vertici 1,2,3)
        frozenset({0, 2, 4}),  # archi 12,14,24  (vertici 1,2,4)
        frozenset({1, 2, 5}),  # archi 13,14,34  (vertici 1,3,4)
        frozenset({3, 4, 5}),  # archi 23,24,34  (vertici 2,3,4)
    }
    assert as_sets == expected


def test_maxterms_are_triangle_free_maximal():
    f = _triangle_f()
    Mts = maxterms(f, N)
    assert len(Mts) == 7  # i 7 grafi triangle-free massimali su K4
    for M in Mts:
        assert f(M) == 0  # triangle-free
        # massimale: accendere un arco spento crea un triangolo
        for i in range(N):
            if M[i] == 0:
                y = list(M); y[i] = 1
                assert f(tuple(y)) == 1


def test_kw_matrix_shape_and_nonempty():
    f = _triangle_f()
    mat, rows, cols = kw_plus_matrix(f, N)
    assert len(rows) == 4 and len(cols) == 7
    assert len(mat) == 4 and all(len(r) == 7 for r in mat)
    # ogni entrata non vuota (proprieta' del gioco KW+ per f monotona)
    for r in range(4):
        for c in range(7):
            assert mat[r][c]


# --------------------------------------------------------------------------- #
#  (b) lo split e' UNSAT e l'interpolante computa f su tutti i 64 α           #
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def refuted():
    s = clique_triangle_K4()
    s.check_split()
    ref = dag_refute(s, max_clauses=REFUTE_CAP)
    return s, ref


@pytest.mark.slow
@pytest.mark.timeout(60)
def test_split_unsat_and_interpolant_equals_f(refuted):
    s, ref = refuted
    assert ref.found_empty and not ref.capped
    interp = build_interpolant(s, ref)
    ver = verify_interpolant(s, interp)
    assert ver["ok"], ver["violations"]
    # nessun don't-care: l'interpolante e' FORZATO = f su tutti i 64 input
    f = _triangle_f()
    zs = sorted(s.shared)
    dc = 0
    for bits in product((0, 1), repeat=N):
        z = dict(zip(zs, bits))
        a = _restrict_sat(s.a_clauses, s.shared, s.a_private, z)
        b = _restrict_sat(s.b_clauses, s.shared, s.b_private, z)
        if not a and not b:
            dc += 1
        assert eval_gate(interp.root, z) == f(bits)
    assert dc == 0


@pytest.mark.slow
@pytest.mark.timeout(60)
def test_interpolant_is_monotone_in_z(refuted):
    s, ref = refuted
    interp = build_interpolant(s, ref)
    zs = sorted(s.shared)
    for bits in product((0, 1), repeat=N):
        z = dict(zip(zs, bits))
        v = eval_gate(interp.root, z)
        for i in range(N):
            if bits[i] == 0:
                b2 = list(bits); b2[i] = 1
                z2 = dict(zip(zs, b2))
                assert eval_gate(interp.root, z2) >= v  # monotona crescente


# --------------------------------------------------------------------------- #
#  (c) BUCO-2: lo SCAMBIO della regola privata rompe verify_interpolant       #
# --------------------------------------------------------------------------- #
@pytest.mark.slow
@pytest.mark.timeout(60)
def test_swap_breaks_semantics(refuted):
    """Se l'istanza forza la regola a→OR/b→AND, scambiarla (a→AND/b→OR) DEVE
    far fallire verify_interpolant su almeno un α. Buco-2 del ciclo 3 chiuso."""
    s, ref = refuted
    interp_swapped = build_interpolant_swapped(s, ref)
    ver = verify_interpolant(s, interp_swapped)
    assert not ver["ok"], "FALLIMENTO DI BANCO: lo scambio NON rompe la semantica"
    assert len(ver["violations"]) > 0


# --------------------------------------------------------------------------- #
#  (d) i TRE numeri esatti S, P, C                                             #
# --------------------------------------------------------------------------- #
@pytest.mark.slow
@pytest.mark.timeout(60)
def test_S_exact(refuted):
    s, ref = refuted
    interp = build_interpolant(s, ref)
    assert interp.gate_count == S_EXACT
    assert interp.bool_gates == S_BOOL_EXACT
    assert interp.mux_gates == S_MUX_EXACT


def test_P_exact():
    f = _triangle_f()
    mat, _, _ = kw_plus_matrix(f, N)
    assert partition_number(mat) == P_EXACT


def test_C_exact():
    f = _triangle_f()
    mat, _, _ = kw_plus_matrix(f, N)
    assert dcc(mat) == C_EXACT


def test_discriminant_S_minus_P():
    # Discriminante dichiarato dall'Explorer: S = P = 2^C (a meno di +1) =>
    # RESTATEMENT; S - P > 1 strutturale => segnale di contenuto nuovo.
    # Qui MISURATO: S=19, P=10, 2^C=16  ->  S-P=9 (non +1).
    assert S_EXACT - P_EXACT == 9
    assert 2 ** C_EXACT == 16


# --------------------------------------------------------------------------- #
#  unita': partition_number e dcc su una matrice giocattolo nota              #
# --------------------------------------------------------------------------- #
def test_partition_number_toy():
    # matrice 2x2: tutte le entrate condividono il colore 0 -> 1 rettangolo
    mat = (
        (frozenset({0}), frozenset({0})),
        (frozenset({0}), frozenset({0})),
    )
    assert partition_number(mat) == 1
    assert dcc(mat) == 0  # gia' monocromatica: 0 bit


def test_dcc_toy_two_colors():
    # 2x2 con due colori incompatibili in diagonale: serve 1 split (1 bit)
    mat = (
        (frozenset({0}), frozenset({0})),
        (frozenset({1}), frozenset({1})),
    )
    # le due righe non condividono colore -> Alice manda 1 bit, poi mono
    assert dcc(mat) == 1
    assert partition_number(mat) == 2
