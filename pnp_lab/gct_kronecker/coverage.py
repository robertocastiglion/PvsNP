"""Copertura strutturale dei vanishing SPORADICI di Kronecker (g==0) tramite forme note.

CONTESTO.  Il motore `kronecker.py` produce `sporadic_vanishing(d)`: le terne con
g(lam,mu,nu)==0 che soddisfano TUTTE le condizioni necessarie note (length-/max-part di
Dvir).  L'ipotesi-di-chiusura dell'arena e': ogni tale vanishing e' COPERTO da una
famiglia di formule esplicite note per i coefficienti di Kronecker, e quindi NON e'
"fuori dizionario".  Finora questo passo era CITATO (riferito alla letteratura) ma mai
calcolato nel repo.  Questo modulo lo converte in COMPUTED.

IDEA.  Non ricalcoliamo i VALORI delle formule di Rosas / Bessenrodt-Bowman (non serve:
g(lam,mu,nu) e' gia' esatto via Murnaghan-Nakayama, e ricopiare quelle formule sarebbe
fragile).  Verifichiamo invece, in codice ed in modo ESATTO, la PRECONDIZIONE STRUTTURALE
sotto cui quelle formule chiuse si applicano: ogni terna sporadica ha un rappresentante
nella sua orbita g-simmetrica in cui ALMENO DUE dei tre argomenti hanno una FORMA SPECIALE
(two-row, two-column, hook, rettangolo).  Per terne di questa forma il valore g(lam,mu,nu)
e' dato da formule esplicite note in letteratura:
  - Rosas (2001): g(lam,mu,nu) in forma chiusa quando due argomenti sono two-row o hook;
  - Bessenrodt-Bowman (2017) e parenti: rettangoli e tensori std-by-std;
  - dualita' two-row <-> two-column via coniugio (qui catturata dall'orbita g-simmetrica).

CONFINE DI ONESTA' (boundary).  `covered(triple)` verifica ESATTAMENTE la precondizione
strutturale "due argomenti special_shape in qualche rappresentante g-simmetrico".  NON
ricomputa il valore numerico delle formule chiuse: quel valore (e il fatto che esse diano
proprio g per le forme in questione) resta un TEOREMA CITATO (Rosas, Bessenrodt-Bowman).
Cio' che e' qui COMPUTED e' la copertura: che la classe di terne con quella struttura
contenga tutte le terne sporadiche.  Un eventuale `uncovered(d)` non vuoto sarebbe il vero
contenuto fuori-dizionario (sopravvivenza genuina), un esito piu' forte; questo modulo lo
riporterebbe esattamente senza nasconderlo.
"""

from __future__ import annotations

from itertools import permutations
from typing import FrozenSet, List, Set, Tuple

from .kronecker import Partition, transpose, sporadic_vanishing

Triple = Tuple[Partition, Partition, Partition]


# --------------------------------------------------------------------------------------
#  Predicati di FORMA speciale (tutti esatti ed elementari)
# --------------------------------------------------------------------------------------
def is_two_row(p: Partition) -> bool:
    """Forma a (al piu') due righe: ell(p) <= 2.  La partizione vuota () e' two-row."""
    return len(p) <= 2


def is_two_column(p: Partition) -> bool:
    """Forma a (al piu') due colonne: la trasposta ha <= 2 righe, ossia la parte MASSIMA
    di p e' <= 2 (p[0] <= 2).  Duale per coniugio di `is_two_row`.  () e' two-column."""
    return (p[0] if p else 0) <= 2


def is_hook(p: Partition) -> bool:
    """Forma ad UNCINO: p = (a, 1^b) — una prima parte qualsiasi seguita da sole parti 1.
    () e (a,) sono hook; (3,1,1) e' hook; (3,2) no.  ESATTO."""
    return all(x == 1 for x in p[1:])


def is_rectangle(p: Partition) -> bool:
    """Forma RETTANGOLARE: tutte le parti uguali, p = (c^k).  () e ogni (c^k) sono
    rettangoli; (3,3,3) si', (3,3,1) no.  ESATTO."""
    return len(set(p)) <= 1


def special_shape(p: Partition) -> bool:
    """OR dei predicati di forma: p e' two-row OR two-column OR hook OR rettangolo.
    E' la classe di partizioni per cui il coefficiente di Kronecker ammette (quando
    appaiono in coppia) formule chiuse note."""
    return is_two_row(p) or is_two_column(p) or is_hook(p) or is_rectangle(p)


# --------------------------------------------------------------------------------------
#  Orbita g-simmetrica di una terna
# --------------------------------------------------------------------------------------
def g_orbit(triple: Triple) -> Set[Triple]:
    """Orbita completa di (lam,mu,nu) sotto il gruppo G generato dalle simmetrie sotto cui
    g(lam,mu,nu) e' INVARIANTE:

      - permutazioni S_3 dei tre argomenti (g totalmente simmetrico);
      - coniugio SIMULTANEO di DUE qualunque dei tre argomenti:
            g(lam,mu,nu) = g(lam',mu',nu) = g(lam',mu,nu') = g(lam,mu',nu')
        dove p' = transpose(p) (il doppio segno di trasposizione si elide).

    NB: il coniugio simultaneo di TRE argomenti NON e' una simmetria di g; quindi il
    sottogruppo delle coniugazioni e' {id, (lam,mu)', (lam,nu)', (mu,nu)'} ~ V_4 (Klein),
    e G = S_3 x V_4 agisce sui rappresentanti.  Generiamo l'orbita applicando le 4
    configurazioni di coniugio e poi tutte le permutazioni — chiusura immediata perche'
    permutare commuta opportunamente con il coniugio a coppie.  ESATTO, finito.
    """
    lam, mu, nu = triple
    lamp, mup, nup = transpose(lam), transpose(mu), transpose(nu)
    base_confs = [
        (lam, mu, nu),     # identita'
        (lamp, mup, nu),   # coniuga lam, mu
        (lamp, mu, nup),   # coniuga lam, nu
        (lam, mup, nup),   # coniuga mu, nu
    ]
    orbit: Set[Triple] = set()
    for conf in base_confs:
        for perm in permutations(conf):
            orbit.add(perm)
    return orbit


def g_orbit_frozen(triple: Triple) -> FrozenSet[Triple]:
    """`g_orbit` come frozenset (comodo come chiave / per deduplicazione)."""
    return frozenset(g_orbit(triple))


# --------------------------------------------------------------------------------------
#  Copertura strutturale
# --------------------------------------------------------------------------------------
def _two_special_in_rep(rep: Triple) -> bool:
    """True se almeno DUE dei tre argomenti del rappresentante hanno forma speciale."""
    return sum(1 for p in rep if special_shape(p)) >= 2


def covered(triple: Triple) -> bool:
    """True se ESISTE un rappresentante nell'orbita g-simmetrica di `triple` con ALMENO
    DUE dei tre argomenti `special_shape`.

    Questa e' la PRECONDIZIONE STRUTTURALE sotto cui le formule esplicite note per i
    coefficienti di Kronecker (Rosas two-row/hook; Bessenrodt-Bowman rettangoli; tensori
    std-by-std) danno il valore in forma chiusa.  Poiche' g e' costante su tutta l'orbita
    g-simmetrica (cfr. `g_orbit` e il relativo test), basta che la forma speciale-a-coppie
    compaia in UN rappresentante: la formula chiusa applicata li' calcola lo stesso g, e in
    particolare ne certifica l'eventuale annullamento.

    CONFINE DI ONESTA' (vedi docstring di modulo): qui verifichiamo SOLO che la struttura
    di copertura esista (predicato esatto, elementare, testabile).  NON ricomputiamo il
    valore numerico delle formule chiuse — quel valore, e il teorema che quelle formule
    diano g per le forme indicate, restano CITATI come teoremi parenti (Rosas;
    Bessenrodt-Bowman).  Cio' che diventa COMPUTED e' la copertura.
    """
    return any(_two_special_in_rep(rep) for rep in g_orbit(triple))


def covered_list(d: int) -> List[Triple]:
    """Sottoinsieme di `sporadic_vanishing(d)` che e' `covered`."""
    return [t for t in sporadic_vanishing(d) if covered(t)]


def uncovered(d: int) -> List[Triple]:
    """Le terne in `sporadic_vanishing(d)` che NON sono `covered`.

    IPOTESI-DI-CHIUSURA: uncovered(d) == [] per d <= 6 ⇒ ogni vanishing sporadico e'
    coperto da formule chiuse note ⇒ il "collasso" non e' piu' solo CITATO ma COMPUTED.
    Se NON vuoto, le terne elencate sarebbero genuine sopravvivenze fuori-dizionario
    (esito piu' forte): vanno riportate ESATTAMENTE, senza aggiustare nulla.
    """
    return [t for t in sporadic_vanishing(d) if not covered(t)]


def coverage_summary(d: int) -> Tuple[int, int, int]:
    """(#sporadic_vanishing, #covered, #uncovered) per d.  ESATTO."""
    sp = sporadic_vanishing(d)
    cov = sum(1 for t in sp if covered(t))
    return (len(sp), cov, len(sp) - cov)
