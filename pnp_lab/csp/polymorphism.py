"""CICLO 2 della direzione B — POLITOMORFISMI di relazioni booleane piccole.

Contesto. La direzione A è collassata in σ(cost) (RESEARCH_LOG Entry 9): ogni invariante
costruito dalla formula-size resta dentro σ(cost) e non può essere il falsificatore di
Entry 7. La diagnosi del restart program impone di rompere uno tra (1) scalare, (2)
minimo di copertura, (3) unario. La direzione B cambia ARENA: i POLITOMORFISMI di una
relazione Γ — le operazioni f: D^k → D che PRESERVANO Γ — sono un oggetto ALGEBRICO, NON
derivato dal costo. Rompe (2) [lascia il mondo copertura/formula-size] ed è il punto in
cui le CSP toccano P vs NP (dicotomia Bulatov–Zhuk: CSP(Γ)∈P ⟺ Γ ha un politomorfismo di
Taylor/WNU; NP-completo altrimenti).

IPOTESI H-B (Explorer). Il PROFILO simmetrico di Γ — per quali arità k esiste un
politomorfismo SIMMETRICO idempotente — porta informazione OLTRE i marker già noti
(la tractabilità di Schaefer = chiusura sotto AND/OR/MAJ/MINORITY/costante).

PARENT-KILLER DICHIARATO IN ANTICIPO (se scatta → RESTATEMENT):
  PK  il profilo simmetrico coincide con la tractabilità di Schaefer / la larghezza BLP:
      "BLP decide CSP(Γ) ⟺ Γ ha politomorfismi simmetrici di ogni arità" (Barto–Kozik;
      su dominio booleano = dicotomia di Schaefer/reticolo di Post). Cioè il "nuovo"
      profilo è un teorema noto rietichettato.
  K-deg  artefatto di non-idempotenza / di core (relazioni degeneri: ∅, costanti).

ATTENZIONE (scope). Constatazione sul METODO su istanze FINITE, NON un claim su P vs NP.
Dominio booleano D={0,1}; tutto ESATTO e deterministico (enumerazione finita, interi).
Una relazione di arità m è R ⊆ {0,1}^m (frozenset di tuple). Un'operazione k-aria è una
tavola di verità intera: ``op(x_0..x_{k-1}) = (op_tt >> sum_i x_i 2^i) & 1``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import FrozenSet, List, Tuple

Relation = FrozenSet[Tuple[int, ...]]


# --------------------------------------------------------------------------- #
#  Politomorfismi: l'operazione preserva la relazione?                        #
# --------------------------------------------------------------------------- #

def op_value(op_tt: int, args: Tuple[int, ...]) -> int:
    """Valore dell'operazione k-aria ``op_tt`` su ``args`` (indice = sum x_i 2^i)."""
    idx = 0
    for i, x in enumerate(args):
        idx |= (x & 1) << i
    return (op_tt >> idx) & 1


def preserves(op_tt: int, k: int, R: Relation) -> bool:
    """``op_tt`` (k-aria) è un politomorfismo di R? Per OGNI scelta di k tuple di R,
    l'applicazione colonna-per-colonna ricade in R."""
    if not R:
        return True
    m = len(next(iter(R)))
    for rows in product(R, repeat=k):
        result = tuple(op_value(op_tt, tuple(rows[r][j] for r in range(k)))
                       for j in range(m))
        if result not in R:
            return False
    return True


def symmetric_ops(k: int, *, idempotent: bool = True) -> List[int]:
    """Tutte le operazioni k-arie SIMMETRICHE (dipendono solo dal peso di Hamming).
    ``idempotent`` forza op(0..0)=0 e op(1..1)=1. Sono 2^(k-1) (idempotenti) o 2^(k+1)."""
    out: List[int] = []
    weights = range(k + 1)
    for choice in product((0, 1), repeat=k + 1):  # choice[w] = output a peso w
        if idempotent and (choice[0] != 0 or choice[k] != 1):
            continue
        tt = 0
        for idx in range(1 << k):
            w = bin(idx).count("1")
            if choice[w]:
                tt |= 1 << idx
        out.append(tt)
    return out


def has_symmetric_polymorphism(R: Relation, k: int, *, idempotent: bool = True) -> bool:
    """R ha un politomorfismo simmetrico (idempotente) di arità k?"""
    return any(preserves(op, k, R) for op in symmetric_ops(k, idempotent=idempotent))


def symmetric_profile(R: Relation, max_arity: int = 5) -> Tuple[int, ...]:
    """Le arità k∈[2,max_arity] per cui R ha un politomorfismo simmetrico idempotente."""
    return tuple(k for k in range(2, max_arity + 1) if has_symmetric_polymorphism(R, k))


# --------------------------------------------------------------------------- #
#  Marker noti: le operazioni di Schaefer (la dicotomia booleana)             #
# --------------------------------------------------------------------------- #

def _named_op(k: int, fn) -> int:
    tt = 0
    for idx in range(1 << k):
        args = tuple((idx >> i) & 1 for i in range(k))
        if fn(args):
            tt |= 1 << idx
    return tt


AND2 = _named_op(2, lambda a: a[0] & a[1])
OR2 = _named_op(2, lambda a: a[0] | a[1])
MAJ3 = _named_op(3, lambda a: 1 if sum(a) >= 2 else 0)
MINORITY3 = _named_op(3, lambda a: a[0] ^ a[1] ^ a[2])


def schaefer_tractable(R: Relation) -> bool:
    """Marker NOTO (P): R è Schaefer-tractabile ⟺ è 0-valida, 1-valida, Horn (chiusa sotto
    AND), dual-Horn (OR), affine (MINORITY/XOR) o bijunctive (MAJ). (Schaefer 1978.)
    NB: P ⊋ BLP — l'affine (XOR) è in P ma NON BLP-risolvibile."""
    if not R:
        return True
    m = len(next(iter(R)))
    if tuple([0] * m) in R or tuple([1] * m) in R:
        return True
    return any([
        preserves(AND2, 2, R), preserves(OR2, 2, R),
        preserves(MAJ3, 3, R), preserves(MINORITY3, 3, R),
    ])


def blp_solvable(R: Relation) -> bool:
    """Marker NOTO (BLP = Basic LP, Sherali–Adams livello 1): R è BLP-risolvibile ⟺ è
    0/1-valida o SEMILATTICE (chiusa sotto AND = Horn, oppure OR = dual-Horn). NB: NON
    include MAJ (bijunctive/2-SAT è bounded-width ma NON BLP: la LP è frazionaria sui
    cicli dispari, vedi ≠ / 2-colorabilità) né l'affine. AND/OR sono associative →
    chiusura binaria ⟹ chiusura simmetrica di OGNI arità: è proprio il termine DESTRO del
    parent-killer 'BLP ⟺ politomorfismi simmetrici di ogni arità' (Kun et al./Barto–Kozik)."""
    if not R:
        return True
    m = len(next(iter(R)))
    if tuple([0] * m) in R or tuple([1] * m) in R:
        return True
    return preserves(AND2, 2, R) or preserves(OR2, 2, R)


# --------------------------------------------------------------------------- #
#  Il test del parent-killer su tutte le relazioni booleane piccole           #
# --------------------------------------------------------------------------- #

@dataclass
class PolyReport:
    arity: int
    num_relations: int
    max_sym_arity: int
    mismatches: List[Tuple[Relation, Tuple[int, ...], bool]]  # (R, sym_profile, blp)

    @property
    def parent_killer_holds(self) -> bool:
        """PK: 'ha simmetrici di ogni arità testata' coincide con BLP-risolvibile
        (Barto–Kozik). Se sì, il profilo simmetrico è il teorema noto rietichettato."""
        return len(self.mismatches) == 0

    @property
    def verdict(self) -> str:
        return ("RESTATEMENT (parent-killer: symmetric profile == BLP-solvable)"
                if self.parent_killer_holds
                else "DIVERGENCE (symmetric profile vs BLP disagree)")


def all_relations(arity: int) -> List[Relation]:
    """Tutte le relazioni booleane di arità data: ogni sottoinsieme di {0,1}^arity."""
    tuples = list(product((0, 1), repeat=arity))
    rels: List[Relation] = []
    for mask in range(1 << len(tuples)):
        rels.append(frozenset(t for i, t in enumerate(tuples) if (mask >> i) & 1))
    return rels


def is_degenerate(R: Relation) -> bool:
    """R è 0-valid o 1-valid: ha un politomorfismo COSTANTE (non idempotente) → CSP
    banalmente soddisfacibile. Sono il caso ``K-deg`` (artefatto di core) da escludere
    per testare il parent-killer nel setting IDEMPOTENTE."""
    if not R:
        return True
    m = len(next(iter(R)))
    return tuple([0] * m) in R or tuple([1] * m) in R


def analyze(arity: int, max_sym_arity: int = 5, *, idempotent_only: bool = True) -> PolyReport:
    """Su tutte le relazioni booleane di arità data: il profilo simmetrico idempotente
    (ha simmetrici per OGNI arità fino a ``max_sym_arity``) coincide con la
    BLP-risolvibilità (il parent-killer)? ``idempotent_only`` esclude le relazioni
    degeneri 0/1-valid (killer K-deg): BLP-risolvibili via la costante NON-idempotente,
    dove il profilo idempotente è vuoto per artefatto. Una divergenza NON degenere e NON
    spiegata dal teorema = candidato di contenuto fuori-dizionario."""
    rels = all_relations(arity)
    mismatches = []
    considered = 0
    for R in rels:
        if idempotent_only and is_degenerate(R):
            continue
        considered += 1
        has_all_sym = all(has_symmetric_polymorphism(R, k)
                          for k in range(2, max_sym_arity + 1))
        blp = blp_solvable(R)
        if has_all_sym != blp:
            mismatches.append((R, symmetric_profile(R, max_sym_arity), blp))
    return PolyReport(arity=arity, num_relations=considered,
                      max_sym_arity=max_sym_arity, mismatches=mismatches)
