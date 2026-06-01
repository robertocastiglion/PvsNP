"""Algorithmic Method Lab — il metodo di Williams: «SAT veloce ⇒ lower bound».

L'unico approccio noto che ha rotto TUTTE e tre le barriere (relativizzazione,
natural proofs, algebrizzazione) e prodotto separazioni nuove (NEXP ⊄ ACC⁰,
2011). È la direzione più solida verso lower bound — pur restando lontana dal
risolvere P vs NP.

Rendiamo eseguibile il MECCANISMO, citando la matematica profonda:
  - ``speedup`` : il cuore — circuiti strutturati hanno polinomi sparsi, quindi
                  si conta #SAT su tutti i 2^n input senza enumerarli (esatto).
  - ``winwin``  : la catena 'speedup + NEXP⊆C ⇒ contraddizione con la gerarchia'
                  e la soglia super-polinomiale che la fa scattare.
  - ``barrier`` : perché aggira tutte e tre le barriere (e cosa resta citato).
  - ``lab``     : ASCII + SVG (la curva 2^n vs polinomio sparso).
"""

from .speedup import (
    SparsePoly,
    SatCount,
    count_bruteforce,
    count_fast,
    speedup_factor,
    conj_poly,
    disjoint_dnf_poly,
    or_poly,
)
from .winwin import (
    SpeedupClass,
    WinWin,
    standard_speedups,
    ratio_table,
    win_win,
    analyze_all,
)
from .barrier import BarrierEvasion, evasion_report, algorithmic_method_summary
from .lab import ascii_speedup, ascii_winwin, to_svg_speedup, write_svg

__all__ = [
    "SparsePoly", "SatCount", "count_bruteforce", "count_fast", "speedup_factor",
    "conj_poly", "disjoint_dnf_poly", "or_poly",
    "SpeedupClass", "WinWin", "standard_speedups", "ratio_table", "win_win", "analyze_all",
    "BarrierEvasion", "evasion_report", "algorithmic_method_summary",
    "ascii_speedup", "ascii_winwin", "to_svg_speedup", "write_svg",
]
