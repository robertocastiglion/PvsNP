"""
Funzioni booleane come **truth-table intere** e le operazioni di base.

Per lavorare con la complessità di circuito su n piccolo conviene rappresentare
una funzione su n variabili con un intero: il bit i (0 ≤ i < 2^n) è il valore
della funzione sull'input la cui codifica binaria è i. Con N = 2^n input, la
maschera ``mask = (1<<N) - 1`` tiene i conti dentro N bit.

Esempio (n=2): la variabile x0 vale 1 sugli input 01 e 11 (indici 1 e 3),
quindi la sua truth table è 0b1010 = 10.
"""
from __future__ import annotations


def mask_for(n: int) -> int:
    """Maschera di 2^n bit a 1."""
    return (1 << (1 << n)) - 1


def projection(n: int, j: int) -> int:
    """Truth table della variabile x_j (0-based) su n variabili.

    Bit i acceso ⇔ il bit j-esimo dell'indice i è 1.
    """
    if not (0 <= j < n):
        raise ValueError(f"variabile {j} fuori range per n={n}")
    N = 1 << n
    return sum(1 << i for i in range(N) if (i >> j) & 1)


def NOT(a: int, n: int) -> int:
    """Negazione bit a bit dentro 2^n bit."""
    return (~a) & mask_for(n)


def AND(a: int, b: int) -> int:
    return a & b


def OR(a: int, b: int) -> int:
    return a | b


def parity_table(n: int) -> int:
    """Truth table della parità (XOR di tutte le n variabili)."""
    N = 1 << n
    return sum(1 << i for i in range(N) if bin(i).count("1") & 1)


def popcount_table(table: int, n: int) -> int:
    """Numero di input su cui la funzione vale 1 (peso di Hamming della tabella)."""
    return bin(table & mask_for(n)).count("1")


def truth_rows(table: int, n: int) -> list[tuple[int, ...]]:
    """Gli input (come tuple di n bit) su cui la funzione vale 1."""
    N = 1 << n
    return [
        tuple((i >> j) & 1 for j in range(n))
        for i in range(N)
        if (table >> i) & 1
    ]
