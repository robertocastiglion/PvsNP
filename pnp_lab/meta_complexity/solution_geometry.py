"""CICLO 1 della direzione A — GEOMETRIA DELLO SPAZIO DELLE SOLUZIONI (OGP minuscolo).

Contesto (restart out-of-dictionary). Il loop si era fermato (Module 19, Entry 7) e la
caccia al falsificatore (Entry 8) ha INDURITO il collasso: su n≤4 ogni discriminante
finora muore dentro σ(cost). La diagnosi del restart program: ogni discriminante provato
era (1) SCALARE, (2) il minimo di un programma di copertura/un suo gradiente, (3) UNARIO
(su una funzione sola). Una direzione è ammissibile SOLO se ne rompe esplicitamente una.

DIREZIONE A. Invece di un numero (cost) o di un argmin di copertura, guardare la
GEOMETRIA dell'INSIEME delle rappresentazioni OTTIME di f — lo "spazio delle soluzioni".
Rompe (1) [è un insieme/grafo, non uno scalare] e (3) [è relazionale: struttura di un
insieme di soluzioni]. La formula-size NON è un programma di copertura → rompe anche (2).

OGGETTO ESATTO E CANONICO. La formula-size è additiva: una formula ottima di f si spezza
in cima come f = op(a, b) con op∈{∧,∨} e cost(a)+cost(b)+1 = cost(f). L'insieme degli
SPLIT OTTIMI ``OptSplit(f) = {(op,a,b) : op(a,b)=f, cost[a]+cost[b]+1=cost[f]}`` è
ricostruibile ESATTAMENTE dal cost table (Module 6). Lo "spazio delle soluzioni" di f è
il DAG degli split ottimi (ricorsivamente, fino ai letterali). Le sue invarianti di
geometria sono definite su FUNZIONI (non su stringhe di formula), quindi sono GIÀ
invarianti rispetto a commutatività/associatività dell'encoding (pre-empta il killer K2
sulla parte geometrica; resta solo su N_min, che è un conteggio di alberi).

IPOTESI H-A (Explorer). La geometria dello spazio delle soluzioni SEPARA funzioni di pari
chiave-scalare (cost, |orbita B_n±|, N_min): esiste struttura nell'INSIEME degli ottimi
non catturata dalla sua cardinalità (N_min, direzione E) né dagli scalari del dizionario.

KILLER DICHIARATI IN ANTICIPO (se uno scatta → RESTATEMENT):
  K1  la geometria è ricostruibile da (cost, |orbita|, N_min) — nessuna coppia di pari
      chiave-scalare è separata dalla geometria → il segnale è il conteggio rivestito.
  K2  (canonicità) il verdetto cambia passando da N_min ORDINATO (alberi di parsing
      ordinati) a N_min NON-ordinato (quoziente AC): artefatto di encoding (come S nel
      ciclo 4, d_flip nel ciclo 5).
  K3  la geometria è determinata da Aut(f)/orbita: a |orbita| fissa la geometria è
      costante → riduzione alla simmetria.

RISULTATO DEL CICLO (onesto). n=3: SOTTO-SOGLIA — la chiave-scalare (cost,|orbita|,N_min)
ha già 14 classi == |P_orbit±|=14, nessuno spazio per la geometria (test vacuo). n=4
(esaustivo, 65536 funzioni): la geometria RAFFINA la chiave-scalare da 209 a 222 ==
|P_orbit±|, separando 12+ coppie di pari (cost,|orbita|,N_min) in modo K2-canonico —
sembra "contenuto nuovo". L'ADVERSARY lo UCCIDE: il K1 ingenuo ("ricostruibile dai 3
scalari") era troppo debole; il criterio vero (Entry 7) è "NON ricostruibile da cost".
La geometria è costruita INTERAMENTE dal cost table (``optimal_splits`` usa solo AND/OR e
il confronto di cost) → è in σ(cost) per costruzione. Inoltre, essendo B_n±-invariante,
ogni coppia che separa sta in orbite DIVERSE; il dizionario del Ciclo 6 è orbit-completo
a n=4 (|P_Σ|=222), quindi separa GIÀ tutte quelle coppie — il solo cofactor_cost_profile
(∈ σ(cost)) le separa tutte. Verdetto: RESTATEMENT (settimo collasso). Lezione di metodo:
la direzione A era STRUTTURALMENTE incapace di produrre il falsificatore, perché ogni suo
invariante è a valle della formula-size (σ(cost)); per uscire da σ(cost) serve una
struttura NON derivata dal costo → direzione B (politomorfismi).

ATTENZIONE (scope). Constatazione sul METODO su istanze FINITE, NON un claim su P vs NP.
Tutto ESATTO e deterministico (interi). ``analyze`` espone il check adversariale
``sigma_cost_dominated`` che declassa il verdetto a RESTATEMENT quando la separazione
geometrica è già in σ(cost).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Tuple

from pnp_lab.circuits.circuit import AND, NOT, OR, projection
from pnp_lab.circuits.synthesis import ComplexityTable
from pnp_lab.meta_complexity.falsifier_hunt import cofactor_cost_profile, cost_orbit


Split = Tuple[str, int, int]


# --------------------------------------------------------------------------- #
#  Lo spazio delle soluzioni: split ottimi, DAG, conteggi                     #
# --------------------------------------------------------------------------- #

def optimal_splits(ct: ComplexityTable) -> Dict[int, List[Split]]:
    """``OptSplit(t)`` per ogni t: tutti gli split ORDINATI (op, a, b) con
    op(a,b)=t e cost[a]+cost[b]+1=cost[t]. Un solo passaggio O(N²) sulle coppie.

    Ordinati = (a,b) e (b,a) entrambi presenti → conta gli alberi di parsing ORDINATI;
    la versione AC-quozientata si ottiene a valle (vedi ``n_min`` unordered).
    Riferimento O(N²): pratico solo per n=3; per n=4 usare ``optimal_splits_via_dp``."""
    cost = ct.cost
    splits: Dict[int, List[Split]] = {t: [] for t in cost}
    items = list(cost.items())
    for a, ca in items:
        for b, cb in items:
            s = ca + cb + 1
            t_and = AND(a, b)
            if cost.get(t_and) == s:
                splits[t_and].append(("and", a, b))
            t_or = OR(a, b)
            if cost.get(t_or) == s:
                splits[t_or].append(("or", a, b))
    return splits


def optimal_splits_via_dp(n: int, cap: int = 60) -> Tuple[Dict[int, int], Dict[int, List[Split]]]:
    """Costruisce cost-table E tutti gli split ottimi nella STESSA DP per costo
    crescente (stesso lavoro di ``min_formula_sizes``, niente scan O(N²)). Fattibile
    per n=4. Registra OGNI split che raggiunge il costo ottimo, non solo il primo."""
    total = 1 << (1 << n)
    cost: Dict[int, int] = {}
    splits: Dict[int, List[Split]] = defaultdict(list)
    by_cost: Dict[int, List[int]] = defaultdict(list)

    for j in range(n):
        xj = projection(n, j)
        for lit in (xj, NOT(xj, n)):
            if lit not in cost:
                cost[lit] = 0
                by_cost[0].append(lit)

    size = 1
    while len(cost) < total and size <= cap:
        newly: List[int] = []
        for i in range(size):
            left = by_cost[i]
            right = by_cost[size - 1 - i]
            for a in left:
                for b in right:
                    for t, op in ((AND(a, b), "and"), (OR(a, b), "or")):
                        c = cost.get(t)
                        if c is None:
                            cost[t] = size
                            newly.append(t)
                            splits[t].append((op, a, b))
                        elif c == size:          # altro split, stesso costo ottimo
                            splits[t].append((op, a, b))
                        # c < size: split non ottimo → ignorato
        by_cost[size].extend(newly)
        size += 1

    for t in cost:                                # letterali: nessuno split
        splits.setdefault(t, [])
    return dict(cost), dict(splits)


def complexity_table_from_cost(n: int, cost: Dict[int, int]) -> ComplexityTable:
    """Avvolge un cost-dict (dalla DP) in un ComplexityTable (expr non usato qui)."""
    return ComplexityTable(n=n, cost=cost, expr={}, complete=(len(cost) == (1 << (1 << n))))


def _by_increasing_cost(ct: ComplexityTable) -> List[int]:
    return sorted(ct.cost, key=lambda t: ct.cost[t])


def n_min_ordered(ct: ComplexityTable, splits: Dict[int, List[Split]]) -> Dict[int, int]:
    """N_min(t) = numero di alberi di parsing OTTIMI ORDINATI di t (letterale = 1)."""
    nm: Dict[int, int] = {}
    for t in _by_increasing_cost(ct):
        if ct.cost[t] == 0:
            nm[t] = 1
        else:
            nm[t] = sum(nm[a] * nm[b] for _, a, b in splits[t])
    return nm


def n_min_unordered(ct: ComplexityTable, splits: Dict[int, List[Split]]) -> Dict[int, int]:
    """N_min AC-quozientato: gli split commutativi {a,b} contati UNA volta; per a==b
    il numero di coppie non ordinate di alberi da k è k(k+1)/2. Sonda di canonicità K2."""
    nm: Dict[int, int] = {}
    for t in _by_increasing_cost(ct):
        if ct.cost[t] == 0:
            nm[t] = 1
            continue
        seen = set()
        total = 0
        for op, a, b in splits[t]:
            key = (op, min(a, b), max(a, b))
            if key in seen:
                continue
            seen.add(key)
            if a == b:
                total += nm[a] * (nm[a] + 1) // 2
            else:
                total += nm[a] * nm[b]
        nm[t] = total
    return nm


def reach(ct: ComplexityTable, splits: Dict[int, List[Split]]) -> Dict[int, FrozenSet[int]]:
    """DAG dello spazio delle soluzioni: ``reach(t)`` = t più tutte le sottofunzioni
    ottime raggiungibili ricorsivamente. Calcolato in ordine di costo crescente."""
    rc: Dict[int, FrozenSet[int]] = {}
    for t in _by_increasing_cost(ct):
        acc = {t}
        for _, a, b in splits[t]:
            acc |= rc[a]
            acc |= rc[b]
        rc[t] = frozenset(acc)
    return rc


# --------------------------------------------------------------------------- #
#  Invarianti di geometria (su FUNZIONI → encoding-independent)               #
# --------------------------------------------------------------------------- #

@dataclass
class Geometry:
    dag_size: int                 # |reach(f)|: numero di nodi del DAG ottimo
    branching: Tuple[int, ...]    # multiset ordinato di |OptSplit(g)|, g in reach(f)
    frontier: Tuple[int, ...]     # multiset ordinato di cost[g], g in reach(f)

    def as_tuple(self) -> Tuple:
        return (self.dag_size, self.branching, self.frontier)


def geometry(t: int, ct: ComplexityTable, splits: Dict[int, List[Split]],
             rc: Dict[int, FrozenSet[int]]) -> Geometry:
    nodes = rc[t]
    branching = tuple(sorted(len(splits[g]) for g in nodes))
    frontier = tuple(sorted(ct.cost[g] for g in nodes))
    return Geometry(dag_size=len(nodes), branching=branching, frontier=frontier)


# --------------------------------------------------------------------------- #
#  Il test del discriminante + i killer                                       #
# --------------------------------------------------------------------------- #

@dataclass
class GeoSplit:
    """Due funzioni di pari chiave-scalare (cost, |orbita|, N_min) ma geometria diversa."""
    scalar_key: Tuple
    pair: Tuple[int, int]
    geom_a: Tuple
    geom_b: Tuple


@dataclass
class GeoReport:
    n: int
    num_funcs: int
    num_scalar_classes: int
    num_geo_classes: int                 # raffinamento aggiungendo la geometria
    separated: List[GeoSplit] = field(default_factory=list)
    k2_canonical: bool = True            # il verdetto regge ordinato↔non-ordinato?
    sigma_cost_dominated: bool = True    # ADVERSARY: ogni coppia separata dalla geometria
                                         # è GIÀ separata da cofactor_cost_profile ∈ σ(cost)?

    @property
    def k1_collapses(self) -> bool:
        """K1 (debole): nessuna coppia di pari chiave-scalare separata dalla geometria.
        NB: K1 PROPRIO (Entry 7) = 'ricostruibile da cost' = ``sigma_cost_dominated``."""
        return len(self.separated) == 0

    @property
    def verdict(self) -> str:
        if self.k1_collapses:
            return "COLLAPSE (geometry adds nothing over the scalar key)"
        if not self.k2_canonical:
            return "ARTIFACT (K2: verdict flips ordered<->unordered)"
        if self.sigma_cost_dominated:
            return ("RESTATEMENT (sigma(cost): every geometry-separated pair is already "
                    "split by cofactor_cost_profile = the Cycle-6 dictionary)")
        return "GEOMETRY-SEPARATES (candidate out-of-dictionary content)"


def _scalar_key(t: int, ct: ComplexityTable, nm: Dict[int, int], n: int,
                ordered: bool) -> Tuple:
    return (ct.cost[t], len(cost_orbit(t, n, True)), nm[t])


def analyze(n: int, cap: int = 60, max_examples: int = 12) -> GeoReport:
    """Misura primaria: la geometria dello spazio delle soluzioni separa funzioni di
    pari (cost, |orbita B_n±|, N_min)? Con sonda di canonicità K2 (ordinato↔non-ord.)."""
    cost, splits = optimal_splits_via_dp(n, cap)
    ct = complexity_table_from_cost(n, cost)
    rc = reach(ct, splits)
    nm_ord = n_min_ordered(ct, splits)
    nm_uno = n_min_unordered(ct, splits)
    funcs = list(ct.cost)

    geo = {t: geometry(t, ct, splits, rc).as_tuple() for t in funcs}

    def separated_under(nm: Dict[int, int]) -> List[GeoSplit]:
        groups: Dict[Tuple, List[int]] = defaultdict(list)
        for t in funcs:
            groups[_scalar_key(t, ct, nm, n, True)].append(t)
        out: List[GeoSplit] = []
        for key, members in groups.items():
            by_geo: Dict[Tuple, List[int]] = defaultdict(list)
            for t in members:
                by_geo[geo[t]].append(t)
            if len(by_geo) >= 2:
                reps = sorted(min(v) for v in by_geo.values())
                out.append(GeoSplit(key, (reps[0], reps[1]), geo[reps[0]], geo[reps[1]]))
        return out

    sep_ord = separated_under(nm_ord)
    sep_uno = separated_under(nm_uno)
    # K2: il verdetto (separa / non separa) deve coincidere tra ordinato e non-ordinato
    k2_canonical = (len(sep_ord) > 0) == (len(sep_uno) > 0)

    # ADVERSARY (K1 proprio = σ(cost)): ogni coppia separata dalla geometria è GIÀ
    # separata dal cofactor_cost_profile (raffinamento di cost del Ciclo 6)? Se sì, la
    # geometria non esce da σ(cost) → RESTATEMENT, non contenuto nuovo.
    sigma_cost_dominated = all(
        cofactor_cost_profile(s.pair[0], n) != cofactor_cost_profile(s.pair[1], n)
        for s in sep_ord
    )

    scalar_classes = len({_scalar_key(t, ct, nm_ord, n, True) for t in funcs})
    geo_classes = len({(_scalar_key(t, ct, nm_ord, n, True), geo[t]) for t in funcs})

    sep_ord.sort(key=lambda s: s.pair)
    return GeoReport(
        n=n, num_funcs=len(funcs), num_scalar_classes=scalar_classes,
        num_geo_classes=geo_classes, separated=sep_ord[:max_examples],
        k2_canonical=k2_canonical, sigma_cost_dominated=sigma_cost_dominated,
    )
