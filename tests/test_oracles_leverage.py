"""Cycle 1 del programma "Relativization Obstruction as a Leverage Operator".

Test esatti e deterministici: l'altezza dell'ostruzione depth(OR)=2^n verificata da una
ricorsione DT generica (n<=3), il lemma della riserva, headroom/break-even, e la
pianificazione online delle lunghezze (riuso della diagonalizzazione BGS verificata).
"""

from pnp_lab.oracles import leverage as lev
from pnp_lab.oracles.separation import EXAMPLE_MACHINES


# ── altezza dell'ostruzione: depth(OR) su 2^n variabili ────────────────────

def test_dt_depth_of_or_equals_num_vars():
    """VERIFICA (non assume) che la profondità DT dell'OR su m variabili è m, per m piccolo
    — il lemma della riserva di BGS reso esatto dalla ricorsione generica."""
    for m in (1, 2, 3, 4, 5, 6):
        assert lev._dt_depth(lev._or_truth_table(m), m) == m


def test_obstruction_height_is_slice_size():
    """L'altezza dell'ostruzione al livello n è 2^n (verificata per n<=3)."""
    for n in (1, 2, 3):
        assert lev.or_decision_tree_depth(n) == (1 << n)


def test_dt_depth_constant_is_zero():
    assert lev._dt_depth((0, 0, 0, 0), 2) == 0
    assert lev._dt_depth((1, 1, 1, 1), 2) == 0


def test_dt_depth_single_variable():
    """f = x0 (su 2 variabili) ha profondità 1: basta leggere x0."""
    # tavola: indice = x1 x0 ; f = x0  -> [0,1,0,1]
    assert lev._dt_depth((0, 1, 0, 1), 2) == 1


# ── il lemma della riserva ─────────────────────────────────────────────────

def test_reservation_can_fool_iff_budget_below_slice():
    r = lev.reservation(4, 7)            # 2^4 = 16, budget 7
    assert r.free_strings == 9 and r.can_be_fooled
    r2 = lev.reservation(3, 8)           # 2^3 = 8, budget 8 = slice -> NON ingannabile
    assert r2.free_strings == 0 and not r2.can_be_fooled


# ── la scala della leva: headroom e break-even ─────────────────────────────

def test_headroom_values():
    assert lev.headroom(4, 2) == 16 - 16    # == 0 : n^2 raggiunge la slice a n=4
    assert lev.headroom(5, 2) == 32 - 25    # == 7
    assert lev.headroom(1, 1) == 2 - 1      # == 1


def test_break_even_lengths():
    """n*(k) = min n con 2^n > n^k.  k=1: 2^1=2>1 -> n*=1; k=2: 2^5=32>25 -> n*=5;
    k=3: 2^n>n^3 prima a n=10 (1024>1000)."""
    assert lev.break_even_length(1) == 1
    assert lev.break_even_length(2) == 5
    assert lev.break_even_length(3) == 10


def test_leverage_staircase_shape():
    rows = {r.n: r for r in lev.leverage_staircase((1, 2, 3, 4), (1, 2, 3))}
    assert rows[4].obstruction_height == 16
    assert rows[4].slice_size == 16
    # h(n,1) = 2^n - n : cresce 1,2,5,12
    assert tuple(rows[n].headroom_k[0] for n in (1, 2, 3, 4)) == (1, 2, 5, 12)


# ── il candidato non-collassante: pianificazione online ────────────────────

def test_freshness_schedule_defeats_all_and_matches_greedy():
    """La diagonalizzazione sconfigge tutte le macchine di esempio E la sua pianificazione
    online delle lunghezze coincide con l'aritmetica greedy dei budget — il candidato
    cross-stadio si riduce all'aritmetica (esito RESTATEMENT atteso, qui congelato)."""
    fs = lev.freshness_schedule(EXAMPLE_MACHINES)
    assert fs.all_defeated
    assert fs.matches_greedy
    assert fs.lengths == fs.greedy_lengths


def test_honesty_note_has_no_pvsnp_claim():
    note = lev.honesty_note()
    assert "No separation, no P vs NP claim" in note
