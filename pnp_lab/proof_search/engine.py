"""Motore di riscrittura equazionale — un mini-prover SOUND e autosufficiente.

È il "verificatore" del Modulo 11: niente magia, niente rete. Un obiettivo è
un'uguaglianza `lhs = rhs`; una "tattica" applica una regola di riscrittura
(un lemma) a un sottotermine; una prova è la catena di riscritture che porta
`lhs` a coincidere con `rhs`. Ogni passo è ricontrollabile, quindi qualunque
prova trovata dalla ricerca è verificata per costruzione.

Usiamo come teoria-giocattolo l'algebra dei gruppi (identità, inverso, prodotto):
piccola ma reale, con teoremi che richiedono catene di 1–3 riscritture.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Tuple, Union


@dataclass(frozen=True)
class Var:
    """Variabile di pattern (compare solo nelle regole, non negli obiettivi)."""
    name: str


@dataclass(frozen=True)
class Term:
    """Termine: un simbolo `op` applicato ad argomenti (le costanti hanno arità 0)."""
    op: str
    args: Tuple["Pattern", ...] = ()


Pattern = Union[Var, Term]


# ── stampa leggibile ──────────────────────────────────────────────────────

def show(t: Pattern) -> str:
    if isinstance(t, Var):
        return t.name
    if not t.args:
        return t.op
    return f"{t.op}(" + ", ".join(show(a) for a in t.args) + ")"


# ── pattern matching (one-way) e sostituzione ─────────────────────────────

def match(pat: Pattern, term: Term, subst: Optional[Dict[str, Term]] = None) -> Optional[Dict[str, Term]]:
    """Match unidirezionale di `pat` (con variabili) contro `term` (senza)."""
    subst = {} if subst is None else subst
    if isinstance(pat, Var):
        if pat.name in subst:
            return subst if subst[pat.name] == term else None
        s = dict(subst)
        s[pat.name] = term
        return s
    if not isinstance(term, Term) or term.op != pat.op or len(term.args) != len(pat.args):
        return None
    for p, a in zip(pat.args, term.args):
        subst = match(p, a, subst)
        if subst is None:
            return None
    return subst


def instantiate(pat: Pattern, subst: Dict[str, Term]) -> Term:
    """Applica una sostituzione a un pattern, producendo un termine concreto."""
    if isinstance(pat, Var):
        return subst[pat.name]
    return Term(pat.op, tuple(instantiate(a, subst) for a in pat.args))


def variables(pat: Pattern) -> set:
    if isinstance(pat, Var):
        return {pat.name}
    out: set = set()
    for a in pat.args:
        out |= variables(a)
    return out


# ── posizioni e sostituzione di sottotermini ──────────────────────────────

def positions(term: Term) -> Iterator[Tuple[int, ...]]:
    """Tutte le posizioni (cammini) nel termine, radice inclusa."""
    yield ()
    for i, a in enumerate(term.args):
        if isinstance(a, Term):
            for p in positions(a):
                yield (i,) + p


def subterm_at(term: Term, pos: Tuple[int, ...]) -> Term:
    for i in pos:
        term = term.args[i]  # type: ignore[assignment]
    return term


def replace_at(term: Term, pos: Tuple[int, ...], new: Term) -> Term:
    if not pos:
        return new
    i, rest = pos[0], pos[1:]
    new_args = list(term.args)
    new_args[i] = replace_at(term.args[i], rest, new)  # type: ignore[arg-type]
    return Term(term.op, tuple(new_args))


# ── regole e tattiche ─────────────────────────────────────────────────────

@dataclass(frozen=True)
class Rule:
    name: str
    lhs: Pattern
    rhs: Pattern


@dataclass(frozen=True)
class Tactic:
    """Un passo: applica `rule` (in avanti o all'indietro) alla posizione `pos`."""
    rule: str
    forward: bool
    pos: Tuple[int, ...]

    def show(self) -> str:
        arrow = "→" if self.forward else "←"
        return f"rw[{self.rule} {arrow}] @{self.pos if self.pos else 'root'}"


def _apply_oriented(lhs: Pattern, rhs: Pattern, term: Term, pos: Tuple[int, ...]) -> Optional[Term]:
    sub = subterm_at(term, pos)
    s = match(lhs, sub, {})
    if s is None:
        return None
    if not variables(rhs).issubset(s.keys()):
        return None  # la riscrittura introdurrebbe variabili libere
    return replace_at(term, pos, instantiate(rhs, s))


def apply_tactic(rules: Dict[str, Rule], term: Term, tac: Tactic) -> Optional[Term]:
    r = rules[tac.rule]
    if tac.forward:
        return _apply_oriented(r.lhs, r.rhs, term, tac.pos)
    return _apply_oriented(r.rhs, r.lhs, term, tac.pos)


def applicable_tactics(rules: Dict[str, Rule], term: Term, *, allow_reverse: bool = True) -> List[Tactic]:
    """Tutte le tattiche che si possono applicare al termine corrente."""
    out: List[Tactic] = []
    poss = list(positions(term))
    for name, r in rules.items():
        for pos in poss:
            if apply_tactic(rules, term, Tactic(name, True, pos)) is not None:
                out.append(Tactic(name, True, pos))
            if allow_reverse and apply_tactic(rules, term, Tactic(name, False, pos)) is not None:
                out.append(Tactic(name, False, pos))
    return out


# ── distanza euristica fra termini ────────────────────────────────────────

def symbol_multiset(term: Term) -> Dict[str, int]:
    out: Dict[str, int] = {}
    stack: List[Pattern] = [term]
    while stack:
        t = stack.pop()
        if isinstance(t, Term):
            out[t.op] = out.get(t.op, 0) + 1
            stack.extend(t.args)
    return out


def distance(a: Term, b: Term) -> int:
    """Distanza strutturale: differenza simmetrica dei multinsiemi di simboli."""
    ma, mb = symbol_multiset(a), symbol_multiset(b)
    keys = set(ma) | set(mb)
    return sum(abs(ma.get(k, 0) - mb.get(k, 0)) for k in keys)


# ── la teoria-giocattolo (algebra dei gruppi) e i benchmark ───────────────

def _c(name: str) -> Term:
    return Term(name)


def group_rules() -> Dict[str, Rule]:
    x, y, z = Var("x"), Var("y"), Var("z")
    rules = [
        Rule("id_left", Term("mul", (Term("e"), x)), x),
        Rule("id_right", Term("mul", (x, Term("e"))), x),
        Rule("inv_left", Term("mul", (Term("inv", (x,)), x)), Term("e")),
        Rule("inv_right", Term("mul", (x, Term("inv", (x,)))), Term("e")),
        Rule("assoc", Term("mul", (Term("mul", (x, y)), z)),
                       Term("mul", (x, Term("mul", (y, z))))),
        Rule("inv_e", Term("inv", (Term("e"),)), Term("e")),
        Rule("inv_inv", Term("inv", (Term("inv", (x,)),)), x),
    ]
    return {r.name: r for r in rules}


@dataclass(frozen=True)
class Goal:
    name: str
    start: Term
    target: Term


def benchmark_goals() -> List[Goal]:
    a, b = _c("a"), _c("b")
    e = _c("e")

    def mul(p, q): return Term("mul", (p, q))
    def inv(p): return Term("inv", (p,))

    return [
        Goal("id_left", mul(e, a), a),
        Goal("id_right", mul(a, e), a),
        Goal("inv_e", inv(e), e),
        Goal("inv_inv", inv(inv(a)), a),
        Goal("e_times_inv", mul(e, inv(a)), inv(a)),
        Goal("double_id", mul(e, mul(e, a)), a),
        Goal("id_both_sides", mul(mul(e, a), e), a),
        Goal("inv_left_const", mul(inv(a), a), e),
        Goal("assoc_step", mul(mul(a, b), e), mul(a, b)),
        Goal("nested_id", mul(mul(e, a), mul(e, b)), mul(a, b)),
        # più impegnativi: catene di 3 passi, una con riscrittura all'indietro
        Goal("cancel_left", mul(inv(a), mul(a, b)), b),
        Goal("cancel_right", mul(mul(a, inv(b)), b), a),
    ]
