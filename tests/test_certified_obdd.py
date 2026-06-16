"""Certified-bounds regime, Cycle 1 — EXPLICIT OBDD family with a PROVABLE order gap.

Congela ESATTAMENTE il SOLO core valido: la ricorrenza certificata good=4,6,8,10 /
bad=4,8,16,32 e il cross-check con min_obdd_size ai due ordini, il gap g(n), la prova
fondante 6!=8.  L'evidenza-MURO del primo draft (A(n), r(n), discriminatore size-matched,
size_pair_determinism) e' STRUCK — era un category error (certified_drop_spread applicato
a UNA singola funzione, arg N-vs-n); vedi la docstring del modulo.  Nessun test la congela.
"""

import pytest

from pnp_lab.meta_complexity import certified_obdd as co
from pnp_lab.meta_complexity import order_locality as ol


# ── la famiglia, il relabel, e i bound certificati ─────────────────────────

def test_family_or_and_small():
    """f_2 = x0 AND x1 -> truth-table 0b1000 = 8 (HARD solo su x=3)."""
    assert co.family_or_and(2) == 0b1000
    # f_4 = (x0&x1)|(x2&x3): bit x acceso sse coppia adiacente (0,1) o (2,3) entrambi 1
    t4 = co.family_or_and(4)
    for x in range(16):
        want = (((x >> 0) & 1) and ((x >> 1) & 1)) or (((x >> 2) & 1) and ((x >> 3) & 1))
        assert ((t4 >> x) & 1) == (1 if want else 0)
    with pytest.raises(ValueError):
        co.family_or_and(3)


def test_permute_vars_is_general_relabel():
    """permute_vars generalizza variable_swap: con perm che scambia i due indici (i,j)
    deve coincidere con order_locality.variable_swap."""
    n = 4
    t = co.family_or_and(n)
    perm = list(range(n))
    perm[1], perm[2] = perm[2], perm[1]
    assert co.permute_vars(t, n, perm) == ol.variable_swap(t, n, 1, 2)
    # identita' = no-op
    assert co.permute_vars(t, n, list(range(n))) == t
    with pytest.raises(ValueError):
        co.permute_vars(t, n, [0, 0, 1, 2])


def test_bad_perm_is_the_interleaved_order():
    """bad_perm realizza l'ordine di lettura interlacciato [0,2,...,n-2,1,3,...,n-1]."""
    assert co.bad_perm(2) == [0, 1]
    assert co.bad_perm(4) == [0, 2, 1, 3]
    assert co.bad_perm(6) == [0, 3, 1, 4, 2, 5]
    assert co.bad_perm(8) == [0, 4, 1, 5, 2, 6, 3, 7]
    assert co.good_perm(6) == [0, 1, 2, 3, 4, 5]


def test_certified_sizes_frozen():
    """I bound CERTIFICATI: good = n+2 = 4,6,8,10 e bad = 2^(n/2+1) = 4,8,16,32 a
    n=2,4,6,8.  Congelati (la ricorrenza, non l'esatto)."""
    assert [co.size_good(n) for n in (2, 4, 6, 8)] == [4, 6, 8, 10]
    assert [co.size_bad(n) for n in (2, 4, 6, 8)] == [4, 8, 16, 32]


def test_gap_frozen():
    """Il gap certificato g(n) = 2^(n/2+1) - (n+2) = 0,2,8,22 a n=2,4,6,8 — istanza
    finita esatta del bound CITATO di Bryant/Wegener (RESTATEMENT #12)."""
    assert [co.gap(n) for n in (2, 4, 6, 8)] == [0, 2, 8, 22]


def test_recurrence_equals_exact_min_obdd_size():
    """ANCHOR DI FEDELTA': la ricorrenza certificata == min_obdd_size esatto a n=2,4,6,8
    ai DUE ordini.  certify_recurrence solleva AssertionError se devia."""
    assert co.certify_recurrence([2, 4, 6, 8]) == [(2, 4, 4), (4, 6, 8), (6, 8, 16), (8, 10, 32)]


def test_founding_witness_6_neq_8_at_n4():
    """LA PROVA FONDANTE: la famiglia a n=4 ha OBDD 6 all'ordine buono e 8 al cattivo —
    6 != 8, lo stesso testimone di Module 22 ((x0&x1)|(x2&x3) vs var 1,2 scambiate)."""
    n = 4
    t = co.family_or_and(n)
    sg = ol.min_obdd_size(co.permute_vars(t, n, co.good_perm(n)), n)
    sb = ol.min_obdd_size(co.permute_vars(t, n, co.bad_perm(n)), n)
    assert (sg, sb) == (6, 8)
    assert sg != sb


def test_measure_table_frozen():
    """La tabella certificata (SOLO il layer di taglia valido): n, good, bad, gap."""
    rows = co.measure([2, 4, 6, 8])
    assert [r.n for r in rows] == [2, 4, 6, 8]
    assert [r.size_good for r in rows] == [4, 6, 8, 10]
    assert [r.size_bad for r in rows] == [4, 8, 16, 32]
    assert [r.gap for r in rows] == [0, 2, 8, 22]
