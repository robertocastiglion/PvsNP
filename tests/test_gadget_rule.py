"""Test ESATTI della REGOLA sui gadget per il gap del lift (Modulo 18, ciclo 1).

Ipotesi dell'Explorer: per F = f ∘ g^k con gadget integrale a 1 bit, il gap
G* > 0 si apre SSE g e' una matrice di PERMUTAZIONE ({XOR, EQ}) E l'outer f
apre la pattern-matrix non integrale; per i 7 gadget non-permutazione il lift
resta integrale per ogni outer.

Tutto su istanze minuscole, aritmetica razionale esatta (Fraction). I test su k=3
usano SOLO celle sparse (cover esatto istantaneo) o l'equivalenza strutturale
XOR/EQ a meno di permutazione (nessun LP costoso sulle 8x8 dense).
"""

from fractions import Fraction

from pnp_lab.exactness_composes import GADGETS_1BIT
from pnp_lab.exactness_composes.gadget_rule import (
    gap_table,
    is_permutation_gadget,
    measured_gap,
    predict_gap,
    rule_matches_measurement,
    xor_eq_same_up_to_col_perm,
)

# Le 4 (e sole) celle con gap su {6 outer x 9 gadget} a k=2.
GAP_CELLS_K2 = [("OR", "XOR"), ("OR", "EQ"), ("NAND", "XOR"), ("NAND", "EQ")]


# --- gadget di permutazione = esattamente {XOR, EQ} ---------------------------

def test_permutation_gadgets_are_exactly_xor_and_eq():
    perms = {n for n, g in GADGETS_1BIT.items() if is_permutation_gadget(g)}
    assert perms == {"XOR", "EQ"}


def test_is_permutation_gadget_basic():
    assert is_permutation_gadget(GADGETS_1BIT["XOR"]) is True
    assert is_permutation_gadget(GADGETS_1BIT["EQ"]) is True
    assert is_permutation_gadget(GADGETS_1BIT["AND"]) is False
    assert is_permutation_gadget(GADGETS_1BIT["OR"]) is False
    assert is_permutation_gadget(GADGETS_1BIT["PROJ_X"]) is False


# --- le 4 celle-gap a k=2: Cov=4, LP=3, G*=1 ----------------------------------

def test_four_gap_cells_k2_exact_values():
    t = gap_table(k=2)
    for cell in GAP_CELLS_K2:
        cov, lp, gs = t[cell]
        assert (cov, lp, gs) == (4, Fraction(3), Fraction(1)), cell


def test_only_four_cells_have_gap_k2():
    t = gap_table(k=2)
    gap_cells = sorted(c for c, (_, _, gs) in t.items() if gs > 0)
    assert gap_cells == sorted(GAP_CELLS_K2)
    assert len(t) == 54  # 6 outer x 9 gadget


def test_and_xor_maj_nor_have_no_gap_with_any_gadget_k2():
    t = gap_table(k=2)
    for f in ("AND", "XOR", "MAJ", "NOR"):
        for g in GADGETS_1BIT:
            assert t[(f, g)][2] == 0, (f, g)


# --- coerenza predict_gap <-> G* misurato su TUTTE le celle k=2 ---------------

def test_predict_gap_matches_measurement_k2():
    ok, mismatches = rule_matches_measurement(k=2)
    assert ok, f"discrepanze previsione/misura: {mismatches}"


def test_predict_gap_true_exactly_on_gap_cells_k2():
    for f in ("AND", "OR", "XOR", "MAJ", "NAND", "NOR"):
        for g in GADGETS_1BIT:
            assert predict_gap(f, g, 2) == ((f, g) in GAP_CELLS_K2), (f, g)


# --- DISCRIMINANTE EQ-vs-XOR --------------------------------------------------

def test_eq_opens_gap_exactly_like_xor_k2():
    # numeri esatti: entrambi G* = 1 a k=2
    assert measured_gap("OR", "EQ", 2) == 1
    assert measured_gap("OR", "XOR", 2) == 1
    assert measured_gap("OR", "EQ", 2) == measured_gap("OR", "XOR", 2)
    assert measured_gap("NAND", "EQ", 2) == measured_gap("NAND", "XOR", 2) == 1


def test_xor_eq_equal_up_to_column_permutation_all_k():
    # PROVA strutturale: lift(f,XOR,k) = lift(f,EQ,k) a meno di permutare le colonne
    # => G*(XOR) = G*(EQ) per OGNI k (anche k=3, senza LP costoso).
    for f in ("AND", "OR", "XOR", "MAJ", "NAND", "NOR"):
        for k in (2, 3):
            assert xor_eq_same_up_to_col_perm(f, k) is True, (f, k)


# --- k=3: celle SPARSE (cover esatto istantaneo) ------------------------------

def test_k3_sparse_cells_are_integral():
    # outer sparsi a k=3: AND/NOR -> matrici 8x8 con pochi 1, cover esatto immediato.
    # La regola prevede G*=0 (outer non apre la pattern-matrix, per ogni gadget).
    sparse = gap_table(outers=("AND", "NOR"), k=3)
    assert len(sparse) == 18  # 2 outer x 9 gadget
    for cell, (cov, lp, gs) in sparse.items():
        assert gs == 0, cell
        assert predict_gap(*cell, 3) is False


def test_k3_and_xor_specific_integral():
    # cella sparsa concreta a k=3: (AND, XOR) e (AND, EQ) -> 8x8 con 8 uni, Cov=LP=8.
    t = gap_table(outers=("AND",), gadgets=("XOR", "EQ"), k=3)
    assert t[("AND", "XOR")] == (8, Fraction(8), Fraction(0))
    assert t[("AND", "EQ")] == (8, Fraction(8), Fraction(0))
