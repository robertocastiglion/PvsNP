"""Oracolo A con P^A = NP^A, illustrato con un oracolo PSPACE-completo (TQBF).

Teorema (parte "collasso" di Baker–Gill–Solovay). Se A è PSPACE-completo
(per esempio A = TQBF, l'insieme delle formule booleane quantificate vere),
allora
        P^A = NP^A = PSPACE.
Intuizione: un oracolo PSPACE-completo è così potente che la capacità di
"indovinare" di NP non aggiunge nulla — sia P^A sia NP^A possono risolvere
qualunque problema in PSPACE, e nessuno dei due va oltre, perché una macchina
polinomiale (anche nondeterministica) con oracolo in PSPACE resta dentro
PSPACE.

Cosa è ESEGUIBILE qui (e cosa no, onestamente):
  - L'uguaglianza P^A = NP^A è un TEOREMA su classi di complessità: non è una
    cosa che "si calcola".
  - Ma possiamo rendere concreta la direzione cruciale NP^A ⊆ P^A su un
    esempio: SAT è in NP, e con l'oracolo TQBF lo si decide in modo
    DETERMINISTICO con UNA SOLA query (φ è soddisfacibile ⇔ ∃x. φ(x) è una
    QBF vera). Il nondeterminismo sparisce: è il cuore del collasso.

Rappresentazione delle formule (mini-AST):
  proposizionali:  ('const', bool) | ('var', nome) | ('not', f)
                   ('and', f1, f2, …) | ('or', f1, f2, …)
  quantificate:    ('exists', var, f) | ('forall', var, f)
"""

from __future__ import annotations

from dataclasses import dataclass


def _eval_prop(expr, assign: dict[str, bool]) -> bool:
    """Valuta una formula proposizionale (senza quantificatori) su un assegnamento."""
    tag = expr[0]
    if tag == "const":
        return bool(expr[1])
    if tag == "var":
        return assign[expr[1]]
    if tag == "not":
        return not _eval_prop(expr[1], assign)
    if tag == "and":
        return all(_eval_prop(e, assign) for e in expr[1:])
    if tag == "or":
        return any(_eval_prop(e, assign) for e in expr[1:])
    raise ValueError(f"operatore proposizionale sconosciuto: {tag!r}")


def eval_qbf(formula, assign: dict[str, bool] | None = None) -> bool:
    """Valuta una formula booleana quantificata (QBF).

    Usa spazio polinomiale (profondità di ricorsione = numero di variabili) ma
    tempo esponenziale: è esattamente il profilo di PSPACE. L'oracolo è
    onnipotente entro PSPACE, quindi questo va benissimo come modello di A.
    """
    assign = dict(assign or {})
    tag = formula[0]
    if tag in ("exists", "forall"):
        _, var, sub = formula
        outcomes = []
        for value in (False, True):
            assign[var] = value
            outcomes.append(eval_qbf(sub, assign))
        del assign[var]
        return any(outcomes) if tag == "exists" else all(outcomes)
    return _eval_prop(formula, assign)


def tqbf_oracle(formula) -> bool:
    """L'oracolo A = TQBF: dice se la QBF data è VERA. (PSPACE-completo.)"""
    return eval_qbf(formula)


# ---------------------------------------------------------------------------
# Dimostrazione concreta: NP ⊆ P^TQBF su SAT, con UNA sola query
# ---------------------------------------------------------------------------

# Un letterale è (nome_variabile, polarità):  ("x1", True) = x1,  ("x1", False) = ¬x1
# Una clausola è una lista di letterali (in OR); una CNF è una lista di clausole (in AND).
Literal = tuple
Clause = list
CNF = list


def cnf_to_qbf(cnf: CNF, variables: list[str]):
    """Trasforma una CNF in la QBF chiusa  ∃v1 ∃v2 … (clausola1 ∧ clausola2 ∧ …).

    Questa QBF è vera esattamente quando la CNF è soddisfacibile.
    """
    clause_exprs = []
    for clause in cnf:
        lits = []
        for name, polarity in clause:
            lits.append(("var", name) if polarity else ("not", ("var", name)))
        clause_exprs.append(("or", *lits) if lits else ("const", False))
    body = ("and", *clause_exprs) if clause_exprs else ("const", True)
    formula = body
    for var in reversed(variables):
        formula = ("exists", var, formula)
    return formula


@dataclass
class SatResult:
    satisfiable: bool
    oracle_queries: int
    qbf: tuple

    def __str__(self) -> str:
        return (
            f"SAT {'SODDISFACIBILE' if self.satisfiable else 'NON soddisfacibile'} "
            f"deciso con {self.oracle_queries} query all'oracolo TQBF "
            f"(deterministico, polinomiale)"
        )


def solve_sat_via_oracle(cnf: CNF, variables: list[str]) -> SatResult:
    """Decide SAT in modo DETERMINISTICO con una sola query all'oracolo TQBF.

    Mostra concretamente che SAT ∈ P^TQBF: il "guess" nondeterministico di NP
    viene assorbito dentro la QBF e risolto dall'oracolo. È la direzione
    NP^A ⊆ P^A resa eseguibile su un caso.
    """
    qbf = cnf_to_qbf(cnf, variables)
    answer = tqbf_oracle(qbf)  # UNA query
    return SatResult(satisfiable=answer, oracle_queries=1, qbf=qbf)
