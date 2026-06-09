"""Test per il Modulo 16 — Bounded Observer.

Verifichiamo, in modo ESATTO sulle istanze minuscole:
  - il funzionale Δ è ben definito e simmetrico/in [0,1];
  - RELATIVIZZAZIONE: Δ della classe a ≤ t query booleane = t/N (query complexity);
  - ALGEBRIZZAZIONE: una query algebrica batte una booleana (𝒜_alg ⊋ 𝒜_rel), e il
    lemma di Schwartz–Zippel vale (agreement ≤ k/p) sull'istanza;
  - NATURAL PROOFS: il riuso del Modulo 15 dà un Δ in [0,1] (informazione satura);
  - PROOF COMPLEXITY: il template FALLISCE — il lato D0 è IDENTICAMENTE 0 (sanità),
    resolution è sound (mai refuta una formula soddisfacibile) e completa sulle
    insoddisfacibili tiny; la quantità reale è una LUNGHEZZA (intero), non un ε.
"""

import pytest

from pnp_lab.bounded_observer import (
    advantage,
    algebrization_one_query_advantage,
    class_advantage,
    is_satisfiable,
    natural_proofs_advantage,
    proof_complexity_probe,
    proof_complexity_worlds,
    proof_system_observer,
    refutation_depth,
    relativization_advantage,
    relativization_worlds,
    schwartz_zippel_agreement,
    unified_report,
    unified_summary,
    verdict_note,
)
from pnp_lab.bounded_observer.observer import _resolve


# ── Δ, il funzionale unico ───────────────────────────────────────────────────

def test_advantage_basic_properties():
    d0, d1 = relativization_worlds(4)
    # osservatore costante: nessun vantaggio
    assert advantage(lambda w: 0, d0, d1) == 0.0
    assert advantage(lambda w: 1, d0, d1) == 0.0
    # un valore di Δ è sempre in [0,1]
    val = advantage(lambda w: 1 if w else 0, d0, d1)
    assert 0.0 <= val <= 1.0


def test_class_advantage_is_supremum():
    d0, d1 = relativization_worlds(4)
    a = lambda w: 0
    b = lambda w: 1 if (0 in w) else 0          # interroga il punto 0
    assert class_advantage([a, b], d0, d1) == max(
        advantage(a, d0, d1), advantage(b, d0, d1)
    )


# ── (1) Relativizzazione: Δ = t/N ────────────────────────────────────────────

@pytest.mark.parametrize("n,t", [(4, 0), (4, 1), (4, 2), (5, 1), (6, 2)])
def test_relativization_advantage_equals_t_over_n(n, t):
    assert relativization_advantage(n, t) == pytest.approx(t / n)


def test_relativization_decreases_with_domain():
    # a budget fisso, più grande il dominio, più piccolo Δ (→ 0 asintotico)
    assert relativization_advantage(8, 1) < relativization_advantage(4, 1)


# ── (2) Algebrizzazione: interfaccia più ricca + Schwartz–Zippel ─────────────

def test_algebraic_query_beats_boolean_query():
    adv_alg, adv_bool = algebrization_one_query_advantage(k=3, p=5)
    # UNA query algebrica distingue perfettamente; una booleana vede solo 1/N
    assert adv_alg == pytest.approx(1.0)
    assert adv_bool == pytest.approx(1.0 / 8)
    assert adv_alg > adv_bool                    # 𝒜_alg ⊋ 𝒜_rel


def test_schwartz_zippel_bound_holds():
    k, p = 2, 7
    # due polinomi multilineari distinti su 2 variabili
    a = {frozenset(): 1, frozenset({0}): 1}                 # 1 + x0
    b = {frozenset(): 1, frozenset({1}): 1}                 # 1 + x1
    agree = schwartz_zippel_agreement(a, b, k, p)
    assert agree <= k / p + 1e-12                # lemma: ≤ deg/|F| ≤ k/p
    # polinomi identici: coincidono ovunque
    assert schwartz_zippel_agreement(a, a, k, p) == pytest.approx(1.0)


# ── (3) Natural proofs: riuso Modulo 15 ──────────────────────────────────────

def test_natural_proofs_advantage_in_unit_interval():
    val = natural_proofs_advantage(s=3)
    assert 0.0 <= val <= 1.0
    # informazione satura + più calcolo non può ridurre il vantaggio
    assert natural_proofs_advantage(s=3) >= natural_proofs_advantage(s=1) - 1e-12


# ── (4) Proof complexity: il template fallisce ───────────────────────────────

def test_resolution_is_sound_on_satisfiable_formulas():
    # nessuna formula soddisfacibile è refutabile a QUALUNQUE profondità
    d0, _ = proof_complexity_worlds()
    for world, _ in d0:
        clauses = [frozenset(c) for c in world]
        assert is_satisfiable(clauses)
        assert refutation_depth(clauses, max_depth=20) is None


def test_resolution_is_complete_on_tiny_unsat():
    _, d1 = proof_complexity_worlds()
    for world, _ in d1:
        clauses = [frozenset(c) for c in world]
        assert not is_satisfiable(clauses)
        depth = refutation_depth(clauses, max_depth=20)
        assert depth is not None and depth >= 1     # esiste, ed è un INTERO


def test_resolve_rejects_tautological_resolvent():
    # risolvendo (x ∨ y) e (¬x ∨ ¬y) sul pivot x si otterrebbe (y ∨ ¬y): scartata
    c1 = frozenset({1, 2})
    c2 = frozenset({-1, -2})
    assert _resolve(c1, c2) is None
    # pivot unico e pulito: (x) e (¬x ∨ y) → (y)
    assert _resolve(frozenset({1}), frozenset({-1, 2})) == frozenset({2})


def test_proof_complexity_template_fails():
    probe = proof_complexity_probe()
    # (a) PRIMO punto di rottura: il lato D0 è IDENTICAMENTE 0 (sanità) → niente ε
    assert probe.d0_acceptance == 0.0
    # (b) Δ degenera nel solo lato D1 ed è monotòno nel budget
    deltas = [d for _, d in probe.delta_by_budget]
    assert all(later >= earlier - 1e-12 for earlier, later in zip(deltas, deltas[1:]))
    # (c) la quantità reale è una lunghezza (intero) per ogni mondo UNSAT
    assert all(m is None or isinstance(m, int) for m in probe.min_lengths)
    assert any(isinstance(m, int) for m in probe.min_lengths)


def test_d0_acceptance_is_zero_at_every_budget():
    d0, _ = proof_complexity_worlds()
    for t in range(0, 8):
        acc = sum(p for w, p in d0 if proof_system_observer(t)(w))
        assert acc == 0.0


# ── rendering ────────────────────────────────────────────────────────────────

def test_reports_render():
    assert "Δ" in unified_summary()
    rep = unified_report()
    assert "RELATIVIZZAZIONE" in rep and "PROOF COMPLEXITY" in rep
    assert "NON RIENTRA" in rep
    v = verdict_note()
    assert "PRIMO PUNTO DI FALLIMENTO" in v
