"""Rappresentazione e enumerazione delle funzioni booleane.

Una funzione booleana su ``n`` variabili è una mappa f: {0,1}^n -> {0,1}.
È descritta completamente dalla sua *tabella di verità* (truth table): una
sequenza di N = 2^n bit, dove il bit in posizione ``i`` è il valore di f
sull'input la cui codifica binaria è ``i``.

Il numero TOTALE di funzioni booleane su n variabili è 2^N = 2^(2^n):
    n = 1 ->        4 funzioni
    n = 2 ->       16
    n = 3 ->      256
    n = 4 ->    65 536      (enumerazione esatta ancora fattibile)
    n = 5 -> ~4.3 miliardi  (qui si passa al campionamento)

Questa crescita doppiamente esponenziale è esattamente il motivo per cui
l'enumerazione esatta è possibile solo per n piccolo.
"""

from __future__ import annotations

import random
from typing import Iterator, Sequence


class BooleanFunction:
    """Una funzione booleana su ``n`` variabili, descritta dalla truth table.

    La truth table è una tupla di N = 2^n valori in {0, 1}. L'indice ``i``
    corrisponde all'input i cui bit sono la rappresentazione binaria di ``i``
    (bit più significativo = prima variabile).
    """

    __slots__ = ("n", "N", "truth_table")

    def __init__(self, n: int, truth_table: Sequence[int]) -> None:
        N = 1 << n
        if len(truth_table) != N:
            raise ValueError(
                f"la truth table deve avere lunghezza 2^{n} = {N}, "
                f"ricevuti {len(truth_table)} valori"
            )
        self.n = n
        self.N = N
        self.truth_table = tuple(int(bool(v)) for v in truth_table)

    # -- costruttori alternativi ------------------------------------------

    @classmethod
    def from_int(cls, n: int, code: int) -> "BooleanFunction":
        """Costruisce la funzione il cui codice (truth table letta come intero) è ``code``.

        ``code`` va da 0 a 2^(2^n) - 1; il bit ``i`` di ``code`` è f sull'input ``i``.
        """
        N = 1 << n
        if not (0 <= code < (1 << N)):
            raise ValueError(f"code fuori range per n={n}: atteso 0..2^{N}-1")
        return cls(n, [(code >> i) & 1 for i in range(N)])

    # -- accesso -----------------------------------------------------------

    def to_int(self) -> int:
        """Codifica la truth table come un singolo intero (utile per hashing/identità)."""
        code = 0
        for i, v in enumerate(self.truth_table):
            if v:
                code |= 1 << i
        return code

    def __call__(self, *bits: int) -> int:
        """Valuta f sull'input dato come bit espliciti, es. ``f(0, 1, 1)``."""
        if len(bits) != self.n:
            raise ValueError(f"attese {self.n} variabili, ricevuti {len(bits)} bit")
        idx = 0
        for b in bits:
            idx = (idx << 1) | (1 if b else 0)
        return self.truth_table[idx]

    def weight(self) -> int:
        """Numero di input su cui f vale 1 (il 'peso di Hamming' della truth table)."""
        return sum(self.truth_table)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, BooleanFunction)
            and self.n == other.n
            and self.truth_table == other.truth_table
        )

    def __hash__(self) -> int:
        return hash((self.n, self.truth_table))

    def __repr__(self) -> str:
        bits = "".join(str(v) for v in self.truth_table)
        return f"BooleanFunction(n={self.n}, tt=0b{bits})"


def num_functions(n: int) -> int:
    """Numero totale di funzioni booleane su n variabili: 2^(2^n)."""
    return 1 << (1 << n)


def all_functions(n: int) -> Iterator[BooleanFunction]:
    """Enumera TUTTE le 2^(2^n) funzioni booleane su n variabili.

    Praticabile solo per n piccolo (n <= 4 dà 65 536 funzioni). Per n grande
    usare ``random_function`` con campionamento Monte Carlo.
    """
    total = num_functions(n)
    for code in range(total):
        yield BooleanFunction.from_int(n, code)


def random_function(n: int, rng: random.Random | None = None) -> BooleanFunction:
    """Restituisce una funzione booleana scelta uniformemente a caso su n variabili."""
    r = rng or random
    N = 1 << n
    return BooleanFunction(n, [r.getrandbits(1) for _ in range(N)])
