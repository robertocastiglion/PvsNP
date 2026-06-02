"""Algebraic Separation — il cuore di query complexity di P^Ã ≠ NP^Ã.

Completa il Modulo 9: là si vedevano potenza e limite dell'accesso algebrico;
qui li si combina nella SEPARAZIONE vera e propria, nel modello a query.

  - ``separation`` : il modello (funzionali di valutazione χ_·(r)), il lato NP
                     (1 query), il lato P (lower bound κ via avversario di
                     cancellazione), tutto esatto.
  - ``barrier``    : la morale e il confine onesto (versione forte = AW, citata).
  - ``lab``        : ASCII + SVG del divario NP=1 vs P≥κ.
  - ``lift``       : il SOLLEVAMENTO (passo #1) — l'avversario di cancellazione
                     diventa il gadget di una diagonalizzazione che costruisce un
                     oracolo O e una lingua in NP^Ã \\ P^Ã.

ESEGUIAMO il cuore combinatorio e ora anche la diagonalizzazione (su macchine
concrete). Il teorema su TUTTE le macchine e la versione forte con communication
complexity (Aaronson–Wigderson) restano citati.
"""

from .separation import (
    CancellationAdversary,
    SeparationResult,
    all_field_points,
    all_boolean_oracles,
    chi_vector,
    evaluate,
    boolean_kernel_witness,
    kills_all_kernels,
    cancellation_example,
    deterministic_lower_bound,
    verify_nondet_one_query,
)
from .barrier import separation_summary
from .lab import ascii_separation, to_svg_separation, write_svg
from .lift import (
    NamedMachine,
    StageResult,
    LiftResult,
    NPCertificate,
    const_machine,
    cube_scan_machine,
    field_probe_machine,
    default_adversary_machines,
    diagonalize_stage,
    build_oracle,
    np_certificate,
    ascii_lift,
    to_svg_lift,
    lift_summary,
)

__all__ = [
    "CancellationAdversary",
    "SeparationResult",
    "all_field_points",
    "all_boolean_oracles",
    "chi_vector",
    "evaluate",
    "boolean_kernel_witness",
    "kills_all_kernels",
    "cancellation_example",
    "deterministic_lower_bound",
    "verify_nondet_one_query",
    "separation_summary",
    "ascii_separation",
    "to_svg_separation",
    "write_svg",
    # — sollevamento query → oracolo TM (passo #1) —
    "NamedMachine",
    "StageResult",
    "LiftResult",
    "NPCertificate",
    "const_machine",
    "cube_scan_machine",
    "field_probe_machine",
    "default_adversary_machines",
    "diagonalize_stage",
    "build_oracle",
    "np_certificate",
    "ascii_lift",
    "to_svg_lift",
    "lift_summary",
]
