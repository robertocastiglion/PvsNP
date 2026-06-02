"""La categoria sottostante C: l'oggetto che le tre lenti devono *condividere*.

L'ipotesi forte (Roberto, 2026-06-02) è che calcolare / dimostrare / riconoscere
la complessità non siano tre problemi diversi ma gli STESSI morfismi visti tramite
tre arricchimenti incompatibili (categorie arricchite su quantali, Lawvere 1973).
Per misurarlo serve prima fissare UNA categoria sottostante C — le frecce comuni.

Istanza concreta e calcolabile:
  • OGGETTI  = funzioni booleane su n variabili (truth table come intero).
  • MORFISMI = rinomine delle variabili (azione di S_n sulle truth table). Sono
    riduzioni invertibili: rinominare le variabili NON cambia la dimensione di
    formula minima. Quindi sono ISOMETRIE per la lente "calcolare" (la complessità
    è costante sull'orbita). Questo è il test che C è ben definita: se la lente non
    fosse invariante sui morfismi non sarebbe un funtore su C.

Onestà: S_n è un sottogruppo (un gruppoide) delle riduzioni; basta per ESEGUIRE
l'invarianza esatta su n piccolo. Le riduzioni generali (many-one poly) sono CITATE.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import Dict, FrozenSet, List, Tuple


def apply_perm(tt: int, n: int, perm: Tuple[int, ...]) -> int:
    """Azione di una permutazione delle variabili sulla truth table.

    La nuova funzione g vale g(x) = f(y), dove y è x con i bit (= variabili)
    permutati secondo ``perm``. Rinomina pura: l'insieme dei valori non cambia,
    solo l'etichetta degli ingressi.
    """
    N = 1 << n
    out = 0
    for x in range(N):
        y = 0
        for j in range(n):
            if (x >> j) & 1:
                y |= 1 << perm[j]
        if (tt >> y) & 1:
            out |= 1 << x
    return out


def orbit(tt: int, n: int) -> FrozenSet[int]:
    """L'orbita di una funzione sotto tutte le rinomine delle variabili."""
    return frozenset(apply_perm(tt, n, p) for p in permutations(range(n)))


@dataclass
class Category:
    """C in piccolo: oggetti = tutte le funzioni su n variabili; morfismi = S_n."""

    n: int

    @property
    def objects(self) -> List[int]:
        return list(range(1 << (1 << self.n)))

    @property
    def morphisms(self) -> List[Tuple[int, ...]]:
        """Le frecce: le n! rinomine delle variabili."""
        return list(permutations(range(self.n)))

    def orbit(self, tt: int) -> FrozenSet[int]:
        return orbit(tt, self.n)

    def orbits(self) -> List[FrozenSet[int]]:
        """Partiziona lo spazio delle funzioni nelle classi di isomorfismo di C."""
        seen: set = set()
        out: List[FrozenSet[int]] = []
        for tt in self.objects:
            if tt in seen:
                continue
            o = self.orbit(tt)
            seen |= o
            out.append(o)
        return out


@dataclass
class IsometryReport:
    """Esito del test: la lente è invariante sui morfismi di C?"""

    n: int
    measure: str
    num_orbits: int
    invariant: bool          # la misura è costante su ogni orbita?
    violations: int          # quante orbite violano l'invarianza (atteso: 0)


def check_isometry(cat: Category, value: Dict[int, int], measure: str) -> IsometryReport:
    """Verifica che ``value`` (es. il costo MCSP) sia costante su ogni orbita di C.

    Se lo è, i morfismi di C sono isometrie per quella lente ⇒ la lente è un
    funtore ben definito su C. È la pre-condizione perché abbia senso chiedersi se
    le TRE lenti arricchiscano la *stessa* C.
    """
    violations = 0
    orbits = cat.orbits()
    for o in orbits:
        vals = {value[t] for t in o}
        if len(vals) != 1:
            violations += 1
    return IsometryReport(
        n=cat.n,
        measure=measure,
        num_orbits=len(orbits),
        invariant=(violations == 0),
        violations=violations,
    )
