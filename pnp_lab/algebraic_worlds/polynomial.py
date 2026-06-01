"""Polinomi multivariati su GF(p) e il teorema di Schwartz–Zippel.

È il motore di tutti i lower bound "algebrici" (il metodo dei polinomi) che
stanno dietro la barriera dell'algebrizzazione. Rappresentiamo un polinomio come
mappa monomio→coefficiente, dove un monomio è un vettore di esponenti.

Schwartz–Zippel. Un polinomio NON nullo di grado totale d su GF(p) in n variabili
ha al più  d · p^(n-1)  radici; equivalentemente, due polinomi distinti di grado
≤ d coincidono su al più una frazione  d/p  dei punti. Qui lo VERIFICHIAMO in
modo esatto enumerando GF(p)^n su istanze piccole.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Dict, Tuple

from pnp_lab.algebrization import Field

#: un monomio è un vettore di esponenti (uno per variabile)
Exponent = Tuple[int, ...]


@dataclass
class Poly:
    """Polinomio multivariato su GF(p) in `n` variabili.

    `terms` mappa un vettore di esponenti al suo coefficiente (ridotto mod p,
    mai zero: i termini nulli si rimuovono)."""

    n: int
    field: Field
    terms: Dict[Exponent, int]

    def __post_init__(self) -> None:
        cleaned = {}
        for exp, c in self.terms.items():
            cc = self.field.reduce(c)
            if cc != 0:
                cleaned[exp] = cc
        self.terms = cleaned

    def eval(self, point: Tuple[int, ...]) -> int:
        F = self.field
        total = 0
        for exp, c in self.terms.items():
            mono = c
            for xi, e in zip(point, exp):
                if e:
                    mono = F.mul(mono, F.pow(xi, e))
            total = F.add(total, mono)
        return total

    @property
    def total_degree(self) -> int:
        return max((sum(exp) for exp in self.terms), default=0)

    @property
    def is_zero(self) -> bool:
        return len(self.terms) == 0

    def sub(self, other: "Poly") -> "Poly":
        F = self.field
        terms = dict(self.terms)
        for exp, c in other.terms.items():
            terms[exp] = F.sub(terms.get(exp, 0), c)
        return Poly(self.n, F, terms)


def all_points(p: int, n: int):
    """Enumerazione di tutti i punti di GF(p)^n."""
    return product(range(p), repeat=n)


def count_zeros(poly: Poly) -> int:
    """Numero esatto di radici di `poly` su GF(p)^n."""
    return sum(1 for x in all_points(poly.field.p, poly.n) if poly.eval(x) == 0)


def count_agreements(f: Poly, g: Poly) -> int:
    """Numero di punti di GF(p)^n in cui `f` e `g` coincidono = radici di f−g."""
    return count_zeros(f.sub(g))


def schwartz_zippel_zero_bound(degree: int, p: int, n: int) -> int:
    """Massimo numero di radici ammesso dal teorema: d · p^(n-1)."""
    return degree * (p ** (n - 1))


@dataclass
class SZCheck:
    degree: int
    p: int
    n: int
    zeros: int
    bound: int

    @property
    def holds(self) -> bool:
        return self.zeros <= self.bound

    @property
    def agreement_fraction(self) -> float:
        return self.zeros / (self.p ** self.n)


def verify_schwartz_zippel(poly: Poly) -> SZCheck:
    """Verifica esatta del bound di Schwartz–Zippel per un polinomio dato.

    (Per un polinomio non nullo le radici devono stare sotto d · p^(n-1).)"""
    d = poly.total_degree
    z = count_zeros(poly)
    return SZCheck(degree=d, p=poly.field.p, n=poly.n, zeros=z,
                   bound=schwartz_zippel_zero_bound(d, poly.field.p, poly.n))
