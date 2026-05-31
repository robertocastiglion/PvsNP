"""
Il lower bound **esatto** della parità in profondità 2 (DNF) — e perché conta.

AC0 = circuiti di profondità costante, taglia polinomiale, gate ∧/∨ a fan-in
illimitato (+ ¬). Il risultato celebre (Furst–Saxe–Sipser 1981; Håstad 1986 con
lo *switching lemma*) è: **la parità non sta in AC0**. È uno dei pochissimi
lower bound espliciti che *funzionano* — e che, non a caso, aggira la barriera
Natural Proofs (vedi Modulo 1 e Modulo 3).

Lo switching lemma non è verificabile a forza bruta, ma il suo **caso base in
profondità 2 sì**, ed è esatto: la DNF (OR di AND, cioè profondità 2) più piccola
per la parità su n variabili ha **esattamente 2^(n-1) termini, ciascuno di
larghezza n**. La ragione è limpida e la verifichiamo col metodo di
Quine–McCluskey: due minterm della parità non differiscono *mai* in un solo bit
(numeri di peso dispari distano un numero pari di bit), quindi nessuno si può
fondere → ogni implicante primo è un minterm isolato → la copertura minima è
forzata e usa tutti i 2^(n-1) minterm. Esponenziale: ecco il muro, esatto.
"""
from __future__ import annotations

from dataclasses import dataclass

from .circuit import parity_table

# Un implicante: tupla di lunghezza n con valori in {0, 1, None}. None = "-".
Implicant = tuple


def _minterms(table: int, n: int) -> list[tuple[int, ...]]:
    return [
        tuple((i >> j) & 1 for j in range(n))
        for i in range(1 << n)
        if (table >> i) & 1
    ]


def prime_implicants(table: int, n: int) -> set[tuple]:
    """Implicanti primi di una funzione via Quine–McCluskey.

    Ogni implicante è una tupla lunga n con valori in {0, 1, None} (None = bit
    indifferente). Due implicanti si fondono se differiscono in *esattamente* una
    posizione concreta e coincidono in tutte le altre (don't-care inclusi).
    """
    current: set[tuple] = set(
        tuple(b for b in m) for m in _minterms(table, n)
    )
    primes: set[tuple] = set()

    while current:
        cur = list(current)
        used: set[tuple] = set()
        nxt: set[tuple] = set()
        for i in range(len(cur)):
            a = cur[i]
            for k in range(i + 1, len(cur)):
                b = cur[k]
                diff = [p for p in range(n) if a[p] != b[p]]
                if len(diff) == 1 and a[diff[0]] is not None and b[diff[0]] is not None:
                    merged = list(a)
                    merged[diff[0]] = None
                    nxt.add(tuple(merged))
                    used.add(a)
                    used.add(b)
        primes |= set(current) - used
        current = nxt

    return primes


def implicant_width(imp: tuple) -> int:
    """Numero di letterali (posizioni concrete) di un implicante."""
    return sum(1 for v in imp if v is not None)


@dataclass(frozen=True)
class ParityLowerBound:
    n: int
    num_prime_implicants: int
    expected: int               # 2^(n-1)
    all_full_width: bool        # ogni primo usa tutti gli n letterali?
    is_tight: bool              # num_prime_implicants == expected e full width

    def pretty(self) -> str:
        ok = "OK" if self.is_tight else "!!"
        return (
            f"n={self.n}: parità → DNF minima = {self.num_prime_implicants} termini "
            f"(atteso 2^(n-1) = {self.expected}), larghezza piena: "
            f"{self.all_full_width}  [{ok}]"
        )


def parity_dnf_lower_bound(n: int) -> ParityLowerBound:
    """Verifica esatta: la DNF minima della parità su n variabili ha 2^(n-1)
    termini, ciascuno di larghezza n."""
    table = parity_table(n)
    primes = prime_implicants(table, n)
    expected = 1 << (n - 1)
    all_full = all(implicant_width(p) == n for p in primes)
    return ParityLowerBound(
        n=n,
        num_prime_implicants=len(primes),
        expected=expected,
        all_full_width=all_full,
        is_tight=(len(primes) == expected and all_full),
    )


def dnf_size(table: int, n: int) -> int:
    """Numero di implicanti primi di una funzione (proxy di taglia DNF).

    Per la parità coincide con la DNF minima (tutti i primi sono essenziali);
    per funzioni 'facili' come AND/OR è piccolo. Serve da contrasto.
    """
    return len(prime_implicants(table, n))
