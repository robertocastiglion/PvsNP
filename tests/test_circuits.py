"""Test del Modulo 6 — Circuit Complexity Sandbox."""

from pnp_lab.circuits import (
    AND,
    NOT,
    OR,
    dnf_size,
    mask_for,
    min_formula_sizes,
    parity_dnf_lower_bound,
    parity_growth,
    parity_table,
    projection,
    prime_implicants,
)


# ── truth table di base ──────────────────────────────────────────────────

def test_projection_n2():
    # x0 vale 1 su input 01 e 11 -> bit 1 e 3 -> 0b1010 = 10
    assert projection(2, 0) == 0b1010
    # x1 vale 1 su input 10 e 11 -> bit 2 e 3 -> 0b1100 = 12
    assert projection(2, 1) == 0b1100


def test_and_or_not_consistent():
    n = 2
    x0, x1 = projection(n, 0), projection(n, 1)
    assert AND(x0, x1) == (x0 & x1)
    assert OR(x0, x1) == (x0 | x1)
    assert NOT(x0, n) == ((~x0) & mask_for(n))
    # x0 ∧ ¬x0 = funzione costante 0
    assert AND(x0, NOT(x0, n)) == 0
    # x0 ∨ ¬x0 = costante 1 (tutti i 2^n bit)
    assert OR(x0, NOT(x0, n)) == mask_for(n)


def test_parity_table_n2():
    # parità su 2 var: 1 su input 01 e 10 (peso dispari) -> bit 1 e 2 -> 0b0110 = 6
    assert parity_table(2) == 0b0110


# ── complessità di formula esatta (Shannon) ──────────────────────────────

def test_formula_sizes_complete_small():
    ct = min_formula_sizes(2)
    assert ct.complete                       # tutte le 16 funzioni coperte
    assert ct.num_functions == 16
    # i letterali hanno costo 0
    assert ct.cost[projection(2, 0)] == 0
    # le costanti emergono con un gate (x ∧ ¬x)
    assert ct.cost[0] == 1
    assert ct.cost[mask_for(2)] == 1


def test_formula_sizes_n3_complete():
    ct = min_formula_sizes(3)
    assert ct.complete
    assert ct.num_functions == 256
    assert ct.max_cost >= 4                   # le funzioni più dure di 3 var


def test_distribution_sums_to_total():
    ct = min_formula_sizes(3)
    assert sum(ct.distribution().values()) == ct.num_functions


def test_most_functions_are_hard():
    # Shannon in piccolo: le funzioni 'facili' (taglia <= 1) sono una minoranza.
    ct = min_formula_sizes(3)
    easy = sum(c for s, c in ct.distribution().items() if s <= 1)
    assert easy < ct.num_functions / 2


# ── lower bound esatto della parità in profondità 2 ──────────────────────

def test_parity_dnf_lower_bound_tight():
    for n in range(2, 6):
        lb = parity_dnf_lower_bound(n)
        assert lb.num_prime_implicants == (1 << (n - 1))   # 2^(n-1)
        assert lb.all_full_width
        assert lb.is_tight


def test_parity_dnf_grows_exponentially():
    rows = parity_growth(max_n=6)
    terms = [r.dnf_terms for r in rows]
    # raddoppia a ogni variabile in più
    for i in range(len(terms) - 1):
        assert terms[i + 1] == 2 * terms[i]
    assert all(r.tight for r in rows)


def test_easy_functions_have_small_dnf():
    # AND di 2 variabili: un solo implicante primo (la DNF è un termine).
    n = 2
    and_table = AND(projection(n, 0), projection(n, 1))
    assert dnf_size(and_table, n) == 1
    # contrasto con la parità: 2 termini su 2 variabili
    assert dnf_size(parity_table(n), n) == 2


def test_prime_implicants_parity_no_merge():
    # Tutti gli implicanti primi della parità sono minterm a larghezza piena.
    n = 4
    primes = prime_implicants(parity_table(n), n)
    assert len(primes) == 8                              # 2^(4-1)
    assert all(all(v is not None for v in p) for p in primes)
