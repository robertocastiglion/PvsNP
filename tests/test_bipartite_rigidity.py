"""Test ESATTI dell'arena Bipartite Rigidity (ancore verdi + killer su tiny).

Veloci di default; i sweep pesanti (k=3 rigidity, perm-spread completo) sono `slow`.
"""

from fractions import Fraction

import pytest

from pnp_lab.bipartite_rigidity import killers as K
from pnp_lab.bipartite_rigidity import rigidity as R


# --------------------------------------------------------------------------- #
#  Ancore verdi (killer di bug)                                               #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("k", [1, 2, 3])
def test_rank_gf2_ip_equals_k(k):
    """rank_gf2(IP_k) = k."""
    assert R.rank_gf2(R.ip_matrix_gf2(k)) == k


@pytest.mark.parametrize("k", [1, 2, 3])
def test_hadamard_full_rank_q(k):
    """La matrice di Hadamard ±1 ha rango razionale pieno = 2^k."""
    assert R.rank_q(R.hadamard_matrix(k)) == (1 << k)


def test_rank_q_accepts_int_and_fraction():
    """rank_q coerente su entrate int e Fraction (stessa matrice)."""
    Mi = R.ip_matrix_gf2(3)                       # entrate int 0/1
    Mf = tuple(tuple(Fraction(e) for e in row) for row in Mi)
    assert R.rank_q(Mi) == R.rank_q(Mf)


def test_rigidity_zero_if_already_low_rank():
    """La rigidita' di una matrice gia' a rango <= r e' 0 (nessun flip)."""
    H = R.hadamard_matrix(2)                       # rank_q = 4
    assert R.rigidity_q_pm_exact(H, 4) == 0        # r = 4 >= rank -> 0
    A = R.ip_matrix_gf2(2)                          # rank_gf2 = 2
    assert R.rigidity_gf2_exact(A, 2) == 0         # r = 2 >= rank -> 0


def test_rigidity_monotone_non_increasing_in_r():
    """R_M(r) e' non-crescente in r (target piu' permissivo -> meno flip).

    Range r in 1..4: per ±1 il rango 0 e' irraggiungibile per sola negazione di segno
    (una matrice ±1 non e' mai nulla), quindi si parte da r=1."""
    H = R.hadamard_matrix(2)
    vals = [R.rigidity_q_pm_exact(H, r, max_flips=6) for r in range(1, 5)]
    assert all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
    assert all(v >= 0 for v in vals)


def test_rigidity_gf2_k2_known_values():
    """Valori esatti GF(2) di IP_2 (4x4): R(0)=6, R(1)=3, R(2)=0, R(3)=0."""
    A = R.ip_matrix_gf2(2)
    assert [R.rigidity_gf2_exact(A, r) for r in range(4)] == [6, 3, 0, 0]


def test_rigidity_q_hadamard_k2_known_values():
    """Valori esatti Q (negazione segno) di H_2 (4x4): R(1)=4, R(2)=3, R(3)=2."""
    H = R.hadamard_matrix(2)
    assert R.rigidity_q_pm_exact(H, 1, max_flips=6) == 4
    assert R.rigidity_q_pm_exact(H, 2, max_flips=6) == 3
    assert R.rigidity_q_pm_exact(H, 3, max_flips=6) == 2


# --------------------------------------------------------------------------- #
#  Lower bound certificato (CITED) — forma chiusa, sempre disponibile          #
# --------------------------------------------------------------------------- #

def test_certified_lb_closed_form():
    """rigidity_certified_lb = floor(n^2 / (4(r+1))), n = 2^k; 0 se r >= n."""
    assert R.rigidity_certified_lb(4, 2) == (256) // (4 * 3)    # 21
    assert R.rigidity_certified_lb(5, 4) == (1024) // (4 * 5)   # 51
    assert R.rigidity_certified_lb(2, 4) == 0                   # r >= n=4


# --------------------------------------------------------------------------- #
#  Killer su k=2 — FAST su campione deterministico (l'esaustivo 65536 e' slow) #
# --------------------------------------------------------------------------- #

# k=2: 2k=4 bit -> 2^16 = 65536 truth tables. Campione deterministico per i test fast.
import random as _random

_K2_SAMPLE = sorted(_random.Random(0).sample(range(1 << 16), 400))


def test_killer1_reducible_from_rank_k2_sample():
    """killer-1 su un campione k=2: esatto e deterministico (regressione del verdetto)."""
    reducible, splits = K.reducible_from_rank(2, 2, sample=_K2_SAMPLE, max_flips=4)
    assert isinstance(reducible, bool)
    assert reducible == (len(splits) == 0)        # coerenza interna del verdetto
    for key, vals in splits:
        assert len(vals) >= 2


def test_killer2_dict_table_k2_sample():
    """killer-2 su un campione k=2: dizionario congiunto vs rigidita'."""
    reconstructible, splits = K.dict_table(2, 2, sample=_K2_SAMPLE, max_flips=4)
    assert isinstance(reconstructible, bool)
    for key, vals in splits:
        assert len(vals) >= 2


def test_side_mixing_control_sensitivity_flat():
    """Controllo perm-non-invarianza: sotto S_4 che mescola i lati, la sensitivity
    (perm-invariant) e' PIATTA (un solo valore), mentre la rigidita' puo' variare."""
    tt = 0b0110100110010110
    rig, sens = K.side_mixing_spread(tt, 2, 2, max_flips=6)
    assert len(set(sens)) == 1            # statistica globale di f: PIATTA (anchor)
    assert len(rig) == 24                 # |S_4| = 24


# --------------------------------------------------------------------------- #
#  Sweep pesanti — SLOW                                                       #
# --------------------------------------------------------------------------- #

@pytest.mark.slow
@pytest.mark.timeout(300)
def test_rigidity_gf2_k3_boundary():
    """k=3 (8x8) GF(2): boundary ONESTO.  IP_3 ha rank_gf2=3 => R(r)=0 per r>=3.
    Per r=2 (< rango) il minimo e' STRETTAMENTE > 3 entro budget pratico: la ricerca
    esaustiva oltre esplode (C(64,t)), quindi CERTIFICHIAMO solo il lower bound, non
    un valore esatto (onesta': nessun valore inventato)."""
    A = R.ip_matrix_gf2(3)
    assert R.rigidity_gf2_exact(A, 3) == 0
    # r=2: confermiamo R > 3 (il budget 3 NON basta) -> RuntimeError atteso.
    with pytest.raises(RuntimeError):
        R.rigidity_gf2_exact(A, 2, max_flips=3)


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_hadamard_k3_rigidity_lower_bound():
    """k=3 (8x8) Q ±1 Hadamard a target r=4=2^{k-1}: R > 2 entro budget pratico
    (budget 3 ~ 86 s).  Boundary onesto: l'esatto e' fuori portata dell'esaustivo;
    il regime k=3 e' COMPUTED solo come lower bound, non come valore esatto."""
    H = R.hadamard_matrix(3)
    with pytest.raises(RuntimeError):
        R.rigidity_q_pm_exact(H, 4, max_flips=2)


@pytest.mark.slow
@pytest.mark.timeout(900)
def test_killer_k2_exhaustive():
    """Sweep ESAUSTIVO k=2 (tutte le 65536 truth table su 2k=4 bit): il verdetto
    esatto dei killer sull'intera popolazione.  Una sola passata di rigidita'
    (~450 s), poi entrambe le riduzioni sulle stesse righe."""
    rows = K.rig_rows(2, 2, max_flips=4)
    reducible, sp1 = K.reducible_from_rank_rows(rows)
    ct = K._load_cost_table(4)
    reconstructible, sp2 = K.dict_table_rows(rows, 4, ct)
    # Predizione lever-A: ENTRAMBI i killer NON sparano (rigidita' fuori dizionario).
    assert reducible is False and len(sp1) >= 1
    assert reconstructible is False and len(sp2) >= 1


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_side_mixing_spread_nontrivial_exists():
    """Esiste una f su 4 bit la cui rigidita' VARIA sotto mescolamento dei lati
    (spread>1) mentre la sua sensitivity resta piatta — conferma il lever-A
    (non-perm-invariant) su almeno un testimone (cerca su un prefisso di funzioni)."""
    found = False
    for tt in range(2000):
        rig, sens = K.side_mixing_spread(tt, 2, 2, max_flips=4)
        if len(set(rig)) > 1:
            assert len(set(sens)) == 1
            found = True
            break
    assert found
