"""La "killer search" della congettura EXACTNESS COMPOSES (Modulo 18).

Congettura (post-audit, vedi docs/duality-gap-theory.md): definito il gap pinnato
sul LP  G*(M) = Cov(M) - LP(M), la classe delle relazioni a copertura INTEGRALE
(G* = 0) e' chiusa per gadget composition.

Questo file la RISOLVE su istanze minuscole, in due letture:

* `smallest_gap_matrix(...)`   -- la piu' piccola matrice con G* > 0 (esiste? quanto?);
* `tensor_closure_holds(...)`  -- versione MATRICE∘MATRICE (tensore): e' chiusa?
* `lift_counterexamples(...)`  -- versione GADGET-SUBSTITUTION (lift): si apre un gap?

Verdetto (vedi `resolution()`): la congettura e' VERA per il tensore (ma segue dalla
moltiplicativita' nota della copertura frazionaria, quindi non e' contenuto nuovo) e
FALSA per il lift, l'arena che la congettura intendeva. Controesempio minimo:
f = OR_2, gadget g = XOR  ->  matrice di DISUGUAGLIANZA J - I_4, Cov=4, LP=3, G*=1.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import List, Optional, Tuple

from .gap import BoolMatrix, as_matrix, cover_number, frac_cover, gstar
from .compose import GADGETS_1BIT, base_function, lift, lift_named, tensor


def _all_matrices(m: int, n: int):
    for bits in product([0, 1], repeat=m * n):
        yield as_matrix([bits[i * n : (i + 1) * n] for i in range(m)])


def smallest_gap_matrix(max_cells: int = 16) -> Optional[Tuple[BoolMatrix, Fraction]]:
    """Cerca, per dimensione crescente, la PRIMA matrice booleana con G* > 0.

    Ritorna (M, G*) oppure None se nessuna entro il budget di celle. Esito noto:
    nessun gap fino a 3x4/3x5; il primo gap e' una 4x4 con G* = 1/2.
    """
    shapes: List[Tuple[int, int]] = []
    for total in range(1, max_cells + 1):
        for m in range(1, total + 1):
            if total % m == 0:
                n = total // m
                if m <= n:  # evita doppioni per trasposizione
                    shapes.append((m, n))
    for m, n in shapes:
        for M in _all_matrices(m, n):
            g = gstar(M)
            if g > 0:
                return M, g
    return None


def tensor_closure_holds(shapes=((2, 2), (2, 3))) -> Tuple[bool, int, bool]:
    """Versione MATRICE∘MATRICE: il tensore di due matrici integrali e' integrale?

    Ritorna (chiusa?, #coppie testate, fracCov_moltiplicativa?). Su tutte le coppie
    di matrici (necessariamente integrali a queste dimensioni) il tensore resta
    integrale e LP(A⊗B) = LP(A)·LP(B) -- la congettura e' VERA qui, ma come corollario
    della moltiplicativita' della copertura frazionaria.
    """
    pairs = 0
    closed = True
    multiplicative = True
    for s1 in shapes:
        for A in _all_matrices(*s1):
            fa = frac_cover(A)
            for s2 in shapes:
                for B in _all_matrices(*s2):
                    pairs += 1
                    T = tensor(A, B)
                    if gstar(T) != 0:
                        closed = False
                    if frac_cover(T) != fa * frac_cover(B):
                        multiplicative = False
    return closed, pairs, multiplicative


def lift_counterexamples(
    fnames=("OR", "AND", "XOR", "MAJ", "NAND", "NOR"),
    gnames=tuple(GADGETS_1BIT.keys()),
    ks=(2, 3),
) -> List[Tuple[str, str, int, Fraction]]:
    """Versione GADGET-SUBSTITUTION: lift f∘g^k con gadget INTEGRALE; G* > 0?

    Ritorna la lista di (fname, gname, k, G*) per cui il lift ha gap, ordinata per
    (k, G*). Tutti i gadget a 1 bit (2x2) sono integrali, quindi ogni voce e' un
    controesempio alla congettura nella sua arena intesa.
    """
    out: List[Tuple[str, str, int, Fraction]] = []
    for k in ks:
        for fname in fnames:
            f = base_function(fname, k)
            for gname in gnames:
                g = GADGETS_1BIT[gname]
                if gstar(g) != 0:
                    continue  # gadget non integrale: salta (qui mai)
                M = lift(f, g, k)
                gv = gstar(M)
                if gv > 0:
                    out.append((fname, gname, k, gv))
    out.sort(key=lambda t: (t[2], t[3]))
    return out


def smallest_lift_counterexample() -> Tuple[str, str, int, BoolMatrix, int, Fraction]:
    """Il controesempio-lift minimo: f=OR_2, g=XOR -> J - I_4.

    Ritorna (fname, gname, k, M, Cov, LP). G* = Cov - LP = 1.
    """
    M = lift_named("OR", "XOR", 2)
    return "OR", "XOR", 2, M, cover_number(M), frac_cover(M)


def resolution() -> str:
    """Verdetto in chiaro della killer search (testo)."""
    fname, gname, k, M, cov, lp = smallest_lift_counterexample()
    closed, pairs, mult = tensor_closure_holds()
    sm = smallest_gap_matrix()
    lines = []
    lines.append("EXACTNESS COMPOSES -- verdetto della killer search")
    lines.append("")
    lines.append("(1) Esiste un gap di integralita'? SI, il minimo e' 4x4:")
    if sm:
        M0, g0 = sm
        for row in M0:
            lines.append("        " + " ".join(map(str, row)))
        lines.append(f"    G* = {g0}  (nessun gap a dimensione <= 3x5; esaustivo)")
    lines.append("")
    lines.append("(2) Versione MATRICE∘MATRICE (tensore di Kronecker):")
    lines.append(f"    {pairs} coppie integrali testate; chiusa = {closed}; "
                 f"LP moltiplicativa = {mult}.")
    lines.append("    => VERA, ma corollario di LP(A⊗B)=LP(A)·LP(B) (Lovasz) +")
    lines.append("       Cov(A⊗B) <= Cov(A)·Cov(B). NON e' contenuto nuovo.")
    lines.append("")
    lines.append("(3) Versione GADGET-SUBSTITUTION (lift, l'arena intesa): FALSA.")
    lines.append(f"    Controesempio minimo: f={fname}_2 (G*_query=0) o gadget "
                 f"g={gname} (G*_comm=0),")
    lines.append("    lift = matrice di DISUGUAGLIANZA J - I_4:")
    for row in M:
        lines.append("        " + " ".join(map(str, row)))
    lines.append(f"    Cov = {cov},  LP = {lp},  G* = {cov - lp} > 0.")
    lines.append("    Il gap NASCE nel lift query->comunicazione (dove la composizione")
    lines.append("    e' lossy), esattamente dove la memoria lo prevedeva (il '+1').")
    lines.append("")
    lines.append("VERDETTO: congettura UCCISA. L'unica forma vera (tensore) e' un")
    lines.append("restatement della moltiplicativita' LP; la forma intesa (lift) e' falsa")
    lines.append("su 4 bit. Nessun nuovo potere predittivo: collasso pulito (spec sec. 9).")
    return "\n".join(lines)
