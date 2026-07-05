"""Test ESATTI per il modulo beyond_wall (Ciclo 1 'la caccia').

Verifica:
  - nc_dvir_full e nc_triangle: ZERO falsi positivi su d<=5 (g>0 => NC True).
  - nc_dvir_full e nc_triangle: catturano zeri noti.
  - explained_zero / g_canonical: comportamento su casi costruiti.
  - hunt(d) per d=4,5: conteggi esatti + sanity Entry 30.
  - hunt(6): sanity Entry 30 (slow).
  - hunt(7): misura oltre il muro (slow).
  - stretch_triple: valori esatti.
"""

import pytest

from pnp_lab.gct_kronecker.beyond_wall import (
    _diagram_intersection,
    nc_dvir_full,
    nc_triangle,
    explained_zero,
    covered_ext,
    g_canonical,
    hunt,
    sanity_entry30,
    stretch_triple,
    false_positives_dvir,
    false_positives_triangle,
    HuntResult,
)
from pnp_lab.gct_kronecker.fast import g_fast, character_table
from pnp_lab.gct_kronecker.kronecker import _triples
from pnp_lab.gct_kronecker.coverage import g_orbit


# ─────────────────────────────────────────────────────────────────────────────
#  _diagram_intersection
# ─────────────────────────────────────────────────────────────────────────────

def test_diagram_intersection_identical():
    """L'intersezione di un diagramma con se stesso e' l'intero diagramma."""
    mu = (4, 2, 1)
    assert _diagram_intersection(mu, mu) == sum(mu)


def test_diagram_intersection_disjoint_lengths():
    """mu=(4,) e nu=(1,1,1,1): solo la prima riga conta."""
    assert _diagram_intersection((4,), (1, 1, 1, 1)) == 1


def test_diagram_intersection_empty():
    """Intersezione con partizione vuota = 0."""
    assert _diagram_intersection((), (3, 2)) == 0
    assert _diagram_intersection((3, 2), ()) == 0


def test_diagram_intersection_known():
    """mu=(4,3), nu=(3,2,1,1): min(4,3)+min(3,2)+min(0,1)+min(0,1) = 3+2+0+0 = 5."""
    assert _diagram_intersection((4, 3), (3, 2, 1, 1)) == 5


# ─────────────────────────────────────────────────────────────────────────────
#  nc_dvir_full: zero falsi positivi su d<=5
# ─────────────────────────────────────────────────────────────────────────────

def test_nc_dvir_full_no_false_positives_d4():
    """nc_dvir_full non restituisce mai False quando g>0, per d=4."""
    assert false_positives_dvir(4) == []


def test_nc_dvir_full_no_false_positives_d5():
    """nc_dvir_full non restituisce mai False quando g>0, per d=5."""
    assert false_positives_dvir(5) == []


# ─────────────────────────────────────────────────────────────────────────────
#  nc_triangle: zero falsi positivi su d<=5
# ─────────────────────────────────────────────────────────────────────────────

def test_nc_triangle_no_false_positives_d4():
    """nc_triangle non restituisce mai False quando g>0, per d=4."""
    assert false_positives_triangle(4) == []


def test_nc_triangle_no_false_positives_d5():
    """nc_triangle non restituisce mai False quando g>0, per d=5."""
    assert false_positives_triangle(5) == []


# ─────────────────────────────────────────────────────────────────────────────
#  nc_dvir_full: controlla che spari su un caso noto
# ─────────────────────────────────────────────────────────────────────────────

def test_nc_dvir_full_fires_on_known_zero():
    """nc_dvir_full rileva lo zero g((6,1),(4,3),(3,2,1,1))=0 tramite l1>|mu cap nu|.

    |mu cap nu| = |(4,3) cap (3,2,1,1)| = 3+2+0+0 = 5; lam[0]=6 > 5 => False.
    """
    lam, mu, nu = (6, 1), (4, 3), (3, 2, 1, 1)
    # Verifica la struttura dell'intersezione
    assert _diagram_intersection(mu, nu) == 5
    # nc_dvir_full deve sparare (la permutazione (lam,mu,nu) ha lam[0] > |mu cap nu|)
    assert not nc_dvir_full(lam, mu, nu)
    # e g deve effettivamente essere 0
    character_table(7)
    assert g_fast(lam, mu, nu) == 0


# ─────────────────────────────────────────────────────────────────────────────
#  nc_triangle: controlla che spari su un caso costruito
# ─────────────────────────────────────────────────────────────────────────────

def test_nc_triangle_fires_correctly():
    """nc_triangle spara quando mu[0]+nu[0]-d > lam[0].

    Caso costruito d=7: lam=(2,2,2,1), mu=(6,1), nu=(6,1).
    mu[0]+nu[0]-d = 6+6-7 = 5 > lam[0]=2 => nc_triangle=False => g=0.
    """
    lam, mu, nu = (2, 2, 2, 1), (6, 1), (6, 1)
    assert not nc_triangle(lam, mu, nu)
    character_table(7)
    assert g_fast(lam, mu, nu) == 0


def test_nc_triangle_passes_trivially():
    """nc_triangle e' True quando tutte le prime righe soddisfano la disuguaglianza."""
    # lam=(3,), mu=(2,1), nu=(2,1), d=3: 3>=2+2-3=1 ✓; 2>=3+2-3=2 ✓; 2>=3+2-3=2 ✓
    assert nc_triangle((3,), (2, 1), (2, 1))


# ─────────────────────────────────────────────────────────────────────────────
#  g_canonical: invarianza sull'orbita g-simmetrica
# ─────────────────────────────────────────────────────────────────────────────

def test_g_canonical_same_for_orbit_members():
    """Tutti i membri dell'orbita g-simmetrica hanno lo stesso canonico."""
    t = ((3, 2), (4, 1), (2, 2, 1))
    orbit = g_orbit(t)
    canon = g_canonical(t)
    for rep in orbit:
        assert g_canonical(rep) == canon


def test_g_canonical_is_minimum():
    """g_canonical e' il minimo lessicografico dell'orbita."""
    t = ((2, 1), (3,), (2, 1))
    orbit = g_orbit(t)
    assert g_canonical(t) == min(orbit)


# ─────────────────────────────────────────────────────────────────────────────
#  hunt(4): sanity Entry 30 e conteggi esatti
# ─────────────────────────────────────────────────────────────────────────────

def test_hunt_d4_entry30_sanity():
    """hunt(4): i conteggi con NC VECCHIE coincidono con Entry 30 (2/2/0)."""
    r = hunt(4)
    ok, expected = sanity_entry30(r)
    assert ok, (
        f"Sanity Entry 30 FALLITA a d=4: "
        f"atteso {expected}, "
        f"ottenuto ({r.n_sporadic_old},{r.n_covered_old},{r.n_uncovered_old})"
    )


def test_hunt_d4_extended_ncs():
    """hunt(4): le NC estese possono solo ridurre i sporadici rispetto alle vecchie."""
    r = hunt(4)
    assert r.n_sporadic <= r.n_sporadic_old, (
        "Le NC estese non possono AUMENTARE i sporadici rispetto alle vecchie"
    )
    assert r.n_uncovered <= r.n_sporadic, "uncovered e' un sottoinsieme di sporadic"
    assert r.n_covered_ext + r.n_uncovered <= r.n_sporadic


def test_hunt_d5_entry30_sanity():
    """hunt(5): i conteggi con NC VECCHIE coincidono con Entry 30 (5/5/0)."""
    r = hunt(5)
    ok, expected = sanity_entry30(r)
    assert ok, (
        f"Sanity Entry 30 FALLITA a d=5: "
        f"atteso {expected}, "
        f"ottenuto ({r.n_sporadic_old},{r.n_covered_old},{r.n_uncovered_old})"
    )


def test_hunt_d5_consistency():
    """hunt(5): somme interne consistenti."""
    r = hunt(5)
    assert r.n_explained + r.n_sporadic == r.n_zeros
    assert r.n_covered_ext + r.n_uncovered <= r.n_sporadic
    assert len(r.uncovered_canon) == r.n_uncovered


# ─────────────────────────────────────────────────────────────────────────────
#  stretch_triple
# ─────────────────────────────────────────────────────────────────────────────

def test_stretch_triple_n1_identity():
    """stretch_triple(t, 1) == t."""
    t = ((3, 2), (4, 1), (3, 1, 1))
    assert stretch_triple(t, 1) == t


def test_stretch_triple_n2_values():
    """stretch_triple(t, 2) raddoppia ogni parte."""
    t = ((2, 1), (2, 1), (2, 1))
    s = stretch_triple(t, 2)
    assert s == ((4, 2), (4, 2), (4, 2))


def test_stretch_triple_sum():
    """La somma di N*lam = N * sum(lam)."""
    t = ((3, 1, 1), (2, 2, 1), (4, 1))
    N = 3
    s = stretch_triple(t, N)
    for p_orig, p_str in zip(t, s):
        assert sum(p_str) == N * sum(p_orig)


# ─────────────────────────────────────────────────────────────────────────────
#  hunt(6): sanity Entry 30 (slow — richiede d=6)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.slow
@pytest.mark.timeout(300)
def test_hunt_d6_entry30_sanity():
    """hunt(6): i conteggi con NC VECCHIE coincidono con Entry 30 (44/44/0)."""
    r = hunt(6)
    ok, expected = sanity_entry30(r)
    assert ok, (
        f"Sanity Entry 30 FALLITA a d=6: "
        f"atteso {expected}, "
        f"ottenuto ({r.n_sporadic_old},{r.n_covered_old},{r.n_uncovered_old})"
    )


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_hunt_d6_nc_fp_check():
    """nc_dvir_full e nc_triangle hanno zero falsi positivi a d=6."""
    assert false_positives_dvir(6) == []
    assert false_positives_triangle(6) == []


# ─────────────────────────────────────────────────────────────────────────────
#  hunt(7): misura oltre il muro (slow)
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.slow
@pytest.mark.timeout(300)
def test_hunt_d7_runs_and_consistent():
    """hunt(7): termina e produce conteggi consistenti (oltre il muro)."""
    r = hunt(7)
    assert r.d == 7
    assert r.n_zeros >= 0
    assert r.n_explained + r.n_sporadic == r.n_zeros
    assert r.n_covered_ext + r.n_uncovered <= r.n_sporadic
    assert len(r.uncovered_canon) == r.n_uncovered
    # uncovered_canon e' ordinato e deduplico per orbita g-simmetrica
    for t in r.uncovered_canon:
        assert g_canonical(t) == t, f"Canonico non normalizzato: {t}"


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_hunt_d7_uncovered_are_genuine_zeros():
    """Ogni uncovered a d=7 ha g=0 e tutte le NC soddisfatte."""
    r = hunt(7)
    character_table(7)
    for t in r.uncovered_canon:
        assert g_fast(*t) == 0, f"uncovered ha g>0: {t}"
        lam, mu, nu = t
        from pnp_lab.gct_kronecker.kronecker import nc_length, nc_maxpart
        assert nc_length(lam, mu, nu), f"nc_length violata su uncovered: {t}"
        assert nc_dvir_full(lam, mu, nu), f"nc_dvir_full violata su uncovered: {t}"
        assert nc_triangle(lam, mu, nu), f"nc_triangle violata su uncovered: {t}"
