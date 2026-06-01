"""Aritmetica nel campo finito GF(p) con p primo.

L'algebrizzazione vive qui: per "aritmetizzare" una formula booleana la si
solleva a un polinomio su un campo. Lavoriamo nel campo primo GF(p) = interi
modulo p, dove ogni elemento non nullo è invertibile (piccolo teorema di
Fermat: a^(p-1) = 1, quindi a^(-1) = a^(p-2) mod p).

Tutto il modulo è esatto: nessun float, solo interi modulo p.
"""

from __future__ import annotations

from dataclasses import dataclass


def is_prime(n: int) -> bool:
    """Test di primalità per tentativi (basta per i piccoli primi che usiamo)."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


@dataclass(frozen=True)
class Field:
    """Il campo primo GF(p). Tutte le operazioni restituiscono il rappresentante
    canonico in 0..p-1."""

    p: int

    def __post_init__(self) -> None:
        if not is_prime(self.p):
            raise ValueError(f"{self.p} non è primo: GF(p) richiede p primo")

    def reduce(self, a: int) -> int:
        return a % self.p

    def add(self, a: int, b: int) -> int:
        return (a + b) % self.p

    def sub(self, a: int, b: int) -> int:
        return (a - b) % self.p

    def neg(self, a: int) -> int:
        return (-a) % self.p

    def mul(self, a: int, b: int) -> int:
        return (a * b) % self.p

    def pow(self, a: int, e: int) -> int:
        return pow(a % self.p, e, self.p)

    def inv(self, a: int) -> int:
        """Inverso moltiplicativo via Fermat: a^(p-2) mod p."""
        a %= self.p
        if a == 0:
            raise ZeroDivisionError("0 non è invertibile in GF(p)")
        return pow(a, self.p - 2, self.p)
