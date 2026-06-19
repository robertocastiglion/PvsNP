"""L'ostruzione della relativizzazione letta come OPERATORE DI LEVA cross-livello.

EN-first summary at the bottom (Honesty boundary).

PERCHÉ QUESTO MODULO.  ``separation.py`` ESEGUE già la diagonalizzazione di
Baker–Gill–Solovay (costruisce B con P^B ≠ NP^B e verifica che ogni macchina sbagli).
Ciò che NON misura è l'OPERATORE DI LEVA cross-livello — ed è lo strumento più recente
del lab, nato dalla Magnification Frontier appena chiusa (``docs/cross-level-survival-arc.md``):
là si è cercato per cicli di misurare un'amplificazione cross-livello fedele senza
riuscirci, perché la leva dell'oggetto era asintotica (n=7 = 2^128 fuori portata).

LA RELATIVIZZAZIONE È IL CROGIOLO.  La sua ostruzione è il più pulito divario di
conteggio della complessità ed è ESATTA E CON CRESCITA ESPLICITA: una macchina P^B
ispeziona ≤ q(n) = n^k delle 2^n stringhe di lunghezza n, quindi la headroom di
diagonalizzazione h(n,k) = 2^n − n^k è un intero esatto che cresce davvero.  Domanda
(falsificabile): misurata con la lente della leva, l'ostruzione è un genuino operatore
cross-livello — oppure collassa sul fatto totale singolo "depth(OR) = 2^n"?

COSA SI MISURA (tutto intero, esatto):
  * ``or_decision_tree_depth(n)`` = profondità dell'albero di decisione deterministico
    dell'OR su 2^n variabili (l'ALTEZZA dell'ostruzione).  È il meccanismo fedele di BGS:
    finché un lettore non ha letto tutte le 2^n stringhe, una stringa libera può ribaltare
    l'OR (lemma della riserva).  Verificato per costruzione generica su n≤3.
  * ``reservation`` (n, q): le stringhe libere 2^n − q e se un budget q può essere ingannato
    (q < 2^n) — il nucleo combinatorio della diagonalizzazione.
  * ``headroom`` h(n,k) = 2^n − n^k e ``break_even_length`` n*(k) = min n con 2^n > n^k:
    la SCALA della leva (lo "staircase" che la Magnification Frontier non trovò).
  * ``freshness_schedule``: la pianificazione ONLINE delle lunghezze attraverso gli stadi
    (il candidato NON-collassante: un oggetto cross-stadio che la depth(OR) di una singola
    funzione non vede), strumentando ``build_separating_oracle``.

Nessun claim su P vs NP.  BGS è CITATO; qui si misura un operatore esatto sulla
costruzione già eseguibile.  Vedi Honesty boundary in fondo.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Sequence, Tuple

from .separation import OracleMachine, EXAMPLE_MACHINES, build_separating_oracle


# ── l'altezza dell'ostruzione: depth(OR) su 2^n variabili ──────────────────

def _dt_depth(values: Tuple[int, ...], m: int) -> int:
    """Profondità dell'albero di decisione deterministico della funzione booleana data
    dalla sua tavola di verità ``values`` (lunghezza 2^m, indicizzata dall'assegnazione
    interpretata in binario con la variabile 0 nel bit meno significativo).

    Ricorsione standard memoizzata su (maschera-fissate, valori-fissati): f ristretta
    costante ⇒ 0; altrimenti min su una variabile libera di 1 + max dei due rami.  Esatta;
    usata per VERIFICARE (non assumere) che depth(OR_m) = m su m piccolo."""
    memo: dict = {}

    def consistent(fixed_mask: int, fixed_val: int) -> List[int]:
        free = [i for i in range(m) if not (fixed_mask >> i) & 1]
        out = []
        for combo in range(1 << len(free)):
            idx = fixed_val
            for b, i in enumerate(free):
                if (combo >> b) & 1:
                    idx |= (1 << i)
            out.append(values[idx])
        return out

    def rec(fixed_mask: int, fixed_val: int) -> int:
        key = (fixed_mask, fixed_val)
        if key in memo:
            return memo[key]
        vals = consistent(fixed_mask, fixed_val)
        if all(v == vals[0] for v in vals):
            memo[key] = 0
            return 0
        best = None
        for i in range(m):
            if (fixed_mask >> i) & 1:
                continue
            nm = fixed_mask | (1 << i)
            d = 1 + max(rec(nm, fixed_val), rec(nm, fixed_val | (1 << i)))
            if best is None or d < best:
                best = d
        memo[key] = best
        return best

    return rec(0, 0)


def _or_truth_table(m: int) -> Tuple[int, ...]:
    """Tavola di verità dell'OR su m variabili: 0 solo per l'input tutto-zero."""
    return tuple(0 if k == 0 else 1 for k in range(1 << m))


def or_decision_tree_depth(n: int, verify_max_vars: int = 8) -> int:
    """Altezza dell'ostruzione al livello n: la profondità DT dell'OR su m = 2^n variabili.

    Vale esattamente m = 2^n (lemma della riserva).  Per m ≤ ``verify_max_vars`` lo
    VERIFICA con la ricorsione generica ``_dt_depth`` (nessuna assunzione); oltre, ritorna
    2^n citando il fatto noto depth(OR_m) = m (la verifica esplode come 3^m)."""
    m = 1 << n
    if m <= verify_max_vars:
        d = _dt_depth(_or_truth_table(m), m)
        assert d == m, f"depth(OR_{m}) = {d} != {m} (atteso)"
    return m


# ── il nucleo combinatorio: il lemma della riserva ─────────────────────────

@dataclass
class Reservation:
    n: int
    q: int                       # budget di query alla lunghezza n
    free_strings: int            # 2^n − q : stringhe non interrogabili
    can_be_fooled: bool          # q < 2^n : esiste una stringa libera da ribaltare


def reservation(n: int, q: int) -> Reservation:
    """Il nucleo esatto della diagonalizzazione: con budget q alla lunghezza n restano
    ``2^n − q`` stringhe libere e la macchina può essere ingannata sse ``q < 2^n``."""
    total = 1 << n
    return Reservation(n=n, q=q, free_strings=total - q, can_be_fooled=q < total)


# ── la scala della leva: headroom e break-even ─────────────────────────────

def headroom(n: int, k: int) -> int:
    """h(n,k) = 2^n − n^k : la headroom di diagonalizzazione per un budget poly q(n)=n^k.
    Positiva ⇒ la macchina di grado k è sconfiggibile alla lunghezza n."""
    return (1 << n) - n ** k


def break_even_length(k: int, n_max: int = 200) -> int:
    """n*(k) = il livello del SORPASSO PERMANENTE: il più piccolo n tale che 2^{n'} > n'^k
    per ogni n' ≥ n.  (2^n > n^k vale banalmente già a n=1, poi cede per 2≤n<n*; n*(k) è il
    gradino oltre cui l'esponenziale batte definitivamente il polinomio.)  Lo si calcola
    come 1 + l'ultimo n con 2^n ≤ n^k.  k=1 → 1, k=2 → 5, k=3 → 10."""
    last_fail = 0
    for n in range(1, n_max + 1):
        if (1 << n) <= n ** k:
            last_fail = n
    return last_fail + 1


@dataclass
class LeverageRow:
    n: int
    slice_size: int              # 2^n
    obstruction_height: int      # depth(OR) = 2^n
    headroom_k: Tuple[int, ...]  # h(n,k) per i k richiesti


def leverage_staircase(ns: Sequence[int] = (1, 2, 3, 4),
                       ks: Sequence[int] = (1, 2, 3)) -> List[LeverageRow]:
    """La tabella dell'operatore di leva: per ogni livello n l'altezza dell'ostruzione
    (2^n) e la headroom h(n,k) per ciascun grado poly k.  La crescita di queste colonne
    è l'operatore di amplificazione che la Magnification Frontier non poté misurare."""
    rows: List[LeverageRow] = []
    for n in ns:
        rows.append(LeverageRow(
            n=n, slice_size=1 << n,
            obstruction_height=or_decision_tree_depth(n),
            headroom_k=tuple(headroom(n, k) for k in ks)))
    return rows


# ── il candidato NON-collassante: la pianificazione online delle lunghezze ──

@dataclass
class FreshnessSchedule:
    lengths: Tuple[int, ...]         # n_i scelto a ogni stadio dalla diagonalizzazione
    greedy_lengths: Tuple[int, ...]  # n_i ricostruito dall'aritmetica greedy dei budget
    matches_greedy: bool             # la pianificazione È l'aritmetica greedy?
    all_defeated: bool               # sanity: ogni macchina sconfitta (riuso separation)


def _greedy_lengths(machines: Sequence[OracleMachine], start_length: int = 1) -> Tuple[int, ...]:
    """Ricostruisce le lunghezze SOLO dall'aritmetica greedy dei budget: a ogni stadio
    n = min lunghezza ≥ (reach precedente) con budget(n) < 2^n; la reach avanza di max(n,
    'lunghezza massima interrogabile').  Per le macchine di esempio la reach di query è
    limitata dal budget come |query| ≤ budget alla lunghezza n, ma la pianificazione di
    ``separation`` usa max_query_length OSSERVATA; qui usiamo il limite n (le macchine di
    esempio non interrogano oltre la lunghezza n), così il confronto è onesto."""
    out: List[int] = []
    nxt = start_length
    for m in machines:
        n = nxt
        while m.budget(n) >= (1 << n):
            n += 1
        out.append(n)
        nxt = n + 1                      # le macchine di esempio non interrogano oltre n
    return tuple(out)


def freshness_schedule(machines: Sequence[OracleMachine] = tuple(EXAMPLE_MACHINES),
                       start_length: int = 1) -> FreshnessSchedule:
    """La pianificazione ONLINE delle lunghezze attraverso gli stadi della
    diagonalizzazione (il candidato cross-stadio che la depth(OR) di una singola funzione
    non vede), confrontata con l'aritmetica greedy.  Riusa ``build_separating_oracle``."""
    res = build_separating_oracle(machines, start_length=start_length)
    actual = tuple(s.length for s in res.stages)
    greedy = _greedy_lengths(machines, start_length=start_length)
    return FreshnessSchedule(
        lengths=actual, greedy_lengths=greedy,
        matches_greedy=(actual == greedy),
        all_defeated=res.all_machines_defeated)


# ── CYCLE 2: fidelity stress-test against adaptive cross-length machines ────
#
# EXAMPLE_MACHINES (separation.py) are all simple and never query above their input
# length n.  Cycle 2 stresses the EXISTING BGS construction against a strictly harder
# class — ADAPTIVE (next query depends on prior answers) and CROSS-LENGTH (queries
# strings longer/shorter than n) machines — to test two things:
#   (FIDELITY) does build_separating_oracle still defeat them, and does the STABILITY
#     theorem hold (re-running each machine against the FINAL B still defeats it — i.e.
#     later stages' plants never perturb an earlier machine, the freshness invariant)?
#   (LEVERAGE) is the freshness length-schedule now EXECUTION-DEPENDENT (reach varies
#     with the oracle built so far), or still closed-form budget arithmetic?

def _binary(k: int, n: int) -> str:
    return format(k, "b").zfill(n)


def make_probe_long(reach_factor: int = 2, per_len: int = 2) -> OracleMachine:
    """Macchina CROSS-LUNGHEZZA non adattiva: su 1^n interroga ``per_len`` stringhe a ogni
    lunghezza da n a reach_factor*n e accetta se ne trova una in B.  Reach = reach_factor*n
    (oltre n) ⇒ forza la pianificazione a saltare; budget alla lunghezza n = per_len."""
    def decide(n: int, query: QueryFn) -> bool:
        for L in range(n, reach_factor * n + 1):
            for k in range(min(per_len, 1 << L)):
                if query(_binary(k, L)):
                    return True
        return False
    return OracleMachine(name=f"probe_long_x{reach_factor}", decide=decide,
                         budget=lambda n: per_len,
                         description="cross-length: interroga fino a reach_factor*n")


def make_adaptive(per_len: int = 3) -> OracleMachine:
    """Macchina ADATTIVA: la prossima query dipende dalla risposta precedente.  Su 1^n
    interroga 0^n; se in B prova 0^{n}1.. variando, altrimenti scende; reach <= n
    (resta alla lunghezza n) ma il pattern di query dipende dall'oracolo."""
    def decide(n: int, query: QueryFn) -> bool:
        k = 0
        for _ in range(per_len):
            s = _binary(k % (1 << n), n)
            if query(s):
                return True
            k = k * 2 + 1            # prossima stringa scelta in base al fallimento
        return False
    return OracleMachine(name="adaptive", decide=decide, budget=lambda n: per_len,
                         description="adattiva alla lunghezza n")


def make_backscan(look_back: int = 2, per_len: int = 1) -> OracleMachine:
    """Macchina che interroga stringhe PIÙ CORTE (lunghezza n-1, n-2, ...), dove stadi
    PRECEDENTI potrebbero aver piantato stringhe ⇒ la sua risposta (e reach) dipende dal B
    già costruito.  Non interroga la lunghezza n ⇒ reach < n, niente salto in avanti."""
    def decide(n: int, query: QueryFn) -> bool:
        for d in range(1, look_back + 1):
            L = n - d
            if L < 1:
                break
            for k in range(min(per_len, 1 << L)):
                if query(_binary(k, L)):
                    return True
        return False
    return OracleMachine(name="backscan", decide=decide, budget=lambda n: 0,
                         description="interroga stringhe più corte (plant precedenti)")


#: Classe più dura di EXAMPLE_MACHINES: adattive + cross-lunghezza.
HARD_MACHINES: List[OracleMachine] = [
    make_probe_long(2),
    make_adaptive(),
    make_backscan(),
    make_probe_long(3),
]


@dataclass
class FidelityResult:
    all_defeated_in_construction: bool   # ogni macchina sbaglia durante la costruzione
    stable_under_final_B: bool           # re-eseguita contro il B FINALE, sbaglia ancora
    schedule: Tuple[int, ...]            # lunghezze scelte attraverso gli stadi
    reaches: Tuple[int, ...]             # max_query_length realizzato per stadio
    execution_dependent_reach: bool      # qualche reach != reach a oracolo VUOTO?


def _empty_oracle_reach(machine: OracleMachine, n: int) -> int:
    """La reach (massima lunghezza interrogata) della macchina su 1^n con oracolo VUOTO."""
    reach = 0
    def q(s: str) -> bool:
        nonlocal reach
        reach = max(reach, len(s))
        return False
    machine.decide(n, q)
    return reach


def fidelity_stress_test(machines: Sequence[OracleMachine] = tuple(HARD_MACHINES),
                         start_length: int = 1) -> FidelityResult:
    """Cycle 2 — stress-test della costruzione BGS esistente contro ``machines`` dure.

    FEDELTÀ: ogni macchina è sconfitta durante la costruzione, e — ri-eseguendola contro il
    B FINALE — resta sconfitta (teorema di stabilità: la freshness impedisce agli stadi
    successivi di perturbare le macchine precedenti).  LEVA: la reach realizzata per stadio
    è confrontata con la reach a oracolo vuoto; se differiscono la pianificazione è
    esecuzione-dipendente (non aritmetica chiusa)."""
    res = build_separating_oracle(machines, start_length=start_length)
    all_def = res.all_machines_defeated
    # stabilità: ri-esegui ogni macchina contro il B finale, deve ancora sbagliare
    stable = True
    reaches: List[int] = []
    exec_dep = False
    for machine, stage in zip(machines, res.stages):
        reach = 0
        def q(s: str, _r=None) -> bool:
            nonlocal reach
            reach = max(reach, len(s))
            return s in res.B
        accepts_final = bool(machine.decide(stage.length, q))
        lb_final = any(len(s) == stage.length for s in res.B)
        if accepts_final == lb_final:      # non più sbagliata ⇒ instabile
            stable = False
        reaches.append(reach)
        if reach != _empty_oracle_reach(machine, stage.length):
            exec_dep = True
    return FidelityResult(
        all_defeated_in_construction=all_def,
        stable_under_final_B=stable,
        schedule=tuple(s.length for s in res.stages),
        reaches=tuple(reaches),
        execution_dependent_reach=exec_dep)


def honesty_note() -> str:
    """One-paragraph honesty boundary (string; no asymptotic / P-vs-NP claim)."""
    return (
        "COMPUTED exactly: depth(OR) on 2^n variables (verified by a generic decision-tree "
        "recursion for n<=3, where 2^n<=8), the reservation counts 2^n-q, the headroom "
        "h(n,k)=2^n-n^k, the break-even n*(k), and the freshness length-schedule (reusing "
        "the verified BGS diagonalization in separation.py).  CITED, never re-proved: "
        "Baker-Gill-Solovay 1975 (the barrier itself) and depth(OR_m)=m for m>8 (textbook; "
        "the generic verification explodes as 3^m).  This measures whether the relativization "
        "obstruction, read as a cross-level leverage operator, is genuine or collapses to the "
        "single total fact depth(OR)=2^n.  No separation, no P vs NP claim."
    )
