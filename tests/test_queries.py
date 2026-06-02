"""Test della strada #3 — certificate/query complexity della durezza."""

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.enriched_meta import (
    certificate_summary,
    exact_min_separating_set,
    greedy_separating_set,
    separates,
)
from pnp_lab.enriched_meta.recognize_class import critical_window


def test_full_coordinate_set_always_separates():
    # leggere TUTTA la tavola di verità distingue funzioni diverse ⇒ separa sempre
    ct = min_formula_sizes(3)
    win = critical_window(ct.cost, 3, half_width=1)
    items = [(tt, ct.cost[tt] > 3) for tt in win]
    assert separates(range(8), items)


def test_exact_min_n3_needs_whole_truth_table():
    # risultato esatto: a n=3, sullo strato critico, servono tutte le 8 coordinate
    ct = min_formula_sizes(3)
    win = critical_window(ct.cost, 3, half_width=1)
    res = exact_min_separating_set(ct.cost, 3, 3, win)
    assert res.exact and res.separable
    assert res.size == 8
    assert res.fraction == 1.0


def test_greedy_is_upper_bound_on_exact():
    ct = min_formula_sizes(3)
    win = critical_window(ct.cost, 3, half_width=1)
    g = greedy_separating_set(ct.cost, 3, 3, win)
    e = exact_min_separating_set(ct.cost, 3, 3, win)
    assert g.separable and e.separable
    assert g.size >= e.size            # il greedy non può battere il minimo esatto


def test_mmax_gives_lower_bound_when_not_separable():
    # nessun sottoinsieme di taglia ≤ 3 separa a n=3 ⇒ separable False (min > 3)
    ct = min_formula_sizes(3)
    win = critical_window(ct.cost, 3, half_width=1)
    res = exact_min_separating_set(ct.cost, 3, 3, win, mmax=3)
    assert res.exact and not res.separable
    assert res.size == 3


def test_certificate_summary_is_honest():
    c = certificate_summary()
    assert "nessun risultato nuovo" in c.honest_limit.lower()
    assert "certificat" in c.relation_to_theory.lower() or "query" in c.relation_to_theory.lower()
