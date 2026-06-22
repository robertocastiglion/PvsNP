"""Test ESATTI della lente door-C (Entry 32): leva cross-livello del lifting come
crescita del gap di integralita'  G_k = Cov(M_k) - LP(M_k).

Tutto su istanze minuscole (k <= 3, matrici <= 8x8), aritmetica razionale esatta
(Fraction).  I test che spazzano TUTTE le 54 celle a k=3 (alcune dense, set-cover
generico costoso) sono marcati `slow`; i test veloci usano la forma chiusa esatta
per le SOLE celle con gap (J - I_8) e verificano leggi/ancora/closed-form.
"""

from fractions import Fraction

import pytest

from pnp_lab.exactness_composes.compose import lift_named
from pnp_lab.exactness_composes.gap import cover_number, frac_cover, as_matrix
from pnp_lab.exactness_composes.integrality_leverage import (
    ji_cover_number,
    ji_frac_cover,
    gap_at,
    gap_sequence,
    leverage_row,
    law_multiplicative,
    law_affine,
    law_poly_gadget,
    killer_table,
    doorC_candidates,
    DEFAULT_OUTERS,
    DEFAULT_GADGETS,
)


def _JI(m):
    return as_matrix([[0 if i == j else 1 for j in range(m)] for i in range(m)])


# --- forma chiusa J - I_m vs risolutore generico ------------------------------

def test_ji_closed_form_matches_generic_small():
    """Cov/LP della forma chiusa J - I_m == risolutore generico per m = 2..6."""
    for m in range(2, 7):
        M = _JI(m)
        assert ji_cover_number(m) == cover_number(M), f"Cov mismatch m={m}"
        assert ji_frac_cover(m) == frac_cover(M), f"LP mismatch m={m}"


def test_ji_closed_form_values():
    """Valori ESATTI noti della forma chiusa (Cov, LP) per m = 2..8."""
    assert [ji_cover_number(m) for m in range(2, 9)] == [2, 3, 4, 4, 4, 5, 5]
    assert [ji_frac_cover(m) for m in range(2, 9)] == [
        Fraction(2), Fraction(3), Fraction(3),
        Fraction(10, 3), Fraction(10, 3), Fraction(7, 2), Fraction(7, 2),
    ]


def test_ji8_cover_constructive_upper_bound():
    """Cov(J - I_8) <= 5 per costruzione esplicita (Sperner): copre tutte le coppie."""
    from itertools import combinations
    from math import comb

    m = 8
    d = ji_cover_number(m)  # = 5
    codes = list(combinations(range(d), d // 2))[:m]
    covered = set()
    for t in range(d):
        R = [i for i in range(m) if t in codes[i]]
        C = [j for j in range(m) if t not in codes[j]]
        for i in R:
            for j in C:
                covered.add((i, j))
    allpairs = {(i, j) for i in range(m) for j in range(m) if i != j}
    assert covered == allpairs
    assert d == 5


# --- ancora nota Modulo 18: OR ∘ XOR a k=2 -> J - I_4, Cov=4, LP=3, G_2=1 ------

def test_anchor_or_xor_k2():
    """SANITY: OR ∘ XOR a k=2 riproduce l'ancora del Modulo 18 (J - I_4)."""
    row = leverage_row("OR", "XOR")
    assert row["Cov2"] == 4
    assert row["LP2"] == Fraction(3)
    assert row["G2"] == Fraction(1)


def test_anchor_or_xor_full_sequence():
    """La sequenza (G_1, G_2, G_3) di OR ∘ XOR e' (0, 1, 3/2) ESATTA."""
    seq = gap_sequence("OR", "XOR", (1, 2, 3))
    assert seq[1] == Fraction(0)
    assert seq[2] == Fraction(1)
    assert seq[3] == Fraction(3, 2)


def test_gap_at_or_xor_k3_is_three_halves():
    """G_3(OR, XOR) = Cov(J - I_8) - LP(J - I_8) = 5 - 7/2 = 3/2."""
    assert gap_at("OR", "XOR", 3) == Fraction(3, 2)


# --- le tre leggi di composizione (killer) ------------------------------------

def test_laws_predicates_basic():
    g1, g2 = Fraction(0), Fraction(1)
    # moltiplicativa: G_2^2 = 1
    assert law_multiplicative(g1, g2, Fraction(1)) is True
    assert law_multiplicative(g1, g2, Fraction(3, 2)) is False
    # affine: 2*G_2 - G_1 = 2
    assert law_affine(g1, g2, Fraction(2)) is True
    assert law_affine(g1, g2, Fraction(3, 2)) is False
    # poly-del-gadget: 2 * gadget_g2 = 2*1 = 2
    assert law_poly_gadget(g1, g2, Fraction(2), Fraction(1)) is True
    assert law_poly_gadget(g1, g2, Fraction(3, 2), Fraction(1)) is False


def test_doorC_candidate_cells_not_killed():
    """Le 4 celle a gap (OR/NAND x XOR/EQ): G_3 = 3/2 NON ricostruito da nessuna
    delle 3 leggi (mult=1, affine=2, poly=2 != 3/2)."""
    for fname, gname in (("OR", "XOR"), ("OR", "EQ"), ("NAND", "XOR"), ("NAND", "EQ")):
        g1 = gap_at(fname, gname, 1)
        g2 = gap_at(fname, gname, 2)
        g3 = gap_at(fname, gname, 3)
        assert (g1, g2, g3) == (Fraction(0), Fraction(1), Fraction(3, 2))
        assert not law_multiplicative(g1, g2, g3)
        assert not law_affine(g1, g2, g3)
        # gadget_g2 caratteristico = max G_2 per quel gadget = 1
        assert not law_poly_gadget(g1, g2, g3, Fraction(1))


def test_killer_table_on_candidate_outers_only():
    """killer_table ristretta a {OR, NAND} x {XOR, EQ}: tutte e 4 door-C candidate,
    nessuna killed.  (Veloce: solo celle J - I, forma chiusa.)"""
    rows = killer_table(outers=("OR", "NAND"), gadgets=("XOR", "EQ"))
    assert len(rows) == 4
    for r in rows:
        assert r["G3"] == Fraction(3, 2)
        assert r["killed"] is False
        assert r["doorC_candidate"] is True
        assert r["distinct_vals"] == 3  # 0, 1, 3/2 distinti


# --- sweep completo (lento: celle dense a k=3) --------------------------------

@pytest.mark.slow
@pytest.mark.timeout(300)
def test_full_sweep_killer_table():
    """Sweep ESATTO su tutte le 54 coppie (f, g) a k=2,3.

    Esito misurato: SOLO le 4 celle di permutazione con outer OR/NAND aprono un
    gap (G_2=1, G_3=3/2); tutte le altre 50 hanno G_2=G_3=0 (killed banalmente
    dalle leggi, sequenza costante).  I 4 candidati door-C non sono killed.
    """
    rows = killer_table()
    assert len(rows) == len(DEFAULT_OUTERS) * len(DEFAULT_GADGETS) == 54

    gap_cells = {(r["f"], r["g"]): (r["G1"], r["G2"], r["G3"]) for r in rows
                 if r["G2"] != 0 or r["G3"] != 0}
    assert set(gap_cells.keys()) == {
        ("OR", "XOR"), ("OR", "EQ"), ("NAND", "XOR"), ("NAND", "EQ")
    }
    for trip in gap_cells.values():
        assert trip == (Fraction(0), Fraction(1), Fraction(3, 2))

    candidates = {(r["f"], r["g"]) for r in rows if r["doorC_candidate"]}
    assert candidates == set(gap_cells.keys())

    # le altre 50 celle hanno sequenza costante 0 -> killed, non candidate
    for r in rows:
        if (r["f"], r["g"]) not in gap_cells:
            assert r["G2"] == 0 and r["G3"] == 0
            assert r["killed"] is True
            assert r["doorC_candidate"] is False


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_full_sweep_doorC_candidates():
    """doorC_candidates() (sweep completo) = esattamente le 4 celle J - I."""
    cands = {(r["f"], r["g"]) for r in doorC_candidates()}
    assert cands == {
        ("OR", "XOR"), ("OR", "EQ"), ("NAND", "XOR"), ("NAND", "EQ")
    }
