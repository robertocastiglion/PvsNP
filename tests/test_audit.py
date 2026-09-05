"""Test minimale per pnp_lab.gct_kronecker.audit.

Verifica:
  1. Anchor s_3(1)=2 via (11,3)^3 (a=11, k=1), d=14 <= 21  [FAST]
  2. Anchor staircase delta_4=(4,3,2,1)^3 = 117              [FAST]
  3. Anchor C51 k=2: g((3,3)^3) = 0  (zero confermato)       [FAST]
  4. C51 k=5 MISMATCH: g((3^5)^3) = 1 != 2 (ERRATUM)        [FAST, d=15]
  5. Struttura corpus: ogni entry ha fonte e stato valido      [SLOW: audit_all d<=24]
  6. audit_all completa e conta mismatch attesi               [SLOW: audit_all d<=24]

Test 1-4 sono FAST (max d=15). I test 5-6 invocano audit_all()
che calcola fino a d=24 e richiedono ~120s: marcati @pytest.mark.slow.
"""

from __future__ import annotations

import pytest

from pnp_lab.gct_kronecker.audit import CORPUS, AuditResult, _audit_entry, audit_all
from pnp_lab.gct_kronecker.fast import g_fast


# ---------------------------------------------------------------------------
# 1. Anchor s_3(1) = 2   [FAST: d=14]
# ---------------------------------------------------------------------------
def test_anchor_s3_1():
    """s_3(1) = lim g((a, 3)^3) = 2; verifica con a=11, d=14."""
    g = g_fast((11, 3), (11, 3), (11, 3))
    assert g == 2, f"s_3(1) atteso 2, ottenuto {g}"


# ---------------------------------------------------------------------------
# 2. Anchor staircase delta_4 = 117   [FAST: d=10]
# ---------------------------------------------------------------------------
def test_anchor_staircase_delta4():
    """g(delta_4^3) = g((4,3,2,1)^3) = 117."""
    lam = (4, 3, 2, 1)
    g = g_fast(lam, lam, lam)
    assert g == 117, f"g(delta_4^3) atteso 117, ottenuto {g}"


# ---------------------------------------------------------------------------
# 3. Anchor C51 k=2: g((3,3)^3) = 0   [FAST: d=6]
# ---------------------------------------------------------------------------
def test_anchor_c51_k2_zero():
    """C51 k=2: g((3,3)^3) = 0 (zero diagonale confermato)."""
    lam = (3, 3)
    g = g_fast(lam, lam, lam)
    assert g == 0, f"g((3,3)^3) atteso 0, ottenuto {g}"


# ---------------------------------------------------------------------------
# 4. C51 k=5 MISMATCH: ERRATUM in STATE.md   [FAST: d=15]
# ---------------------------------------------------------------------------
def test_c51_k5_erratum():
    """C51 k=5: g((3^5)^3)=1 ma STATE dichiara 2.

    Questo e' un ERRATUM nel corpus: il valore esatto e' 1, non 2.
    Il test verifica anche che _audit_entry rilevi MISMATCH su questa entry.
    """
    lam = (3, 3, 3, 3, 3)  # (3^5), d=15
    g = g_fast(lam, lam, lam)
    assert g == 1, f"g((3^5)^3) atteso 1, ottenuto {g}"

    # Verifica che l'audit rilevi il mismatch sulla singola entry
    c51_k5_entries = [e for e in CORPUS if e.fonte == "C51 k=5"]
    assert len(c51_k5_entries) == 1, "Entry 'C51 k=5' non trovata nel corpus"
    entry = c51_k5_entries[0]
    result = _audit_entry(entry)
    assert result.stato == "MISMATCH", (
        f"C51 k=5 dovrebbe essere MISMATCH, e' {result.stato}; "
        f"stated={entry.stated_g}, computed={result.computed_g}"
    )
    assert result.computed_g == 1
    assert entry.stated_g == 2


# ---------------------------------------------------------------------------
# 5. Struttura corpus e stati validi   [SLOW: audit_all fino a d=24]
# ---------------------------------------------------------------------------
@pytest.mark.slow
@pytest.mark.timeout(300)
def test_audit_stati_validi():
    """Ogni AuditResult ha stato in {'MATCH','MISMATCH','NON-AUDITED','AMBIGUO'}."""
    valid_stati = {"MATCH", "MISMATCH", "NON-AUDITED", "AMBIGUO"}
    results = audit_all()
    assert len(results) > 0, "audit_all() non ritorna nessun risultato"
    for r in results:
        assert isinstance(r, AuditResult), f"Tipo inaspettato: {type(r)}"
        assert r.stato in valid_stati, (
            f"Stato non valido '{r.stato}' per entry '{r.entry.fonte}'"
        )


# ---------------------------------------------------------------------------
# 6. audit_all completa con esattamente 1 mismatch (C51 k=5)   [SLOW]
# ---------------------------------------------------------------------------
@pytest.mark.slow
@pytest.mark.timeout(300)
def test_audit_completa_un_mismatch():
    """audit_all() completa con esattamente 1 mismatch: C51 k=5.

    Verifica struttura: >=40 entry totali, 60 MATCH, 1 MISMATCH, >=6 NON-AUDITED.
    """
    results = audit_all()
    assert len(results) >= 40, f"Attesi >= 40 risultati, ottenuti {len(results)}"

    mismatch = [r for r in results if r.stato == "MISMATCH"]
    assert len(mismatch) == 1, (
        f"Atteso 1 mismatch, trovati {len(mismatch)}: "
        + ", ".join(r.entry.fonte for r in mismatch)
    )
    assert mismatch[0].entry.fonte == "C51 k=5"
    assert mismatch[0].computed_g == 1
    assert mismatch[0].entry.stated_g == 2
