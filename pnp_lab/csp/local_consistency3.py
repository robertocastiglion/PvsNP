"""Module 21 (Local-Consistency Width) — Direzione: il VALORE quantitativo w*(Γ).

Regime: "esatto-PER-ISTANZA su campione". Dominio D={0,1,2}. Per Γ DENTRO la classe
trattabile (ha WNU binario o ternario noto) misuriamo NON il verdetto si`/no della
dicotomia, ma un INTERO: la larghezza di consistenza locale w*(Γ) richiesta affinche` la
(k,k+1)-consistenza decida la soddisfacibilita` su una BATTERIA CONGELATA di istanze-test.

IPOTESI H (Explorer). w*(Γ) separa relazioni che la dicotomia di Bulatov-Zhuk dichiara
equivalenti (stesso g, stesso profilo simmetrico, tutte WNU), e w* NON e` ricostruibile
da |Pol-slice| ne` dal verdetto si`/no.

ATTENZIONE ONESTA` (Barto-Kozik). Il teorema "bounded width = (2,3)-consistency" dice che
OGNI CSP di larghezza limitata e` gia` deciso dalla (2,3)-consistenza. Se sul campione
w*<=2 ovunque e w*=1 <=> ha-maggioranza, l'ipotesi e` molto probabilmente il DECIMO
collasso su Barto-Kozik/Feder-Vardi. Il predicato K-bw23 verifica esattamente questo ed e`
controllato per PRIMO.

----------------------------------------------------------------------------------------
DEFINIZIONI ESATTE
----------------------------------------------------------------------------------------

CSP istanza  Phi = (n_vars, constraints), constraints = lista di (scope, R) dove
    scope = tupla di indici di variabile distinti, R = relazione su D=3 di arieta`
    len(scope). Le variabili sono 0..n_vars-1.

is_sat(Phi): forza bruta ESATTA su 3^n assegnamenti (n<=6 -> <=729). Restituisce True sse
    esiste un assegnamento totale che soddisfa OGNI vincolo. Interi, deterministico.

(k,k+1)-minimality (Barto-Kozik, "Constraint satisfaction problems solvable by local
consistency methods", JACM 2014, def. di (l,k)-consistency). Implementiamo la
(k,k+1)-minimality cosi`:
    - Per OGNI sottoinsieme S di variabili con |S|<=k mantieniamo un insieme P[S] di
      assegnamenti parziali (tuple indicizzate sulle variabili ordinate di S) ammissibili.
      Inizialmente P[S] = tutti i 3^|S| assegnamenti che soddisfano ogni vincolo
      INTERAMENTE contenuto in S.
    - Propaghiamo a punto fisso la regola di ESTENSIONE: un assegnamento a in P[S] (con
      |S|=k) sopravvive solo se per OGNI variabile v non in S esiste un'estensione di a a
      S∪{v} che (i) e` in P di ogni sotto-insieme di taglia <=k e (ii) soddisfa ogni
      vincolo contenuto in S∪{v}. Inoltre la coerenza incrociata: a in P[S] sopravvive solo
      se ogni sua restrizione a S'⊆S resta in P[S'] (e viceversa P[S'] tiene solo le
      restrizioni ancora supportate). Iteriamo finche` nessun P[S] cambia.
    - Phi e` (k,k+1)-consistente sse al punto fisso NESSUN P[S] e` vuoto (per |S|<=k con S
      che tocca almeno una variabile -> in pratica controlliamo P[S] non vuoto per ogni S).
    k=1 coincide con la node+arc-consistency (domini di singole variabili filtrati
    dall'estendibilita` lungo ogni vincolo). k=2 e` la (2,3)-consistency. Esatta e
    polinomiale (n^(k+1) sottoinsiemi, 3^(k+1) assegnamenti) per k piccolo.

SOUNDNESS. SAT => (k,k+1)-consistente per ogni k (un modello totale induce assegnamenti
parziali coerenti che non vengono mai cancellati). Quindi kk1_consistent(Phi,k) e`
implicata da is_sat(Phi); il gap interessante e` UNSAT ma localmente consistente.

w*(Gamma, max_k) = min{ k<=max_k : per OGNI Phi nella batteria T(Gamma),
    kk1_consistent(Phi,k) == is_sat(Phi) }, oppure None se nessun k<=max_k basta.

T(Gamma): batteria CONGELATA e deterministica di istanze-test costruite copiando Gamma su
scope di <=6 variabili. Include istanze SAT facili e istanze UNSAT "cicliche"
(path/ciclo che chiudono una contraddizione globale ma restano localmente consistenti a
basso k). La batteria e` una SCELTA (lo dira` l'Adversary): w* e` relativo a T(Gamma).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations, product
from typing import Dict, FrozenSet, List, Optional, Tuple

from pnp_lab.csp.polymorphism3 import (
    CATALOG,
    MAJORITY3,
    MEDIAN3,
    _binary_table_from_offdiag,
    count_wnu_witnesses,
    g,
    has_wnu,
    preserves3,
    symmetric_profile3,
    unary_automorphisms,
)

Relation = FrozenSet[Tuple[int, ...]]
Scope = Tuple[int, ...]
Constraint = Tuple[Scope, Relation]

D = (0, 1, 2)


# --------------------------------------------------------------------------- #
#  Istanza CSP e SAT esatto                                                    #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class CSP:
    """Istanza CSP su D={0,1,2}. ``n_vars`` variabili 0..n_vars-1, ``constraints`` lista
    di (scope, R). Ogni scope e` una tupla di indici di variabile DISTINTI; R ha arieta`
    pari a len(scope) ed e` interpretata nell'ordine dello scope."""
    n_vars: int
    constraints: Tuple[Constraint, ...]


def _satisfies(assignment: Tuple[int, ...], constraint: Constraint) -> bool:
    """L'assegnamento totale soddisfa il vincolo? Proietta sullo scope e controlla in R."""
    scope, R = constraint
    return tuple(assignment[v] for v in scope) in R


def is_sat(phi: CSP) -> bool:
    """SAT ESATTO per forza bruta su 3^n assegnamenti (n<=6 -> <=729). Interi,
    deterministico. True sse esiste assegnamento totale che soddisfa OGNI vincolo."""
    for assignment in product(D, repeat=phi.n_vars):
        if all(_satisfies(assignment, c) for c in phi.constraints):
            return True
    return False


# --------------------------------------------------------------------------- #
#  (k,k+1)-minimality a punto fisso                                            #
# --------------------------------------------------------------------------- #

def _constraints_within(phi: CSP, S: FrozenSet[int]) -> List[Constraint]:
    """I vincoli il cui scope e` interamente contenuto in S."""
    return [c for c in phi.constraints if set(c[0]).issubset(S)]


def _partial_satisfies(S_sorted: Tuple[int, ...], values: Tuple[int, ...],
                       constraint: Constraint) -> bool:
    """L'assegnamento parziale (sulle variabili S_sorted, ordinate) soddisfa un vincolo il
    cui scope e` contenuto in S_sorted. ``values[i]`` e` il valore di S_sorted[i]."""
    pos = {v: i for i, v in enumerate(S_sorted)}
    scope, R = constraint
    return tuple(values[pos[v]] for v in scope) in R


def kk1_consistent(phi: CSP, k: int) -> bool:
    """(k,k+1)-minimality (Barto-Kozik) a punto fisso. Vedi docstring di modulo per la
    definizione ESATTA implementata. Restituisce True sse al punto fisso nessun insieme di
    assegnamenti parziali P[S] (|S|<=k) si svuota.

    k=1 = node+arc-consistency. k=2 = (2,3)-consistency. Esatta, deterministica.
    """
    if k < 1:
        raise ValueError("k deve essere >= 1")
    n = phi.n_vars
    kk = min(k, n)

    # Sottoinsiemi S di taglia 1..kk, ordinati come tuple crescenti.
    subsets: List[Tuple[int, ...]] = []
    for size in range(1, kk + 1):
        subsets.extend(combinations(range(n), size))

    # P[S] = set di tuple-valori ammissibili (allineate a S ordinato).
    P: Dict[Tuple[int, ...], set] = {}
    for S in subsets:
        Sset = frozenset(S)
        within = _constraints_within(phi, Sset)
        adm = set()
        for vals in product(D, repeat=len(S)):
            if all(_partial_satisfies(S, vals, c) for c in within):
                adm.add(vals)
        P[S] = adm

    # Propagazione a punto fisso.
    changed = True
    while changed:
        changed = False
        for S in subsets:
            if not P[S]:
                continue
            Sset = frozenset(S)
            survivors = set()
            for vals in P[S]:
                if _supported(phi, S, vals, P, kk, n):
                    survivors.add(vals)
            if survivors != P[S]:
                P[S] = survivors
                changed = True

    # (k,k+1)-consistente sse nessun P[S] vuoto.
    return all(len(P[S]) > 0 for S in subsets)


def _supported(phi: CSP, S: Tuple[int, ...], vals: Tuple[int, ...],
               P: Dict[Tuple[int, ...], set], kk: int, n: int) -> bool:
    """L'assegnamento parziale (S, vals) sopravvive?

    (a) Coerenza verso il basso: ogni restrizione di (S,vals) a un sottoinsieme S'⊆S deve
        essere ancora in P[S'].
    (b) Estensione verso l'alto (solo se |S|==kk e |S|<n): per OGNI variabile v non in S,
        deve esistere x in D tale che l'estensione a S∪{v} sia coerente con P su tutti i
        sotto-insiemi di taglia <=kk e soddisfi i vincoli entro S∪{v}.
    """
    pos = {var: i for i, var in enumerate(S)}

    # (a) restrizioni verso il basso
    for size in range(1, len(S)):
        for Sub in combinations(S, size):
            sub_vals = tuple(vals[pos[v]] for v in Sub)
            if sub_vals not in P.get(Sub, set()):
                return False

    # (b) estensione verso l'alto (lookahead a una variabile)
    if len(S) == kk and len(S) < n:
        others = [v for v in range(n) if v not in pos]
        for v in others:
            T = tuple(sorted(S + (v,)))
            within = _constraints_within(phi, frozenset(T))
            found = False
            for x in D:
                # costruisci i valori sull'ordine di T
                full = {var: vals[pos[var]] for var in S}
                full[v] = x
                tvals = tuple(full[var] for var in T)
                if not all(_partial_satisfies(T, tvals, c) for c in within):
                    continue
                # coerenza: ogni sotto-insieme di T di taglia <=kk deve avere la sua
                # proiezione in P
                ok = True
                for sz in range(1, kk + 1):
                    for Sub in combinations(T, sz):
                        if Sub == S:
                            continue
                        proj = tuple(full[var] for var in Sub)
                        if proj not in P.get(Sub, set()):
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    found = True
                    break
            if not found:
                return False
    return True


# --------------------------------------------------------------------------- #
#  Batteria di istanze-test T(Gamma) — CONGELATA / deterministica             #
# --------------------------------------------------------------------------- #

def T(Gamma: Relation) -> List[Tuple[str, CSP]]:
    """GENERATORE BATTERIA di istanze-test da Gamma (vincoli = copie di Gamma su scope di
    variabili, n<=6). DETERMINISTICA e CONGELATA.

    Include, per arieta` m = arieta`(Gamma):
      (A) istanze chiaramente SAT (cammino corto / pochi vincoli, soddisfacibile);
      (B) per Gamma BINARIA: catene/cicli di copie di Gamma su 3..6 variabili. Il ciclo
          chiude la relazione su se stessa: se Gamma e` una relazione "di tipo <" o ciclica
          questo crea contraddizioni globali che restano localmente consistenti a basso k
          (e` il cuore che separa w*).
      (C) per Gamma di arieta` qualunque: copie su scope distinti e copie sovrapposte
          (condividono variabili) per stressare la propagazione.

    La SCELTA della batteria e` esplicita (lo dira` l'Adversary): w* e` relativo a essa.
    Supportiamo SOLO arieta` 2 e 3; per altre arieta` la batteria e` vuota.
    """
    if not Gamma:
        return []
    m = len(next(iter(Gamma)))
    if m not in (2, 3):
        return []
    out: List[Tuple[str, CSP]] = []

    if m == 2:
        # (B) cicli e cammini di copie di Gamma: x0 R x1 R x2 ... R x0
        for nvar in (3, 4, 5, 6):
            # ciclo: archi (i, i+1 mod nvar)
            cons = tuple(((i, (i + 1) % nvar), Gamma) for i in range(nvar))
            out.append((f"cycle{nvar}", CSP(nvar, cons)))
            # cammino aperto: archi (i, i+1) per i<nvar-1 (no chiusura)
            cons_p = tuple(((i, i + 1), Gamma) for i in range(nvar - 1))
            out.append((f"path{nvar}", CSP(nvar, cons_p)))
        # ciclo con una "corda" inversa per stressare (chiude due percorsi)
        chord = tuple(((i, (i + 1) % 5), Gamma) for i in range(5)) + (((0, 2), Gamma),)
        out.append(("cycle5_chord", CSP(5, chord)))

    elif m == 3:
        # (C) copie ternarie: una copia (SAT banale), due copie disgiunte, due copie che
        # condividono una variabile, tre copie a ventaglio condividendo una variabile.
        out.append(("one", CSP(3, (((0, 1, 2), Gamma),))))
        out.append(("two_disjoint", CSP(6, (((0, 1, 2), Gamma), ((3, 4, 5), Gamma)))))
        out.append(("two_share1", CSP(5, (((0, 1, 2), Gamma), ((2, 3, 4), Gamma)))))
        out.append(("fan_share0", CSP(5, (((0, 1, 2), Gamma),
                                          ((0, 3, 4), Gamma)))))
        # catena ternaria a 6 var che sovrappone due variabili tra copie consecutive
        out.append(("chain6", CSP(6, (((0, 1, 2), Gamma),
                                      ((1, 2, 3), Gamma),
                                      ((2, 3, 4), Gamma),
                                      ((3, 4, 5), Gamma)))))
        # permutazioni dello scope per rcompere eventuali simmetrie di propagazione
        out.append(("perm_scope", CSP(4, (((0, 1, 2), Gamma),
                                          ((2, 3, 0), Gamma)))))

    # (A) un'istanza con un solo vincolo (sempre SAT se Gamma non vuota) — controllo che
    # la consistenza locale NON dichiari mai UNSAT una SAT banale.
    out.append(("single", CSP(m, ((tuple(range(m)), Gamma),))))

    return out


# --------------------------------------------------------------------------- #
#  w*                                                                          #
# --------------------------------------------------------------------------- #

def w_star(Gamma: Relation, max_k: int = 4) -> Optional[int]:
    """w*(Gamma) = min{ k<=max_k : per OGNI Phi in T(Gamma),
    kk1_consistent(Phi,k) == is_sat(Phi) }, oppure None se nessun k<=max_k basta.

    Esatto: ogni is_sat e` enumerazione completa <=729, ogni kk1_consistent e` un punto
    fisso esatto. La conclusione e` relativa alla batteria T(Gamma)."""
    battery = T(Gamma)
    if not battery:
        return None
    sat_cache = {name: is_sat(phi) for name, phi in battery}
    for k in range(1, max_k + 1):
        if all(kk1_consistent(phi, k) == sat_cache[name] for name, phi in battery):
            return k
    return None


# --------------------------------------------------------------------------- #
#  Catalogo Gamma trattabili (WNU) + extra ternarie                           #
# --------------------------------------------------------------------------- #

def tractable_catalog() -> Dict[str, Relation]:
    """Le relazioni del CATALOG di polymorphism3 che sono TRATTABILI (has_wnu(R,2) o
    has_wnu(R,3)), piu` alcune Gamma ternarie costruite a mano per coprire i marker:
      - min_graph (semilattice): atteso w*=1 (chiusura width-1);
      - between/leq/lt (ordine): near-unanimity (mediana ternaria);
      - majority_graph: relazione preservata dalla MAGGIORANZA ternaria (ha-maggioranza).
    Le NON-WNU (neq, nae3, alldiff3) sono ESCLUSE: w* fuori dalla classe trattabile non e`
    la quantita` di H.
    """
    cat: Dict[str, Relation] = {}
    for name, R in CATALOG.items():
        if has_wnu(R, 2) or has_wnu(R, 3):
            cat[name] = R

    # Grafo della maggioranza ternaria come relazione 4-aria sarebbe troppo grande; usiamo
    # invece una relazione BINARIA su cui la maggioranza agisce non banalmente: il grafo di
    # un albero/struttura preservata da majority. Prendiamo "leq" gia` presente (preservata
    # dalla mediana = near-unanimity). Aggiungiamo una relazione binaria a 2 elementi
    # (sotto-dominio {0,1}) su cui agiscono majority booleani.
    # Relazione binaria "implies01": su valori in {0,1}, x<=y, piu` lo 0/1 puro.
    cat["impl01"] = frozenset({(0, 0), (0, 1), (1, 1)})
    # Relazione binaria "eq01": uguaglianza ristretta a {0,1} (riflessiva su 0,1).
    cat["eq012"] = frozenset({(0, 0), (1, 1), (2, 2)})
    return cat


# --------------------------------------------------------------------------- #
#  Analisi e predicati-killer                                                  #
# --------------------------------------------------------------------------- #

def _has_majority(R: Relation) -> bool:
    """R ha la MAGGIORANZA ternaria come politomorfismo? (near-unanimity binaria ->
    larghezza (2,3) e tipicamente w*<=2; la maggioranza implica width-1 su molti casi).
    Usiamo MAJORITY3 di polymorphism3."""
    return preserves3(MAJORITY3, 3, R)


@dataclass
class WRow:
    name: str
    R: Relation
    g_value: int
    sym_profile: Tuple[int, ...]
    has_majority: bool
    n_pol_slice: int  # |fetta Pol|: #testimoni WNU binari (proxy di |Pol_maj| locale)
    w: Optional[int]


@dataclass
class WReport:
    rows: List[WRow]
    max_k: int

    @property
    def w_values(self) -> List[Optional[int]]:
        return [r.w for r in self.rows]

    @property
    def w_star_range(self) -> Tuple[Optional[int], Optional[int]]:
        """(min, max) dei w* FINITI sul campione (esclude None)."""
        finite = [r.w for r in self.rows if r.w is not None]
        if not finite:
            return (None, None)
        return (min(finite), max(finite))

    @property
    def k_bw23_holds(self) -> bool:
        """K-bw23 (PRINCIPALE): max w* finito sul campione <= 2? (Barto-Kozik: bounded
        width = (2,3)-consistency). Se True -> il range collassa a {1,2}."""
        finite = [r.w for r in self.rows if r.w is not None]
        return bool(finite) and max(finite) <= 2

    @property
    def w1_tracks_majority(self) -> bool:
        """w*=1 <=> ha_majority su 100% del campione (sui Gamma con w* finito)?"""
        for r in self.rows:
            if r.w is None:
                continue
            if (r.w == 1) != r.has_majority:
                return False
        return True

    @property
    def k_polslice_collapses(self) -> bool:
        """K-Pol-slice: w* e` funzione esatta di (g, profilo, |Pol-slice|) sul campione?
        (stessa tripla => stesso w*). Se True -> w* e` un re-encoding di quelle quantita`."""
        by_key: Dict[Tuple, set] = {}
        for r in self.rows:
            key = (r.g_value, r.sym_profile, r.n_pol_slice)
            by_key.setdefault(key, set()).add(r.w)
        return all(len(s) == 1 for s in by_key.values())

    @property
    def h_separates(self) -> Tuple[bool, List[Tuple[str, str]]]:
        """Separazione H: esiste coppia stesso-g, stesso-profilo, ma w* diverso?
        Restituisce (esiste?, lista coppie testimoni)."""
        witnesses: List[Tuple[str, str]] = []
        for i in range(len(self.rows)):
            for j in range(i + 1, len(self.rows)):
                a, b = self.rows[i], self.rows[j]
                if a.g_value == b.g_value and a.sym_profile == b.sym_profile \
                        and a.w != b.w:
                    witnesses.append((a.name, b.name))
        return (len(witnesses) > 0, witnesses)


def analyze_consistency(catalog: Dict[str, Relation] = None,
                        max_k: int = 4, max_arity: int = 3) -> WReport:
    """Per ogni Gamma trattabile calcola (g, symmetric_profile3, ha_majority,
    |Pol-slice|, w*) e i predicati-killer. NON trae conclusioni: solo numeri esatti."""
    if catalog is None:
        catalog = tractable_catalog()
    rows: List[WRow] = []
    for name in sorted(catalog):
        R = catalog[name]
        rows.append(WRow(
            name=name,
            R=R,
            g_value=g(R),
            sym_profile=symmetric_profile3(R, max_arity),
            has_majority=_has_majority(R),
            n_pol_slice=count_wnu_witnesses(R),
            w=w_star(R, max_k=max_k),
        ))
    return WReport(rows=rows, max_k=max_k)
