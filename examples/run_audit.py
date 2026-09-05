"""Demo: audit meccanico dei valori Kronecker hardcoded in STATE.md.

Stampa la tabella completa con colonne:
  fonte | d | stated_g | computed_g | R_stated | R_computed | STATO

Le voci con d > 24 sono NON-AUDITED (annotate con motivo).
Le voci ambigue (partizione non identificabile) sono AMBIGUO.

Uso:
    py -m examples.run_audit
    oppure
    py examples/run_audit.py
"""

import sys

sys.stdout.reconfigure(encoding="utf-8")

from pnp_lab.gct_kronecker.audit import audit_all, tabella

if __name__ == "__main__":
    results = audit_all()
    tabella(results)
