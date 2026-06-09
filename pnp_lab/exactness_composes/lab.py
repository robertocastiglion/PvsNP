"""Render testuale del Modulo 18 (EXACTNESS COMPOSES) per la demo."""

from __future__ import annotations

from .gap import cover_number, frac_cover, gstar
from .search import (
    lift_counterexamples,
    resolution,
    smallest_gap_matrix,
    smallest_lift_counterexample,
)


def gap_table() -> str:
    """Tabella dei controesempi-lift (gadget integrale, gap aperto)."""
    rows = lift_counterexamples()
    out = ["  k   f       gadget   G*", "  " + "-" * 30]
    for fname, gname, k, gv in rows:
        out.append(f"  {k}   {fname:<6}  {gname:<6}   {gv}")
    return "\n".join(out)


def witness_note() -> str:
    """Dettaglio certificato del controesempio minimo."""
    fname, gname, k, M, cov, lp = smallest_lift_counterexample()
    out = []
    out.append(f"Controesempio minimo: f={fname}_2 ∘ g={gname}  =  J - I_4 (4x4)")
    out.append("")
    for row in M:
        out.append("    " + " ".join(map(str, row)))
    out.append("")
    out.append(f"  Cov(M) = {cov}   (copertura intera, set-cover esatto)")
    out.append(f"  LP(M)  = {lp}   (copertura frazionaria, simplesso razionale)")
    out.append(f"  G*(M)  = {gstar(M)}  > 0   => congettura FALSIFICATA")
    out.append("")
    out.append("  Certificato LP=3: peso 1/2 sui 6 rettangoli 2x2 bilanciati")
    out.append("  (R x C, |R|=|C|=2, R∩C=∅) copre ogni cella con peso esattamente 1.")
    out.append("  Cov=4: nessuna partizione delle 12 celle in tre rettangoli 2x2.")
    return "\n".join(out)


def report() -> str:
    return resolution()
