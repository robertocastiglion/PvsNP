"""La frontiera: MCSP ↔ Natural Proofs, e l'hardness magnification.

Due idee, una eseguibile e una citata.

1) IL LEGAME CON NATURAL PROOFS (eseguibile, esatto).
   Razborov–Rudich (Modulo 1): una "prova naturale" è una proprietà delle funzioni
   COSTRUTTIVA (decidibile in fretta) + LARGA (vale per molte funzioni) + UTILE
   (rifiuta tutte le funzioni semplici). Ma una proprietà utile+larga e per giunta
   costruttiva è ESATTAMENTE un algoritmo efficiente che distingue le funzioni a
   bassa complessità dalle altre — cioè (quasi) un risolutore di MCSP. Se esistesse,
   romperebbe i generatori pseudo-casuali. Qui lo VEDIAMO: la proprietà ovvia "f è
   dura" è utile e larga, ma decidere l'appartenenza = calcolare la complessità =
   MCSP. La barriera È la durezza di MCSP.

2) HARDNESS MAGNIFICATION (citata).
   Lower bound MINUSCOLI (appena super-lineari, n^{1+ε}) per problemi specifici come
   gap-MCSP/MKtP si AMPLIFICANO in separazioni enormi (NP ⊄ P/poly). La soglia è
   sorprendentemente bassa — eppure non superata, perché quei lower bound sembrano
   richiedere tecniche non-naturali (la "barriera di magnificazione"). È il filo più
   vivo del 2018+. Lo CITIAMO con i riferimenti.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, List

from pnp_lab.circuits import ComplexityTable


# ── 1) il legame MCSP ↔ Natural Proofs (esatto) ───────────────────────────

def hard_property(ct: ComplexityTable, s: int) -> FrozenSet[int]:
    """La proprietà 'f è dura': {f : dimensione minima > s}."""
    return frozenset(t for t, c in ct.cost.items() if c > s)


def is_useful(prop: FrozenSet[int], ct: ComplexityTable, s: int) -> bool:
    """UTILE contro la taglia s: la proprietà rifiuta TUTTE le funzioni con dim ≤ s."""
    return all(ct.cost[t] > s for t in prop)


def largeness(prop: FrozenSet[int], ct: ComplexityTable) -> float:
    """LARGA: frazione di funzioni che soddisfano la proprietà."""
    return len(prop) / ct.num_functions


@dataclass
class NaturalProofsLink:
    s: int
    useful: bool
    large_fraction: float
    constructive_cost: str   # quanto costa decidere l'appartenenza (= MCSP)
    conclusion: str


def analyze_link(ct: ComplexityTable, s: int) -> NaturalProofsLink:
    """Mostra che la proprietà 'f è dura' è utile + larga, ma la sua costruttività
    equivale a risolvere MCSP — ed è lì che scatta la barriera Razborov–Rudich."""
    prop = hard_property(ct, s)
    return NaturalProofsLink(
        s=s,
        useful=is_useful(prop, ct, s),
        large_fraction=largeness(prop, ct),
        constructive_cost="decidere l'appartenenza = calcolare la complessità = MCSP "
                          "(nessun algoritmo efficiente noto)",
        conclusion="utile + larga ✓; SE fosse anche costruttiva sarebbe una prova "
                   "naturale efficiente ⇒ niente PRG (Razborov–Rudich). La barriera "
                   "= durezza di MCSP.",
    )


# ── 2) hardness magnification (citata) ────────────────────────────────────

@dataclass
class MagnificationFact:
    weak_lower_bound: str    # il lower bound (piccolo) che basterebbe
    implies: str             # la separazione (grande) che ne seguirebbe
    reference: str


def magnification_results() -> List[MagnificationFact]:
    """Teoremi di amplificazione noti (CITATI): piccolo LB ⇒ grande separazione."""
    return [
        MagnificationFact(
            "Circuiti n^{1+ε} per gap-MCSP (parametro piccolo)",
            "NP ⊄ P/poly  (quindi P ≠ NP)",
            "Oliveira–Pich 2019; Chen–Jin–Williams 2019/2020"),
        MagnificationFact(
            "LB appena super-lineari per MKtP in modelli ristretti",
            "separazioni maggiori (es. contro formule/branching programs)",
            "McKay–Murray–Williams 2019"),
        MagnificationFact(
            "LB super-lineari per problemi 'sparsi' (poche istanze YES)",
            "EXP ⊄ P/poly e affini",
            "Oliveira–Santhanam; Chen et al. 2019–2020"),
    ]


@dataclass
class MagnificationGap:
    known_lower_bound: str
    magnifying_threshold: str
    why_uncrossed: str


def threshold_gap() -> MagnificationGap:
    """Quanto siamo vicini — e perché non basta (ancora)."""
    return MagnificationGap(
        known_lower_bound="lower bound noti ~ n · polylog(n)  (quasi-lineari)",
        magnifying_threshold="soglia che amplificherebbe ~ n^{1+ε}  (appena sopra!)",
        why_uncrossed="i LB che amplificherebbero sembrano richiedere tecniche "
                      "NON-naturali / non-locali: la 'barriera di magnificazione'. "
                      "Si torna esattamente alle barriere dei Moduli 1, 2, 7-10.",
    )
