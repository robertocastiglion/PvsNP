"""Modulo 16 — Bounded Observer: le barriere come (in)distinguibilità.

Domanda. Esiste UNA definizione di "osservatore limitato" che contenga come casi
particolari relativizzazione (limite di query), algebrizzazione (limite di query
algebriche), natural proofs (limite di calcolo) e proof complexity (limite di
lunghezza di prova)? E le quattro barriere si scrivono tutte come

    Δ(𝒞; D0, D1) ≤ ε

per classi 𝒞 diverse di osservatori? Questo modulo costruisce l'astrazione,
istanzia le quattro barriere su mondi MINUSCOLI e MISURA esattamente la risposta.

L'astrazione (minimale). Un osservatore è una tripla T = (𝒜, 𝒭, t):
  • 𝒜 = INTERFACCIA di accesso — l'insieme di query ammesse e la funzione
    risposta ans(w, q). È l'asse INFORMAZIONE (quanti bit per sonda).
  • 𝒭 = RISORSA di calcolo — la classe di funzioni con cui combinare le risposte
    in un bit. È l'asse CALCOLO.
  • t = BUDGET — numero di query / lunghezza del transcript / taglia del
    certificato.
Decisione: T(w) = 𝒭( (q1, ans(w,q1)), …, (qt, ans(w,qt)) ) ∈ {0,1}.

Il vantaggio di distinzione UNICO, su una classe 𝒞 e due distribuzioni di mondi:

    Δ(𝒞; D0, D1) = sup_{T ∈ 𝒞} | Pr_{w~D1}[T(w)=1] − Pr_{w~D0}[T(w)=1] | .

Esito misurato (vedi docs/bounded-observer.md per il ragionamento completo):
  • RELATIVIZZAZIONE e ALGEBRIZZAZIONE rientrano ESATTAMENTE: stesso template,
    differenza SOLO nell'interfaccia 𝒜 (query booleane vs query alla estensione
    di basso grado). Δ ≤ ε è un lower bound di query complexity. 𝒭 illimitata.
  • NATURAL PROOFS rientra sull'asse ORTOGONALE: 𝒜 satura (legge tutta la truth
    table), Δ ≤ ε viene dal calcolo 𝒭 limitato (è il Modulo 15).
  • PROOF COMPLEXITY NON rientra. Qui lo DIMOSTRIAMO numericamente: un sistema di
    prova è SANO, quindi sul mondo "falso" D0 la probabilità di produrre una
    refutazione è IDENTICAMENTE 0 — non c'è ε. Δ degenera in una quantità
    UNILATERALE (esiste un certificato di lunghezza ≤ t?), il cui complessità
    governante è min |Π| ∈ ℕ ∪ {∞}: un tipo DIVERSO da sup|E1−E0| ∈ [0,1].

Onestà (vincolante per questo repo). Sono misure ESATTE su istanze MINUSCOLE, non
le barriere asintotiche. In particolare per l'algebrizzazione mostriamo
l'ARRICCHIMENTO dell'interfaccia e il lemma (Schwartz–Zippel) su cui poggia il
bound, NON riproduciamo un lower bound algebrico asintotico (servirebbe la
separazione di classi alla Aaronson–Wigderson). Nessun risultato qui tocca P vs NP.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Callable, FrozenSet, Hashable, List, Optional, Sequence, Tuple

# Un "mondo" è un qualunque oggetto hashable; una distribuzione è una lista di
# coppie (mondo, probabilità). Δ è definito su queste.
World = Hashable
Dist = Sequence[Tuple[World, float]]


def advantage(decide: Callable[[World], int], d0: Dist, d1: Dist) -> float:
    """| Pr_{D1}[decide=1] − Pr_{D0}[decide=1] | per UN osservatore `decide`."""
    p1 = sum(p for w, p in d1 if decide(w))
    p0 = sum(p for w, p in d0 if decide(w))
    return abs(p1 - p0)


def class_advantage(
    observers: Sequence[Callable[[World], int]], d0: Dist, d1: Dist
) -> float:
    """Δ(𝒞; D0, D1) = sup_T Δ(T) sulla classe `observers` (qui finita: esatto)."""
    return max((advantage(o, d0, d1) for o in observers), default=0.0)


# ════════════════════════════════════════════════════════════════════════════
# (1) RELATIVIZZAZIONE — interfaccia: query BOOLEANE; 𝒭 illimitata; budget t.
# ════════════════════════════════════════════════════════════════════════════
#
# Mondo = oracolo A ⊆ {0,…,N−1}. Problema della "needle" (= il separatore
# canonico P vs NP relativo: decidere se ∃ x ∈ A):
#     D1 = "nessuna needle"  (A = ∅)
#     D0 = "una needle"      (A = {i}, i uniforme in 0..N−1)
# Osservatore: sceglie un insieme S di ≤ t punti, interroga "i ∈ A?" (un BIT
# ciascuno), poi applica una funzione booleana ARBITRARIA g alle t risposte
# (calcolo illimitato). Δ della classe = t/N: si distingue solo se si interroga
# la cella della needle; mancandola, i due mondi sono identici.

def relativization_worlds(n: int) -> Tuple[Dist, Dist]:
    """(D0, D1) per la needle su N punti. D1 = vuoto, D0 = una needle uniforme."""
    d1: Dist = [(frozenset(), 1.0)]
    d0: Dist = [(frozenset({i}), 1.0 / n) for i in range(n)]
    return d0, d1


def _boolean_query_observers(n: int, t: int) -> List[Callable[[World], int]]:
    """Tutti gli osservatori a ≤ t query booleane: scegli S (|S|=t), poi g
    arbitraria sulle risposte. 𝒭 = illimitata (g qualunque)."""
    obs: List[Callable[[World], int]] = []
    for s in combinations(range(n), t):
        for accept in range(1 << (1 << t)):           # ogni g: {0,1}^t → {0,1}
            def decide(world, s=s, accept=accept):
                ans = 0
                for k, point in enumerate(s):
                    if point in world:
                        ans |= 1 << k
                return (accept >> ans) & 1
            obs.append(decide)
    return obs


def relativization_advantage(n: int, t: int) -> float:
    """Δ ESATTO della classe a ≤ t query booleane sulla needle (= t/N)."""
    d0, d1 = relativization_worlds(n)
    return class_advantage(_boolean_query_observers(n, t), d0, d1)


# ════════════════════════════════════════════════════════════════════════════
# (2) ALGEBRIZZAZIONE — interfaccia: query alla ESTENSIONE di basso grado.
# ════════════════════════════════════════════════════════════════════════════
#
# Stesso mondo (needle), ma l'osservatore può interrogare l'estensione
# MULTILINEARE Ã: F_p^k → F_p dell'oracolo in QUALUNQUE punto di campo (riceve un
# ELEMENTO di campo, non un bit). È la stessa tripla (𝒜, 𝒭, t): cambia SOLO 𝒜.
# Mostriamo che 𝒜_alg ⊋ 𝒜_rel — UNA query algebrica già batte t query booleane —
# e il lemma di Schwartz–Zippel su cui poggia il bound algebrico.

def _ml_indicator(a: Tuple[int, ...], x: Tuple[int, ...], p: int) -> int:
    """Estensione multilineare dell'indicatore del punto booleano a, valutata in
    x ∈ F_p^k:  Π_i [ x_i  se a_i=1  altrimenti (1−x_i) ]  (mod p)."""
    val = 1
    for ai, xi in zip(a, x):
        val = (val * (xi if ai == 1 else (1 - xi))) % p
    return val


def algebrization_one_query_advantage(k: int, p: int) -> Tuple[float, float]:
    """Confronto su needle in N=2^k punti, p primo:
        ritorna (Δ con 1 query ALGEBRICA, Δ con 1 query BOOLEANA).
    La query algebrica usa un punto di campo fuori dal cubo (coord = 2), così
    Ã(x) ≠ 0 per OGNI needle ⇒ Δ_alg = 1; la booleana vede 1/N. 𝒜_alg ⊋ 𝒜_rel."""
    n = 1 << k
    needles = list(product((0, 1), repeat=k))      # le 2^k posizioni booleane
    x = tuple(2 % p for _ in range(k))             # punto di campo fuori dal cubo
    # D1 (oracolo vuoto): Ã ≡ 0 ⇒ la query dà 0 ⇒ decide=0 sempre.
    # D0 (needle a uniforme): decide=1 sse Ã_a(x) ≠ 0.
    nonzero = sum(1 for a in needles if _ml_indicator(a, x, p) != 0)
    adv_alg = nonzero / n                            # = 1 con questo x
    adv_bool = 1.0 / n                               # una query booleana: t/N, t=1
    return adv_alg, adv_bool


def _eval_multilinear(coeffs: dict, x: Tuple[int, ...], p: int) -> int:
    """Valuta un polinomio MULTILINEARE (coeffs: frozenset(vars) → coeff) in x."""
    total = 0
    for support, c in coeffs.items():
        term = c % p
        for v in support:
            term = (term * x[v]) % p
        total = (total + term) % p
    return total


def schwartz_zippel_agreement(coeffs_a: dict, coeffs_b: dict, k: int, p: int) -> float:
    """Frazione ESATTA di F_p^k su cui due polinomi multilineari coincidono
    (enumerazione completa). Per A≠B il lemma dà ≤ deg/|F| ≤ k/p: è la base del
    bound di query algebrica (interrogazioni rivelano poco se i gradi sono bassi)."""
    points = list(product(range(p), repeat=k))
    agree = sum(
        1 for x in points
        if _eval_multilinear(coeffs_a, x, p) == _eval_multilinear(coeffs_b, x, p)
    )
    return agree / len(points)


# ════════════════════════════════════════════════════════════════════════════
# (3) NATURAL PROOFS — interfaccia SATURA, bound dal CALCOLO 𝒭 (= Modulo 15).
# ════════════════════════════════════════════════════════════════════════════
#
# L'osservatore legge TUTTA la truth table (2^n bit, informazione satura) ma è
# limitato nel CALCOLO. Δ ≤ ε viene dall'asse ortogonale. Riusiamo la misura
# esatta del Modulo 15: D0 = funzioni FACILI, D1 = funzioni DURE, classe C(ℓ=n, s).

def natural_proofs_advantage(s: int = 3) -> float:
    """Δ del distinguitore DURE-vs-FACILI con informazione satura (ℓ=n=3) e
    calcolo ≤ s gate. Riuso diretto del Modulo 15 (misura esatta su n=3)."""
    from pnp_lab.distinguishing import advantage_matrix, default_split

    m = advantage_matrix(default_split())
    return m.get(3, s).epsilon


# ════════════════════════════════════════════════════════════════════════════
# (4) PROOF COMPLEXITY — il template Δ ≤ ε FALLISCE. Lo dimostriamo.
# ════════════════════════════════════════════════════════════════════════════
#
# Tentativo di forzare il template: mondo = formula CNF; D1 = formule
# INSODDISFACIBILI (c'è qualcosa da certificare), D0 = formule SODDISFACIBILI (il
# mondo "falso"); osservatore = "esiste una refutazione di resolution di
# profondità ≤ t?". Misuriamo e mostriamo i due punti di rottura:
#   (a) SANITÀ ⇒ Pr_{D0}[decide=1] ≡ 0 per OGNI t: il lato D0 è identicamente
#       nullo, non c'è alcun ε bilaterale.
#   (b) la quantità che la proof complexity limita è min |Π| ∈ ℕ ∪ {∞} (lunghezza
#       di un TESTIMONE esistenziale), non un sup di differenza di medie ∈ [0,1].

Clause = FrozenSet[int]          # letterali: +v / −v, variabili 1..m


def _resolve(c1: Clause, c2: Clause) -> Optional[Clause]:
    """Risolvente di resolution: pivot UNICO; tautologie scartate (None)."""
    pivots = [lit for lit in c1 if -lit in c2]
    if len(pivots) != 1:
        return None
    p = pivots[0]
    r = (c1 - {p}) | (c2 - {-p})
    if any(-lit in r for lit in r):
        return None                                # tautologia ⇒ non utile
    return frozenset(r)


def refutation_depth(clauses: Sequence[Clause], max_depth: int = 16) -> Optional[int]:
    """Profondità della refutazione di resolution più corta (clausola vuota),
    o None se non refutabile entro max_depth. È un INTERO: una LUNGHEZZA."""
    known = set(frozenset(c) for c in clauses)
    if frozenset() in known:
        return 0
    for d in range(1, max_depth + 1):
        cur = list(known)
        new: List[Clause] = []
        for i in range(len(cur)):
            for j in range(i + 1, len(cur)):
                r = _resolve(cur[i], cur[j])
                if r is not None and r not in known:
                    known.add(r)
                    if len(r) == 0:
                        return d
                    new.append(r)
        if not new:
            break
    return None


def is_satisfiable(clauses: Sequence[Clause]) -> bool:
    """SAT per forza bruta (istanze minuscole): c'è un assegnamento che soddisfa?"""
    variables = sorted({abs(lit) for c in clauses for lit in c})
    for bits in product((0, 1), repeat=len(variables)):
        assign = {v: b for v, b in zip(variables, bits)}
        ok = True
        for c in clauses:
            if not any((lit > 0) == bool(assign[abs(lit)]) for lit in c):
                ok = False
                break
        if ok:
            return True
    return False


def proof_system_observer(t: int) -> Callable[[World], int]:
    """L'"osservatore" della proof complexity al budget t: accetta φ sse ha una
    refutazione di profondità ≤ t. (Il mondo è la tupla di clausole.)"""
    def decide(world: World) -> int:
        clauses = [frozenset(c) for c in world]
        d = refutation_depth(clauses, max_depth=t)
        return 1 if (d is not None and d <= t) else 0
    return decide


def proof_complexity_worlds() -> Tuple[Dist, Dist]:
    """(D0, D1): D0 = CNF SODDISFACIBILI (mondo falso), D1 = INSODDISFACIBILI."""
    # mondi rappresentati come tuple di tuple (hashable)
    def W(*clauses: Sequence[int]) -> World:
        return tuple(tuple(c) for c in clauses)

    unsat = [
        W((1,), (-1,)),                              # x ∧ ¬x
        W((1, 2), (1, -2), (-1, 2), (-1, -2)),       # tutte le 2-clausole su {x,y}
        W((1,), (-1, 2), (-2,)),                     # x, ¬x∨y, ¬y
    ]
    sat = [
        W((1,), (2,)),                               # x ∧ y
        W((1, 2), (-1, 2)),                          # (x∨y) ∧ (¬x∨y)
        W((1, -2), (-1, 2)),                         # x↔y
    ]
    d1: Dist = [(w, 1.0 / len(unsat)) for w in unsat]
    d0: Dist = [(w, 1.0 / len(sat)) for w in sat]
    return d0, d1


@dataclass
class ProofComplexityProbe:
    """Cosa succede quando si prova a misurare Δ per la proof complexity."""
    d0_acceptance: float          # Pr_{D0}[decide=1] — DEVE essere 0 (sanità)
    delta_by_budget: List[Tuple[int, float]]   # (t, Δ(t)) = Pr_{D1}[refut ≤ t]
    min_lengths: List[Optional[int]]           # min |Π| per ogni mondo di D1


def proof_complexity_probe(budgets: Sequence[int] = (0, 1, 2, 3, 4)) -> ProofComplexityProbe:
    """MISURA il fallimento del template Δ ≤ ε per la proof complexity.

    (a) il lato D0 (formule soddisfacibili) ha accettazione IDENTICAMENTE 0 a
        ogni budget — è la sanità del sistema di prova, NON un ε.
    (b) la quantità reale è min |Π| ∈ ℕ ∪ {∞} su D1, un TIPO diverso da Δ ∈ [0,1].
    """
    d0, d1 = proof_complexity_worlds()
    # (a) lato D0: per ogni budget, deve risultare 0 (lo verifichiamo sul budget
    # massimo, che domina; per sanità è 0 a ogni profondità).
    tmax = max(budgets)
    d0_acc = sum(p for w, p in d0 if proof_system_observer(tmax)(w))
    # (b) Δ(t) = Pr_{D1}[refutazione ≤ t] (il lato D1; l'altro lato è 0).
    delta = [(t, advantage(proof_system_observer(t), d0, d1)) for t in budgets]
    mins = [refutation_depth([frozenset(c) for c in w]) for w, _ in d1]
    return ProofComplexityProbe(d0_acceptance=d0_acc, delta_by_budget=delta,
                                min_lengths=mins)


# ════════════════════════════════════════════════════════════════════════════
# Sintesi unificata
# ════════════════════════════════════════════════════════════════════════════

def unified_summary() -> str:
    return "\n".join([
        "  Bounded Observer — le 4 barriere come Δ(𝒞; D0, D1) ≤ ε.",
        "  T = (𝒜 interfaccia | 𝒭 calcolo | t budget);  Δ = sup_T |Pr_D1 − Pr_D0|.",
        "    (1) relativizzazione : 𝒜 = query booleane     | 𝒭 illimitata | t = poly",
        "    (2) algebrizzazione  : 𝒜 = query algebriche    | 𝒭 illimitata | t = poly",
        "    (3) natural proofs   : 𝒜 = truth table satura  | 𝒭 limitata   | t = 2^n",
        "    (4) proof complexity : NON è un Δ ≤ ε (vedi sotto).",
        "  Onestà: misure ESATTE su istanze minuscole, non le barriere asintotiche;",
        "  per (2) si mostra l'arricchimento dell'interfaccia + Schwartz–Zippel, non",
        "  un lower bound algebrico asintotico. Niente tocca P vs NP.",
    ])
