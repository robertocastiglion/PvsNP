"""Order-locality (Magnification Frontier, Cycle 3) — MBPSP[s] at a FIXED order.

The reopening of the program: a meta-object that is NOT permutation-invariant.
Exact integers, frozen and CI-reproducible.  The decisive n=4 measurement runs in
~2s (OBDD costs need no DP table), so it is NOT marked slow; only the MCSP control
(which needs the n=4 formula-size cache) is gated.
"""

import pickle
from itertools import combinations
from pathlib import Path

import pytest

from pnp_lab.meta_complexity import locality
from pnp_lab.meta_complexity import order_locality as ol

_CT4_CACHE = Path(__file__).resolve().parent.parent / ".cache" / "ct4.pkl"


# ── ROBDD a ordine fisso: correttezza esatta ───────────────────────────────

def test_min_obdd_size_known_functions():
    """Valori canonici. f=x0 (n=1): 1 nodo interno + 2 terminali = 3.  costante 0:
    1 terminale.  AND a 2 var: nodo x1 -> (term0, nodo x0 -> (term0,term1)) = 4."""
    assert ol.min_obdd_size(0b10, 1) == 3          # f = x0
    assert ol.min_obdd_size(0, 1) == 1             # f = 0 (un terminale)
    assert ol.min_obdd_size(0b11, 1) == 1          # f = 1 (truth-table 0b11)
    assert ol.min_obdd_size(8, 2) == 4             # f = x0 AND x1 (truth-table 0b1000)


def test_obdd_invariant_under_variable_negation():
    """Negare una variabile scambia i due figli di un nodo: la dimensione OBDD NON
    cambia.  (E' l'invarianza per traslazione che rende l'influenza di singola
    coordinata inutile -> serve la pair-influence.)"""
    n = 3
    for t in (0b10110100, 0b11010010, 0b01101001):
        # negare la variabile 0 = scambiare, per ogni input, x con x^1
        neg = 0
        for x in range(1 << n):
            if (t >> x) & 1:
                neg |= 1 << (x ^ 1)
        assert ol.min_obdd_size(neg, n) == ol.min_obdd_size(t, n)


def test_min_obdd_size_NOT_permutation_invariant():
    """LA PROVA FONDANTE.  La stessa funzione, con due variabili scambiate, e' una
    truth-table diversa con dimensione OBDD diversa allo stesso ordine: 6 vs 8 per
    f = (x0&x1)|(x2&x3) contro (x0&x2)|(x1&x3).  La dimensione di FORMULA non puo'
    distinguerle (e' simmetrica) — qui sta tutta la differenza con MCSP."""
    n = 4

    def tt(f):
        out = 0
        for x in range(1 << n):
            b = [(x >> j) & 1 for j in range(n)]
            if f(b):
                out |= 1 << x
        return out

    tg = tt(lambda b: (b[0] & b[1]) | (b[2] & b[3]))
    tp = ol.variable_swap(tg, n, 1, 2)
    assert tp == tt(lambda b: (b[0] & b[2]) | (b[1] & b[3]))   # swap = la funzione attesa
    assert ol.min_obdd_size(tg, n) == 6
    assert ol.min_obdd_size(tp, n) == 8
    assert ol.min_obdd_size(tg, n) != ol.min_obdd_size(tp, n)  # NON invariante


# ── pair-influence e spread per classe di peso (n=2,3: ordine silente) ─────

def test_pairinf_spread_zero_at_n2_n3():
    """A n=2,3 lo spread e' 0 in ogni classe di peso: pairinf dipende solo dal peso.
    L'ordine NON morde ancora (la funzione testimone (x0 x1)|(x2 x3) richiede n=4).
    Valori esatti congelati."""
    # n=2: maxOBDD=5, s=round(2.5)=2 (banker's), H=14
    c2 = ol.obdd_costs(2)
    assert max(c2) == 5
    s2 = ol.fixed_fraction_threshold(c2)
    assert s2 == 2
    meta2 = ol.meta_truth_table_obdd(c2, s2)
    assert ol.hard_count(meta2) == 14
    wcs2 = ol.weight_class_spread(meta2, 4)
    assert [wc.spread for wc in wcs2] == [0, 0]
    assert [wc.lo for wc in wcs2] == [8, 8]

    # n=3: maxOBDD=7, s=round(3.5)=4, H=224
    c3 = ol.obdd_costs(3)
    assert max(c3) == 7
    s3 = ol.fixed_fraction_threshold(c3)
    assert s3 == 4
    meta3 = ol.meta_truth_table_obdd(c3, s3)
    assert ol.hard_count(meta3) == 224
    wcs3 = ol.weight_class_spread(meta3, 8)
    assert [wc.spread for wc in wcs3] == [0, 0, 0]
    assert [wc.lo for wc in wcs3] == [104, 112, 128]


# ── IL TEST DECISIVO: n=4, l'ordine SOPRAVVIVE (killer dell'Explorer) ──────

def test_DECISIVE_order_survives_at_n4():
    """KILLER (Explorer Cycle 3).  Ipotesi: MBPSP[s] e' un oggetto meta-livello NON
    permutazione-invariante <=> pairinf(d) dipende dal SUPPORTO di d, non solo dal
    peso <=> spread > 0 in qualche classe.  Killer FIRES se spread=0 ovunque anche a
    n=4 (l'ordine si laverebbe via -> 6 collasso).  ESITO: PASSA.  A n=4 (maxOBDD=11,
    s=6, H=64282) lo spread e' 184/176/16/0 per w=1..4.  Valori esatti congelati;
    veloce (nessuna DP, ~2s)."""
    costs = ol.obdd_costs(4)
    assert max(costs) == 11
    s = ol.fixed_fraction_threshold(costs)
    assert s == 6
    meta = ol.meta_truth_table_obdd(costs, s)
    assert ol.hard_count(meta) == 64282

    wcs = ol.weight_class_spread(meta, 16)
    assert [wc.spread for wc in wcs] == [184, 176, 16, 0]      # ordine sopravvive
    assert any(wc.spread > 0 for wc in wcs)

    # struttura per supporto (congelata): w=1, l'influenza dipende da QUALE variabile.
    w1 = {d: v for d, v in wcs[0].pairinf}
    assert w1 == {1: 4024, 2: 3872, 4: 3880, 8: 4056}
    # differire nella variabile in cima all'ordine (x3, d=8) != differire in x1 (d=2)
    assert w1[8] != w1[2]


def test_order_asymmetry_staircase_frozen():
    """La leva attraverso i livelli: spread=0 a n=2,3 (ordine silente), >0 a n=4
    (accensione).  order_survives traccia esattamente dove parte la scala."""
    rows = ol.order_asymmetry([2, 3, 4])
    assert [r.N for r in rows] == [4, 8, 16]
    assert [r.s for r in rows] == [2, 4, 6]
    assert [r.H for r in rows] == [14, 224, 64282]
    assert [r.spreads for r in rows] == [[0, 0], [0, 0, 0], [184, 176, 16, 0]]
    assert [r.order_survives for r in rows] == [False, False, True]


# ── IL CONTROLLO: MCSP[s] (formula) si lava via anche a n=4 ────────────────

@pytest.mark.slow
@pytest.mark.timeout(120)
def test_MCSP_control_washes_out_at_n4():
    """CONTRO-PROVA.  Sulla stessa misura, la meta-funzione MCSP a FORMULA (Module 21)
    ha spread = 0 in OGNI classe anche a n=4 (s=8, H=25954): pairinf dipende solo dal
    peso = permutazione-invariante.  E' la ragione strutturale per cui il sotto-ramo
    locality si chiuse; il contrasto con MBPSP (spread>0) e' tutto il punto del ciclo.
    Gated sulla cache formula-size n=4."""
    if not _CT4_CACHE.exists():
        pytest.skip(f"cache n=4 assente: {_CT4_CACHE}")
    with open(_CT4_CACHE, "rb") as f:
        ct4 = pickle.load(f)
    assert ct4.complete and ct4.max_cost == 15

    N = 16
    form = [ct4.cost[t] for t in range(1 << N)]
    s = ol.fixed_fraction_threshold(form)       # round(15*0.5)=8
    assert s == 8
    meta = ol.meta_truth_table_obdd(form, s)     # riusa la stessa soglia/meta
    assert ol.hard_count(meta) == 25954

    wcs = ol.weight_class_spread(meta, N)
    assert [wc.spread for wc in wcs] == [0, 0, 0, 0]      # permutazione-invariante
    assert [wc.lo for wc in wcs] == [31080, 31288, 31896, 31896]


# ── CICLO 4: l'ordine RAGGIUNGE il muro FEDELE di Module 21 ────────────────

def test_certified_drop_IS_the_Module21_wall():
    """FEDELTA': certified_drop_pair non e' una ridefinizione. Il MAX su tutte le coppie
    rilasciate eguaglia ESATTAMENTE locality.certified_k_local(meta, N, N-2) (il muro di
    certificazione pura-dura di Module 21). Verificato a n=3 (=152). E la traslazione-
    invarianza: certified_drop(a,b)=certified_drop(0,a^b) (negazione di variabile =
    permutazione delle posizioni, simmetria di MBPSP)."""
    n, N = 3, 8
    costs = ol.obdd_costs(n)
    s = ol.fixed_fraction_threshold(costs)
    meta = ol.meta_truth_table_obdd(costs, s)
    mx = max(ol.certified_drop_pair(meta, a, b) for a, b in combinations(range(N), 2))
    assert mx == locality.certified_k_local(meta, N, N - 2) == 152
    assert all(ol.certified_drop_pair(meta, a, b) == ol.certified_drop_pair(meta, 0, a ^ b)
               for a, b in combinations(range(N), 2))


def test_wall_isotropic_at_n3():
    """A n=3 il muro e' ISOTROPICO (ordine silente): certified_drop dipende solo dal
    peso. Valori esatti congelati."""
    costs = ol.obdd_costs(3)
    s = ol.fixed_fraction_threshold(costs)
    meta = ol.meta_truth_table_obdd(costs, s)
    dcs = ol.certified_drop_spread(meta, 8)
    assert [dc.spread for dc in dcs] == [0, 0, 0]
    assert [dc.lo for dc in dcs] == [152, 144, 128]


def test_DECISIVE_wall_sees_order_at_n4():
    """KILLER (Explorer Cycle 4). Ipotesi: il MURO fedele di Module 21 e' order-
    anisotropico su MBPSP <=> certified_drop(d) dipende dal SUPPORTO di d (spread>0).
    Killer FIRES se spread=0 ovunque anche a n=4 (la massimizzazione resterebbe vacua
    sul muro -> ricaduta nella trappola simmetrica di Module 21 -> 12 collasso). ESITO:
    PASSA. n=4 (s=6, H=64282): spread = 144,144,16,0. Veloce, niente cache. Congelato."""
    costs = ol.obdd_costs(4)
    s = ol.fixed_fraction_threshold(costs)
    meta = ol.meta_truth_table_obdd(costs, s)
    assert (s, ol.hard_count(meta)) == (6, 64282)

    dcs = ol.certified_drop_spread(meta, 16)
    assert [dc.spread for dc in dcs] == [144, 144, 16, 0]      # muro vede l'ordine
    assert any(dc.spread > 0 for dc in dcs)

    # struttura per supporto (congelata): w=1, il muro dipende da QUALE variabile.
    w1 = {d: v for d, v in dcs[0].certified}
    assert w1 == {1: 61480, 2: 61592, 4: 61592, 8: 61448}
    assert w1[2] != w1[8]


def test_wall_anisotropy_staircase_frozen():
    """La leva del ciclo 4 attraverso i livelli: muro isotropico a n=3, anisotropico a
    n=4. wall_sees_order traccia dove l'ordine raggiunge il muro fedele."""
    rows = ol.wall_anisotropy([3, 4])
    assert [r.N for r in rows] == [8, 16]
    assert [r.s for r in rows] == [4, 6]
    assert [r.H for r in rows] == [224, 64282]
    assert [r.spreads for r in rows] == [[0, 0, 0], [144, 144, 16, 0]]
    assert [r.wall_sees_order for r in rows] == [False, True]


@pytest.mark.slow
@pytest.mark.timeout(120)
def test_MCSP_wall_isotropic_at_n4_control():
    """CONTRO-PROVA. Lo stesso muro certified_drop su MCSP (formula) e' ISOTROPICO in
    OGNI classe anche a n=4 (s=8, H=25954): spread=0 -> la massimizzazione e' vacua, il
    muro e' una statistica simmetrica del set duro = la trappola che chiuse Module 21.
    Gated sulla cache formula-size n=4."""
    if not _CT4_CACHE.exists():
        pytest.skip(f"cache n=4 assente: {_CT4_CACHE}")
    with open(_CT4_CACHE, "rb") as f:
        ct4 = pickle.load(f)
    assert ct4.complete and ct4.max_cost == 15

    form = [ct4.cost[t] for t in range(1 << 16)]
    s = ol.fixed_fraction_threshold(form)
    meta = ol.meta_truth_table_obdd(form, s)
    assert (s, ol.hard_count(meta)) == (8, 25954)

    dcs = ol.certified_drop_spread(meta, 16)
    assert [dc.spread for dc in dcs] == [0, 0, 0, 0]          # isotropico
    assert [dc.lo for dc in dcs] == [12136, 11152, 10440, 10584]
