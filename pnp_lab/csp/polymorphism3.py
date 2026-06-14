"""Module 20 (Inv-Pol Collapse) — Direzione B, ciclo TERNARIO — politomorfismi su D={0,1,2}.

Crystallized 2026-06-14. Verdetto: RESTATEMENT (g = |Pol2^{comm,idem}|, fetta del clone
Inv-Pol). Nono collasso, quarta arena. NON un claim su P vs NP. Vedi docs/invpol-collapse.md
e RESEARCH_LOG Entry 11.

Contesto. Il modulo booleano ``polymorphism.py`` ha mostrato che, nel setting idempotente,
il profilo dei politomorfismi simmetrici coincide con la BLP-risolvibilita` (parent-killer
di Barto-Kozik). MA su dominio booleano siamo SOTTO la soglia dove la dicotomia di
Bulatov-Zhuk diventa decisiva: il test vero richiede |D|>=3. Questo modulo porta l'arena
su D={0,1,2}, tutto ESATTO/deterministico/finito (interi, enumerazione finita).

IPOTESI H (Explorer). Quantita` centrale:

    g(R) = numero di WNU binari idempotenti COMMUTATIVI distinti che preservano R,
           QUOZIENTATO per gli automorfismi unari di D (permutazioni di {0,1,2} che
           fissano R), agendo per coniugazione sui testimoni.

H: g separa coppie di relazioni che i tre marker noti (has_wnu, profilo simmetrico,
   |Aut|) NON distinguono, e g NON e` funzione del profilo simmetrico ne` di |Aut|.

OGGETTO. Un'operazione binaria idempotente commutativa f: D^2 -> D e` fissata dai 3 valori
off-diagonali f(0,1), f(0,2), f(1,2) in D (la diagonale e` x->x, e f(y,x)=f(x,y)). Sono
esattamente 3^3 = 27. Sono i candidati WNU binari (un WNU binario = operazione binaria
commutativa idempotente: f(x,y)=f(y,x), f(x,x)=x).

CONVENZIONE INDICE. Un'operazione k-aria su D=3 e` una tavola ``op_table`` di valori in
{0,1,2} indicizzata in BASE 3: idx = sum_i args[i]*3^i (il booleano usa bit-shift; qui base
tre). |op_table| = 3^k.

Una relazione di arieta` m e` R subset D^m (frozenset di tuple).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import permutations, product
from typing import Dict, FrozenSet, List, Tuple

Relation = FrozenSet[Tuple[int, ...]]
OpTable = Tuple[int, ...]  # tavola di un'operazione k-aria, valori in {0,1,2}, base 3

D = (0, 1, 2)


# --------------------------------------------------------------------------- #
#  Operazioni generiche D^k -> D e politomorfismi                             #
# --------------------------------------------------------------------------- #

def op_value3(op_table: OpTable, args: Tuple[int, ...]) -> int:
    """Valore dell'operazione k-aria ``op_table`` su ``args`` (indice in BASE 3:
    idx = sum_i args[i]*3^i)."""
    idx = 0
    p = 1
    for x in args:
        idx += x * p
        p *= 3
    return op_table[idx]


def preserves3(op_table: OpTable, k: int, R: Relation) -> bool:
    """``op_table`` (k-aria, su D=3) e` un politomorfismo di R? Per OGNI scelta di k tuple
    di R, l'applicazione colonna-per-colonna ricade in R. Identico in spirito a
    ``preserves`` booleano, ma su D={0,1,2}."""
    if not R:
        return True
    m = len(next(iter(R)))
    for rows in product(R, repeat=k):
        result = tuple(
            op_value3(op_table, tuple(rows[r][j] for r in range(k)))
            for j in range(m)
        )
        if result not in R:
            return False
    return True


# --------------------------------------------------------------------------- #
#  Le 27 operazioni binarie idempotenti commutative                           #
# --------------------------------------------------------------------------- #

def _binary_table_from_offdiag(v01: int, v02: int, v12: int) -> OpTable:
    """Costruisce la tavola binaria completa (|tavola|=9, base 3) di un'operazione
    idempotente commutativa con f(0,1)=v01, f(0,2)=v02, f(1,2)=v12 (diagonale x->x)."""
    off = {(0, 1): v01, (1, 0): v01,
           (0, 2): v02, (2, 0): v02,
           (1, 2): v12, (2, 1): v12}
    table = [0] * 9
    for x in D:
        for y in D:
            idx = x + 3 * y  # base 3, k=2: idx = x*3^0 + y*3^1
            table[idx] = x if x == y else off[(x, y)]
    return tuple(table)


def commutative_idempotent_binary_ops() -> List[OpTable]:
    """Le 27 operazioni binarie idempotenti COMMUTATIVE su D={0,1,2}, ciascuna come tavola
    completa di 9 valori (base 3). Fissate dai 3 gradi di liberta` off-diagonali
    (f(0,1), f(0,2), f(1,2)) in D. Sono i candidati WNU binari."""
    return [
        _binary_table_from_offdiag(v01, v02, v12)
        for v01 in D for v02 in D for v12 in D
    ]


# --------------------------------------------------------------------------- #
#  Automorfismi unari di R                                                     #
# --------------------------------------------------------------------------- #

def _apply_perm_to_relation(perm: Tuple[int, int, int], R: Relation) -> Relation:
    """Applica la permutazione ``perm`` di {0,1,2} componente-per-componente a ogni tupla
    di R (perm[d] e` l'immagine di d)."""
    return frozenset(tuple(perm[c] for c in t) for t in R)


def unary_automorphisms(R: Relation) -> List[Tuple[int, int, int]]:
    """Le permutazioni pi di {0,1,2} (<=6) che mandano R in se` (pi applicata
    componente-per-componente a ogni tupla lascia R invariata). Restituite come tuple
    (pi(0), pi(1), pi(2))."""
    return [p for p in permutations(D) if _apply_perm_to_relation(p, R) == R]


# --------------------------------------------------------------------------- #
#  WNU-testimoni e la quantita` g                                             #
# --------------------------------------------------------------------------- #

def count_wnu_witnesses(R: Relation) -> int:
    """#{op tra le 27 binarie idempotenti commutative : preserves3(op, 2, R)}."""
    return sum(1 for op in commutative_idempotent_binary_ops() if preserves3(op, 2, R))


def wnu_witnesses(R: Relation) -> List[OpTable]:
    """Le tavole delle operazioni testimoni (binarie idempotenti commutative che
    preservano R)."""
    return [op for op in commutative_idempotent_binary_ops() if preserves3(op, 2, R)]


def _conjugate_binary_op(op: OpTable, perm: Tuple[int, int, int]) -> OpTable:
    """Coniugazione di un'operazione binaria op per la permutazione pi:
        (pi^{-1} . f . (pi x pi))(x,y) = pi^{-1}( f(pi(x), pi(y)) ).
    Se pi e` un automorfismo unario di R e f preserva R, allora anche la coniugata
    preserva R: le 27 testimoni sono CHIUSE sotto questa azione di Aut_unari(R)."""
    inv = [0, 0, 0]
    for d in D:
        inv[perm[d]] = d
    table = [0] * 9
    for x in D:
        for y in D:
            idx = x + 3 * y
            val = op_value3(op, (perm[x], perm[y]))
            table[idx] = inv[val]
    return tuple(table)


def g(R: Relation) -> int:
    """g(R) = numero di WNU-testimoni quozientato per l'azione (per coniugazione) degli
    automorfismi unari di R.

    DEFINIZIONE ESATTA DEL QUOZIENTE. Sia W l'insieme delle operazioni testimoni
    (binarie idempotenti commutative che preservano R) e A = Aut_unari(R) le permutazioni
    di {0,1,2} che fissano R. A agisce su W per coniugazione
    pi . f = pi^{-1} . f . (pi x pi) (chiusa su W: se f preserva R e pi fissa R, anche
    pi.f preserva R). g(R) e` il NUMERO DI ORBITE di W sotto A. Per A banale (solo
    l'identita`) g(R) = |W| = count_wnu_witnesses(R)."""
    W = set(wnu_witnesses(R))
    A = unary_automorphisms(R)
    seen: set = set()
    orbits = 0
    for op in W:
        if op in seen:
            continue
        orbits += 1
        for perm in A:
            seen.add(_conjugate_binary_op(op, perm))
    return orbits


# --------------------------------------------------------------------------- #
#  Marker noti su D=3                                                          #
# --------------------------------------------------------------------------- #

def has_wnu(R: Relation, k: int) -> bool:
    """Marker NOTO: R ha un politomorfismo WNU (weak near-unanimity) idempotente di
    arieta` k? La dicotomia di Bulatov-Zhuk: CSP(Γ)∈P <=> Γ ha un WNU (di QUALCHE arieta`),
    NP-completo altrimenti.

    k=2 (ESATTO): un WNU binario e` esattamente un'operazione binaria commutativa
    idempotente, quindi has_wnu(R,2) <=> count_wnu_witnesses(R) > 0.

    k=3 (LIMITATO — vedi sotto): NON enumeriamo le 3^27 operazioni ternarie. Verifichiamo
    solo operazioni WNU ternarie SPECIFICHE note: la MAGGIORANZA (majority) e la MEDIANA
    (median) sull'ordine 0<1<2, entrambe WNU idempotenti. Quindi has_wnu(R,3) qui e` una
    SOTTO-stima: True se R preserva una di queste, ma False NON esclude un WNU ternario
    diverso. Limite dichiarato apposta per non esplodere su 3^27."""
    if k == 2:
        return count_wnu_witnesses(R) > 0
    if k == 3:
        return any(preserves3(op, 3, R) for op in (MAJORITY3, MEDIAN3))
    raise ValueError("has_wnu su D=3: implementato solo per k in {2,3}")


def _ternary_table(fn) -> OpTable:
    """Costruisce la tavola (|tavola|=27, base 3) di un'operazione ternaria da una
    funzione fn(a,b,c)->valore."""
    table = [0] * 27
    for a in D:
        for b in D:
            for c in D:
                idx = a + 3 * b + 9 * c
                table[idx] = fn(a, b, c)
    return tuple(table)


def _majority(a: int, b: int, c: int) -> int:
    """Maggioranza: se due (o tre) argomenti coincidono restituisce quel valore; altrimenti
    (tutti distinti) e` idempotente solo dove possibile -> qui scegliamo il mediano come
    fallback per restare un'operazione totale ben definita (non cambia il fatto che sia
    WNU: e` idempotente e simmetrica)."""
    if a == b or a == c:
        return a
    if b == c:
        return b
    return sorted((a, b, c))[1]  # tutti distinti: mediano dell'ordine 0<1<2


def _median(a: int, b: int, c: int) -> int:
    """Mediana sull'ordine lineare 0<1<2 (WNU idempotente, simmetrica)."""
    return sorted((a, b, c))[1]


MAJORITY3 = _ternary_table(_majority)
MEDIAN3 = _ternary_table(_median)


# --------------------------------------------------------------------------- #
#  Profilo simmetrico su D=3 (enumerazione ESATTA delle operazioni simmetriche)#
# --------------------------------------------------------------------------- #

def _multiset_types(k: int) -> List[Tuple[int, int, int]]:
    """I tipi-multiset (n0,n1,n2) con n0+n1+n2=k: i possibili conteggi degli argomenti di
    un'operazione simmetrica k-aria su D=3. Sono C(k+2,2)."""
    out = []
    for n0 in range(k + 1):
        for n1 in range(k + 1 - n0):
            n2 = k - n0 - n1
            out.append((n0, n1, n2))
    return out


def _is_constant_type(t: Tuple[int, int, int], k: int) -> int:
    """Se il tipo e` costante (tutti gli argomenti uguali a d) restituisce d (forzato
    dall'idempotenza); altrimenti -1."""
    for d in D:
        if t[d] == k:
            return d
    return -1


def symmetric_idempotent_ops(k: int) -> List[OpTable]:
    """Le operazioni k-arie SIMMETRICHE idempotenti su D=3, enumerate ESATTAMENTE.

    Un'operazione simmetrica dipende solo dal tipo-multiset (n0,n1,n2) degli argomenti
    (C(k+2,2) tipi). L'idempotenza fissa il valore sui 3 tipi COSTANTI (k,0,0)->0,
    (0,k,0)->1, (0,0,k)->2. Sui restanti tipi NON-costanti il valore e` libero in {0,1,2}.
    Quindi #operazioni = 3^(#tipi-non-costanti), con #tipi-non-costanti = C(k+2,2) - 3.

    FATTIBILITA` (per la docstring): k=2 -> tipi=6, non-cost=3 -> 27 op; k=3 -> tipi=10,
    non-cost=7 -> 2187 op; k=4 -> tipi=15, non-cost=12 -> 531441 op; k=5 -> tipi=21,
    non-cost=18 -> 3^18 ~ 3.9e8 (TROPPO -> marcato slow / evitato di default)."""
    types = _multiset_types(k)
    free: List[Tuple[int, int, int]] = []
    forced: Dict[Tuple[int, int, int], int] = {}
    for t in types:
        d = _is_constant_type(t, k)
        if d >= 0:
            forced[t] = d
        else:
            free.append(t)

    # mappa: per ogni indice base-3 calcoliamo il suo tipo-multiset una volta sola
    idx_type: List[Tuple[int, int, int]] = []
    for idx in range(3 ** k):
        rem = idx
        counts = [0, 0, 0]
        for _ in range(k):
            counts[rem % 3] += 1
            rem //= 3
        idx_type.append((counts[0], counts[1], counts[2]))

    ops: List[OpTable] = []
    for assign in product(D, repeat=len(free)):
        value_of: Dict[Tuple[int, int, int], int] = dict(forced)
        for t, v in zip(free, assign):
            value_of[t] = v
        table = tuple(value_of[idx_type[idx]] for idx in range(3 ** k))
        ops.append(table)
    return ops


def has_symmetric_polymorphism3(R: Relation, k: int) -> bool:
    """R ha un politomorfismo simmetrico idempotente di arieta` k su D=3?"""
    return any(preserves3(op, k, R) for op in symmetric_idempotent_ops(k))


def symmetric_profile3(R: Relation, max_arity: int = 3) -> Tuple[int, ...]:
    """Le arieta` k in [2, max_arity] per cui R ha un politomorfismo simmetrico idempotente
    su D=3. Default max_arity=3 per restare veloce (k=4 e` 531441 operazioni: usare
    esplicitamente e con cautela)."""
    return tuple(k for k in range(2, max_arity + 1)
                 if has_symmetric_polymorphism3(R, k))


# --------------------------------------------------------------------------- #
#  Catalogo di relazioni canoniche su {0,1,2}                                 #
# --------------------------------------------------------------------------- #

def _build_catalog() -> Dict[str, Relation]:
    """Catalogo NOMINALE di relazioni piccole su D={0,1,2}, scelte a mano e documentate."""
    cat: Dict[str, Relation] = {}

    # Ordine lineare <= sull'ordine 0<1<2 (binaria).
    cat["leq"] = frozenset((x, y) for x in D for y in D if x <= y)

    # Ordine stretto < (binaria).
    cat["lt"] = frozenset((x, y) for x in D for y in D if x < y)

    # Disuguaglianza != (binaria): tutte le coppie con x!=y.
    cat["neq"] = frozenset((x, y) for x in D for y in D if x != y)

    # Ciclo diretto C3: 0->1->2->0 (binaria).
    cat["cycle3"] = frozenset({(0, 1), (1, 2), (2, 0)})

    # Semilattice min: il grafo dell'operazione min sull'ordine 0<1<2
    # come relazione ternaria {(x,y,min(x,y))}.
    cat["min_graph"] = frozenset((x, y, min(x, y)) for x in D for y in D)

    # Grafo della mediana (ternaria): {(x,y,z,med(x,y,z))} sarebbe 4-aria; usiamo invece
    # la relazione ternaria "betweenness" debole: terne ordinate {(x,y,z): x<=y<=z}.
    cat["between"] = frozenset((x, y, z) for x in D for y in D for z in D
                               if x <= y <= z)

    # NAE ternario (not-all-equal) su D=3: terne in cui NON tutti e tre coincidono.
    cat["nae3"] = frozenset((x, y, z) for x in D for y in D for z in D
                            if not (x == y == z))

    # "Rook"/all-different ternario: terne con i tre valori TUTTI distinti (permutazioni
    # di (0,1,2)).
    cat["alldiff3"] = frozenset(permutations(D))

    return cat


CATALOG: Dict[str, Relation] = _build_catalog()


# --------------------------------------------------------------------------- #
#  Analisi e killer                                                           #
# --------------------------------------------------------------------------- #

@dataclass
class RelRow:
    name: str
    R: Relation
    g_value: int
    sym_profile: Tuple[int, ...]
    n_aut: int
    wnu2: bool
    wnu3: bool


@dataclass
class Report3:
    rows: List[RelRow]
    # coppie (nameA, nameB) marker-identiche ma g-diverse: testimoni di H
    witness_pairs: List[Tuple[str, str]] = field(default_factory=list)

    def _marker_key(self, row: RelRow) -> Tuple:
        """La firma dei tre marker NOTI (escluso g): (has_wnu2, has_wnu3,
        symmetric_profile3, |Aut|). Due relazioni con la stessa firma sono
        indistinguibili dai marker noti."""
        return (row.wnu2, row.wnu3, row.sym_profile, row.n_aut)

    @property
    def k_marker_collapses(self) -> bool:
        """K-marker: OGNI coppia g-separata cade gia` in classi-marker diverse?
        Se True -> g non separa nulla di nuovo rispetto ai marker -> RESTATEMENT.
        Se False -> esiste una coppia con stessa firma-marker ma g diverso (testimone H)."""
        return len(self.witness_pairs) == 0

    @property
    def k_sigma_collapses(self) -> bool:
        """K-sigma: g e` funzione del solo profilo simmetrico sul catalogo?
        (stesso symmetric_profile3 => stesso g). Se True -> g e` un re-encoding del
        profilo -> RESTATEMENT."""
        by_prof: Dict[Tuple[int, ...], set] = {}
        for row in self.rows:
            by_prof.setdefault(row.sym_profile, set()).add(row.g_value)
        return all(len(s) == 1 for s in by_prof.values())

    @property
    def k_aut_collapses(self) -> bool:
        """K-aut: g e` funzione di |Aut_unari| sul catalogo?
        (stesso |Aut| => stesso g). Se True -> g e` un invariante unario mascherato."""
        by_aut: Dict[int, set] = {}
        for row in self.rows:
            by_aut.setdefault(row.n_aut, set()).add(row.g_value)
        return all(len(s) == 1 for s in by_aut.values())

    @property
    def verdict(self) -> str:
        killers = []
        if self.k_marker_collapses:
            killers.append("K-marker")
        if self.k_sigma_collapses:
            killers.append("K-sigma")
        if self.k_aut_collapses:
            killers.append("K-aut")
        if killers:
            return "RESTATEMENT/collapse via " + "+".join(killers)
        return "NESSUN killer scatta sul catalogo (g separa fuori dai marker noti)"


def analyze3(catalog: Dict[str, Relation] = None, max_arity: int = 3) -> Report3:
    """Per ogni R del catalogo calcola (g, symmetric_profile3, |Aut_unari|, verdetti
    marker) e i tre killer di H. NON trae conclusioni: produce solo i numeri esatti."""
    if catalog is None:
        catalog = CATALOG
    rows: List[RelRow] = []
    for name in sorted(catalog):
        R = catalog[name]
        rows.append(RelRow(
            name=name,
            R=R,
            g_value=g(R),
            sym_profile=symmetric_profile3(R, max_arity),
            n_aut=len(unary_automorphisms(R)),
            wnu2=has_wnu(R, 2),
            wnu3=has_wnu(R, 3),
        ))

    # coppie marker-identiche ma g-diverse
    rep = Report3(rows=rows)
    witnesses: List[Tuple[str, str]] = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rep._marker_key(rows[i]) == rep._marker_key(rows[j]) \
                    and rows[i].g_value != rows[j].g_value:
                witnesses.append((rows[i].name, rows[j].name))
    rep.witness_pairs = witnesses
    return rep
