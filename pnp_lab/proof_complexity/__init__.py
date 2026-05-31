"""Modulo 5 — Proof Complexity Lab.

L'altra metà della storia. I Moduli 1–3 mostrano *perché* le tecniche
falliscono (le barriere). Questo modulo mostra un lower bound che **funziona
davvero**: ogni refutazione per resolution del principio della piccionaia cresce
in modo esponenziale (Haken 1985). Via Cook–Reckhow, lower bound forti per ogni
sistema di prova implicherebbero NP ≠ coNP, quindi P ≠ NP.
"""

from .formula import CNF, Clause, horn_chain_cnf, pigeonhole_cnf
from .resolution import RefutationResult, refute, resolve
from .dpll import DpllResult, dpll
from .lab import (
    GrowthRow,
    GrowthStudy,
    ascii_chart,
    run_growth_study,
    to_svg,
    write_svg,
)

__all__ = [
    "CNF",
    "Clause",
    "pigeonhole_cnf",
    "horn_chain_cnf",
    "resolve",
    "refute",
    "RefutationResult",
    "dpll",
    "DpllResult",
    "run_growth_study",
    "GrowthStudy",
    "GrowthRow",
    "ascii_chart",
    "to_svg",
    "write_svg",
]
