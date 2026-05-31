"""Oracolo separatore B con P^B ≠ NP^B (costruzione di Baker–Gill–Solovay).

Idea. Per QUALSIASI oracolo B definiamo il linguaggio

    L_B = { 1^n : esiste una stringa x di lunghezza n con x ∈ B }.

Osservazione 1 — L_B è SEMPRE in NP^B: su input 1^n una macchina
nondeterministica "indovina" una stringa x di lunghezza n e con UNA query
all'oracolo verifica se x ∈ B. Tempo polinomiale.

Osservazione 2 — possiamo COSTRUIRE B in modo che L_B NON sia in P^B.
Per diagonalizzazione contro l'enumerazione delle macchine deterministiche
polinomiali con oracolo M_0, M_1, M_2, …:

  Allo stadio i scegliamo una lunghezza fresca n (più grande di qualunque
  stringa interrogabile dagli stadi precedenti) e abbastanza grande che il
  budget di query p_i(n) sia < 2^n. Simuliamo M_i^B(1^n) rispondendo "no" a
  ogni query di lunghezza n (al momento B è vuoto a quella lunghezza). Poiché
  M_i fa meno di 2^n query, esiste una stringa di lunghezza n che NON ha
  interrogato.
    - se M_i ACCETTA 1^n → non mettiamo NULLA di lunghezza n in B
      ⇒ L_B(1^n) = falso, ma M_i ha accettato: M_i sbaglia.
    - se M_i RIFIUTA 1^n → mettiamo in B una stringa di lunghezza n NON
      interrogata ⇒ L_B(1^n) = vero, ma M_i ha rifiutato: M_i sbaglia.
      (La stringa aggiunta non era stata interrogata, quindi l'esecuzione di
       M_i non cambia.)

In entrambi i casi M_i non decide L_B. Quindi L_B ∉ P^B mentre L_B ∈ NP^B,
cioè P^B ≠ NP^B.

Questo modulo implementa la diagonalizzazione su un insieme finito ma
rappresentativo di macchine e VERIFICA, eseguendole sull'oracolo finale, che
ciascuna sbagli su L_B.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Sequence

#: Una funzione-query dell'oracolo: data una stringa binaria, dice se è in B.
QueryFn = Callable[[str], bool]


@dataclass
class OracleMachine:
    """Modello di una macchina deterministica polinomiale con oracolo.

    ``decide(n, query)`` riceve l'input 1^n (rappresentato dall'intero n) e una
    funzione ``query`` per interrogare l'oracolo; restituisce True (accetta) o
    False (rifiuta). ``budget(n)`` è il numero massimo di query su input 1^n
    (un qualunque polinomio: è ciò che rende la macchina "polinomiale").
    """

    name: str
    decide: Callable[[int, QueryFn], bool]
    budget: Callable[[int], int]
    description: str = ""


def language_L_B(B: set[str], n: int) -> bool:
    """L_B(1^n): vero se B contiene almeno una stringa di lunghezza n."""
    return any(len(s) == n for s in B)


def _binary(k: int, n: int) -> str:
    """La k-esima stringa binaria di lunghezza n (k in 0..2^n-1)."""
    return format(k, "b").zfill(n)


def _first_unqueried(queried: set[str], n: int) -> str:
    """Prima stringa di lunghezza n non presente in ``queried``.

    Esiste sempre quando |queried ∩ {len n}| < 2^n, garantito dal budget.
    """
    for k in range(1 << n):
        s = _binary(k, n)
        if s not in queried:
            return s
    raise RuntimeError("nessuna stringa libera: budget >= 2^n (non dovrebbe accadere)")


@dataclass
class SeparationStage:
    """Esito di un singolo stadio della diagonalizzazione (una macchina)."""

    machine: str
    length: int                # n scelto per questo stadio
    machine_accepts: bool      # risposta di M_i su 1^n durante la simulazione
    queries_at_length: int     # quante stringhe di lunghezza n ha interrogato
    budget_at_length: int      # budget p_i(n) (< 2^n)
    added_to_B: str | None     # stringa aggiunta a B (se la macchina rifiutava)
    L_B_value: bool            # valore vero di L_B(1^n) dopo la decisione
    machine_is_wrong: bool     # machine_accepts != L_B_value ?


@dataclass
class SeparationResult:
    B: set[str]
    stages: list[SeparationStage] = field(default_factory=list)

    @property
    def all_machines_defeated(self) -> bool:
        return all(s.machine_is_wrong for s in self.stages)

    def __str__(self) -> str:
        lines = [
            "=" * 72,
            "  ORACOLO SEPARATORE B  —  costruzione di P^B ≠ NP^B (Baker–Gill–Solovay)",
            "=" * 72,
            "  L_B = { 1^n : esiste x di lunghezza n con x ∈ B }   (∈ NP^B per ogni B)",
            "  Diagonalizziamo contro le macchine P^B per renderlo NON in P^B.",
            "",
        ]
        for i, s in enumerate(self.stages):
            verdict = "SCONFITTA" if s.machine_is_wrong else "NON sconfitta"
            decision = (
                f"aggiunge {s.added_to_B!r} a B" if s.added_to_B is not None
                else "non aggiunge nulla a B"
            )
            lines += [
                f"  Stadio {i}: macchina {s.machine!r}",
                f"    lunghezza scelta n = {s.length}   "
                f"(budget query = {s.budget_at_length} < 2^{s.length} = {1 << s.length})",
                f"    M({s.machine}) su 1^{s.length}: "
                f"{'ACCETTA' if s.machine_accepts else 'RIFIUTA'}  "
                f"(ha interrogato {s.queries_at_length} stringhe di lunghezza {s.length})",
                f"    diagonalizzazione: {decision}  ⇒  L_B(1^{s.length}) = "
                f"{'VERO' if s.L_B_value else 'FALSO'}",
                f"    {verdict}: la macchina dà la risposta sbagliata su L_B.",
                "",
            ]
        lines += [
            f"  B finale = {sorted(self.B)}",
            f"  Tutte le macchine P^B sconfitte? "
            f"{'SÌ → L_B ∉ P^B, ma L_B ∈ NP^B ⇒ P^B ≠ NP^B' if self.all_machines_defeated else 'NO'}",
            "=" * 72,
        ]
        return "\n".join(lines)


def build_separating_oracle(
    machines: Sequence[OracleMachine],
    *,
    start_length: int = 1,
) -> SeparationResult:
    """Costruisce B diagonalizzando contro ``machines`` e verifica ogni stadio.

    Restituisce un :class:`SeparationResult` con l'oracolo finale e il log
    dettagliato di ogni stadio.
    """
    B: set[str] = set()
    stages: list[SeparationStage] = []
    next_min_length = start_length

    for machine in machines:
        # 1) scegli n: fresco e con budget < 2^n
        n = next_min_length
        while machine.budget(n) >= (1 << n):
            n += 1

        # 2) simula M^B(1^n); B non ha (ancora) stringhe di lunghezza n
        queried: set[str] = set()
        max_query_length = 0

        def query(s: str, _q=queried) -> bool:
            nonlocal max_query_length
            _q.add(s)
            if len(s) > max_query_length:
                max_query_length = len(s)
            return s in B

        accepts = bool(machine.decide(n, query))
        queried_at_n = {s for s in queried if len(s) == n}

        # 3) diagonalizza: contraddici la risposta della macchina
        if accepts:
            added = None  # niente di lunghezza n in B ⇒ L_B(1^n) = falso
        else:
            added = _first_unqueried(queried_at_n, n)  # ⇒ L_B(1^n) = vero
            B.add(added)

        lb_value = language_L_B(B, n)
        stages.append(
            SeparationStage(
                machine=machine.name,
                length=n,
                machine_accepts=accepts,
                queries_at_length=len(queried_at_n),
                budget_at_length=machine.budget(n),
                added_to_B=added,
                L_B_value=lb_value,
                machine_is_wrong=(accepts != lb_value),
            )
        )

        # 4) la prossima lunghezza deve superare ogni stringa interrogabile ora,
        #    così future aggiunte a B non perturbano questa macchina.
        next_min_length = max(n + 1, max_query_length + 1)

    return SeparationResult(B=B, stages=stages)


# ---------------------------------------------------------------------------
# Macchine P^B di esempio (strategie deterministiche che provano a decidere L_B)
# ---------------------------------------------------------------------------

def _m_always_accept(n: int, query: QueryFn) -> bool:
    return True


def _m_always_reject(n: int, query: QueryFn) -> bool:
    return False


def _m_query_zeros(n: int, query: QueryFn) -> bool:
    # interroga solo la stringa 0^n e accetta se è in B
    return query("0" * n)


def _m_query_prefix(n: int, query: QueryFn) -> bool:
    # interroga le prime n^2 stringhe di lunghezza n (entro budget) e accetta
    # se almeno una è in B — un tentativo "ragionevole" ma limitato dal budget
    limit = min(n * n, (1 << n))
    for k in range(limit):
        if query(_binary(k, n)):
            return True
    return False


#: Insieme rappresentativo di macchine contro cui diagonalizzare.
EXAMPLE_MACHINES: list[OracleMachine] = [
    OracleMachine(
        name="always_accept",
        decide=_m_always_accept,
        budget=lambda n: 0,
        description="accetta sempre (0 query)",
    ),
    OracleMachine(
        name="always_reject",
        decide=_m_always_reject,
        budget=lambda n: 0,
        description="rifiuta sempre (0 query)",
    ),
    OracleMachine(
        name="query_zeros",
        decide=_m_query_zeros,
        budget=lambda n: 1,
        description="interroga solo 0^n",
    ),
    OracleMachine(
        name="query_prefix_n2",
        decide=_m_query_prefix,
        budget=lambda n: n * n,
        description="interroga le prime n^2 stringhe di lunghezza n",
    ),
]
