"""Modulo 17 — Survival Test (𝒭=∞): un criterio MISURABILE che separa le barriere.

Domanda. I quattro ostacoli a P vs NP si dividono in due famiglie ben note
(informazione vs calcolo, Modulo 15). Esiste un UNICO test, eseguibile su istanze
minuscole, che data una barriera dica a quale famiglia appartiene? Sì:

    SURVIVAL TEST.  Si calcola il vantaggio di distinzione Δ della barriera quando
    al distinguitore si concede CALCOLO ILLIMITATO (𝒭 = ∞), lasciando solo il suo
    limite di INTERFACCIA 𝒜.  Allora:

        Δ(𝒭=∞) < 1   ⟹  barriera INFORMATION-THEORETIC (incondizionata)
        Δ(𝒭=∞) = 1   ⟹  barriera COMPUTATIONAL  (= un'ipotesi di pseudocasualità)

Idea. Una barriera "sopravvive" al calcolo illimitato se il suo bound resta anche
quando l'osservatore può calcolare qualunque cosa: allora il bound vive sull'asse
INFORMAZIONE 𝒜 (hai mancato l'ago: nessun calcolo recupera ciò che non hai visto)
ed è un TEOREMA incondizionato. Se invece il bound EVAPORA (Δ→1) appena il calcolo
è illimitato, allora esisteva SOLO perché 𝒭 era limitato: è l'ipotesi che "duro"
sembri "facile" al calcolo limitato, cioè la pseudocasualità.

Esito misurato (esatto, istanze minuscole; vedi docs/survival-test.md):
  • RELATIVIZZAZIONE: Δ(𝒭=∞) = t/N < 1. Il calcolo illimitato NON aiuta (la classe
    massimizza già su ogni g). Bound sull'interfaccia. SOPRAVVIVE → information-theoretic.
  • NATURAL PROOFS: Δ sale 0.264 → 0.324 → … → 1.000 al crescere del calcolo, perché
    il predicato "duro" È una funzione della truth table satura: con 𝒭=∞ lo si calcola
    e si distingue perfettamente. NON sopravvive → computational (debito pseudocasuale).

Onestà (vincolante). NON è un nuovo lower bound: è un CRITERIO DI CLASSIFICAZIONE che
ri-deriva i due assi del Modulo 15 con un test scalare misurabile. Misure ESATTE su
istanze minuscole (needle N=8; truth table n=3), non le barriere asintotiche; le celle
ad alto calcolo del Modulo 15 sono cote inferiori certificate. Non tocca P vs NP.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

from pnp_lab.bounded_observer.observer import relativization_advantage
from pnp_lab.distinguishing import advantage_matrix, default_split
from pnp_lab.distinguishing.advantage import HardEasySplit

# Soglia di "trivialità": Δ a calcolo illimitato indistinguibile da 1.
TRIVIAL_TOL = 1e-9


@dataclass(frozen=True)
class SurvivalResult:
    """Esito del survival test per UNA barriera."""
    name: str
    axis: str                         # "𝒜 (informazione)" | "𝒭 (calcolo)"
    delta_compute_bounded: float      # Δ con calcolo LIMITATO (rappresentativo)
    delta_compute_unbounded: float    # Δ con 𝒭 = ∞
    kind: str                         # "information-theoretic" | "computational"
    margin: float                     # 1 − Δ(𝒭=∞): > 0 ⟺ sopravvive

    @property
    def survives(self) -> bool:
        return self.margin > TRIVIAL_TOL


def classify(
    name: str, axis: str, delta_bounded: float, delta_unbounded: float
) -> SurvivalResult:
    """Applica il criterio: Δ(𝒭=∞) < 1 ⟹ information-theoretic, altrimenti computational."""
    margin = 1.0 - delta_unbounded
    kind = "information-theoretic" if margin > TRIVIAL_TOL else "computational"
    return SurvivalResult(
        name=name, axis=axis,
        delta_compute_bounded=delta_bounded,
        delta_compute_unbounded=delta_unbounded,
        kind=kind, margin=margin,
    )


# ════════════════════════════════════════════════════════════════════════════
# RELATIVIZZAZIONE — bound sull'interfaccia 𝒜; il calcolo illimitato è INERTE.
# ════════════════════════════════════════════════════════════════════════════
#
# La classe degli osservatori a ≤ t query booleane (Modulo 16) combina già le
# risposte con una g ARBITRARIA: è 𝒭 = ∞. Eppure Δ = t/N. Quindi sia il valore a
# calcolo limitato che quello a calcolo illimitato sono t/N: il calcolo NON aiuta,
# il bound è interamente sull'interfaccia (hai interrogato t celle su N).

def relativization_survival(n: int = 8, t: int = 2) -> SurvivalResult:
    """Survival test della relativizzazione (needle su N=n punti, budget t query).
    Δ(𝒭=∞) = t/N: poiché restringere g può solo RIDURRE Δ, il valore a calcolo
    limitato è ≤ t/N, e quello a 𝒭=∞ è esattamente t/N < 1. Sopravvive."""
    delta_inf = relativization_advantage(n, t)          # 𝒭 già illimitato → t/N
    return classify(
        "relativization", "𝒜 (informazione)",
        delta_bounded=delta_inf,    # restringere il calcolo non può superarlo
        delta_unbounded=delta_inf,
    )


# ════════════════════════════════════════════════════════════════════════════
# NATURAL PROOFS — bound sul calcolo 𝒭; con 𝒭=∞ il bound EVAPORA (Δ→1).
# ════════════════════════════════════════════════════════════════════════════
#
# Informazione satura (legge tutta la truth table, ℓ=n=3). Con calcolo limitato s
# gate, Δ(ℓ=3,s) è piccolo (Modulo 15). Ma il predicato "duro" (complessità ≥ τ) È
# una funzione della truth table: a 𝒭=∞ l'osservatore OTTIMO è il suo indicatore,
# che separa perfettamente duri da facili ⇒ Δ = 1. Il bound esisteva solo perché 𝒭
# era limitato: è la pseudocasualità.

def natural_proofs_curve(ss: Sequence[int] = (1, 2, 3)) -> List[Tuple[int, float]]:
    """Δ(ℓ=3, s) al crescere del budget di calcolo s — la curva che sale verso 1."""
    m = advantage_matrix(default_split(), ells=(3,), ss=tuple(ss))
    return [(s, m.get(3, s).epsilon) for s in ss]


def natural_proofs_unbounded_advantage(split: HardEasySplit) -> float:
    """Δ a 𝒭 = ∞: l'osservatore ottimo è l'INDICATORE di 'duro' (funzione della
    truth table satura). Lo CALCOLIAMO (non hard-coded): D1 = uniforme sui duri,
    D0 = uniforme sui facili, decide(f)=1 sse f è duro ⇒ Pr_D1=1, Pr_D0=0, Δ=1."""
    hard = set(split.hard)
    p1 = sum(1 for f in split.hard if f in hard) / len(split.hard)   # = 1
    p0 = sum(1 for f in split.easy if f in hard) / len(split.easy)   # = 0
    return abs(p1 - p0)


def natural_proofs_survival(ss: Sequence[int] = (1, 2, 3)) -> SurvivalResult:
    """Survival test delle natural proofs. Δ a calcolo limitato (s minimo) vs Δ a
    𝒭=∞ (= 1, indicatore del predicato di durezza). Non sopravvive → computational."""
    split = default_split()
    curve = natural_proofs_curve(ss)
    delta_bounded = curve[0][1]                          # Δ al calcolo più piccolo
    delta_inf = natural_proofs_unbounded_advantage(split)
    return classify(
        "natural proofs", "𝒭 (calcolo)",
        delta_bounded=delta_bounded,
        delta_unbounded=delta_inf,
    )


# ════════════════════════════════════════════════════════════════════════════
# Sintesi
# ════════════════════════════════════════════════════════════════════════════

def survival_results(n: int = 8, t: int = 2, ss: Sequence[int] = (1, 2, 3)) -> List[SurvivalResult]:
    """I due poli misurati del test: relativizzazione (informazione) e natural
    proofs (calcolo). Algebrizzazione si raggruppa con la prima (interfaccia 𝒜
    arricchita, Modulo 16); proof complexity con la seconda (debito pseudocasuale,
    docs/duality-gap-theory.md) — qui misuriamo i due poli puliti."""
    return [relativization_survival(n, t), natural_proofs_survival(ss)]


def criterion_summary() -> str:
    return "\n".join([
        "  Survival Test (𝒭=∞): a quale famiglia appartiene una barriera?",
        "    Δ(𝒭=∞) < 1  ⟹  information-theoretic  (incondizionata, asse 𝒜)",
        "    Δ(𝒭=∞) = 1  ⟹  computational         (= pseudocasualità, asse 𝒭)",
        "  Onestà: criterio di CLASSIFICAZIONE (ri-deriva i due assi del Modulo 15),",
        "  NON un nuovo lower bound. Misure esatte su istanze minuscole. Non tocca P vs NP.",
    ])
