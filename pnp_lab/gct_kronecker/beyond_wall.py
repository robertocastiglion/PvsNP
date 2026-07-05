"""Caccia agli zeri di Kronecker fuori dizionario a d=7,8,9 — Ciclo 1 "la caccia".

Condizioni necessarie ESTESE per il non-vanishing g(lam,mu,nu)>0:
  nc_dvir_full  : lam[0] <= sum_i min(mu[i], nu[i])  (e permutazioni) — Dvir 1993, Thm 1.6
  nc_triangle   : lam[0] >= mu[0]+nu[0]-d             (e permutazioni) — Klyachko 2004

La misura `hunt(d)` classifica TUTTI i vanishing (g=0) in:
  explained   : g=0 e almeno una NC violata
  sporadic    : g=0 e TUTTE le NC soddisfatte (vecchie + nuove)
  covered_ext : sporadici con copertura strutturale (coverage.covered sull'orbita g)
  uncovered   : sporadici non coperti, deduplicate per orbita g-simmetrica

CONFINE DI ONESTA'.  La copertura riusa le stesse famiglie di Entry 30 (coverage.covered:
Rosas two-row/hook, std-otimes-std, Bessenrodt-Bowman rettangoli) senza modificarle.
Le famiglie B5 (multiplicity-free, Bessenrodt-Bowman 2017) e B6 (two-column/hook, Pak-Panova)
del dizionario prior-art NON sono implementate qui: un uncovered potrebbe essere coperto da B5/B6
(survival-by-omission dichiarato; cfr. docs/prior-art-kronecker-zeros.md, KILLER-0).
Il censimento numerico a d=7..9 e' una riproduzione di dati noti (Dataset ML; Coquereaux-Zuber);
la classificazione covered/sporadic per famiglie e' il discriminante potenzialmente nuovo.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Dict, List, Optional, Set, Tuple

from .kronecker import Partition, transpose, nc_length, nc_maxpart, _triples
from .coverage import covered, g_orbit
from .fast import g_fast, character_table

Triple = Tuple[Partition, Partition, Partition]


# ─────────────────────────────────────────────────────────────────────────────
#  Intersezione dei diagrammi di Young
# ─────────────────────────────────────────────────────────────────────────────

def _diagram_intersection(mu: Partition, nu: Partition) -> int:
    """Numero di celle del diagramma intersezione mu cap nu: sum_i min(mu_i, nu_i).

    Il diagramma intersezione di mu e nu e' il diagramma di Young con la riga i
    di lunghezza min(mu_i, nu_i).  Il conteggio totale e' sum_i min(mu_i, nu_i).
    ESATTO, aritmetica intera.
    """
    n = max(len(mu), len(nu))
    if n == 0:
        return 0
    return sum(
        min(mu[i] if i < len(mu) else 0, nu[i] if i < len(nu) else 0)
        for i in range(n)
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Condizioni necessarie estese
# ─────────────────────────────────────────────────────────────────────────────

def nc_dvir_full(lam: Partition, mu: Partition, nu: Partition) -> bool:
    """NC Dvir piena: g(lam,mu,nu)>0 ==> lam[0] <= |mu cap nu| (e TUTTE le permutazioni).

    Fonte: Dvir 1993, Thm 1.6.  |mu cap nu| = sum_i min(mu_i, nu_i).
    La condizione si applica a tutte e tre le permutazioni (g e' totalmente simmetrico).

    Restituisce True se la condizione E' soddisfatta (g POTREBBE essere >0).
    Restituisce False se la condizione E' violata (g DEVE essere 0).

    Verificata empiricamente su d<=6: ZERO falsi positivi (mai False quando g>0).
    NB: questa e' la forma COMPLETA di Dvir, potenzialmente piu' forte della variante
    nc_maxpart in kronecker.py che implementa un rilassamento via nc_length coniugato.
    """
    l1 = lam[0] if lam else 0
    m1 = mu[0] if mu else 0
    n1 = nu[0] if nu else 0
    return (
        l1 <= _diagram_intersection(mu, nu)
        and m1 <= _diagram_intersection(lam, nu)
        and n1 <= _diagram_intersection(lam, mu)
    )


def nc_triangle(lam: Partition, mu: Partition, nu: Partition) -> bool:
    """NC triangolare: g(lam,mu,nu)>0 ==> lam[0] >= mu[0]+nu[0]-d (e permutazioni).

    Fonte: Klyachko 2004; Christandl-Mitchison 2006 (faccette del politopo dei momenti
    di Kronecker).  Richiede che le prime righe (lam[0], mu[0], nu[0]) soddisfino
    la disuguaglianza triangolare rispetto a d: se mu[0]+nu[0]-d > lam[0] allora g=0.
    La condizione e' vuota (sempre soddisfatta) quando mu[0]+nu[0] <= d.

    Restituisce True se soddisfatta, False se violata.
    Verificata su d<=6: ZERO falsi positivi.
    """
    d = sum(lam)
    l1 = lam[0] if lam else 0
    m1 = mu[0] if mu else 0
    n1 = nu[0] if nu else 0
    return (
        l1 >= m1 + n1 - d
        and m1 >= l1 + n1 - d
        and n1 >= l1 + m1 - d
    )


def _all_ncs_old(lam: Partition, mu: Partition, nu: Partition) -> bool:
    """True se TUTTE le NC VECCHIE (length, maxpart) sono soddisfatte.

    Usato per il confronto con Entry 30 (sanity check).
    """
    return nc_length(lam, mu, nu) and nc_maxpart(lam, mu, nu)


def _all_ncs_ok(lam: Partition, mu: Partition, nu: Partition) -> bool:
    """True se TUTTE le NC (vecchie: length, maxpart; nuove: dvir_full, triangle) sono ok.

    Una terna con g=0 e _all_ncs_ok == True e' un vanishing SPORADICO ESTESO.
    """
    return (
        nc_length(lam, mu, nu)
        and nc_maxpart(lam, mu, nu)
        and nc_dvir_full(lam, mu, nu)
        and nc_triangle(lam, mu, nu)
    )


def explained_zero(triple: Triple) -> bool:
    """True se il vanishing e' SPIEGATO da almeno una NC estesa violata.

    Non verifica g=0 internamente (il chiamante deve garantire g(triple)==0).
    Una terna non spiegata (False) e' un candidato SPORADICO.
    """
    lam, mu, nu = triple
    return not _all_ncs_ok(lam, mu, nu)


def covered_ext(triple: Triple) -> bool:
    """Copertura strutturale estesa: riusa coverage.covered sull'orbita g-simmetrica.

    Identico a coverage.covered(triple): covered gia' controlla TUTTI i 24 rappresentanti
    dell'orbita g-simmetrica (S_3 x V_4).  Definito esplicitamente qui per chiarezza e per
    rendere visibile che covered_ext == covered (nessuna famiglia aggiuntiva implementata).
    """
    return covered(triple)


# ─────────────────────────────────────────────────────────────────────────────
#  Canonicalizzazione per orbita g-simmetrica
# ─────────────────────────────────────────────────────────────────────────────

def g_canonical(triple: Triple) -> Triple:
    """Rappresentante canonico dell'orbita g-simmetrica: minimo lessicografico.

    L'orbita e' generata da:
      - le 6 permutazioni S_3 dei tre argomenti;
      - il coniugio simultaneo di DUE qualsiasi dei tre argomenti (V_4 di Klein).
    Totale: max 24 rappresentanti distinti (|G| = |S_3 x V_4| = 24).

    Il canonico e' il minimo lessicografico su tuple di tuple di int.
    Usato per deduplicare i testimoni uncovered: due terne nella stessa orbita
    appaiono una volta sola nella lista finale.

    DEFINIZIONE ESATTA DELL'ORBITA (carico funzionale): identica a coverage.g_orbit,
    ossia {perm(conf): conf in {(l,m,n),(l',m',n),(l',m,n'),(l,m',n')}, perm in S_3}
    dove p' = transpose(p).
    """
    return min(g_orbit(triple))


# ─────────────────────────────────────────────────────────────────────────────
#  Risultato della caccia
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class HuntResult:
    """Risultato di hunt(d): classificazione completa dei vanishing g=0 a grado d.

    Conteggi con NC ESTESE (vecchie + dvir_full + triangle):
      n_zeros      : totale g=0 in _triples(d) (canonical form, no g-orbit dedup)
      n_explained  : g=0 e almeno una NC estesa violata
      n_sporadic   : g=0 e tutte le NC estese ok  (= n_zeros - n_explained)
      n_covered_ext: sporadici coperti da coverage.covered
      n_uncovered  : len(uncovered_canon) — g-orbit deduplicato
      uncovered_canon: tuple di rappresentanti canonici (min lex per orbita g)

    Conteggi con NC VECCHIE (solo nc_length + nc_maxpart) per confronto Entry 30:
      n_sporadic_old, n_covered_old, n_uncovered_old
    """
    d: int
    n_zeros: int
    n_explained: int
    n_sporadic: int
    n_covered_ext: int
    n_uncovered: int
    uncovered_canon: tuple          # tuple of Triple
    n_sporadic_old: int
    n_covered_old: int
    n_uncovered_old: int


# Entry 30 reference per il sanity check (NC vecchie: length + maxpart)
_ENTRY30_OLD: Dict[int, Tuple[int, int, int]] = {
    4: (2, 2, 0),
    5: (5, 5, 0),
    6: (44, 44, 0),
}


def sanity_entry30(result: HuntResult) -> Tuple[bool, Optional[Tuple[int, int, int]]]:
    """Verifica il sanity check di Entry 30 per d=4,5,6.

    Ritorna (ok, expected):
      ok=True  se i conteggi OLD corrispondono a Entry 30 (o d non in Entry 30).
      ok=False se divergono; `expected` e' il valore di riferimento.
    """
    d = result.d
    if d not in _ENTRY30_OLD:
        return True, None
    expected = _ENTRY30_OLD[d]
    actual = (result.n_sporadic_old, result.n_covered_old, result.n_uncovered_old)
    return actual == expected, expected


# ─────────────────────────────────────────────────────────────────────────────
#  Funzione principale: hunt(d)
# ─────────────────────────────────────────────────────────────────────────────

def hunt(d: int) -> HuntResult:
    """Misura principale: classifica tutti i vanishing g=0 di grado d.

    Algoritmo:
      1. Precalcola character_table(d) una volta sola.
      2. Itera su _triples(d) (terne canoniche lam<=mu<=nu per indice di partizione).
      3. Per ogni zero g=0: verifica NC estese e copertura.
      4. Deduplica gli uncovered per orbita g-simmetrica (g_canonical).
      5. Calcola i conteggi OLD (nc_length+nc_maxpart) per sanity Entry 30.

    Performance:
      d=4..6: < 5 sec (tavola piccola, terne poche).
      d=7:    < 30 sec (p(7)=15, 680 terne).
      d=8:    < 2 min  (p(8)=22, 2024 terne).
      d=9:    < 5 min  (p(9)=30, ~5000 terne); marcare slow nei test.
    """
    # 1. Tavola dei caratteri precalcolata
    character_table(d)

    # 2. Tutti i vanishing
    all_triples = _triples(d)
    zeros: List[Triple] = [t for t in all_triples if g_fast(*t) == 0]

    # 3a. Classificazione con NC ESTESE
    sporadic_list: List[Triple] = [t for t in zeros if _all_ncs_ok(*t)]
    n_explained = len(zeros) - len(sporadic_list)

    cov_list = [t for t in sporadic_list if covered_ext(t)]
    uncov_raw = [t for t in sporadic_list if not covered_ext(t)]

    # 4. Deduplicazione uncovered per orbita g-simmetrica
    seen: Set[Triple] = set()
    uncov_canon: List[Triple] = []
    for t in uncov_raw:
        canon = g_canonical(t)
        if canon not in seen:
            seen.add(canon)
            uncov_canon.append(canon)
    uncov_canon.sort()

    # 3b. Conteggi con NC VECCHIE (per sanity Entry 30)
    n_sp_old = sum(1 for t in zeros if _all_ncs_old(*t))
    n_cov_old = sum(1 for t in zeros if _all_ncs_old(*t) and covered_ext(t))
    n_unc_old = n_sp_old - n_cov_old

    return HuntResult(
        d=d,
        n_zeros=len(zeros),
        n_explained=n_explained,
        n_sporadic=len(sporadic_list),
        n_covered_ext=len(cov_list),
        n_uncovered=len(uncov_canon),
        uncovered_canon=tuple(uncov_canon),
        n_sporadic_old=n_sp_old,
        n_covered_old=n_cov_old,
        n_uncovered_old=n_unc_old,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Stretch dei testimoni uncovered
# ─────────────────────────────────────────────────────────────────────────────

def stretch_triple(triple: Triple, N: int) -> Triple:
    """Dilata la terna di un fattore N: ogni parte di ogni partizione x N."""
    return tuple(tuple(N * x for x in p) for p in triple)


def stretch_witnesses(
    uncovered_canon: tuple,
    n_max: int = 2,
) -> List[Dict]:
    """Calcola g_fast(N*lam, N*mu, N*nu) per N=2..n_max per ogni uncovered canonico.

    Per ogni testimone ritorna un dict:
      {'triple': t,
       'g_base': 0,           # sempre 0 per definizione di uncovered
       'stretch': {N: g(N*t) per N in 2..n_max},
       'hole': g(2*t) > 0,    # HOLE = non-saturazione / RAY = annullamento persistente
      }

    AVVERTENZA: richiede character_table(N*d) per ogni d = sum(lam).
    A 2d=14 (d=7): p(14)=135, ~18000 entries — puo' impiegare qualche minuto.
    A 2d=16 (d=8): p(16)=231, ~53000 entries — puo' impiegare 5-15 minuti.
    A 2d=18 (d=9): p(18)=385, ~148000 entries — puo' richiedere > 10 min; saltare.
    """
    results = []
    for t in uncovered_canon:
        d = sum(t[0])
        stretch_vals: Dict[int, int] = {}
        for N in range(2, n_max + 1):
            st = stretch_triple(t, N)
            character_table(N * d)  # precalcola tavola per N*d
            stretch_vals[N] = g_fast(*st)
        results.append({
            "triple": t,
            "g_base": 0,
            "stretch": stretch_vals,
            "hole": stretch_vals.get(2, 0) > 0,
        })
    return results


# ─────────────────────────────────────────────────────────────────────────────
#  Falsi positivi: verifica NC su TUTTE le terne g>0
# ─────────────────────────────────────────────────────────────────────────────

def false_positives_dvir(d: int) -> List[Triple]:
    """Terne con g>0 ma nc_dvir_full=False (= falsi positivi della NC).

    Deve essere vuota per ogni d in cui nc_dvir_full e' una NC valida.
    """
    character_table(d)
    return [
        t for t in _triples(d)
        if g_fast(*t) > 0 and not nc_dvir_full(*t)
    ]


def false_positives_triangle(d: int) -> List[Triple]:
    """Terne con g>0 ma nc_triangle=False (= falsi positivi della NC).

    Deve essere vuota per ogni d in cui nc_triangle e' una NC valida.
    """
    character_table(d)
    return [
        t for t in _triples(d)
        if g_fast(*t) > 0 and not nc_triangle(*t)
    ]


# ─────────────────────────────────────────────────────────────────────────────
#  Confine di onesta'
# ─────────────────────────────────────────────────────────────────────────────

def honesty_note() -> str:
    return (
        "Honesty boundary (Ciclo 1 'la caccia'): "
        "hunt(d) e' un calcolo ESATTO (g_fast = Murnaghan-Nakayama intero) di tutti "
        "i vanishing g=0 a grado d, classificati con NC estese (Dvir piena + triangolare) "
        "e copertura strutturale (Rosas/Bessenrodt-Bowman, famiglie di Entry 30). "
        "Le famiglie B5 (multiplicity-free) e B6 (two-column/hook) NON sono implementate: "
        "un 'uncovered' potrebbe essere coperto da quelle famiglie (survival-by-omission "
        "dichiarato; cfr. docs/prior-art-kronecker-zeros.md, KILLER-0). "
        "Il censimento d=7..9 e' riproduzione di dati noti. "
        "Nessun claim su Kronecker positivity, GCT o P vs NP."
    )
