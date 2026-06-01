"""Il protocollo sum-check — la tecnica algebrizzante, resa eseguibile.

PROBLEMA. Un verificatore vuole controllare l'affermazione

        H  =  Σ_{x ∈ {0,1}^n} g(x)

dove g è un polinomio su GF(p) di grado ≤ d in ciascuna variabile. La somma ha
2^n termini: il verificatore NON può calcolarla da solo. Eppure, parlando con un
prover (potente ma inaffidabile), si convince con UNA sola valutazione di g.

PROTOCOLLO (Lund–Fortnow–Karloff–Nisan 1990 — il motore di IP = PSPACE).
  Round i = 1..n: il prover invia il polinomio univariato

        g_i(X) = Σ_{x_{i+1..n} ∈ {0,1}}  g(r_1, …, r_{i-1}, X, x_{i+1}, …, x_n).

  Il verificatore controlla   g_i(0) + g_i(1) == (valore atteso)   — all'inizio H,
  poi g_{i-1}(r_{i-1}) — sceglie un punto casuale r_i ∈ GF(p) e aggiorna il valore
  atteso a g_i(r_i).
  Alla fine controlla   g(r_1, …, r_n) == (valore atteso)  con UNA query a g.

PERCHÉ È LA TECNICA CHE ROMPE LA RELATIVIZZAZIONE. Il verificatore non legge mai
i 2^n termini: interroga g in punti del CAMPO (estensione algebrica), non solo
sui vertici 0/1. È ciò che ha permesso a IP = PSPACE di NON relativizzare. La
barriera dell'algebrizzazione (Aaronson–Wigderson 2008) osserva poi che questa
tecnica funziona rispetto a ogni estensione polinomiale a basso grado di un
oracolo — e dimostra che, da sola, neppure essa basta a risolvere P vs NP.

Qui eseguiamo prover e verificatore per davvero, e verifichiamo:
  • COMPLETEZZA  — il prover onesto è sempre accettato;
  • SOUNDNESS    — un prover che mente su H viene smascherato (con prob. ≥ 1-d/p
                   per round), e lo si vede: l'inganno passa i controlli locali
                   ma fallisce la valutazione finale di g nel punto casuale.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field as dc_field
from itertools import product
from typing import Callable, List, Sequence, Tuple

from .field import Field

#: Un polinomio multivariato come funzione valutabile su GF(p)^n.
Polynomial = Callable[[Sequence[int]], int]


def sum_over_cube(g: Polynomial, n: int, field: Field) -> int:
    """Calcola direttamente Σ_{x ∈ {0,1}^n} g(x) (i 2^n termini: solo per piccoli n)."""
    total = 0
    for x in product((0, 1), repeat=n):
        total = field.add(total, g(x))
    return total


def lagrange_eval(field: Field, xs: Sequence[int], ys: Sequence[int], r: int) -> int:
    """Valuta in r il polinomio che interpola i punti (xs[j], ys[j]) su GF(p)."""
    total = 0
    for j in range(len(xs)):
        num = ys[j]
        den = 1
        for k in range(len(xs)):
            if k == j:
                continue
            num = field.mul(num, field.sub(r, xs[k]))
            den = field.mul(den, field.sub(xs[j], xs[k]))
        total = field.add(total, field.mul(num, field.inv(den)))
    return total


@dataclass
class SumcheckRound:
    var: int            # indice della variabile fissata in questo round
    samples: List[int]  # g_i valutato in 0, 1, …, d
    expected: int       # valore atteso prima del round
    local_ok: bool      # g_i(0) + g_i(1) == expected ?
    challenge: int      # r_i estratto a caso


@dataclass
class SumcheckResult:
    n: int
    degree: int
    claimed_sum: int
    accepted: bool
    rounds: List[SumcheckRound] = dc_field(default_factory=list)
    final_point: Tuple[int, ...] = ()
    final_check: bool = False
    oracle_queries: int = 0   # quante volte il verificatore ha valutato g

    @property
    def local_checks_passed(self) -> bool:
        return all(r.local_ok for r in self.rounds)


def run_sumcheck(
    g: Polynomial,
    n: int,
    field: Field,
    *,
    degree: int = 1,
    claimed_sum: int | None = None,
    rng: random.Random | None = None,
    cheat: bool = False,
) -> SumcheckResult:
    """Esegue prover + verificatore sul sum-check di g.

    Se ``claimed_sum`` è None usa la somma vera (prover onesto). Con ``cheat`` il
    prover afferma una somma sbagliata e falsifica ogni round per superare i
    controlli locali: lo scopo è mostrare che viene comunque smascherato alla
    valutazione finale.
    """
    if rng is None:
        rng = random.Random(0)
    true_sum = sum_over_cube(g, n, field)
    if claimed_sum is None:
        claimed_sum = field.add(true_sum, 1) if cheat else true_sum

    xs = list(range(degree + 1))
    expected = claimed_sum
    prefix: List[int] = []
    rounds: List[SumcheckRound] = []

    for i in range(n):
        expected_before = expected
        # --- prover: g_i(t) = somma di g sui suffissi booleani, fissato x_i=t ---
        m = n - i - 1
        ys = []
        for t in xs:
            s = 0
            for suffix in product((0, 1), repeat=m):
                point = tuple(prefix) + (t,) + suffix
                s = field.add(s, g(point))
            ys.append(s)

        # --- prover disonesto: forgia g_i(0) per far quadrare il controllo locale ---
        if cheat:
            ys = list(ys)
            ys[0] = field.sub(expected, ys[1])  # ⇒ ys[0] + ys[1] == expected

        # --- verificatore: controllo locale, poi sfida casuale ------------------
        local_ok = field.add(ys[0], ys[1]) == expected_before
        r = rng.randrange(field.p)
        expected = lagrange_eval(field, xs, ys, r)
        prefix.append(r)
        rounds.append(SumcheckRound(var=i, samples=list(ys), expected=expected_before, local_ok=local_ok, challenge=r))

    # --- verificatore: unica valutazione di g nel punto casuale finale ----------
    final_point = tuple(prefix)
    final_check = g(final_point) == expected
    accepted = all(rd.local_ok for rd in rounds) and final_check

    return SumcheckResult(
        n=n,
        degree=degree,
        claimed_sum=claimed_sum,
        accepted=accepted,
        rounds=rounds,
        final_point=final_point,
        final_check=final_check,
        oracle_queries=1,
    )
