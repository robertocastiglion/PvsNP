"""Switching Lemma Lab — lo switching lemma di Håstad, in azione.

Estende il Modulo 6 oltre la profondità 2: invece di un solo lower bound esatto,
mostra il MECCANISMO che porta a «parità ∉ AC0». Si applicano restrizioni
casuali alle variabili e si misura come una DNF di larghezza piccola "si
semplifica" (la sua profondità di albero di decisione crolla), mentre la parità
resiste — la sua profondità resta uguale al numero di variabili libere.

  - ``restriction``    : restrizioni casuali ρ, DNF, restrizione/tabulazione.
  - ``decision_tree``  : profondità dell'albero di decisione OTTIMO D(f).
  - ``lab``            : l'esperimento (bound di Håstad verificato) + ASCII + SVG.
  - ``barrier``        : la morale, parità ∉ AC0.
"""

from .restriction import (
    Restriction,
    DNF,
    random_restriction,
    free_vars,
    restrict_dnf,
    eval_dnf,
    parity_value,
    tabulate,
    random_dnf,
)
from .decision_tree import optimal_dt_depth
from .lab import (
    SwitchingStats,
    run_switching,
    parity_depth_under_restriction,
    ascii_report,
    to_svg_contrast,
    write_svg,
)
from .barrier import switching_summary
from .circuit import (
    AC0Circuit,
    random_ac0,
    parity_as_dnf,
)
from .iterate import (
    RoundStat,
    IterationResult,
    ParityBound,
    iterate_collapse,
    iterate_collapse_joint,
    default_schedule,
    depth_reduction_demo,
    parity_lower_bound,
    ascii_report as ascii_report_iterated,
    bound_report,
    to_svg_trajectory,
    iterate_summary,
)

__all__ = [
    "Restriction",
    "DNF",
    "random_restriction",
    "free_vars",
    "restrict_dnf",
    "eval_dnf",
    "parity_value",
    "tabulate",
    "random_dnf",
    "optimal_dt_depth",
    "SwitchingStats",
    "run_switching",
    "parity_depth_under_restriction",
    "ascii_report",
    "to_svg_contrast",
    "write_svg",
    "switching_summary",
    # — switching iterato in profondità d (passo #2) —
    "AC0Circuit",
    "random_ac0",
    "parity_as_dnf",
    "RoundStat",
    "IterationResult",
    "ParityBound",
    "iterate_collapse",
    "iterate_collapse_joint",
    "default_schedule",
    "depth_reduction_demo",
    "parity_lower_bound",
    "ascii_report_iterated",
    "bound_report",
    "to_svg_trajectory",
    "iterate_summary",
]
