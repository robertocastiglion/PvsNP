"""CICLO 6 — Caccia al falsificatore: test di COMPLETEZZA del dizionario μ_R.

Contesto. Il loop di ricerca si era fermato (Module 19, RESEARCH_LOG Entry 7) sulla
META-CONCLUSIONE "tiny-instance collapse": su n<=4 ogni discriminante locale
costruito finora si riduce, via identità esatta, a un invariante già nel dizionario
μ_R. La regola di ripresa dichiarata era UNA sola:

    riparti SOLO su una direzione fuori-dizionario, col FALSIFICATORE dichiarato
    in anticipo — un discriminante su n<=4 che separi due funzioni di PARI
    MCSP-size E pari cover-LP/G★ e NON sia ricostruibile da ``cost`` né da μ_R.

Finora ``falsifier_status`` (collapse.py) si limitava a verificare che ``d_flip``
NON qualifica (è il gradiente di ``cost``) e ad ASSUMERE — senza ricerca — che gli
altri invarianti della toolbox fossero "già dizionarizzati". Questo modulo CHIUDE
quel buco con una ricerca SISTEMATICA ed ESATTA, e nel farlo COSTRINGE a rendere
ESPLICITO cosa "μ_R" deve contenere.

IDEA (rende la caccia un test FINITO, non vago). Rendo μ_R un insieme GENERATORE di
invarianti, TUTTI invarianti sotto il gruppo di AUTOMORFISMI DEL COSTO:

    formula-cost (Module 6) · DT-depth-cost · multiset-G★/cover-LP (arena dualità)
    · sensitivity · block-sensitivity · gf2-degree · [support-size folded]

Sia ``P_Σ`` la partizione delle funzioni per il loro VETTORE-DIZIONARIO congiunto,
e ``P_orbit`` la partizione per orbita sotto il gruppo di automorfismi del costo.
Poiché ogni generatore è invariante su quel gruppo, ``P_orbit`` RAFFINA ``P_Σ``.
Quindi:

    UN FALSIFICATORE STRUTTURALE ESISTE  <=>  qualche classe di P_Σ si SPEZZA in
    >=2 orbite  (due funzioni identiche su TUTTO il dizionario ma in orbite diverse
    — separabili solo da un invariante FUORI dizionario).

  * se ``P_Σ == P_orbit``  → il dizionario determina la funzione a meno di
    simmetria: NESSUN falsificatore possibile → collasso INDURITO a quasi-teorema.
  * se ``P_Σ`` strettamente più grossa → coppia concreta (f,g) = candidato
    fuori-dizionario, da sottoporre all'adversary.

RISULTATO DEL CICLO (la parte onesta, vedi docs/falsifier-hunt.md). La prima caccia
"ingenua" (gruppo solo B_n, dizionario senza support) trova 8 split su n=3 e sembra
un falsificatore. L'adversary li UCCIDE identificando DUE chiusure mancanti di μ_R,
ENTRAMBE necessarie:
  (1) la NEGAZIONE DELL'OUTPUT è anch'essa un automorfismo del costo (¬f ha la
      stessa formula-size: De Morgan). Il gruppo giusto è B_n± = B_n × {id, ¬}.
  (2) la SUPPORT-SIZE folded ``min(|S|, 2^n-|S|)`` è un invariante di conteggio
      banale ma B_n±-invariante, non ricostruibile dagli altri.
Chiuso μ_R sotto ENTRAMBE, su n=3 ``P_Σ == P_orbit±`` ESATTAMENTE → collasso
COMPLETO. I default di questo modulo SONO la versione corretta (B_n±, +support);
la configurazione ingenua è esposta solo per riprodurre i candidati-fantasma.

RISULTATO A n=4 (il caso decisivo, esaustivo su 65536 funzioni). Col dizionario
``strong`` a 11 generatori sopravvive UN SOLO split: la coppia (2025, 5742), cost 11,
indistinguibile su TUTTI gli 11 generatori (``strong_sep=[]``) eppure in orbite B_n±
diverse. NON è un falsificatore fuori-dizionario: muore al 12° generatore
``cofactor_cost_profile`` — il multiset dei costi dei cofattori (n-1)-var di f, che è
la RICORSIONE stessa della formula-size, quindi vive DENTRO σ(cost). Aggiunto quel
generatore, ``P_Σ == P_orbit± == 222`` ESATTAMENTE → collasso COMPLETO anche a n=4.
(Lo stesso split è ucciso, indipendentemente, dal sensitivity-profile per-punto =
raffinamento di ``sensitivity``/``average_sensitivity``.) AVVERTENZA METODOLOGICA: un
candidato cofattore "ingenuo" che usa la tabella dei costi a n var sui cofattori
(n-1)-var NON è B_n±-invariante e produce |P_Σ|=243 > 222 (over-refinement, #splits=0
VACUO); la guardia ``|P_Σ| ≤ |P_orbit±|`` lo smaschera. Vedi docs/falsifier-hunt.md.

ATTENZIONE (scope). Resta una constatazione sul METODO su istanze FINITE, NON un
claim su P vs NP. Tutto è ESATTO e deterministico (interi/Fraction, niente float).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from itertools import combinations
from typing import Dict, List, Tuple

from pnp_lab.circuits import ComplexityTable, min_formula_sizes
from pnp_lab.exactness_composes.gap import BoolMatrix, cover_number, frac_cover, gstar
from pnp_lab.meta_complexity.collapse import dt_depth
from pnp_lab.meta_complexity.strata_graph import (
    block_sensitivity,
    gf2_degree,
    orbit_B,
    sensitivity,
)


# --------------------------------------------------------------------------- #
#  Gruppo di automorfismi del costo: B_n  oppure  B_n± (con negazione output) #
# --------------------------------------------------------------------------- #

@lru_cache(maxsize=None)
def cost_orbit(tt: int, n: int, output_negation: bool = True) -> frozenset[int]:
    """Orbita di ``f`` sotto il gruppo di automorfismi del costo.

    B_n  = 2^n negazioni di input × n! permutazioni (vedi ``strata_graph.orbit_B``).
    B_n± = B_n × {identità, negazione-output}: la negazione dell'output è anch'essa
    un automorfismo della formula-size (¬f via De Morgan ha la stessa taglia),
    quindi va inclusa nel gruppo "giusto". ``cost`` è costante su tutta l'orbita.
    """
    orb = set(orbit_B(tt, n))
    if output_negation:
        full = (1 << (1 << n)) - 1
        orb |= set(orbit_B(tt ^ full, n))
    return frozenset(orb)


@lru_cache(maxsize=None)
def orbit_canon(tt: int, n: int, output_negation: bool = True) -> int:
    """Etichetta canonica (minimo) dell'orbita di ``f`` sotto il gruppo scelto."""
    return min(cost_orbit(tt, n, output_negation))


# --------------------------------------------------------------------------- #
#  Arena cover-LP/G★ resa un invariante PER-FUNZIONE e B_n±-invariante        #
# --------------------------------------------------------------------------- #

def comm_matrix(tt: int, n: int, alice: Tuple[int, ...]) -> BoolMatrix:
    """Matrice di comunicazione di ``f`` sotto la bipartizione ``alice`` | resto.

    Righe = assegnazioni delle variabili di Alice, colonne = quelle di Bob;
    l'entrata vale ``f`` sull'input combinato. È l'oggetto su cui l'arena della
    dualità (Module 18) misura Cov/LP/G★.
    """
    bob = tuple(i for i in range(n) if i not in alice)
    rows = []
    for a in range(1 << len(alice)):
        row = []
        for b in range(1 << len(bob)):
            idx = 0
            for j, var in enumerate(alice):
                if (a >> j) & 1:
                    idx |= 1 << var
            for j, var in enumerate(bob):
                if (b >> j) & 1:
                    idx |= 1 << var
            row.append((tt >> idx) & 1)
        rows.append(tuple(row))
    return tuple(rows)


def _balanced_alice_sets(n: int) -> List[Tuple[int, ...]]:
    """Tutti i sottoinsiemi di variabili di taglia ``n//2`` (Alice nelle bipart.).

    Includere ogni S di taglia ``k=max(1,n//2)`` tiene il MULTISET dei G★
    invariante sotto B_n: le permutazioni mappano S in perm(S), stessa taglia, e
    ``gstar`` è invariante per trasposizione e per negazione di input.
    """
    k = max(1, n // 2)
    return [tuple(s) for s in combinations(range(n), k)]


@lru_cache(maxsize=None)
def _gstar_cached(M: BoolMatrix):
    return gstar(M)


def _output_fold(tt: int, n: int, raw) -> Tuple:
    """Ripiega un'etichetta cover-LP sulla NEGAZIONE DELL'OUTPUT per renderla
    B_n±-invariante. Le misure di copertura si basano sull'insieme degli 1, che la
    negazione output scambia con gli 0: combinando i valori di ``f`` e ``¬f`` in un
    unico multiset si ottiene un invariante stabile sotto tutto B_n±. (Senza questa
    piega, cover_number spezzerebbe DENTRO le orbite — l'orbita non raffinerebbe
    più P_Σ, e il test perderebbe senso.)"""
    full = (1 << (1 << n)) - 1
    return tuple(sorted(list(raw(tt, n)) + list(raw(tt ^ full, n))))


def _gstar_raw(tt: int, n: int) -> List:
    return [_gstar_cached(comm_matrix(tt, n, a)) for a in _balanced_alice_sets(n)]


def gstar_label(tt: int, n: int) -> Tuple:
    """Etichetta cover-LP/G★ di ``f``: multiset dei G★ sulle bipartizioni bilanciate,
    ripiegato sulla negazione output → B_n±-invariante. Generatore legittimo di μ_R."""
    return _output_fold(tt, n, _gstar_raw)


def support_folded(tt: int, n: int) -> int:
    """Support-size ripiegata ``min(|S|, 2^n-|S|)``: invariante di conteggio banale,
    B_n±-invariante (la negazione output manda |S| in 2^n-|S|). È la chiusura (2)
    che l'adversary ha mostrato necessaria per la completezza su n=3."""
    s = bin(tt).count("1")
    return min(s, (1 << n) - s)


@lru_cache(maxsize=None)
def _sub_cost_table(n: int, cap: int = 60):
    """Tabella formula-size ESATTA sulle funzioni a (n-1) variabili (Module 6).

    Serve ai cofattori: f|xi=b è una funzione a n-1 variabili e il suo costo va letto
    sulla tabella GIUSTA (n-1), non su quella a n. Usare la tabella a n var sui
    cofattori misurerebbe il costo dell'EMBEDDING ``g ∧ ¬xi`` (NON B_n±-invariante)."""
    return min_formula_sizes(n - 1, cap)


def cofactor_cost_profile(tt: int, n: int) -> Tuple:
    """Profilo dei costi dei cofattori: multiset su i di ``sorted(cost(f|xi=0),
    cost(f|xi=1))`` con ``cost`` la formula-size esatta a (n-1)-var. È la RICORSIONE
    stessa che definisce la formula-size, quindi un raffinamento di ``cost`` che vive
    DENTRO σ(cost). B_n±-invariante: la permutazione permuta gli i, la negazione-input
    di xj scambia la coppia (i=j) o relabela i punti senza toccare il costo (i≠j), la
    negazione-output preserva il costo di ogni cofattore. È il 12° generatore che
    CHIUDE l'ultimo split a n=4 — vedi il docstring del modulo e docs/falsifier-hunt.md."""
    ct_sub = _sub_cost_table(n)
    N = 1 << n
    prof = []
    for i in range(n):
        tt0 = tt1 = 0
        pos = 0
        for x in range(N):
            if ((x >> i) & 1) == 0:
                tt0 |= ((tt >> x) & 1) << pos
                tt1 |= ((tt >> (x | (1 << i))) & 1) << pos
                pos += 1
        prof.append(tuple(sorted((ct_sub.cost[tt0], ct_sub.cost[tt1]))))
    return tuple(sorted(prof))


# --------------------------------------------------------------------------- #
#  Generatori FORTI: gli invarianti standard che l'adversary ha dovuto        #
#  aggiungere a n=4 per assorbire i falsificatori apparenti.                  #
# --------------------------------------------------------------------------- #

@lru_cache(maxsize=None)
def _cover_cached(M: BoolMatrix) -> int:
    return cover_number(M)


@lru_cache(maxsize=None)
def _frac_cached(M: BoolMatrix):
    return frac_cover(M)


def _cover_raw(tt: int, n: int) -> List:
    return [_cover_cached(comm_matrix(tt, n, a)) for a in _balanced_alice_sets(n)]


def _frac_raw(tt: int, n: int) -> List:
    return [_frac_cached(comm_matrix(tt, n, a)) for a in _balanced_alice_sets(n)]


def cover_number_label(tt: int, n: int) -> Tuple:
    """Multiset dei Cov(M) (numero di copertura, NON il gap) sulle bipartizioni
    bilanciate, ripiegato sulla negazione output → B_n±-invariante. È l'invariante
    PRIMARIO dell'arena cover-LP, che ``gstar`` (solo il gap, quasi sempre 0) NON
    cattura."""
    return _output_fold(tt, n, _cover_raw)


def frac_cover_label(tt: int, n: int) -> Tuple:
    """Multiset dei LP(M) (copertura frazionaria esatta), ripiegato sulla negazione
    output → B_n±-invariante."""
    return _output_fold(tt, n, _frac_raw)


def average_sensitivity(tt: int, n: int) -> int:
    """Influenza totale = somma sui 2^n input del #variabili sensibili (intero esatto).
    Distinta dalla sensitivity MASSIMA già nel dizionario base."""
    N = 1 << n
    tot = 0
    for idx in range(N):
        b = (tt >> idx) & 1
        for i in range(n):
            if ((tt >> (idx ^ (1 << i))) & 1) != b:
                tot += 1
    return tot


def _walsh(tt: int, n: int) -> List[int]:
    """Trasformata di Walsh-Hadamard di f in forma ±1 (coeff non normalizzati)."""
    N = 1 << n
    f = [1 - 2 * ((tt >> i) & 1) for i in range(N)]
    h = 1
    while h < N:
        for i in range(0, N, h * 2):
            for j in range(i, i + h):
                x, y = f[j], f[j + h]
                f[j], f[j + h] = x + y, x - y
        h *= 2
    return f


def real_degree(tt: int, n: int) -> int:
    """Grado del polinomio multilineare reale (Fourier degree) di f."""
    N = 1 << n
    f = _walsh(tt, n)
    return max((bin(S).count("1") for S in range(N) if f[S] != 0), default=0)


def fourier_fingerprint(tt: int, n: int) -> Tuple:
    """Impronta spettrale: multiset ordinato di (livello |S|, |coeff di Fourier|).
    Invariante sotto B_n± (permutazioni e negazioni di input/output permutano i
    coefficienti e ne lasciano invariato il valore assoluto). È l'invariante
    standard PIÙ FINE della toolbox di analisi booleana."""
    N = 1 << n
    f = _walsh(tt, n)
    return tuple(sorted((bin(S).count("1"), abs(f[S])) for S in range(N)))


# --------------------------------------------------------------------------- #
#  Il vettore-dizionario μ_R (tutti i generatori, esplicito per l'adversary)  #
# --------------------------------------------------------------------------- #

_BASE_GENERATORS = (
    "formula_cost",      # Module 6 (MCSP-size)
    "dt_depth_cost",     # secondo oracolo di costo esatto
    "gstar_multiset",    # arena cover-LP/G★ (Module 18)
    "sensitivity",       # analisi booleana classica
    "block_sensitivity",
    "gf2_degree",
)


# Generatori FORTI aggiunti dall'adversary a n=4 (cover-LP primario + analisi
# booleana fine). Sono ESSI STESSI invarianti standard già nel dizionario μ_R.
_STRONG_GENERATORS = (
    "cover_number",          # arena cover-LP PRIMARIA (non solo il gap)
    "frac_cover",            # LP esatto
    "average_sensitivity",   # influenza totale
    "real_degree",           # grado reale (Fourier)
    "fourier_fingerprint",   # impronta spettrale completa
    "cofactor_cost_profile", # ricorsione di formula-size (in σ(cost)); chiude n=4
)


def dictionary_generators(include_support: bool = True, strong: bool = False) -> Tuple[str, ...]:
    """I nomi dei generatori di μ_R nell'ordine del vettore."""
    names = _BASE_GENERATORS
    if include_support:
        names = names + ("support_folded",)
    if strong:
        names = names + _STRONG_GENERATORS
    return names


def dictionary_vector(tt: int, n: int, ct: ComplexityTable,
                      include_support: bool = True, strong: bool = False) -> Tuple:
    """Il vettore congiunto dei generatori di μ_R su ``f`` (la chiave di P_Σ).

    ``strong=True`` aggiunge i generatori forti che l'adversary ha dovuto includere
    a n=4 per assorbire i falsificatori apparenti (cover_number, frac_cover,
    average_sensitivity, real_degree, fourier_fingerprint) PIÙ il
    cofactor_cost_profile (in σ(cost)) che chiude l'ultimo split a n=4."""
    base = (
        ct.cost[tt],
        dt_depth(tt, n),
        gstar_label(tt, n),
        sensitivity(tt, n),
        block_sensitivity(tt, n),
        gf2_degree(tt, n),
    )
    if include_support:
        base = base + (support_folded(tt, n),)
    if strong:
        base = base + (
            cover_number_label(tt, n),
            frac_cover_label(tt, n),
            average_sensitivity(tt, n),
            real_degree(tt, n),
            fourier_fingerprint(tt, n),
            cofactor_cost_profile(tt, n),
        )
    return base


# --------------------------------------------------------------------------- #
#  Il test di completezza + i witness                                         #
# --------------------------------------------------------------------------- #

@dataclass
class SplitWitness:
    """Una classe di P_Σ che si spezza in >=2 orbite = candidato falsificatore."""
    dict_vector: Tuple
    orbit_reps: List[int]            # un rappresentante per ogni orbita nella classe
    example_pair: Tuple[int, int]    # (f, g) concreti, stesso dizionario, orbite diverse

    @property
    def num_orbits(self) -> int:
        return len(self.orbit_reps)


@dataclass
class HuntReport:
    n: int
    output_negation: bool            # gruppo: B_n± (True) o solo B_n (False)
    include_support: bool            # dizionario chiuso sotto support-size?
    strong: bool                     # dizionario chiuso sotto i generatori forti?
    num_funcs: int
    num_sigma_classes: int           # |P_Σ|
    num_orbits: int                  # |P_orbit|
    relation: str                    # "COINCIDE" (completo) o "RAFFINA"
    splits: List[SplitWitness] = field(default_factory=list)

    @property
    def falsifier_exists(self) -> bool:
        return len(self.splits) > 0

    @property
    def verdict(self) -> str:
        return "FALSIFIER_CANDIDATE" if self.falsifier_exists else "COLLAPSE_HARDENED"


def hunt(n: int, cap: int = 60, *, output_negation: bool = True,
         include_support: bool = True, strong: bool = False,
         max_witnesses: int = 12) -> HuntReport:
    """Test di completezza del dizionario μ_R su TUTTE le funzioni su n var.

    Default = la configurazione ONESTA del ciclo su n=3: gruppo B_n± e dizionario
    base chiuso sotto support-size. ``strong=True`` aggiunge i generatori forti che
    l'adversary ha dovuto includere a n=4. Le flag permettono di riprodurre i
    candidati-fantasma della caccia ingenua e l'assorbimento progressivo.
    """
    ct = min_formula_sizes(n, cap)
    funcs = list(ct.cost)

    sigma: Dict[Tuple, List[int]] = {}
    for tt in funcs:
        key = dictionary_vector(tt, n, ct, include_support, strong)
        sigma.setdefault(key, []).append(tt)

    canon = {tt: orbit_canon(tt, n, output_negation) for tt in funcs}
    num_orbits = len(set(canon.values()))

    splits: List[SplitWitness] = []
    for vec, members in sigma.items():
        by_orbit: Dict[int, List[int]] = {}
        for tt in members:
            by_orbit.setdefault(canon[tt], []).append(tt)
        if len(by_orbit) >= 2:
            reps = sorted(min(v) for v in by_orbit.values())
            splits.append(SplitWitness(vec, reps, (reps[0], reps[1])))

    splits.sort(key=lambda s: (-s.num_orbits, s.example_pair))
    relation = "COINCIDE" if not splits else "RAFFINA"
    return HuntReport(
        n=n, output_negation=output_negation, include_support=include_support,
        strong=strong, num_funcs=len(funcs), num_sigma_classes=len(sigma),
        num_orbits=num_orbits, relation=relation, splits=splits[:max_witnesses],
    )


# --------------------------------------------------------------------------- #
#  Sonda adversariale: la coppia è separata da QUALCHE generatore NOMINATO?   #
# --------------------------------------------------------------------------- #

def named_separators(f: int, g: int, n: int, ct: ComplexityTable,
                     include_support: bool = True, strong: bool = False) -> List[str]:
    """Quali generatori di μ_R separano f e g? Lista vuota = identici su tutto il
    dizionario (è la condizione che rende (f,g) un candidato falsificatore)."""
    a = dictionary_vector(f, n, ct, include_support, strong)
    b = dictionary_vector(g, n, ct, include_support, strong)
    names = dictionary_generators(include_support, strong)
    return [name for name, va, vb in zip(names, a, b) if va != vb]
