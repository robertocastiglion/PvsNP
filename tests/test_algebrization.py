"""Test del Modulo 7 — Algebrization Sandbox (estensione multilineare + sum-check)."""

import random

import pytest

from pnp_lab.algebrization import (
    Field,
    MultilinearExtension,
    bits,
    count_true,
    is_prime,
    lagrange_eval,
    run_sumcheck,
    sum_over_cube,
)


# ── campo GF(p) ───────────────────────────────────────────────────────────

def test_field_requires_prime():
    Field(97)  # ok
    with pytest.raises(ValueError):
        Field(98)


def test_field_inverse():
    F = Field(97)
    for a in range(1, 97):
        assert F.mul(a, F.inv(a)) == 1


def test_is_prime():
    assert is_prime(2) and is_prime(97) and is_prime(101)
    assert not is_prime(1) and not is_prime(0) and not is_prime(91)


# ── estensione multilineare ───────────────────────────────────────────────

def test_extension_agrees_on_cube():
    F = Field(97)
    # AND a 2 variabili: vero solo su (1,1)
    values = (0, 0, 0, 1)
    ext = MultilinearExtension(values, 2, F)
    assert ext.agrees_on_cube()
    for a in range(4):
        assert ext(bits(a, 2)) == values[a]


def test_extension_is_multilinear():
    F = Field(97)
    values = (0, 1, 1, 0, 1, 0, 0, 1)  # parità a 3 variabili
    ext = MultilinearExtension(values, 3, F)
    assert ext.is_multilinear()


def test_extension_off_cube_nontrivial():
    # fuori dal cubo l'estensione assume valori non booleani (è un vero polinomio)
    F = Field(97)
    values = (0, 0, 0, 1)  # AND -> f~(x,y) = x*y
    ext = MultilinearExtension(values, 2, F)
    assert ext((2, 3)) == 6  # 2*3


def test_extension_bad_length():
    F = Field(97)
    with pytest.raises(ValueError):
        MultilinearExtension((0, 1, 1), 2, F)  # servono 4 valori


# ── interpolazione di Lagrange ────────────────────────────────────────────

def test_lagrange_recovers_linear():
    F = Field(97)
    # retta y = 3x + 5: campioni in 0,1
    xs, ys = [0, 1], [5, F.add(F.mul(3, 1), 5)]
    assert lagrange_eval(F, xs, ys, 10) == F.add(F.mul(3, 10), 5)


# ── sum-check: completezza e soundness ────────────────────────────────────

def _php_like_extension(F):
    # 3 variabili, conta gli assegnamenti veri di una funzione qualsiasi
    values = (0, 1, 1, 0, 1, 1, 0, 1)
    return MultilinearExtension(values, 3, F), values


def test_sumcheck_completeness_honest_accepted():
    F = Field(97)
    ext, values = _php_like_extension(F)
    res = run_sumcheck(ext, 3, F, degree=1, rng=random.Random(1))
    assert res.accepted
    assert res.local_checks_passed
    assert res.final_check
    # la somma sul cubo coincide col numero di assegnamenti veri
    assert res.claimed_sum == count_true(values) == sum_over_cube(ext, 3, F)
    assert res.oracle_queries == 1


def test_sumcheck_soundness_cheater_rejected():
    F = Field(97)
    ext, _ = _php_like_extension(F)
    res = run_sumcheck(ext, 3, F, degree=1, rng=random.Random(1), cheat=True)
    # il bugiardo supera i controlli LOCALI (li forgia) ma fallisce la query finale
    assert res.local_checks_passed
    assert not res.final_check
    assert not res.accepted


def test_sumcheck_soundness_within_bound():
    # La soundness è PROBABILISTICA: un prover disonesto può farcela solo se il
    # punto casuale finale capita su una radice della differenza di polinomi.
    # Bound del protocollo: prob. ≤ 1 - (1 - d/p)^n  (qui ≈ 3/97 ≈ 0.031).
    n, degree = 3, 1
    F = Field(97)
    ext, _ = _php_like_extension(F)
    trials = 200
    accepted = sum(
        int(run_sumcheck(ext, n, F, degree=degree, rng=random.Random(seed), cheat=True).accepted)
        for seed in range(trials)
    )
    bound = 1 - (1 - degree / F.p) ** n  # ≈ 0.031
    # il tasso empirico resta sotto il bound (con un po' di margine statistico)
    assert accepted / trials <= bound * 2.0
    # e la verità di base: l'onesto è SEMPRE accettato, il bugiardo quasi mai
    assert accepted < trials // 10


def test_sumcheck_wrong_sum_caught_in_first_round():
    F = Field(97)
    ext, values = _php_like_extension(F)
    wrong = sum_over_cube(ext, 3, F) + 7
    res = run_sumcheck(ext, 3, F, degree=1, claimed_sum=wrong, rng=random.Random(0))
    # prover onesto ma somma dichiarata sbagliata: il primo controllo locale salta
    assert not res.rounds[0].local_ok
    assert not res.accepted
