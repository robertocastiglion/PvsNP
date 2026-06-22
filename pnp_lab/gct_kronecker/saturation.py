"""Stretching (saturazione) N=2 dei vanishing SPORADICI di Kronecker e il loro split.

CONTESTO (PvsNP-lab, Module 30 GCT/Kronecker, riaperto da lever umano).  Il motore
`kronecker.py` produce `sporadic_vanishing(d)`: le terne con g(lam,mu,nu)==0 che soddisfano
TUTTE le condizioni necessarie note (length-/max-part di Dvir).  Il modulo `coverage.py`
le marca tutte `covered` (precondizione strutturale delle formule chiuse note).

IPOTESI (explorer).  Lo "sporadic vanishing" si SPLITTA in due classi via lo STRETCHING
N=2 della terna (moltiplicare ogni parte per N):

  - HOLE       : g(N*lam, N*mu, N*nu) > 0.  Il punto e' DENTRO il cono dei momenti ma g=0
                 alla scala 1 — un "buco" interno: ostruzione NON-locale (non asintotica).
  - RAY-VANISH : g(N*lam, N*mu, N*nu) = 0.  L'annullamento PERSISTE lungo il raggio N*triple
                 (g_N e' eventualmente quasi-polinomiale in N e qui resta 0): ostruzione
                 asintotica/locale, sopravvive alla saturazione.

Il bit hole/ray e' quindi una NUOVA misura ESATTA su ogni terna sporadica, ortogonale al
predittore di vanishing e (a priori) alla copertura.

SIMMETRIA CORRETTA DEL BIT (load-bearing — verificato in codice, vedi test).  g(lam,mu,nu)
e' invariante sull'intera orbita g-simmetrica (S_3 x coniugio-doppio; cfr. `g_orbit`).  MA
lo STRETCHING NON commuta col coniugio: in generale  transpose(N*p) != N*transpose(p)
(es. N=2, p=(4,1):  transpose(8,2)=(2,2,1,1,1,1,1,1)  mentre  2*transpose(4,1)=(4,2,2,2)).
Lo stretching commuta SOLO con la permutazione S_3 dei tre argomenti.  Conseguenza ESATTA:
il bit hole/ray e' costante sull'orbita di PERMUTAZIONE ma NON sull'intera orbita
g-simmetrica.  Esempio reale (d=5): ((4,1),(4,1),(2,2,1)) e ((2,2,1),(2,1,1,1),(2,1,1,1))
sono nella STESSA orbita g-simmetrica (entrambe g_base=0) ma stretching N=2 da' g=0 (RAY) per
la prima e g=8 (HOLE) per la seconda.  Percio' la simmetria ONESTA del bit e' la sola
permutazione S_3: il collision-finder raggruppa e deduplica per un canonico INVARIANTE DI
PERMUTAZIONE, NON per l'orbita g-simmetrica completa (che farebbe collassare bit distinti).

KILLER (collision-finder).  Il bit hole/ray e' una FUNZIONE del dizionario di copertura del
lab?  Raggruppo le terne sporadiche (deduplicate per orbita di PERMUTAZIONE) per chiave
(shape_profile_canonico, covered): ogni gruppo ha bit hole/ray COSTANTE?  Se SI' (nessuna
collisione), il bit e' RICOSTRUIBILE dal dizionario => RESTATEMENT (collasso n+1).  Se NO
(un gruppo con due terne a bit opposto e stessa chiave), il bit e' un invariante
FUORI-dizionario, enumerabile esattamente a due livelli (scala 1 e scala N) => sopravvivenza.

CONFINE DI ONESTA' (boundary, EN).  This is an EXACT finite computation: the hole/ray bit is
g(N*lam,N*mu,N*nu) computed exactly (Murnaghan-Nakayama, integer), and the collision test is
an exact grouping by a permutation-invariant canonical key (the symmetry the bit actually
respects).  No claim is made about the asymptotic quasi-polynomial g_N, about saturation
theorems, or about P vs NP.  An empty `collisions(d)` only means the hole/ray bit is a
function of (shape_profile, covered) on that d; a non-empty one only means it is not — i.e.
an out-of-dictionary invariant survives on that d.
"""

from __future__ import annotations

from itertools import permutations
from typing import Dict, FrozenSet, List, Tuple

from .kronecker import Partition, kronecker, sporadic_vanishing
from .coverage import (
    covered,
    is_hook,
    is_rectangle,
    is_two_column,
    is_two_row,
)

Triple = Tuple[Partition, Partition, Partition]


# --------------------------------------------------------------------------------------
#  Stretching N (saturazione lungo il raggio)
# --------------------------------------------------------------------------------------
def stretch(triple: Triple, N: int) -> Triple:
    """Dilata la terna di un fattore N: ogni parte di ogni partizione e' moltiplicata per N.

    Se p e' una partizione di d (parti decrescenti > 0), N*p e' una partizione di N*d con le
    stesse RIGHE (resta non crescente, parti > 0).  Lo stretching commuta con le permutazioni
    S_3 degli argomenti (si applica argomento per argomento) ma NON col coniugio
    (transpose(N*p) != N*transpose(p) in generale).  ESATTO, finito.
    """
    if N < 1:
        raise ValueError("N deve essere >= 1")
    return tuple(tuple(N * x for x in p) for p in triple)


def g_stretch(triple: Triple, N: int = 2) -> int:
    """g(N*lam, N*mu, N*nu) ESATTO (intero, Murnaghan-Nakayama)."""
    return kronecker(*stretch(triple, N))


def is_hole(triple: Triple, N: int = 2) -> bool:
    """HOLE: g(N*triple) > 0 (buco interno, ostruzione non-locale).  Il complementare e'
    RAY-VANISH (g(N*triple) == 0, ostruzione asintotica/locale che persiste)."""
    return g_stretch(triple, N) > 0


# --------------------------------------------------------------------------------------
#  Orbita di PERMUTAZIONE (la simmetria che il bit hole/ray rispetta davvero)
# --------------------------------------------------------------------------------------
def perm_orbit(triple: Triple) -> FrozenSet[Triple]:
    """Orbita della terna sotto le permutazioni S_3 dei tre argomenti.  Questa e' l'UNICA
    simmetria di g sotto cui anche il bit hole/ray (g_stretch) e' invariante: stretching e
    permutazione commutano.  ESATTA, al piu' 6 elementi."""
    return frozenset(permutations(triple))


def perm_key(triple: Triple) -> Tuple[Triple, ...]:
    """Chiave canonica dell'orbita di permutazione: la tupla ORDINATA dei suoi rappresentanti.
    Serve a deduplicare le terne che differiscono solo per l'ordine degli argomenti (stesso
    g, stesso bit, stesso profilo)."""
    return tuple(sorted(perm_orbit(triple)))


# --------------------------------------------------------------------------------------
#  Profilo-shape CANONICO invariante di permutazione
# --------------------------------------------------------------------------------------
def _shape_signature(p: Partition) -> Tuple[bool, bool, bool, bool]:
    """Firma di forma di una singola partizione: i quattro predicati special-shape
    (two-row, two-column, hook, rettangolo) come tupla di bool.  ESATTA, elementare.

    Usiamo la firma a 4 bit (non il solo OR `special_shape`) cosi' che il profilo distingua
    p.es. un rettangolo da un hook: il collision-finder confronta strutture, non un OR
    collassato."""
    return (is_two_row(p), is_two_column(p), is_hook(p), is_rectangle(p))


def shape_profile(triple: Triple) -> Tuple[Tuple[bool, bool, bool, bool], ...]:
    """Profilo-shape CANONICO della terna, INVARIANTE per permutazione degli argomenti.

    Costruzione: il MULTISET ORDINATO delle firme di forma dei tre argomenti.  Ordinare le
    tre firme rende il profilo identico per ogni permutazione della terna — esattamente la
    simmetria sotto cui il bit hole/ray e' invariante.  E' percio' un canonico ONESTO per il
    collision-finder: due terne che differiscono solo per l'ordine -> stessa chiave (e stesso
    bit, mai una collisione spuria); una collisione richiede DUE orbite di permutazione
    DISTINTE con lo stesso profilo e stessa copertura ma bit opposto.

    NB: NON usiamo l'orbita g-simmetrica completa (S_3 x coniugio) perche' lo stretching non
    commuta col coniugio (vedi docstring di modulo): un canonico g-simmetrico raggrupperebbe
    terne con bit hole/ray DIVERSO, falsando il killer.
    """
    return tuple(sorted(_shape_signature(p) for p in triple))


# --------------------------------------------------------------------------------------
#  Tabella classify
# --------------------------------------------------------------------------------------
def classify(d: int, N: int = 2) -> List[dict]:
    """Per ogni vanishing sporadico di d (deduplicato per orbita di PERMUTAZIONE) una riga:

      {
        'triple'        : rappresentante della terna sporadica,
        'g_base'        : g(lam,mu,nu)            (== 0 per definizione di sporadico),
        'g_stretch'     : g(N*lam, N*mu, N*nu)    (intero ESATTO),
        'hole'          : g_stretch > 0           (True=HOLE, False=RAY-VANISH),
        'covered'       : copertura strutturale   (coverage.covered),
        'shape_profile' : profilo-shape CANONICO invariante di permutazione,
      }

    Deduplichiamo per `perm_key`: terne che differiscono solo per l'ordine degli argomenti
    (stesso g, stesso bit, stesso profilo) compaiono una volta sola, col primo rappresentante
    in ordine deterministico.  ESATTO.
    """
    rows: List[dict] = []
    seen = set()
    for t in sporadic_vanishing(d):
        pk = perm_key(t)
        if pk in seen:
            continue
        seen.add(pk)
        gs = g_stretch(t, N)
        rows.append(
            {
                "triple": t,
                "g_base": kronecker(*t),
                "g_stretch": gs,
                "hole": gs > 0,
                "covered": covered(t),
                "shape_profile": shape_profile(t),
            }
        )
    return rows


# --------------------------------------------------------------------------------------
#  KILLER: collision-finder hole/ray vs dizionario (shape_profile, covered)
# --------------------------------------------------------------------------------------
def collisions(d: int, N: int = 2) -> List[dict]:
    """IL KILLER.  Raggruppa i vanishing sporadici (deduplicati per orbita di permutazione)
    per chiave (shape_profile_canonico, covered) e ritorna i gruppi che contengono SIA un
    HOLE SIA un RAY-VANISH: due terne con la STESSA chiave del dizionario ma bit OPPOSTO.

    Lista VUOTA  = nessuna collisione = il bit hole/ray e' una funzione di
                   (shape_profile, covered) sui sporadici di d => RICOSTRUIBILE dal
                   dizionario => RESTATEMENT (collasso).
    Lista NON vuota = collisione = il bit NON e' funzione del dizionario => invariante
                   FUORI-dizionario, sopravvivenza enumerabile a 2 livelli (scala 1 e N).

    Ogni elemento e' un dict:
      { 'key': (shape_profile, covered),
        'holes': [terne con hole=True], 'rays': [terne con hole=False] }.
    """
    rows = classify(d, N)
    groups: Dict[Tuple, dict] = {}
    for r in rows:
        key = (r["shape_profile"], r["covered"])
        g = groups.setdefault(key, {"key": key, "holes": [], "rays": []})
        (g["holes"] if r["hole"] else g["rays"]).append(r["triple"])
    return [g for g in groups.values() if g["holes"] and g["rays"]]


def summary(d: int, N: int = 2) -> Tuple[int, int, int, int]:
    """(#sporadic, #hole, #ray, #collisions) per d, ESATTO.

    #sporadic e' contato per ORBITE DI PERMUTAZIONE distinte (come `classify`/`collisions`).
    #collisions e' il numero di gruppi (shape_profile, covered) con bit hole/ray misto.
    """
    rows = classify(d, N)
    n_sp = len(rows)
    n_hole = sum(1 for r in rows if r["hole"])
    n_ray = n_sp - n_hole
    n_coll = len(collisions(d, N))
    return (n_sp, n_hole, n_ray, n_coll)
