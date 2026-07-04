"""Test ESATTI per il cono/politopo dei momenti di Kronecker (Module 30, Entry 35 lever).

IPOTESI (explorer): l'inner approximation P_D = conv{point_norm(lam,mu,nu): g>0, d<=D} e'
g-simmetrica per costruzione; cerca BUCHI = sporadic vanishing (g=0) il cui punto e' in P_D.
SUPERFICIALE = in-cono e g(N*)>0 per N in {2,3,4} (gia' visto da saturation); PROFONDO =
in-cono ma g(N*)=0 per N=2,3,4 (invisibile allo stretch).  KILLER-1: ogni in-cono e'
superficiale => collasso.  KILLER-2: ogni faccetta di P_D e' nel dizionario => collasso.
SOPRAVVIVENZA: un buco PROFONDO o una faccetta fuori-dizionario.

Ancore di correttezza (killer di BUG):
  - in_cone esatto su casi costruiti (vertice/baricentro dentro, punto esterno fuori);
  - point() normalizza ogni blocco a somma 1;
  - facets() produce un'H-rep VALIDA (coerente con l'oracolo LP di membership su punti casuali).
Regression dei conteggi summary per d=5,6 + coerenza con saturation.py (i superficiali qui
contengono gli HOLE g-simmetrici di Entry 34).  Marca slow cio' che richiede d=6 o D=4.
"""

from fractions import Fraction

import pytest

from pnp_lab.gct_kronecker import (
    kronecker,
    sporadic_vanishing,
)
from pnp_lab.gct_kronecker.moment_cone import (
    max_parts,
    point,
    support_points,
    in_cone,
    is_deep_hole,
    holes,
    summary,
    facets,
    classify_facet,
    facet_report,
    _is_implied,
    _dictionary_generators,
)
from pnp_lab.gct_kronecker.saturation import perm_key
from pnp_lab.gct_kronecker import classify as sat_classify


# --------------------------------------------------------------------------------------
#  point(): normalizzazione
# --------------------------------------------------------------------------------------
def test_point_block_sums_to_one():
    """Ogni blocco di k coordinate del punto normalizzato somma a 1 (parti / d)."""
    k = max_parts(5)
    for t in sporadic_vanishing(5) + [((2, 1), (2, 1), (2, 1))]:
        p = point(t, k)
        assert len(p) == 3 * k
        for blk in range(3):
            assert sum(p[blk * k : (blk + 1) * k]) == Fraction(1)


def test_point_exact_values():
    """Valori esatti del padding/normalizzazione su un caso noto."""
    # ((2,1),(2,1),(2,1)) d=3, k=3: ogni blocco (2/3,1/3,0)
    p = point(((2, 1), (2, 1), (2, 1)), 3)
    assert p == (
        Fraction(2, 3), Fraction(1, 3), Fraction(0),
        Fraction(2, 3), Fraction(1, 3), Fraction(0),
        Fraction(2, 3), Fraction(1, 3), Fraction(0),
    )


# --------------------------------------------------------------------------------------
#  in_cone(): casi COSTRUITI (ancore della correttezza dell'LP)
# --------------------------------------------------------------------------------------
def test_in_cone_vertex_inside():
    """Un vertice di S e' banalmente in conv(S)."""
    S = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
    ]
    assert in_cone((Fraction(1), Fraction(0)), S)
    assert in_cone((Fraction(0), Fraction(1)), S)


def test_in_cone_barycenter_inside():
    """Il baricentro di S e' in conv(S)."""
    S = [
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    ]
    bary = (Fraction(1, 3), Fraction(1, 3), Fraction(1, 3))
    assert in_cone(bary, S)


def test_in_cone_outside_point():
    """Punti palesemente fuori da conv(S) -> False (esatto)."""
    S = [
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
    ]
    # somma != 1 (fuori dal simplesso) e coordinate negative
    assert not in_cone((Fraction(2), Fraction(-1)), S)
    assert not in_cone((Fraction(1, 2), Fraction(3, 4)), S)  # somma 5/4 != 1
    # dentro l'affine ma fuori dal segmento (estrapolazione)
    assert not in_cone((Fraction(2), Fraction(-1, 1)), S)


def test_in_cone_real_support_vertex():
    """Su S reale (D=3): il punto di una terna g>0 e' nel suo stesso cono."""
    k = max_parts(3)
    S = sorted(support_points(3, k))
    t = ((2, 1), (2, 1), (2, 1))  # g>0 a d=3
    assert kronecker(*t) > 0
    assert in_cone(point(t, k), S)


# --------------------------------------------------------------------------------------
#  Coerenza H-rep <-> oracolo LP (la facets() e' VALIDA)
# --------------------------------------------------------------------------------------
def test_facets_consistent_with_lp_oracle_d3():
    """L'H-rep di P_3 (facets) e' coerente con l'oracolo LP di membership: un punto soddisfa
    TUTTE le faccette sse e' in_cone.  Verifica su un campione deterministico di punti
    (vertici di S = dentro; punti estrapolati oltre una faccetta = fuori)."""
    D = 3
    k = max_parts(D)
    S = sorted(support_points(D, k))
    F = facets(D)
    amb = len(S[0])

    def satisfies_all(p):
        return all(sum(a[t] * p[t] for t in range(amb)) <= b for a, b in F)

    # tutti i vertici di S: dentro l'H-rep E in_cone
    for s in S:
        assert satisfies_all(s)
        assert in_cone(s, S)
    # punti costruiti FUORI: estrapola oltre la prima faccetta dal baricentro
    bary = tuple(Fraction(sum(s[t] for s in S), len(S)) for t in range(amb))
    a0, b0 = F[0]
    # muovi dal baricentro nella direzione +a0 finche' viola la faccetta 0
    out_pt = tuple(bary[t] + 2 * a0[t] for t in range(amb))
    assert not satisfies_all(out_pt)
    assert not in_cone(out_pt, S)


# --------------------------------------------------------------------------------------
#  summary(): regression dei conteggi (d=5 fast, d=6 slow)
# --------------------------------------------------------------------------------------
def test_summary_d5_exact():
    """d=5 vs P_5: (#sp,#in,#sup,#deep,#out) = (5,0,0,0,5).  TUTTI i 5 sporadici sono
    FUORI-CONO: nessun buco a d=5 (ne' superficiale ne' profondo)."""
    assert summary(5, 5) == (5, 0, 0, 0, 5)


def test_d5_robust_against_D6():
    """I 5 sporadici di d=5 restano fuori-cono anche contro P_6 (cono piu' grande)."""
    h = holes(5, 6)
    assert h["n_out"] == 5 and h["n_in_cone"] == 0


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_summary_d6_exact():
    """d=6 vs P_6: (#sp,#in,#sup,#deep,#out) = (44,10,10,0,44-10-... ) = (44,10,10,0,34).
    10 buchi superficiali (g(2*)>0), ZERO buchi profondi, 34 fuori-cono.  LENTO (|S|=692)."""
    assert summary(6, 6) == (44, 10, 10, 0, 34)


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_d6_no_deep_holes_exact():
    """d=6: l'elenco dei buchi PROFONDI e' VUOTO (#deep==0).  Tutti i 10 in-cono sono
    superficiali (gia' visibili allo stretch N=2)."""
    h = holes(6, 6)
    assert h["deep"] == []
    assert h["n_deep"] == 0
    # ogni superficiale e' davvero g(2*)>0
    for t in h["superficial"]:
        assert kronecker(*(tuple(tuple(2 * x for x in p) for p in t))) > 0


# --------------------------------------------------------------------------------------
#  Coerenza con saturation.py: i superficiali in-cono ⊇ gli HOLE di Entry 34
# --------------------------------------------------------------------------------------
@pytest.mark.slow
@pytest.mark.timeout(300)
def test_superficial_supersets_saturation_holes_d6():
    """I buchi SUPERFICIALI in-cono qui contengono gli HOLE g(2*)>0 di saturation.py (Entry 34),
    deduplicati per orbita di permutazione.  (Il viceversa NON e' garantito: un HOLE di
    saturation potrebbe avere il punto fuori-cono.)"""
    h = holes(6, 6)
    superficial_keys = {perm_key(t) for t in h["superficial"]}
    in_cone_keys = {perm_key(t) for t in h["in_cone"]}
    # gli HOLE di saturation che sono ANCHE in-cono devono essere superficiali qui
    sat_holes = [r["triple"] for r in sat_classify(6) if r["hole"]]
    for t in sat_holes:
        if perm_key(t) in in_cone_keys:
            assert perm_key(t) in superficial_keys


# --------------------------------------------------------------------------------------
#  is_deep_hole(): ancora costruita
# --------------------------------------------------------------------------------------
def test_is_deep_hole_false_when_out_of_cone():
    """Un punto fuori-cono non e' mai un buco profondo (corto-circuito su in_cone)."""
    k = max_parts(5)
    S = support_points(5, k)
    for t in sporadic_vanishing(5):
        # a d=5 sono tutti fuori-cono -> is_deep_hole False
        assert not is_deep_hole(t, S, k, n_max=3)


def test_is_deep_hole_requires_all_stretch_zero():
    """is_deep_hole e' True solo se in-cono E g(N*)=0 per ogni N in 2..n_max; un HOLE
    superficiale (g(2*)>0) non e' profondo anche se in-cono."""
    # caso costruito: forziamo un punto-vertice in cono ma con g(2*)>0
    t = ((2, 1), (2, 1), (2, 1))  # g>0 (non sporadico) ma serve solo per il ramo stretch
    k = max_parts(3)
    S = support_points(3, k)
    # in cono (e' un vertice), ma g(2*)>0 -> NON profondo
    assert in_cone(point(t, k), S)
    assert not is_deep_hole(t, S, k, n_max=2)


# --------------------------------------------------------------------------------------
#  FACCETTE (KILLER-2): D=3 fast, D=4 slow
# --------------------------------------------------------------------------------------
def test_facets_d3_count_and_split():
    """D=3: 14 faccette; col test di RIDUCIBILITA' esatto 3 in-dizionario, 11 fuori-dizionario.
    Le 11 fuori-dizionario sono la SOPRAVVIVENZA di KILLER-2 (non implicate da nonneg+ordering)."""
    rep = facet_report(3)
    assert rep["n_facets"] == 14
    assert rep["n_in_dictionary"] == 3
    assert rep["n_out_of_dictionary"] == 11


def test_classify_facet_in_dictionary_example():
    """La faccetta (0,0,0,0,0,0,1,1,-2)<=1 [= x_7+x_8-2x_9 <= 1, parte del terzo blocco] e'
    IMPLICATA dal dizionario (in_dictionary)."""
    k = max_parts(3)
    S = sorted(support_points(3, k))
    ineq = ((0, 0, 0, 0, 0, 0, 1, 1, -2), 1)
    assert ineq in facets(3)
    assert classify_facet(ineq, S, k) == "in_dictionary"


def test_classify_facet_out_of_dictionary_example():
    """La faccetta (-4,5,-1,-2,1,1,-2,1,1)<=-2 NON e' implicata dal dizionario elementare."""
    k = max_parts(3)
    S = sorted(support_points(3, k))
    ineq = ((-4, 5, -1, -2, 1, 1, -2, 1, 1), -2)
    assert ineq in facets(3)
    assert classify_facet(ineq, S, k) == "out_of_dictionary"


def test_is_implied_on_trivial_dictionary_inequality():
    """Sanity del Farkas: una disuguaglianza del dizionario STESSA (es. -x_0 <= 0) e' implicata."""
    k = max_parts(3)
    S = sorted(support_points(3, k))
    amb = 3 * k
    gens, eqs = _dictionary_generators(S, amb, k)
    a = [0] * amb
    a[0] = -1  # -x_0 <= 0
    assert _is_implied(a, 0, gens, eqs, amb)


@pytest.mark.slow
@pytest.mark.timeout(900)
def test_facets_d4_count_and_split():
    """D=4 (dim affine 9, |S|=53): 264 faccette via beneath-beyond razionale (LENTO, ~8 min).
    Regression del numero di faccette e del fatto che esistono faccette fuori-dizionario."""
    rep = facet_report(4)
    assert rep["n_facets"] == 264
    assert rep["n_out_of_dictionary"] > 0
    assert rep["n_in_dictionary"] + rep["n_out_of_dictionary"] == 264
