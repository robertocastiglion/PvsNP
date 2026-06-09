"""Test per il Modulo 17 — Survival Test (𝒭=∞).

Verifichiamo, in modo ESATTO sulle istanze minuscole, il criterio
Δ(𝒭=∞) ≷ 1 che classifica le barriere:
  - RELATIVIZZAZIONE: Δ(𝒭=∞) = t/N < 1 (il calcolo illimitato è inerte) ⟹
    information-theoretic, SOPRAVVIVE;
  - NATURAL PROOFS: Δ a 𝒭=∞ è 1 (l'indicatore del predicato 'duro' separa
    perfettamente) mentre a calcolo limitato è < 1 ⟹ computational, NON sopravvive;
  - il classificatore e il margine sono coerenti col criterio;
  - la curva Δ(ℓ=3, s) è monotòna non decrescente.
"""

import pytest

from pnp_lab.survival_test import (
    SurvivalResult,
    classify,
    criterion_summary,
    natural_proofs_curve,
    natural_proofs_survival,
    natural_proofs_unbounded_advantage,
    relativization_survival,
    survival_report,
    survival_results,
    verdict_note,
)
from pnp_lab.distinguishing import default_split


# ── il classificatore ────────────────────────────────────────────────────────

def test_classify_below_one_is_information_theoretic():
    r = classify("x", "𝒜", delta_bounded=0.25, delta_unbounded=0.25)
    assert r.kind == "information-theoretic"
    assert r.survives
    assert r.margin == pytest.approx(0.75)


def test_classify_at_one_is_computational():
    r = classify("y", "𝒭", delta_bounded=0.3, delta_unbounded=1.0)
    assert r.kind == "computational"
    assert not r.survives
    assert r.margin == pytest.approx(0.0)


# ── (1) Relativizzazione: sopravvive (informazione) ──────────────────────────

@pytest.mark.parametrize("n,t", [(8, 1), (8, 2), (8, 3), (4, 1)])
def test_relativization_unbounded_advantage_is_t_over_n(n, t):
    r = relativization_survival(n, t)
    # 𝒭 è già illimitato nella classe del Modulo 16, eppure Δ = t/N
    assert r.delta_compute_unbounded == pytest.approx(t / n)
    assert r.delta_compute_bounded == pytest.approx(t / n)   # il calcolo è inerte


def test_relativization_is_information_theoretic_and_survives():
    r = relativization_survival(8, 2)
    assert isinstance(r, SurvivalResult)
    assert r.kind == "information-theoretic"
    assert r.axis.startswith("𝒜")
    assert r.survives and r.margin > 0.0


# ── (2) Natural proofs: NON sopravvive (calcolo) ─────────────────────────────

def test_natural_proofs_unbounded_advantage_is_one():
    # con 𝒭=∞ l'indicatore di 'duro' (funzione della truth table) separa al 100%
    split = default_split()
    assert natural_proofs_unbounded_advantage(split) == pytest.approx(1.0)


def test_natural_proofs_bounded_advantage_is_strictly_below_one():
    # a calcolo limitato il vantaggio è ben sotto 1 (è il bound della barriera)
    curve = natural_proofs_curve((1, 2, 3))
    assert all(0.0 <= d < 1.0 for _, d in curve)


def test_natural_proofs_curve_is_monotone_nondecreasing():
    curve = natural_proofs_curve((1, 2, 3))
    deltas = [d for _, d in curve]
    assert all(b >= a - 1e-12 for a, b in zip(deltas, deltas[1:]))


def test_natural_proofs_is_computational_and_does_not_survive():
    r = natural_proofs_survival((1, 2, 3))
    assert r.kind == "computational"
    assert r.axis.startswith("𝒭")
    assert not r.survives
    assert r.margin == pytest.approx(0.0)
    # il bound a calcolo limitato è strettamente sotto il valore a 𝒭=∞
    assert r.delta_compute_bounded < r.delta_compute_unbounded


# ── il contrasto: i due poli cadono in famiglie diverse ──────────────────────

def test_two_poles_classified_into_different_families():
    rel, npr = survival_results()
    assert rel.kind == "information-theoretic"
    assert npr.kind == "computational"
    assert rel.survives and not npr.survives


# ── rendering ────────────────────────────────────────────────────────────────

def test_reports_render():
    assert "𝒭=∞" in criterion_summary()
    rep = survival_report()
    assert "RELATIVIZZAZIONE" in rep and "NATURAL PROOFS" in rep
    assert "SOPRAVVIVE" in rep
    v = verdict_note()
    assert "VERDETTO" in v and "PSEUDOCASUALITÀ" in v
