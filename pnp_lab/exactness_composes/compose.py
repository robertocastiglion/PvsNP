"""Operazioni di composizione su matrici di comunicazione (Modulo 18).

Due composizioni, entrambe candidate al ruolo di "gadget composition" della
congettura EXACTNESS COMPOSES:

* `tensor(A, B)`  -- prodotto di Kronecker booleano (AND): l'unica composizione in
  cui A, B e A∘B sono TUTTE matrici, quindi la congettura "le matrici a copertura
  integrale sono chiuse per composizione" e' letterale e ben tipata;
* `lift(f, g, k)` -- la composizione del LIFTING (Raz-McKenzie / cycle-3):
  F[x, y] = f(g(x_1, y_1), ..., g(x_k, y_k)), con f funzione esterna su k bit e g
  gadget a 1 bit (matrice 2x2). E' l'arena "lossy" dove il +1 del ciclo 3 viveva.
"""

from __future__ import annotations

from itertools import product
from typing import Callable, Dict, Sequence, Tuple

from .gap import BoolMatrix, as_matrix


def tensor(A: BoolMatrix, B: BoolMatrix) -> BoolMatrix:
    """Prodotto di Kronecker AND: (A⊗B)[(i,i'),(j,j')] = A[i][j] & B[i'][j']."""
    ra, ca = len(A), len(A[0])
    rb, cb = len(B), len(B[0])
    out = []
    for i in range(ra):
        for ip in range(rb):
            row = []
            for j in range(ca):
                for jp in range(cb):
                    row.append(A[i][j] & B[ip][jp])
            out.append(row)
    return as_matrix(out)


def tensor_or(A: BoolMatrix, B: BoolMatrix) -> BoolMatrix:
    """Variante OR: (A⊕B)[(i,i'),(j,j')] = A[i][j] | B[i'][j']."""
    ra, ca = len(A), len(A[0])
    rb, cb = len(B), len(B[0])
    out = []
    for i in range(ra):
        for ip in range(rb):
            row = [A[i][j] | B[ip][jp] for j in range(ca) for jp in range(cb)]
            out.append(row)
    return as_matrix(out)


# --- gadget a 1 bit (matrici 2x2), indicizzate g[x][y] -------------------------

GADGETS_1BIT: Dict[str, BoolMatrix] = {
    "AND": as_matrix([[0, 0], [0, 1]]),
    "OR": as_matrix([[0, 1], [1, 1]]),
    "XOR": as_matrix([[0, 1], [1, 0]]),
    "NAND": as_matrix([[1, 1], [1, 0]]),
    "NOR": as_matrix([[1, 0], [0, 0]]),
    "EQ": as_matrix([[1, 0], [0, 1]]),
    "IMP": as_matrix([[1, 1], [0, 1]]),
    "PROJ_X": as_matrix([[0, 0], [1, 1]]),  # g(x,y)=x
    "PROJ_Y": as_matrix([[0, 1], [0, 1]]),  # g(x,y)=y
}


def base_function(name: str, k: int) -> Callable[[Tuple[int, ...]], int]:
    """Funzione esterna f: {0,1}^k -> {0,1}."""
    if name == "AND":
        return lambda b: int(all(b))
    if name == "OR":
        return lambda b: int(any(b))
    if name == "XOR":
        return lambda b: sum(b) & 1
    if name == "MAJ":
        return lambda b: int(sum(b) * 2 > k)
    if name == "NAND":
        return lambda b: int(not all(b))
    if name == "NOR":
        return lambda b: int(not any(b))
    raise ValueError(name)


def lift(f: Callable[[Tuple[int, ...]], int], g: BoolMatrix, k: int) -> BoolMatrix:
    """Matrice di comunicazione del lift F = f ∘ g^k.

    Alice tiene x ∈ {0,1}^k, Bob tiene y ∈ {0,1}^k (gadget a 1 bit per coordinata).
    F[x, y] = f(g[x_1][y_1], ..., g[x_k][y_k]).  Matrice 2^k x 2^k.
    """
    xs = list(product([0, 1], repeat=k))
    ys = list(product([0, 1], repeat=k))
    out = []
    for x in xs:
        row = []
        for y in ys:
            gout = tuple(g[x[i]][y[i]] for i in range(k))
            row.append(f(gout))
        out.append(row)
    return as_matrix(out)


def lift_named(fname: str, gname: str, k: int) -> BoolMatrix:
    """Comodita': lift di funzioni/gadget per nome."""
    return lift(base_function(fname, k), GADGETS_1BIT[gname], k)
