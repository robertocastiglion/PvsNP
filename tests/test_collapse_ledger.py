"""Test per pnp_lab/attractor_theorem/collapse_ledger.py.

Istanze minuscole dove possibile; quando necessita il log reale usa
la fixture `records` (caricata una volta sola per sessione).
Tutti i test sono deterministici e veloci (< 2s totali).
"""

import pytest
from pathlib import Path

from pnp_lab.attractor_theorem.collapse_ledger import (
    load_collapses,
    assign_type,
    cumulative_curve,
    good_turing,
    stability,
    summary,
    _R_TO_ENTRY,
    _LITERAL_FOUND,
)

_LOG_PATH = Path(__file__).parents[1] / "RESEARCH_LOG.md"


# ── fixture ───────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def records():
    """21 record caricati dal log reale (una volta per sessione)."""
    return load_collapses(str(_LOG_PATH))


# ── test 1: numero di record ──────────────────────────────────────────────────

def test_n_records(records):
    """Devono essere esattamente 21 record, uno per RESTATEMENT #1..#21."""
    assert len(records) == 21, (
        f"Attesi 21 record, trovati {len(records)}. "
        f"RESTATEMENT mancanti o duplicati nel log."
    )


# ── test 2: unicità e completezza dei numeri di RESTATEMENT ──────────────────

def test_unique_restatement_numbers(records):
    """I restatement_n devono essere esattamente {1, 2, ..., 21}, unici."""
    ns = [r["restatement_n"] for r in records]
    assert sorted(ns) == list(range(1, 22))


# ── test 3: assign_type deterministico ───────────────────────────────────────

def test_assign_type_deterministic():
    """Stessa stringa → stessa tripla (tipo, trigger, ambiguous) su due chiamate."""
    text = "RESTATEMENT #14 — approx degree orbital-dictionary PERM-INVARIANT witness"
    r1 = assign_type(text)
    r2 = assign_type(text)
    assert r1 == r2


# ── test 4: assign_type pattern OMISSION ─────────────────────────────────────

def test_assign_type_omission():
    """Testo con 'survival-by-omission' → tipo OMISSION, trigger corretto."""
    text = "killed by survival-by-omission of the Sperner law"
    tipo, trigger, rules = assign_type(text)
    assert tipo == "OMISSION"
    assert trigger == "survival-by-omission"


# ── test 5: assign_type pattern PERM-ABSORBED ────────────────────────────────

def test_assign_type_perm_absorbed():
    """Testo con 'perm-invariant' → tipo PERM-ABSORBED."""
    text = "the function is perm-invariant under the orbit action"
    tipo, trigger, rules = assign_type(text)
    assert tipo == "PERM-ABSORBED"


# ── test 6: assign_type default CITED-THEOREM ────────────────────────────────

def test_assign_type_default():
    """Testo senza pattern → tipo default CITED-THEOREM."""
    text = "some generic text about complexity theory and Boolean functions"
    tipo, trigger, rules = assign_type(text)
    assert tipo == "CITED-THEOREM"
    assert rules == []


# ── test 7: assign_type ambiguità multi-regola ───────────────────────────────

def test_assign_type_ambiguous():
    """Testo con 'omissione' e 'orbita' → OMISSION primario, entrambe in ambiguous."""
    text = "per omissione della legge di Sperner; l'orbita è invariante"
    tipo, trigger, regole = assign_type(text)
    assert tipo == "OMISSION"
    assert "OMISSION" in regole
    assert "PERM-ABSORBED" in regole
    assert len(regole) >= 2


# ── test 8: curva cumulativa monotona e lunghezza ─────────────────────────────

def test_cumulative_curve_monotone_length(records):
    """C(i) deve essere non-decrescente e di lunghezza 21."""
    curve = cumulative_curve(records)
    assert len(curve) == 21
    for i in range(1, 21):
        assert curve[i] >= curve[i - 1], (
            f"Curva non monotona in posizione {i}: {curve[i-1]} → {curve[i]}"
        )


# ── test 9: ipotesi H — C(21) ≤ 6 ───────────────────────────────────────────

def test_c_final_leq_6(records):
    """H richiede C(21) ≤ 6 tipi distinti."""
    curve = cumulative_curve(records)
    assert curve[-1] <= 6, f"C(21) = {curve[-1]} > 6: ipotesi H falsificata."


# ── test 10: stabilità — ordine di granularità ───────────────────────────────

def test_stability_range(records):
    """C_coarse ≤ C_normal ≤ C_fine con C_fine = 21."""
    stab = stability(records)
    assert stab["C_coarse"] <= stab["C_normal"] <= stab["C_fine"]
    assert stab["C_fine"] == 21   # ogni record = tipo unico nel refinement massimo


# ── test 11: Good-Turing — campi obbligatori e determinismo ──────────────────

def test_good_turing_fields_and_determinism(records):
    """good_turing restituisce tutti i campi attesi e il risultato è deterministico."""
    gt1 = good_turing(records, n_boot=100, seed=0)
    gt2 = good_turing(records, n_boot=100, seed=0)

    for key in ("freq", "n_singleton", "unseen", "ci_lo", "ci_hi", "seed"):
        assert key in gt1

    assert gt1 == gt2   # deterministico con stesso seed


# ── test 12: probe_file — esistenza su disco ──────────────────────────────────

def test_probe_file_existence(records):
    """Ogni record con probe_file != None deve puntare a un path esistente."""
    import os
    repo = Path(__file__).parents[1]
    for rec in records:
        if rec["probe_file"] is not None:
            full = repo / rec["probe_file"]
            assert full.exists(), (
                f"RESTATEMENT #{rec['restatement_n']}: "
                f"probe_file '{rec['probe_file']}' non trovato su disco."
            )


# ── test 13: tipi noti per record specifici ──────────────────────────────────

def test_known_types(records):
    """Verifica il tipo atteso per RESTATEMENT selezionati (hand-checked)."""
    rec_by_n = {r["restatement_n"]: r for r in records}

    # CITED-THEOREM attesi (nota: R1..R4 = pattern noti / gadget rule)
    for n in (1, 2, 3, 4):
        assert rec_by_n[n]["collapse_type"] == "CITED-THEOREM", (
            f"RESTATEMENT #{n}: atteso CITED-THEOREM, "
            f"trovato {rec_by_n[n]['collapse_type']}"
        )

    # PERM-ABSORBED attesi (orbita / perm-invariant)
    for n in (5, 6, 7):
        assert rec_by_n[n]["collapse_type"] == "PERM-ABSORBED", (
            f"RESTATEMENT #{n}: atteso PERM-ABSORBED, "
            f"trovato {rec_by_n[n]['collapse_type']}"
        )

    # SYMM-ARTIFACT atteso
    assert rec_by_n[19]["collapse_type"] == "SYMM-ARTIFACT", (
        f"RESTATEMENT #19: atteso SYMM-ARTIFACT, "
        f"trovato {rec_by_n[19]['collapse_type']}"
    )


# ── test 14: found_by per record noti ────────────────────────────────────────

def test_found_by_literal_vs_heuristic(records):
    """N in _LITERAL_FOUND devono avere found_by='literal'; gli altri 'heuristic'."""
    for rec in records:
        n  = rec["restatement_n"]
        fb = rec["found_by"]
        if n in _LITERAL_FOUND:
            assert fb == "literal", (
                f"RESTATEMENT #{n}: atteso found_by='literal', trovato '{fb}'"
            )
        else:
            assert fb == "heuristic", (
                f"RESTATEMENT #{n}: atteso found_by='heuristic', trovato '{fb}'"
            )


# ── test 15: Good-Turing n_singleton piccolo ─────────────────────────────────

def test_good_turing_n_singleton_low(records):
    """Il tipo SYMM-ARTIFACT appare una volta sola → n_singleton ≥ 1.
    K-small-sample richiede n_singleton < 4 per non falsificare H."""
    gt = good_turing(records, n_boot=100, seed=0)
    assert gt["n_singleton"] >= 1, "Almeno SYMM-ARTIFACT è singleton."
    assert gt["n_singleton"] < 4, (
        f"n_singleton = {gt['n_singleton']} ≥ 4: K-small-sample FIRES."
    )


# ── test 16: summary — esito completo ────────────────────────────────────────

def test_summary_hypothesis_H():
    """summary() deve dichiarare H_holds = True (C≤6 e gt_ci_hi≤1)."""
    s = summary()
    assert s["n_records"] == 21
    assert s["hypothesis_H"]["H_holds"], (
        f"Ipotesi H falsificata: {s['hypothesis_H']}"
    )
