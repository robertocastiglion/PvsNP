"""Restrizioni casuali ρ e funzioni booleane sotto restrizione.

Una restrizione ρ fissa ogni variabile a 0, a 1, oppure la lascia LIBERA (*).
Con probabilità p una variabile resta libera, altrimenti viene fissata a 0 o a 1
(ciascuno con prob. (1-p)/2). È l'arma dello switching lemma di Håstad: sotto
una restrizione casuale una DNF di larghezza piccola "si semplifica" quasi
sempre a un albero di decisione poco profondo.

Qui rappresentiamo:
  - una restrizione come tupla di valori in {0, 1, None}  (None = libera, '*');
  - una DNF come lista di termini, ogni termine una tupla di letterali
    (indice_variabile, valore_richiesto: bool);
  e forniamo la restrizione simbolica della DNF e la sua tabulazione sulle
  variabili libere (per misurarne poi la complessità).
"""

from __future__ import annotations

import random
from typing import Callable, List, Optional, Sequence, Tuple

#: ρ_i ∈ {0, 1, None}  (None ≡ '*', variabile libera)
Restriction = Tuple[Optional[int], ...]
#: letterale: la variabile `var` deve valere `want`
Literal = Tuple[int, bool]
Term = Tuple[Literal, ...]
DNF = List[Term]


def random_restriction(n: int, p: float, rng: random.Random) -> Restriction:
    """Restrizione casuale su n variabili: '*' con prob. p, altrimenti 0/1."""
    out: List[Optional[int]] = []
    half = (1.0 - p) / 2.0
    for _ in range(n):
        r = rng.random()
        if r < p:
            out.append(None)
        elif r < p + half:
            out.append(0)
        else:
            out.append(1)
    return tuple(out)


def free_vars(restriction: Restriction) -> List[int]:
    """Indici delle variabili lasciate libere da ρ."""
    return [i for i, v in enumerate(restriction) if v is None]


def restrict_dnf(dnf: DNF, restriction: Restriction) -> DNF:
    """Restrizione SIMBOLICA della DNF: mostra come 'si semplifica' sotto ρ.

    Convenzioni sul risultato:
      - ``[()]``  (un unico termine vuoto)  ≡ costante VERO;
      - ``[]``    (nessun termine)          ≡ costante FALSO.
    """
    new_terms: DNF = []
    for term in dnf:
        lits: List[Literal] = []
        alive = True
        for (v, want) in term:
            rv = restriction[v]
            if rv is None:
                lits.append((v, want))               # letterale su variabile libera
            elif (rv == 1) == want:
                continue                              # letterale soddisfatto → si toglie
            else:
                alive = False                         # letterale falso → il termine muore
                break
        if not alive:
            continue
        if not lits:
            return [()]                               # termine vuoto → DNF ≡ VERO
        new_terms.append(tuple(lits))
    return new_terms


def eval_dnf(dnf: DNF, assignment: Sequence[int]) -> int:
    """Valuta la DNF su un assegnamento completo (0/1) di tutte le variabili."""
    for term in dnf:
        if all((assignment[v] == 1) == want for (v, want) in term):
            return 1
    return 0


def parity_value(assignment: Sequence[int]) -> int:
    """Parità: XOR di tutte le variabili dell'assegnamento."""
    return sum(assignment) & 1


def tabulate(evaluator: Callable[[List[int]], int], restriction: Restriction) -> Tuple[Tuple[int, ...], List[int]]:
    """Tabella di verità della funzione ristretta, sulle SOLE variabili libere.

    Restituisce ``(table, free)`` con ``table`` di lunghezza 2^|free| (ordine
    big-endian: la i-esima variabile libera è il bit più significativo dopo le
    precedenti) e ``free`` la lista degli indici liberi.
    """
    free = free_vars(restriction)
    k = len(free)
    base = [0 if v is None else v for v in restriction]
    table: List[int] = []
    for a in range(1 << k):
        assign = list(base)
        for idx, var in enumerate(free):
            assign[var] = (a >> (k - 1 - idx)) & 1
        table.append(evaluator(assign))
    return tuple(table), free


def random_dnf(n: int, width: int, n_terms: int, rng: random.Random) -> DNF:
    """DNF casuale: ``n_terms`` termini, ciascuno con esattamente ``width``
    letterali su variabili distinte e polarità casuali."""
    terms: DNF = []
    for _ in range(n_terms):
        vs = rng.sample(range(n), width)
        terms.append(tuple((v, bool(rng.getrandbits(1))) for v in vs))
    return terms
