"""Estensione multilineare di una funzione booleana — il cuore algebrico.

Data f : {0,1}^n → {0,1}, esiste un UNICO polinomio multilineare f~ su GF(p)
(grado ≤ 1 in ciascuna variabile) che coincide con f su tutto il cubo {0,1}^n:

    f~(x) = Σ_{a ∈ {0,1}^n} f(a) · χ_a(x),   con   χ_a(x) = Π_i [ x_i a_i + (1-x_i)(1-a_i) ].

χ_a è la funzione indicatrice del vertice a: vale 1 se x = a (sul cubo) e 0 su
ogni altro vertice, ed è multilineare. Quindi f~ interpola f.

Perché conta per le barriere. Un algoritmo *algebrico* (l'arithmetization che ha
dimostrato IP = PSPACE) non vede solo l'oracolo booleano f: vede la sua
estensione f~, valutabile in QUALSIASI punto del campo, non solo sui vertici
0/1. È esattamente questo "potere in più" che fa saltare la barriera della
relativizzazione — e su cui poi agisce la barriera dell'algebrizzazione
(Aaronson–Wigderson 2008).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

from .field import Field

Point = Tuple[int, ...]


def bits(a: int, n: int) -> Point:
    """Pattern di bit big-endian di a su n posizioni: (x_0, …, x_{n-1})."""
    return tuple((a >> (n - 1 - i)) & 1 for i in range(n))


def _chi(a_bits: Point, x: Point, field: Field) -> int:
    """χ_a(x) = Π_i [ x_i  se a_i=1 ;  1-x_i  se a_i=0 ]."""
    r = 1
    for ai, xi in zip(a_bits, x):
        term = field.reduce(xi) if ai == 1 else field.sub(1, xi)
        r = field.mul(r, term)
    return r


@dataclass
class MultilinearExtension:
    """L'estensione multilineare f~ di una tabella di verità booleana.

    ``values[a]`` è f(a) ∈ {0,1}, dove a indicizza il vertice ``bits(a, n)``.
    L'istanza è chiamabile: ``ext(point)`` valuta f~ in un punto di GF(p)^n.
    """

    values: Tuple[int, ...]
    n: int
    field: Field

    def __post_init__(self) -> None:
        if len(self.values) != (1 << self.n):
            raise ValueError(
                f"servono 2^{self.n} = {1 << self.n} valori, ricevuti {len(self.values)}"
            )

    def __call__(self, point: Sequence[int]) -> int:
        if len(point) != self.n:
            raise ValueError(f"il punto deve avere {self.n} coordinate")
        total = 0
        for a in range(1 << self.n):
            fa = self.field.reduce(self.values[a])
            if fa == 0:
                continue
            total = self.field.add(total, self.field.mul(fa, _chi(bits(a, self.n), tuple(point), self.field)))
        return total

    # -- verifiche di correttezza --------------------------------------------

    def agrees_on_cube(self) -> bool:
        """f~ coincide con f su ogni vertice {0,1}^n? (deve essere sempre vero)."""
        return all(
            self(bits(a, self.n)) == self.field.reduce(self.values[a])
            for a in range(1 << self.n)
        )

    def is_multilinear(self) -> bool:
        """Verifica esatta che f~ abbia grado ≤ 1 in ogni variabile.

        Per ciascuna variabile i e ogni fissaggio delle altre n-1 variabili sui
        vertici del cubo, f~ ristretta a x_i deve essere affine: la differenza
        seconda f~(x_i=2) - 2 f~(x_i=1) + f~(x_i=0) deve annullarsi in GF(p).
        """
        F = self.field
        for i in range(self.n):
            others = [j for j in range(self.n) if j != i]
            for mask in range(1 << len(others)):
                base = [0] * self.n
                for k, j in enumerate(others):
                    base[j] = (mask >> k) & 1

                def at(t: int) -> int:
                    pt = list(base)
                    pt[i] = t
                    return self(pt)

                second_diff = F.sub(F.add(at(0), at(2)), F.mul(2, at(1)))
                if second_diff != 0:
                    return False
        return True


def count_true(values: Sequence[int]) -> int:
    """Numero di assegnamenti veri = Σ_{vertici} f. È anche Σ_cube f~."""
    return sum(1 for v in values if v != 0)
