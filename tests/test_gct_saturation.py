"""Test ESATTI per lo STRETCHING N=2 dei vanishing sporadici di Kronecker (Module 30, lever).

IPOTESI (explorer): lo sporadic vanishing si splitta in HOLE (g(2*triple)>0, buco interno
non-locale) vs RAY-VANISH (g(2*triple)=0, ostruzione asintotica).  KILLER: il bit hole/ray
e' funzione del dizionario (shape_profile canonico, covered)?  collisions(d) vuoto =
RESTATEMENT; non vuoto = sopravvivenza (collisione = stessa chiave, bit opposto).

Ancore di correttezza (killer di BUG, non dell'ipotesi):
  - g(N*triple) intero e totalmente simmetrico;
  - stretching commuta con la permutazione MA NON col coniugio (il punto load-bearing che
    impone la simmetria di PERMUTAZIONE per il canonico);
  - shape_profile invariante per permutazione.
Regression dei numeri pilot dell'explorer: d=4 -> 2/2 HOLE; d=5 -> 2 hole / 3 ray-vanish.
Test del collision-finder su caso costruito + l'ESITO reale a d=4,5,6.
"""

from itertools import permutations

import pytest

from pnp_lab.gct_kronecker import (
    kronecker,
    transpose,
    sporadic_vanishing,
    covered,
    stretch,
    g_stretch,
    is_hole,
    perm_orbit,
    perm_key,
    shape_profile,
    classify,
    collisions,
    summary,
)


# --------------------------------------------------------------------------------------
#  stretch: ancore elementari
# --------------------------------------------------------------------------------------
def test_stretch_multiplies_each_part():
    assert stretch(((3, 1), (2, 2), (2, 2)), 2) == ((6, 2), (4, 4), (4, 4))
    assert stretch(((4, 1), (4, 1), (2, 2, 1)), 3) == ((12, 3), (12, 3), (6, 6, 3))


def test_stretch_N1_is_identity():
    t = ((4, 1), (3, 2), (2, 1, 1, 1))
    assert stretch(t, 1) == t


def test_stretch_keeps_partition_of_Nd():
    """N*p resta una partizione (non crescente, parti > 0) di N*d."""
    for t in sporadic_vanishing(4) + sporadic_vanishing(5):
        for N in (2, 3):
            st = stretch(t, N)
            for p in st:
                assert all(p[i] >= p[i + 1] for i in range(len(p) - 1))
                assert all(x > 0 for x in p)
            d = sum(t[0])
            assert all(sum(p) == N * d for p in st)


def test_stretch_does_NOT_commute_with_transpose():
    """Punto LOAD-BEARING: transpose(N*p) != N*transpose(p) in generale.  E' la ragione per
    cui il bit hole/ray e' invariante SOLO per permutazione (non per l'orbita g-simmetrica)."""
    p = (4, 1)
    assert transpose(tuple(2 * x for x in p)) == (2, 2, 1, 1, 1, 1, 1, 1)
    assert tuple(2 * x for x in transpose(p)) == (4, 2, 2, 2)
    assert transpose(tuple(2 * x for x in p)) != tuple(2 * x for x in transpose(p))


# --------------------------------------------------------------------------------------
#  g(N*triple): intero, simmetrico, == 0 atteso vs no
# --------------------------------------------------------------------------------------
def test_g_stretch_integer_and_symmetric():
    """g(N*triple) e' intero (>=0) e totalmente simmetrico nelle tre partizioni stretchate."""
    for t in sporadic_vanishing(4) + sporadic_vanishing(5):
        st = stretch(t, 2)
        base = kronecker(*st)
        assert isinstance(base, int) and base >= 0
        for perm in permutations(st):
            assert kronecker(*perm) == base


def test_hole_bit_constant_on_perm_orbit():
    """Il bit hole/ray e' COSTANTE su tutta l'orbita di permutazione (stretching commuta con
    le permutazioni).  Verificato su tutti i sporadici di d=4,5."""
    for d in (4, 5):
        for t in sporadic_vanishing(d):
            b = is_hole(t)
            for rep in perm_orbit(t):
                assert is_hole(rep) == b


def test_hole_bit_NOT_constant_on_g_orbit():
    """CONTROLLO della simmetria corretta: nella STESSA orbita g-simmetrica il bit hole/ray
    PUO' cambiare (lo stretching non commuta col coniugio).  Esempio reale a d=5:
    ((4,1),(4,1),(2,2,1)) [RAY] e ((2,2,1),(2,1,1,1),(2,1,1,1)) [HOLE] sono g-coniugate."""
    ray = ((4, 1), (4, 1), (2, 2, 1))
    hole = ((2, 2, 1), (2, 1, 1, 1), (2, 1, 1, 1))
    # stessa orbita g-simmetrica: stesso g_base
    assert kronecker(*ray) == 0 and kronecker(*hole) == 0
    # ma bit hole/ray OPPOSTO sotto stretching
    assert g_stretch(ray) == 0 and not is_hole(ray)
    assert g_stretch(hole) == 8 and is_hole(hole)


# --------------------------------------------------------------------------------------
#  shape_profile: invariante di permutazione (chiave ONESTA del killer)
# --------------------------------------------------------------------------------------
def test_shape_profile_permutation_invariant():
    """shape_profile e' identico per ogni permutazione degli argomenti (la simmetria sotto
    cui il bit hole/ray e' invariante) -> chiave onesta per il collision-finder."""
    for d in (4, 5, 6):
        for t in sporadic_vanishing(d):
            base = shape_profile(t)
            for rep in perm_orbit(t):
                assert shape_profile(rep) == base


def test_perm_key_groups_only_permutations():
    """perm_key uguale sse le terne differiscono solo per l'ordine; due terne con multiset di
    argomenti diverso hanno perm_key diversa (non sono raggruppate spuriamente)."""
    a = ((3, 3), (3, 1, 1, 1), (2, 1, 1, 1, 1))
    b = ((4, 1, 1), (3, 3), (2, 1, 1, 1, 1))  # multiset diverso (4,1,1) vs (3,1,1,1)
    assert perm_key(a) == perm_key(((3, 1, 1, 1), (3, 3), (2, 1, 1, 1, 1)))  # solo riordino
    assert perm_key(a) != perm_key(b)


# --------------------------------------------------------------------------------------
#  Regression dei NUMERI pilot dell'explorer
# --------------------------------------------------------------------------------------
def test_classify_d4_all_hole_exact():
    """d=4: ENTRAMBE le terne sporadiche sono HOLE (g(2*triple)>0).  Pilot explorer: 2/2."""
    rows = classify(4)
    assert summary(4) == (2, 2, 0, 0)  # (#sp, #hole, #ray, #coll)
    holes = {r["triple"] for r in rows if r["hole"]}
    assert holes == {
        ((3, 1), (2, 2), (2, 2)),
        ((2, 2), (2, 2), (2, 1, 1)),
    }
    for r in rows:
        assert r["g_base"] == 0
        assert r["g_stretch"] == 1 and r["hole"]
        assert r["covered"]


def test_classify_d5_split_2hole_3ray_exact():
    """d=5: split ESATTO 2 HOLE / 3 RAY-VANISH.  Pilot explorer riprodotto come regression."""
    rows = classify(5)
    assert summary(5) == (5, 2, 3, 0)  # (#sp, #hole, #ray, #coll)
    holes = {r["triple"] for r in rows if r["hole"]}
    rays = {r["triple"] for r in rows if not r["hole"]}
    assert holes == {
        ((2, 2, 1), (2, 1, 1, 1), (2, 1, 1, 1)),
        ((2, 1, 1, 1), (2, 1, 1, 1), (2, 1, 1, 1)),
    }
    assert rays == {
        ((4, 1), (4, 1), (2, 2, 1)),
        ((4, 1), (4, 1), (2, 1, 1, 1)),
        ((4, 1), (3, 2), (2, 1, 1, 1)),
    }
    # valori g_stretch esatti
    by_t = {r["triple"]: r["g_stretch"] for r in rows}
    assert by_t[((2, 2, 1), (2, 1, 1, 1), (2, 1, 1, 1))] == 8
    assert by_t[((2, 1, 1, 1), (2, 1, 1, 1), (2, 1, 1, 1))] == 10
    for t in rays:
        assert by_t[t] == 0


# --------------------------------------------------------------------------------------
#  ESITO del KILLER: collisions
# --------------------------------------------------------------------------------------
def test_collisions_empty_d4():
    """d=4: nessuna collisione -> il bit hole/ray e' ricostruibile dal dizionario (RESTATEMENT)."""
    assert collisions(4) == []


def test_collisions_empty_d5():
    """d=5: nessuna collisione -> bit ricostruibile dal dizionario (RESTATEMENT)."""
    assert collisions(5) == []


def test_collisions_d6_exact_one_collision():
    """d=6: ESITO MISURATO — esiste ESATTAMENTE 1 collisione (sopravvivenza).
    Due orbite di permutazione DISTINTE con lo STESSO shape_profile canonico e stessa
    copertura (covered=True) ma bit hole/ray OPPOSTO:
      HOLE = ((3,3),(3,1,1,1),(2,1,1,1,1))      g(2*triple)=1
      RAY  = ((4,1,1),(3,3),(2,1,1,1,1))        g(2*triple)=0
    Il bit NON e' funzione di (shape_profile, covered) a d=6 => invariante fuori-dizionario.
    """
    coll = collisions(6)
    assert len(coll) == 1
    c = coll[0]
    assert c["key"][1] is True  # covered
    assert c["holes"] == [((3, 3), (3, 1, 1, 1), (2, 1, 1, 1, 1))]
    assert c["rays"] == [((4, 1, 1), (3, 3), (2, 1, 1, 1, 1))]
    # le due terne hanno DAVVERO stesso profilo e copertura ma bit opposto
    h, r = c["holes"][0], c["rays"][0]
    assert shape_profile(h) == shape_profile(r)
    assert covered(h) and covered(r)
    assert kronecker(*h) == 0 and kronecker(*r) == 0  # entrambe sporadiche
    assert g_stretch(h) == 1 and is_hole(h)
    assert g_stretch(r) == 0 and not is_hole(r)
    assert perm_key(h) != perm_key(r)  # orbite distinte (collisione genuina, non spuria)


def test_summary_d6_exact():
    """d=6: summary ESATTO (#sp, #hole, #ray, #coll) = (44, 26, 18, 1)."""
    assert summary(6) == (44, 26, 18, 1)


# --------------------------------------------------------------------------------------
#  Collision-finder su un caso COSTRUITO (killer di BUG del finder stesso)
# --------------------------------------------------------------------------------------
def test_collision_finder_on_constructed_case(monkeypatch):
    """Inietto due terne FITTIZIE con stesso shape_profile + covered ma bit hole/ray opposto
    e verifico che collisions le rilevi; poi rendo i bit concordi e verifico che NON le rilevi.
    Controlla la LOGICA del finder isolata dai dati reali.

    Costruisco due terne con partizioni DIVERSE ma stesso shape_profile canonico (uso (5,)
    e (4,), entrambe single-row: stessa firma two-row+hook+rettangolo) in orbite di
    permutazione distinte.
    """
    import pnp_lab.gct_kronecker.saturation as sat

    # due terne con shape_profile uguale ma partizioni (e quindi orbita) diverse
    A = ((5,), (5,), (5,))   # firma di (5,) == firma di (4,) -> stesso profilo di B
    B = ((4,), (4,), (4,))   # partizioni diverse, stesso profilo canonico
    assert sat.shape_profile(A) == sat.shape_profile(B)
    assert sat.perm_key(A) != sat.perm_key(B)

    # caso 1: bit OPPOSTO -> deve esserci collisione
    fake_rows_collision = [
        {"triple": A, "g_base": 0, "g_stretch": 1, "hole": True,
         "covered": True, "shape_profile": sat.shape_profile(A)},
        {"triple": B, "g_base": 0, "g_stretch": 0, "hole": False,
         "covered": True, "shape_profile": sat.shape_profile(B)},
    ]
    monkeypatch.setattr(sat, "classify", lambda d, N=2: fake_rows_collision)
    coll = sat.collisions(99)
    assert len(coll) == 1
    assert coll[0]["holes"] == [A] and coll[0]["rays"] == [B]

    # caso 2: bit CONCORDE -> nessuna collisione
    fake_rows_no_collision = [
        {"triple": A, "g_base": 0, "g_stretch": 1, "hole": True,
         "covered": True, "shape_profile": sat.shape_profile(A)},
        {"triple": B, "g_base": 0, "g_stretch": 2, "hole": True,
         "covered": True, "shape_profile": sat.shape_profile(B)},
    ]
    monkeypatch.setattr(sat, "classify", lambda d, N=2: fake_rows_no_collision)
    assert sat.collisions(99) == []
