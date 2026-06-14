"""Locality barrier (Magnification Frontier, ciclo 1) — test ESATTI su MCSP[s].

Modello eseguibile FEDELE di un muro NOTO (la barriera di localita' della hardness
magnification), non contenuto nuovo. Tutti i numeri sono interi esatti, rigenerabili.
"""

import pickle
from fractions import Fraction
from pathlib import Path

import pytest

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.meta_complexity import locality

_CT4_CACHE = Path(__file__).resolve().parent.parent / ".cache" / "ct4.pkl"


# ── la meta-funzione e la prima misura decisiva (killer-fedelta') ──────────

def test_meta_input_space_is_2_to_the_N():
    """Gli input di MCSP sono 2^N = 2^(2^n) (una per funzione n-bit), NON 2^n.
    A n=3: N=8, quindi 256 meta-input (il bug iniziale usava 8)."""
    ct = min_formula_sizes(3)
    meta = locality.meta_truth_table(ct, 4)
    assert len(meta) == 1 << (1 << ct.n) == 256


def test_hard_count_n3_s4_is_50():
    """H = #{cost>4} a n=3 = 32+16+2 = 50 (dalla distribuzione esatta di Module 6)."""
    ct = min_formula_sizes(3)
    meta = locality.meta_truth_table(ct, 4)
    assert locality.hard_count(meta) == 50


def test_decisive_measurement_killer_fidelity_passes():
    """KILLER-FEDELTA': se MCSP[4] degenerasse a un junta piccolo (loc<=3) a n=3 la
    barriera sarebbe invisibile (giocattolo). Misura: relevant_coordinates = TUTTE
    le 8 -> 8-junta genuino -> killer superato, il muro e' reale a n=3."""
    ct = min_formula_sizes(3)
    meta = locality.meta_truth_table(ct, 4)
    rel = locality.relevant_coordinates(meta, 8)
    assert rel == set(range(8))          # 8/8 rilevanti
    assert locality.loc(meta, 8) == 8


# ── la tabella-ostruzione: il muro come interi (n=3, s=4) ──────────────────

def test_obstruction_table_n3_s4_frozen():
    """Numeri esatti congelati. certified(k) = istanze dure che un argomento
    k-locale certifica con certezza (fibra pura-dura): resta 0 finche' k<=5, poi
    8,16, e raggiunge H=50 solo al junta pieno k=8. E' il muro di localita'."""
    ct = min_formula_sizes(3)
    rows = locality.obstruction(ct, 4)
    certified = [r.certified for r in rows]
    assert certified == [0, 0, 0, 0, 0, 0, 8, 16, 50]
    A = [r.A for r in rows]
    assert A == [206, 206, 206, 206, 210, 214, 218, 222, 256]
    assert all(r.H == 50 for r in rows)


def test_certified_is_monotone_and_endpoints():
    """certified(k) non-decrescente in k; certified(N)=H (junta pieno certifica
    tutto); A(0)=max(H, totale-H) (classificatore costante)."""
    ct = min_formula_sizes(3)
    meta = locality.meta_truth_table(ct, 4)
    rows = locality.obstruction(ct, 4)
    cert = [r.certified for r in rows]
    assert all(cert[i] <= cert[i + 1] for i in range(len(cert) - 1))
    assert cert[-1] == locality.hard_count(meta)        # k=N certifica H
    assert rows[0].A == max(50, 256 - 50)               # A(0) = 206


# ── la LEVA: il muro attraverso i livelli (staircase) ──────────────────────

def test_leverage_staircase_n2_n3_is_degenerate_H2():
    """A n=2,3 la banda-dura ha H=2 (la parita' e la sua negazione: le 2 funzioni
    massimamente dure). Con 2 sole istanze, massimamente sparse, NESSUNA fibra di
    N-1 bit e' pura-dura -> k*=N, rho=1. ATTENZIONE: questo rho=1 NON e' il muro di
    magnification, e' l'artefatto della banda degenere H=2 (vedi il test n4)."""
    cts = [min_formula_sizes(2), min_formula_sizes(3)]
    rows = locality.leverage(cts)
    assert [r.H for r in rows] == [2, 2]                # banda dura degenere
    assert [r.k_star for r in rows] == [4, 8]
    assert [r.N for r in rows] == [4, 8]
    assert all(r.rho == 1.0 for r in rows)
    assert all(r.loc == r.N for r in rows)              # junta non degenere a ogni n


def test_hardest_band_threshold():
    ct = min_formula_sizes(3)
    assert locality.hardest_band_threshold(ct) == max(ct.cost.values()) - 1 == 8


@pytest.mark.slow
@pytest.mark.timeout(900)
def test_leverage_staircase_FALSIFIED_at_n4():
    """IL TAGLIO ORIZZONTALE (falsificazione esatta). n=4 (N=16, 65536 meta-input):
    l'ipotesi 'rho=1 a ogni livello, k* raddoppia 4->8->16' E' FALSA. La banda-dura
    a n=4 ha H=114 (non 2): compaiono fibre pura-dura SOTTO il junta pieno
    (cert(15)=24, cert(14)=8, cert(13)=0), quindi k*=14 e rho=0.875<1. Il rho=1 a
    n<=3 era l'artefatto della banda degenere H=2, non il muro di magnification.

    Usa la cache `.cache/ct4.pkl` se presente (build n=4 ~500-900s); altrimenti la
    ricostruisce (con timeout 900s) — cosi' la falsificazione e' CI-rigenerabile."""
    if _CT4_CACHE.exists():
        with open(_CT4_CACHE, "rb") as f:
            ct4 = pickle.load(f)
    else:
        ct4 = min_formula_sizes(4)
    assert ct4.complete and ct4.max_cost == 15        # no artefatto da `cap`
    rows = locality.leverage([min_formula_sizes(2), min_formula_sizes(3), ct4])
    assert [r.N for r in rows] == [4, 8, 16]
    assert [r.H for r in rows] == [2, 2, 114]          # H non monotona: l'artefatto
    assert [r.k_star for r in rows] == [4, 8, 14]      # NON [4,8,16]
    assert [r.rho for r in rows] == [1.0, 1.0, 0.875]  # rho crolla: leva falsificata
    # la coda del decadimento a n=4 (la pendenza del muro togliendo bit dall'alto)
    meta4 = locality.meta_truth_table(ct4, locality.hardest_band_threshold(ct4))
    tail = [locality.certified_k_local(meta4, 16, k) for k in (16, 15, 14, 13)]
    assert tail == [114, 24, 8, 0]


# ── CICLO 2: il taglio ORIZZONTALE (policy frazione fissa, c(j) razionali) ──

def test_fixed_fraction_threshold_bankers_rounding_frozen():
    """s = round(maxcost * 0.5) con banker's rounding di Python (congelato dal valore
    MISURATO). n=2: maxcost=3 -> round(1.5)=2. n=3: maxcost=9 -> round(4.5)=4 (NON 5:
    banker's). n=4: maxcost=15 -> round(7.5)=8."""
    assert locality.fixed_fraction_threshold(min_formula_sizes(2)) == 2   # round(1.5)
    assert locality.fixed_fraction_threshold(min_formula_sizes(3)) == 4   # round(4.5)=4
    # n=4 senza ricostruire: maxcost noto = 15 -> round(7.5)=8
    assert round(15 * 0.5) == 8


def test_obstruction_curve_n3_frozen_rationals():
    """Curva c(j) a n=3 (s=4, H=50), razionali ESATTI MISURATI e congelati.
    c(0)=1 (junta pieno), c(1)=16/50=8/25, c(2)=8/50=4/25."""
    ct = min_formula_sizes(3)
    s = locality.fixed_fraction_threshold(ct)
    assert s == 4
    meta = locality.meta_truth_table(ct, s)
    assert locality.hard_count(meta) == 50
    c = locality.obstruction_curve(meta, 8, jmax=2)
    assert c == [Fraction(1), Fraction(8, 25), Fraction(4, 25)]


def test_obstruction_curve_empty_when_H_zero():
    """H==0 -> curva VUOTA (documentato): s oltre maxcost rende nessuna istanza dura."""
    ct = min_formula_sizes(2)
    meta = locality.meta_truth_table(ct, 99)   # s enorme -> nessuna dura
    assert locality.hard_count(meta) == 0
    assert locality.obstruction_curve(meta, 4, jmax=2) == []


def test_level_curves_loc_full_at_n2_n3():
    """KILLER-B (fidelity): con frazione fissa loc==N gia' a n=2,3 (junta NON degenere)
    e H>=2. Se loc<N la barriera sarebbe invisibile (giocattolo)."""
    rows = locality.level_curves([min_formula_sizes(2), min_formula_sizes(3)])
    assert [r.N for r in rows] == [4, 8]
    assert [r.s for r in rows] == [2, 4]
    assert [r.H for r in rows] == [2, 50]
    assert all(r.loc == r.N for r in rows)            # junta non degenere
    assert rows[0].c == [Fraction(1), Fraction(0), Fraction(0)]   # n=2 ancora sparso
    assert rows[1].c == [Fraction(1), Fraction(8, 25), Fraction(4, 25)]


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_level_invariance_n3_vs_n4_KILLER_A():
    """IL TEST DECISIVO (killer dell'Explorer ciclo 2). Ipotesi: c(j)=certified(N-j)/H
    e' un INVARIANTE DI LIVELLO (c(1),c(2) coincidono come razionali tra n=3 e n=4).

    ESITO OSSERVATO: KILLER-A E' SCATTATO. c(1) e c(2) DIFFERISCONO:
        c(1)@n3 = 8/25     = 0.320   !=  c(1)@n4 = 8990/12977 = 0.6928
        c(2)@n3 = 4/25     = 0.160   !=  c(2)@n4 = 6068/12977 = 0.4676
    Solo c(0)=1 regge (banale: junta pieno certifica H). L'IPOTESI E' FALSIFICATA:
    c(j) NON e' level-invariant; la frazione certificabile (N-1)/(N-2)-locale CRESCE
    con n. Asserisco i valori VERI misurati (cache ct4.pkl), e l'INDISUGUAGLIANZA.
    """
    if not _CT4_CACHE.exists():
        pytest.skip(f"cache n=4 assente: {_CT4_CACHE}")
    with open(_CT4_CACHE, "rb") as f:
        ct4 = pickle.load(f)
    assert ct4.complete and ct4.max_cost == 15

    ct3 = min_formula_sizes(3)
    s3 = locality.fixed_fraction_threshold(ct3)
    s4 = locality.fixed_fraction_threshold(ct4)
    assert (s3, s4) == (4, 8)

    meta3 = locality.meta_truth_table(ct3, s3)
    meta4 = locality.meta_truth_table(ct4, s4)
    assert locality.hard_count(meta3) == 50
    assert locality.hard_count(meta4) == 25954

    c3 = locality.obstruction_curve(meta3, 8, jmax=2)
    c4 = locality.obstruction_curve(meta4, 16, jmax=2)

    # valori VERI congelati
    assert c3 == [Fraction(1), Fraction(8, 25), Fraction(4, 25)]
    assert c4 == [Fraction(1), Fraction(8990, 12977), Fraction(6068, 12977)]

    # c(0) regge (banale), c(1) e c(2) NO -> KILLER-A
    assert c3[0] == c4[0] == Fraction(1)
    assert c3[1] != c4[1]                 # 8/25 != 8990/12977
    assert c3[2] != c4[2]                 # 4/25 != 6068/12977
    # loc pieno a entrambi (KILLER-B superato anche a frazione fissa)
    assert locality.loc(meta3, 8) == 8
    assert locality.loc(meta4, 16) == 16
