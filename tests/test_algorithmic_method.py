"""Test del Modulo 12 — Algorithmic Method Lab (Williams: SAT veloce ⇒ lower bound)."""

from pnp_lab.algorithmic_method import (
    analyze_all,
    conj_poly,
    count_bruteforce,
    count_fast,
    disjoint_dnf_poly,
    evasion_report,
    or_poly,
    speedup_factor,
    standard_speedups,
    win_win,
)


# ── lo speedup è ESATTO (sound): forza bruta == metodo polinomiale ────────

def test_fast_matches_bruteforce_conj():
    poly = conj_poly(3, 12)
    assert count_bruteforce(poly).value == count_fast(poly).value
    # AND di 3 letterali su 12 var: 2^(12-3) = 512 assegnamenti veri
    assert count_fast(poly).value == 512


def test_fast_matches_bruteforce_dnf():
    poly = disjoint_dnf_poly([[0, 1, 2], [3, 4, 5]], 12)
    b, f = count_bruteforce(poly), count_fast(poly)
    assert b.value == f.value
    # inclusione-esclusione: 2^9 + 2^9 - 2^6 = 960
    assert f.value == 960


def test_fast_matches_bruteforce_dense():
    poly = or_poly(10)
    b, f = count_bruteforce(poly), count_fast(poly)
    assert b.value == f.value == (1 << 10) - 1


# ── lo speedup dipende dalla STRUTTURA (sparsità), non da n ───────────────

def test_structured_is_faster():
    poly = conj_poly(2, 16)
    # un solo monomio: enormemente meno operazioni della forza bruta
    assert count_fast(poly).ops == 1
    assert count_bruteforce(poly).ops == (1 << 16)
    assert speedup_factor(poly) > 1000


def test_dense_gives_no_speedup():
    poly = or_poly(12)
    # OR via inclusione-esclusione è denso (2^n - 1 monomi): nessun guadagno
    assert poly.sparsity == (1 << 12) - 1
    assert speedup_factor(poly) <= 1.01


def test_speedup_scales_with_terms_not_n():
    # stessa struttura (2 gruppi → 3 monomi) a n diversi: la sparsità non cresce con n
    p1 = disjoint_dnf_poly([[0, 1], [2, 3]], 8)
    p2 = disjoint_dnf_poly([[0, 1], [2, 3]], 18)
    assert p1.sparsity == p2.sparsity == 3
    assert speedup_factor(p2) > speedup_factor(p1)  # n più grande ⇒ speedup maggiore


# ── la catena win-win: la soglia è super-polinomiale ──────────────────────

def test_win_win_threshold_superpoly():
    results = {w.speedup.label: w for w in analyze_all()}
    # nessuno speedup e poly: niente lower bound
    assert not any(w.lower_bound for w in analyze_all() if not w.speedup.superpolynomial)
    # super-poly: lower bound
    assert all(w.lower_bound for w in analyze_all() if w.speedup.superpolynomial)


def test_polynomial_speedup_insufficient():
    poly_speedup = next(s for s in standard_speedups() if "n^3" in s.label)
    assert not poly_speedup.superpolynomial
    assert not win_win(poly_speedup).lower_bound


def test_williams_speedup_sufficient():
    williams = next(s for s in standard_speedups() if "Williams" in s.label)
    assert williams.superpolynomial
    assert win_win(williams).lower_bound


# ── aggira tutte e tre le barriere ────────────────────────────────────────

def test_evades_all_three_barriers():
    report = evasion_report()
    assert len(report) == 3
    assert all(b.evaded for b in report)
    names = " ".join(b.barrier for b in report).lower()
    assert "relativizzazione" in names and "natural proofs" in names and "algebrizzazione" in names
