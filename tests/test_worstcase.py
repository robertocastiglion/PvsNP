"""Test della strada #2 — enunciato di caso peggiore (∃/∀): utilità-larghezza e
collisioni di feature (ostruzione distribution-free)."""

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.enriched_meta import (
    feature_collisions,
    useful_largeness,
    worstcase_summary,
)
from pnp_lab.enriched_meta.recognize_class import critical_window


def test_feature_collisions_invariant_n3():
    ct = min_formula_sizes(3)
    win = critical_window(ct.cost, 3, half_width=1)
    fc = feature_collisions(ct.cost, 3, 3, win)
    assert fc.num_hard > 0
    assert 0.0 <= fc.collision_fraction <= 1.0
    assert fc.colliding_hard <= fc.num_hard
    # il tetto alla larghezza utile è esattamente 1 − frazione di collisioni
    assert abs(fc.max_useful_largeness - (1.0 - fc.collision_fraction)) < 1e-12


def test_useful_largeness_is_bounded_by_collisions():
    ct = min_formula_sizes(3)
    win = critical_window(ct.cost, 3, half_width=1)
    fc = feature_collisions(ct.cost, 3, 3, win)
    ul = useful_largeness(ct.cost, 3, 3, depth=3, stratum=win)
    # una proprietà utile non può isolare più dure di quante non collidano
    assert ul.useful_largeness <= fc.max_useful_largeness + 1e-9
    assert 0 <= ul.isolable_hard <= ul.num_hard


def test_useful_largeness_non_decreasing_in_depth():
    ct = min_formula_sizes(3)
    win = critical_window(ct.cost, 3, half_width=1)
    vals = [useful_largeness(ct.cost, 3, 3, d, win).useful_largeness for d in (1, 2, 3)]
    assert all(vals[i] <= vals[i + 1] + 1e-9 for i in range(len(vals) - 1))


def test_depth_zero_useful_largeness_is_zero_on_mixed_window():
    # con foglia unica e finestra mista (facili+dure), l'utilità impone di rifiutare
    ct = min_formula_sizes(3)
    win = critical_window(ct.cost, 3, half_width=1)
    ul = useful_largeness(ct.cost, 3, 3, depth=0, stratum=win)
    assert ul.useful_largeness == 0.0


def test_worstcase_summary_is_honest():
    w = worstcase_summary()
    assert "counting" in w.counting_argument.lower() or "pigeonhole" in w.counting_argument.lower()
    assert "razborov" in w.relation_to_theory.lower()
    # dichiara esplicitamente che come nuovo invariante riduce a (B)/barriera nota
    assert "(b)" in w.honest_limit.lower() or "rid" in w.honest_limit.lower()
