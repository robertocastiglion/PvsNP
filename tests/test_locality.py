"""Locality barrier (Magnification Frontier, ciclo 1) — test ESATTI su MCSP[s].

Modello eseguibile FEDELE di un muro NOTO (la barriera di localita' della hardness
magnification), non contenuto nuovo. Tutti i numeri sono interi esatti, rigenerabili.
"""

import pytest

from pnp_lab.circuits import min_formula_sizes
from pnp_lab.meta_complexity import locality


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
def test_leverage_staircase_FALSIFIED_at_n4():
    """IL TAGLIO ORIZZONTALE (falsificazione esatta). n=4 (N=16, 65536 meta-input):
    l'ipotesi 'rho=1 a ogni livello, k* raddoppia 4->8->16' E' FALSA. La banda-dura
    a n=4 ha H=114 (non 2): compaiono fibre pura-dura SOTTO il junta pieno
    (cert(15)=24, cert(14)=8, cert(13)=0), quindi k*=14 e rho=0.875<1. Il rho=1 a
    n<=3 era l'artefatto della banda degenere H=2, non il muro di magnification."""
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
