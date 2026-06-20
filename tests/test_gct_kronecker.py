"""Test ESATTI per la 7a arena (GCT / coefficienti di Kronecker).

Ancore di correttezza = killer di BUG (non dell'ipotesi):
  - chi^lam_{(1^d)} = dim S^lam = formula degli hook.
  - g([d],mu,nu) = delta_{mu,nu}     (tensore con la triviale).
  - g(lam,[1^d],nu) = delta_{nu,lam'} (tensore con il segno).
  - g totalmente simmetrico, g >= 0.
Poi: 0 falsi positivi delle NC e l'ESITO del killer sporadic_vanishing su d=3,4,(5,6 slow).
"""

from math import factorial

import pytest

from pnp_lab.gct_kronecker import (
    partitions,
    transpose,
    mn_character,
    hook_length_dimension,
    kronecker,
    nc_length,
    nc_maxpart,
    vanishing_table,
    sporadic_vanishing,
    nc_false_positive,
    is_two_row,
    is_two_column,
    is_hook,
    is_rectangle,
    special_shape,
    g_orbit,
    covered,
    uncovered,
    coverage_summary,
)


def _triples(d):
    ps = partitions(d)
    return [
        (ps[i], ps[j], ps[k])
        for i in range(len(ps))
        for j in range(i, len(ps))
        for k in range(j, len(ps))
    ]


# --------------------------------------------------------------------------------------
#  Ancore di correttezza (fast)
# --------------------------------------------------------------------------------------
@pytest.mark.parametrize("d", [1, 2, 3, 4])
def test_chi_at_1d_is_hook_dimension(d):
    """chi^lam_{(1^d)} = dim(S^lam) = formula degli hook, per ogni lam."""
    one = tuple([1] * d)
    for lam in partitions(d):
        assert mn_character(lam, one) == hook_length_dimension(lam)


@pytest.mark.parametrize("d", [1, 2, 3, 4])
def test_sum_of_squared_dims_is_d_factorial(d):
    """sum_lam dim(S^lam)^2 = |S_d| = d! (sanita' delle dimensioni)."""
    assert sum(hook_length_dimension(p) ** 2 for p in partitions(d)) == factorial(d)


@pytest.mark.parametrize("d", [2, 3, 4])
def test_tensor_with_trivial_is_delta(d):
    """g([d],mu,nu) = delta_{mu,nu}."""
    triv = (d,)
    ps = partitions(d)
    for mu in ps:
        for nu in ps:
            assert kronecker(triv, mu, nu) == (1 if mu == nu else 0)


@pytest.mark.parametrize("d", [2, 3, 4])
def test_tensor_with_sign_is_delta_conjugate(d):
    """g(lam,[1^d],nu) = delta_{nu, lam'} (tensore con la rappresentazione segno)."""
    sign = tuple([1] * d)
    ps = partitions(d)
    for lam in ps:
        for nu in ps:
            assert kronecker(lam, sign, nu) == (1 if nu == transpose(lam) else 0)


@pytest.mark.parametrize("d", [2, 3, 4])
def test_kronecker_nonnegative_and_integer(d):
    """g >= 0 su tutte le terne di d (la routine fa gia' assert sul denominatore=1)."""
    for lam, mu, nu in _triples(d):
        g = kronecker(lam, mu, nu)
        assert isinstance(g, int) and g >= 0


@pytest.mark.parametrize("d", [3, 4])
def test_kronecker_totally_symmetric(d):
    """g(lam,mu,nu) e' invariante per ogni permutazione delle tre partizioni."""
    from itertools import permutations

    ps = partitions(d)
    for i, lam in enumerate(ps):
        for mu in ps:
            for nu in ps:
                base = kronecker(lam, mu, nu)
                for a, b, c in permutations((lam, mu, nu)):
                    assert kronecker(a, b, c) == base


def test_known_small_values():
    """Valori di Kronecker noti dalla letteratura (sanita')."""
    assert kronecker((2, 1), (2, 1), (2, 1)) == 1
    assert kronecker((2, 2), (2, 2), (2, 2)) == 1
    assert kronecker((3, 1), (3, 1), (2, 2)) == 1


# --------------------------------------------------------------------------------------
#  Solidita' delle NC (killer di BUG nelle NC): zero falsi positivi
# --------------------------------------------------------------------------------------
@pytest.mark.parametrize("d", [2, 3, 4])
def test_necessary_conditions_have_no_false_positives(d):
    """Se g > 0 allora ENTRAMBE le NC del predittore devono valere (sono NECESSARIE)."""
    for lam, mu, nu in _triples(d):
        if kronecker(lam, mu, nu) > 0:
            assert nc_length(lam, mu, nu)
            assert nc_maxpart(lam, mu, nu)
    assert nc_false_positive(d) == []


# --------------------------------------------------------------------------------------
#  ESITO del killer: sporadic_vanishing (l'ipotesi-lab)  (fast d=3,4)
# --------------------------------------------------------------------------------------
def test_sporadic_vanishing_d3_empty():
    """d=3: nessun vanishing sporadico — le NC note caratterizzano lo zero-set.
    (Il pattern di vanishing COLLASSA nelle NC: ipotesi-lab confermata a d=3.)"""
    assert sporadic_vanishing(3) == []


def test_sporadic_vanishing_d4_nonempty_exact():
    """d=4: ESITO MISURATO — esistono vanishing SPORADICI (g=0 con tutte le NC ok).
    Questo FALSIFICA l'ipotesi-lab a d=4 (primo fuori-dizionario). Fissiamo l'elenco esatto.
    """
    sp = sporadic_vanishing(4)
    assert sp == [
        ((3, 1), (2, 2), (2, 2)),
        ((2, 2), (2, 2), (2, 1, 1)),
    ]
    # ognuna ha davvero g=0 e tutte le NC soddisfatte
    for lam, mu, nu in sp:
        assert kronecker(lam, mu, nu) == 0
        assert nc_length(lam, mu, nu) and nc_maxpart(lam, mu, nu)


# --------------------------------------------------------------------------------------
#  Sweep pesanti (slow): d=5 e d=6
# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
#  Copertura strutturale dei vanishing sporadici (coverage.py)  (fast)
# --------------------------------------------------------------------------------------
def test_shape_predicates_known_cases():
    """Predicati di forma su casi noti (esatti, elementari)."""
    # two-row: ell <= 2
    assert is_two_row((4,)) and is_two_row((3, 2)) and is_two_row(())
    assert not is_two_row((2, 1, 1))
    # two-column: parte massima <= 2 (trasposta a <= 2 righe)
    assert is_two_column((2, 2, 1)) and is_two_column((1, 1, 1)) and is_two_column(())
    assert not is_two_column((3, 1))
    # hook: (a, 1^b)
    assert is_hook((4,)) and is_hook((3, 1, 1)) and is_hook((2, 1)) and is_hook(())
    assert not is_hook((3, 2)) and not is_hook((2, 2, 1))
    # rettangolo: tutte le parti uguali
    assert is_rectangle((2, 2, 2)) and is_rectangle((3, 3)) and is_rectangle((1, 1))
    assert is_rectangle(()) and is_rectangle((5,))
    assert not is_rectangle((3, 1)) and not is_rectangle((2, 2, 1))
    # special_shape = OR
    assert special_shape((4, 1, 1))  # hook
    assert special_shape((3, 3))     # rettangolo + two-row
    assert special_shape((2, 2, 1, 1))  # two-column
    assert not special_shape((3, 2, 1))  # nessuna delle forme


def test_two_column_is_conjugate_two_row():
    """is_two_column(p) <=> is_two_row(transpose(p)) (dualita' per coniugio)."""
    for d in range(0, 7):
        for p in partitions(d):
            assert is_two_column(p) == is_two_row(transpose(p))


@pytest.mark.parametrize("d", [2, 3, 4])
def test_g_constant_over_orbit_all_dle4(d):
    """KILLER DI BUG: g e' costante su tutta l'orbita g-simmetrica, per OGNI terna d<=4.
    Se g variasse, le simmetrie (S_3 + coniugio doppio) sarebbero codificate male."""
    ps = partitions(d)
    for lam, mu, nu in _triples(d):
        g0 = kronecker(lam, mu, nu)
        for rep in g_orbit((lam, mu, nu)):
            assert kronecker(*rep) == g0, ((lam, mu, nu), rep)


def test_g_constant_over_orbit_sample_d5_d6():
    """g costante sull'orbita g-simmetrica su un campione di terne a d=5 e d=6 (fast)."""
    sample = [
        ((4, 1), (4, 1), (2, 2, 1)),
        ((3, 2), (3, 2), (3, 1, 1)),
        ((5, 1), (4, 1, 1), (2, 2, 2)),
        ((3, 3), (3, 3), (3, 2, 1)),
        ((4, 2), (4, 2), (2, 2, 1, 1)),
    ]
    for t in sample:
        g0 = kronecker(*t)
        for rep in g_orbit(t):
            assert kronecker(*rep) == g0, (t, rep)


def test_covered_uses_two_special_in_some_rep():
    """covered True se un rappresentante ha >=2 argomenti special_shape; controesempio
    costruito (tutti gli argomenti non-special in ogni rappresentante => covered False)."""
    # ((3,1),(2,2),(2,2)): (2,2) e' rettangolo/two-row, due copie => covered
    assert covered(((3, 1), (2, 2), (2, 2)))
    # terna con un solo argomento special in ogni rappresentante => non covered
    assert not covered(((3, 2, 1), (3, 2, 1), (3, 2, 1)))  # (3,2,1) non e' special


def test_uncovered_empty_d4():
    """d=4: ogni vanishing sporadico e' COPERTO da formule chiuse note (uncovered==[])."""
    assert uncovered(4) == []
    n_sp, n_cov, n_unc = coverage_summary(4)
    assert (n_sp, n_cov, n_unc) == (2, 2, 0)


def test_uncovered_empty_d5():
    """d=5: uncovered==[] (collasso COMPUTED, non solo CITATO)."""
    assert uncovered(5) == []
    assert coverage_summary(5) == (5, 5, 0)


def test_uncovered_empty_d6():
    """d=6: uncovered==[] (fast: ~0.1s). 44 sporadici, tutti coperti."""
    assert uncovered(6) == []
    assert coverage_summary(6) == (44, 44, 0)


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_d5_anchors_and_sporadic_exact():
    """d=5: ancore + elenco ESATTO dei vanishing sporadici (sweep pesante)."""
    one = tuple([1] * 5)
    for lam in partitions(5):
        assert mn_character(lam, one) == hook_length_dimension(lam)
    assert nc_false_positive(5) == []
    sp = sporadic_vanishing(5)
    assert sp == [
        ((4, 1), (4, 1), (2, 2, 1)),
        ((4, 1), (4, 1), (2, 1, 1, 1)),
        ((4, 1), (3, 2), (2, 1, 1, 1)),
        ((2, 2, 1), (2, 1, 1, 1), (2, 1, 1, 1)),
        ((2, 1, 1, 1), (2, 1, 1, 1), (2, 1, 1, 1)),
    ]
    for lam, mu, nu in sp:
        assert kronecker(lam, mu, nu) == 0
        assert nc_length(lam, mu, nu) and nc_maxpart(lam, mu, nu)


@pytest.mark.slow
@pytest.mark.timeout(600)
def test_d6_anchors_and_no_false_positives():
    """d=6: ancore (hook=chi, sumdim^2, g>=0, simmetria) + 0 falsi positivi delle NC,
    e sporadic_vanishing NON vuoto (sweep pesante)."""
    one = tuple([1] * 6)
    for lam in partitions(6):
        assert mn_character(lam, one) == hook_length_dimension(lam)
    assert sum(hook_length_dimension(p) ** 2 for p in partitions(6)) == factorial(6)
    for lam, mu, nu in _triples(6):
        assert kronecker(lam, mu, nu) >= 0
    assert nc_false_positive(6) == []
    assert len(sporadic_vanishing(6)) > 0
