"""Test del Modulo 13 — Meta-Complexity Lab (MCSP & hardness magnification)."""

from pnp_lab.circuits import parity_table
from pnp_lab.meta_complexity import (
    analyze_link,
    complexity_map,
    hard_property,
    is_useful,
    largeness,
    magnification_results,
    mcsp_decide,
    mcsp_threshold,
    mcsp_witness,
    np_certificate,
    threshold_gap,
)


# ── MCSP calcolato esatto (riuso del Modulo 6) ────────────────────────────

def test_complexity_map_complete_n3():
    ct = complexity_map(3)
    assert ct.complete
    assert ct.num_functions == 256
    assert len(ct.cost) == 256


def test_mcsp_decide_and_witness():
    ct = complexity_map(3)
    # una variabile (proiezione) ha dimensione 0 → MCSP[0] = YES
    x0 = next(t for t, c in ct.cost.items() if c == 0)
    assert mcsp_decide(ct, x0, 0)
    size, formula = mcsp_witness(ct, x0)
    assert size == 0 and isinstance(formula, str)


def test_parity_is_a_hard_instance():
    ct = complexity_map(3)
    par = parity_table(3)
    # la parità è tra le più dure: MCSP[s] = NO per s piccolo, YES per s grande
    cost = ct.cost[par]
    assert cost >= 3
    assert not mcsp_decide(ct, par, cost - 1)
    assert mcsp_decide(ct, par, cost)


def test_np_certificate_poly_in_N():
    cert = np_certificate(n=3, s=4)
    assert cert.input_length_N == 8          # N = 2^3
    assert cert.verify_evaluations == 8       # verifica = N valutazioni
    assert cert.poly_in_N


def test_threshold_shows_hard_majority_for_small_s():
    ct = complexity_map(3)
    rows = mcsp_threshold(ct)
    # per s piccolo la stragrande maggioranza delle funzioni è dura (Shannon)
    assert rows[0].hard_fraction > 0.9       # s=0: solo i letterali sono facili
    assert any(r.hard_fraction > 0.5 for r in rows)
    # la frazione dura è non-crescente in s, e all'ultima soglia tutte sono facili
    fr = [r.hard_fraction for r in rows]
    assert all(fr[i] >= fr[i + 1] for i in range(len(fr) - 1))
    assert rows[-1].hard == 0


# ── legame MCSP ↔ Natural Proofs (esatto) ─────────────────────────────────

def test_hard_property_is_useful_and_large():
    ct = complexity_map(3)
    s = 3
    prop = hard_property(ct, s)
    # UTILE: rifiuta tutte le funzioni facili (dim ≤ s)
    assert is_useful(prop, ct, s)
    # LARGA: una frazione cospicua delle funzioni
    assert largeness(prop, ct) > 0.5


def test_analyze_link_conclusion():
    ct = complexity_map(3)
    link = analyze_link(ct, 3)
    assert link.useful
    assert 0.0 < link.large_fraction <= 1.0
    assert "MCSP" in link.constructive_cost
    assert "Razborov" in link.conclusion or "PRG" in link.conclusion


# ── hardness magnification (citata, ben formata) ──────────────────────────

def test_magnification_results_present():
    facts = magnification_results()
    assert len(facts) >= 2
    assert all(f.reference and f.implies and f.weak_lower_bound for f in facts)
    # almeno uno collega un LB minuscolo a una separazione maggiore
    joined = " ".join(f.implies for f in facts)
    assert "NP" in joined or "EXP" in joined


def test_threshold_gap_honest():
    gap = threshold_gap()
    assert "n^{1+" in gap.magnifying_threshold
    assert "non-natural" in gap.why_uncrossed.lower() or "magnificazione" in gap.why_uncrossed.lower()
