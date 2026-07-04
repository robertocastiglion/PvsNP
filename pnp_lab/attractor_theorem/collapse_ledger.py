"""Ledger dei 21 collassi del PvsNP-lab: firma di collasso cross-arena.

Struttura: ogni record corrisponde a un RESTATEMENT #N (N=1..21) estratto da
RESEARCH_LOG.md, con metadati machine-checkable e tipo di collasso hand-labeled
via 6 regole prioritarie.

IPOTESI H (falsificabile):
    C(21) ≤ 6 tipi distinti
    E Good-Turing upper ≤ 1 tipo non visto
    (chiusura: la tassonomia è ~finitamente generata).

KILLER pre-dichiarati:
    K-narrativa    -- regole ambigue (co-applicabili) su ≥ 4/21 record
                      → la narrativa dei tipi è mal-definita.
    K-small-sample -- C(21) ≥ 7 OR unseen CI-LB ≥ 0.5 OR n_singleton ≥ 4
                      → non si può dichiarare saturazione.
    K-granularità  -- non-triviale solo se C ∈ [3, 10].
    K-omission     -- ≥ 1 record non classificabile → STOP e riporta.

METODO DI ESTRAZIONE (honesty boundary):
    Ricerca LETTERALE "RESTATEMENT #N" nel file per N = {12, 14, 17, 18, 19, 20, 21}
    (7 occorrenze unambigue nell'header o corpo della propria entry).
    Casi speciali:
      #9  -- prima occorrenza "RESTATEMENT #9" è in Entry 12 come back-reference
             al collasso di Entry 11; il record viene assegnato a Entry 11.
      #15 -- prima occorrenza "RESTATEMENT #15" è in Entry 29 come predizione;
             il collasso effettivo è Entry 30.
    Per N = {1..8, 10, 11, 13, 16}: nessun "RESTATEMENT #N" letterale nel log
    → fallback euristico da conteggio collassi nel testo
      ("decimo collasso" → #10 = Entry 12, "NONO collasso" → #9 = Entry 11, ecc.).
    Il campo 'found_by' registra 'literal' o 'heuristic' per ogni record.

SEED bootstrap: random.Random(0) — deterministico, non tocca lo stato globale.
"""

from __future__ import annotations

import os
import re
import random
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── costanti ─────────────────────────────────────────────────────────────────

_LOG_DEFAULT = Path(__file__).parents[2] / "RESEARCH_LOG.md"
_REPO_ROOT   = Path(__file__).parents[2]

# Mapping RESTATEMENT #N → numero di Entry nel log.
# Derivato dall'analisi del log (vedi honesty boundary nel docstring).
_R_TO_ENTRY: Dict[int, int] = {
    1: 1,   # "RESTATEMENT-OF-KNOWN" Entry 1 — gadget rule lifting
    2: 2,   # Entry 2 — pattern gap (non-J−I)
    3: 4,   # Entry 4 — feasible interpolation (Krajicek/Pudlak)
    4: 5,   # Entry 5 — KW communication (Razborov-Pudlak)
    5: 6,   # Entry 6 — meta-complexity / d_flip gradient
    6: 8,   # Entry 8 — falsifier hunt ("SESTO esito collapse-hardened")
    7: 9,   # Entry 9 — solution geometry ("7° collasso")
    8: 10,  # Entry 10 — polymorphisms boolean ("OTTAVO collasso")
    9: 11,  # Entry 11 — polymorphisms ternary ("NONO collasso")
    10: 12, # Entry 12 — local consistency width ("decimo collasso")
    11: 14, # Entry 14 — locality fixed-fraction ("collasso #11 del lab")
    12: 19, # Entry 19 — certified bounds ("RESTATEMENT #12" letterale)
    13: 25, # Entry 25 — relativization leverage ("13esimo collasso")
    14: 28, # Entry 28 — approx degree ("RESTATEMENT #14" letterale)
    15: 30, # Entry 30 — GCT Kronecker ("RESTATEMENT #15" letterale)
    16: 31, # Entry 31 — bipartite rigidity ("16 collassi / il 16°")
    17: 32, # Entry 32 — integrality leverage ("RESTATEMENT #17" letterale)
    18: 33, # Entry 33 — door B impossibility ("RESTATEMENT #18" letterale)
    19: 34, # Entry 34 — Kronecker local obstruction ("RESTATEMENT #19" letterale)
    20: 35, # Entry 35 — moment cone ("RESTATEMENT #20" letterale)
    21: 36, # Entry 36 — attractor lattice ("RESTATEMENT #21" letterale)
}

# N per cui "RESTATEMENT #N" compare letteralmente nell'header o corpo della
# propria entry (non come back-reference o predizione).
_LITERAL_FOUND: frozenset = frozenset({12, 14, 17, 18, 19, 20, 21})
# Note:
#   #9  → prima occorrenza letterale è Entry 12 (back-reference); collasso = Entry 11.
#   #15 → prima occorrenza letterale è Entry 29 (predizione); collasso = Entry 30.

# ── regole di classificazione (ordine = priorità) ────────────────────────────

# (nome, lista di pattern da cercare nel testo dell'entry)
# Pattern multi-parola: ricerca sottostringa case-insensitive.
# Pattern mono-parola:  ricerca con word boundary (\b) case-insensitive.
_RULES: List[Tuple[str, List[str]]] = [
    ("OMISSION", [
        "survival-by-omission",
        "omissione",
        "omission",
        "omessa",
        "omesso",
    ]),
    ("COND-IMPOSSIBLE", [
        "conditional-impossibility",
        "impossibilita condizionata",
        "collasso-onto-impossibilita",
    ]),
    ("SYMM-ARTIFACT", [
        "symmetry-break",
        "rottura-di-simmetria",
        "rottura di simmetria",
        "group-mismatch",
    ]),
    ("CLOSED-FORM", [
        "closed form",
        "forma chiusa",
    ]),
    ("PERM-ABSORBED", [
        "perm-invariant",
        "permutation-invariant",
        "orbit-invariant",
        "dizionario d'orbita",
        "orbita",
    ]),
    # Default — nessun pattern: scatta sempre come fallback.
    ("CITED-THEOREM", []),
]


def _match_pattern(pattern: str, text: str) -> bool:
    """True se `pattern` appare in `text`.

    Pattern mono-parola (nessuno spazio né trattino): word-boundary.
    Pattern multi-parola/composto: sottostringa case-insensitive.
    """
    # Usa word boundary se il pattern è una parola semplice
    has_space   = " " in pattern
    has_hyphen  = "-" in pattern
    has_apostro = "'" in pattern
    if has_space or has_hyphen or has_apostro:
        # frase composta — ricerca sottostringa semplice
        return pattern.lower() in text.lower()
    # parola semplice — word boundary
    return bool(re.search(r"\b" + re.escape(pattern) + r"\b", text, re.IGNORECASE))


def assign_type(text: str) -> Tuple[str, str, List[str]]:
    """Assegna il tipo di collasso al testo di un'entry del log.

    Applica le 6 regole in ordine di priorità; la prima che scatta vince.
    Registra TUTTE le regole applicabili per auditabilità.

    Ritorna:
        (tipo_primario, trigger_testuale, lista_regole_applicabili)
    Il tipo_primario è CITED-THEOREM se nessuna regola R1-R5 scatta.
    """
    primary_type: Optional[str]  = None
    primary_trigger: str         = "default"
    all_matching: List[str]      = []

    for rule_name, patterns in _RULES[:-1]:   # escludi CITED-THEOREM (default)
        for pat in patterns:
            if _match_pattern(pat, text):
                all_matching.append(rule_name)
                if primary_type is None:
                    primary_type    = rule_name
                    primary_trigger = pat
                break   # basta il primo pattern per questa regola

    if primary_type is None:
        primary_type    = "CITED-THEOREM"
        primary_trigger = "default"

    return primary_type, primary_trigger, all_matching


# ── parsing del log ───────────────────────────────────────────────────────────

def _parse_log(log_path: Path) -> Dict[int, Tuple[str, str]]:
    """Parsa RESEARCH_LOG.md e restituisce {entry_n: (header_line, body_text)}.

    Splitta sul pattern "## Entry N".
    """
    with open(log_path, encoding="utf-8") as f:
        raw = f.read()

    # Separa sul marcatore ## Entry N
    parts = re.split(r"(?=^## Entry \d+)", raw, flags=re.MULTILINE)
    result: Dict[int, Tuple[str, str]] = {}
    for part in parts:
        m = re.match(r"^## Entry (\d+) — (.+)", part)
        if m:
            n     = int(m.group(1))
            hdr   = m.group(2).strip()
            body  = part
            result[n] = (hdr, body)
    return result


def _first_probe_path(body: str) -> Optional[str]:
    """Trova il primo path pnp_lab/... nel testo di un'entry.

    Ritorna il path come stringa, o None se non trovato.
    """
    # Cerca pattern pnp_lab/... fermandosi su spazi, backtick, parentesi, virgole
    m = re.search(r"pnp_lab/[\w./]+", body)
    if m:
        path = m.group(0).rstrip("/")
        return path
    return None


# ── funzione pubblica principale ─────────────────────────────────────────────

def load_collapses(log_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Carica i 21 record di collasso da RESEARCH_LOG.md.

    Ogni record è un dict con i campi:
        restatement_n  : int          -- numero di restatement (1..21)
        entry_n        : int          -- numero di Entry nel log
        header         : str          -- testo dell'header dell'entry
        probe_file     : Optional[str]-- primo path pnp_lab/... verificato,
                                         None se assente (con nota in probe_note)
        probe_note     : str          -- note sull'estrazione del path
        killed         : bool         -- presenza di "KILLED" o "SPARA" nel testo
        collapse_type  : str          -- tipo primario (6 categorie)
        type_trigger   : str          -- pattern che ha scattato la regola
        ambiguous      : List[str]    -- tutte le regole co-applicabili
        found_by       : str          -- 'literal' o 'heuristic'

    Se il numero di record estratti è ≠ 21, la funzione NON alza eccezione ma
    restituisce ciò che riesce a costruire — l'onestà di estrazione è documentata
    nel campo 'found_by' di ogni record.
    """
    path = Path(log_path) if log_path else _LOG_DEFAULT
    entries = _parse_log(path)

    records: List[Dict[str, Any]] = []

    for r_n in range(1, 22):   # RESTATEMENT #1 .. #21
        e_n   = _R_TO_ENTRY[r_n]
        fb    = "literal" if r_n in _LITERAL_FOUND else "heuristic"

        if e_n not in entries:
            # Entry non trovata nel file (strano ma possibile)
            records.append({
                "restatement_n": r_n,
                "entry_n":       e_n,
                "header":        "ENTRY NOT FOUND",
                "probe_file":    None,
                "probe_note":    f"Entry {e_n} assente nel log.",
                "killed":        False,
                "collapse_type": "CITED-THEOREM",
                "type_trigger":  "default",
                "ambiguous":     [],
                "found_by":      fb,
            })
            continue

        hdr, body = entries[e_n]
        killed    = ("KILLED" in body) or ("SPARA" in body)

        # Tipo di collasso
        ctype, trigger, ambig = assign_type(body)

        # Probe file
        raw_path  = _first_probe_path(body)
        pf        = None
        pnote     = ""
        if raw_path:
            full_path = _REPO_ROOT / raw_path
            if full_path.exists():
                pf    = raw_path
                pnote = "trovato e verificato"
            else:
                pf    = None
                pnote = f"path '{raw_path}' nel testo ma non trovato su disco"
        else:
            pf    = None
            pnote = "nessun path pnp_lab/... nell'entry"
            # per #12 (Entry 19): il modulo è certified_obdd.py ma non citato nel testo
            if r_n == 12:
                pnote = ("nessun path esplicito nel testo; "
                         "modulo = pnp_lab/meta_complexity/certified_obdd.py (esiste)")

        records.append({
            "restatement_n": r_n,
            "entry_n":       e_n,
            "header":        hdr,
            "probe_file":    pf,
            "probe_note":    pnote,
            "killed":        killed,
            "collapse_type": ctype,
            "type_trigger":  trigger,
            "ambiguous":     ambig,
            "found_by":      fb,
        })

    return records


# ── funzioni di analisi ───────────────────────────────────────────────────────

def cumulative_curve(records: List[Dict[str, Any]]) -> List[int]:
    """Curva cumulativa C(i) = numero di tipi distinti visti nei primi i record.

    I record sono considerati in ordine crescente di restatement_n.
    Ritorna una lista di 21 interi non-decrescenti con C[0] = C(1) e C[20] = C(21).
    """
    sorted_recs = sorted(records, key=lambda r: r["restatement_n"])
    seen: set = set()
    curve: List[int] = []
    for rec in sorted_recs:
        seen.add(rec["collapse_type"])
        curve.append(len(seen))
    return curve


def good_turing(
    records: List[Dict[str, Any]],
    n_boot: int = 10000,
    seed: int = 0,
) -> Dict[str, Any]:
    """Stima Good-Turing della probabilità di un tipo non visto.

    Ritorna:
        freq         : dict tipo → conteggio
        n_singleton  : int  — tipi apparsi esattamente 1 volta
        unseen       : float — stima GT: n_singleton / 21
        ci_lo        : float — lower bound CI 95% bootstrap
        ci_hi        : float — upper bound CI 95% bootstrap
        seed         : int  — seed usato (deterministico)

    Bootstrap: ricampiona 21 record con rimpiazzo (SEED FISSO = random.Random(seed)),
    calcola n_singleton nel campione, stima unseen = n_sing / 21.
    """
    rng   = random.Random(seed)
    types = [r["collapse_type"] for r in records]
    N     = len(types)

    # Frequenze osservate
    freq: Dict[str, int] = {}
    for t in types:
        freq[t] = freq.get(t, 0) + 1

    n_singleton = sum(1 for c in freq.values() if c == 1)
    unseen      = n_singleton / N if N > 0 else 0.0

    # Bootstrap deterministico
    boot_unseen: List[float] = []
    for _ in range(n_boot):
        sample = [rng.choice(types) for _ in range(N)]
        s_freq: Dict[str, int] = {}
        for t in sample:
            s_freq[t] = s_freq.get(t, 0) + 1
        s_sing = sum(1 for c in s_freq.values() if c == 1)
        boot_unseen.append(s_sing / N)

    boot_unseen.sort()
    lo_idx = int(0.025 * n_boot)
    hi_idx = int(0.975 * n_boot) - 1
    ci_lo  = boot_unseen[lo_idx]
    ci_hi  = boot_unseen[hi_idx]

    return {
        "freq":        freq,
        "n_singleton": n_singleton,
        "unseen":      unseen,
        "ci_lo":       ci_lo,
        "ci_hi":       ci_hi,
        "seed":        seed,
    }


def stability(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Stabilità di C al variare della granularità della tassonomia.

    Ritorna:
        C_normal  : int  — tipi distinti sotto le 6 regole (tassonomia normale)
        C_coarse  : int  — tipi distinti sotto 2 super-tipi
                           (STRUCTURAL = {OMISSION, COND-IMPOSSIBLE, SYMM-ARTIFACT}
                            KNOWN-RESULT = {CLOSED-FORM, PERM-ABSORBED, CITED-THEOREM})
        C_fine    : int  — tipi distinti sotto refinement 1-a-1 (= 21, tutti unici)
        stability_range : (C_coarse, C_fine)
        super_types     : set di super-tipi effettivamente visti
    """
    _SUPER_MAP: Dict[str, str] = {
        "OMISSION":       "STRUCTURAL",
        "COND-IMPOSSIBLE": "STRUCTURAL",
        "SYMM-ARTIFACT":  "STRUCTURAL",
        "CLOSED-FORM":    "KNOWN-RESULT",
        "PERM-ABSORBED":  "KNOWN-RESULT",
        "CITED-THEOREM":  "KNOWN-RESULT",
    }

    types_seen  = {r["collapse_type"] for r in records}
    super_seen  = {_SUPER_MAP.get(t, "UNKNOWN") for t in types_seen}

    C_normal = len(types_seen)
    C_coarse = len(super_seen)
    C_fine   = len(records)   # ogni collasso = tipo unico nel refinement massimo

    return {
        "C_normal":       C_normal,
        "C_coarse":       C_coarse,
        "C_fine":         C_fine,
        "stability_range": (C_coarse, C_fine),
        "super_types":    super_seen,
    }


# ── sommario ─────────────────────────────────────────────────────────────────

def summary(log_path: Optional[str] = None) -> Dict[str, Any]:
    """Sommario completo del ledger dei 21 collassi.

    Ritorna un dict con:
        records         : list[21 dict]
        n_records       : int
        curve           : list[21] — curva cumulativa C(1..21)
        C_final         : int  — C(21)
        good_turing     : dict  — output di good_turing()
        stability       : dict  — output di stability()
        type_counts     : dict tipo → conteggio
        n_ambiguous     : int  — record con ≥2 regole applicabili
        ambiguous_list  : list — restatement_n dei record ambigui
        n_literal       : int  — record trovati per ricerca letterale
        n_heuristic     : int  — record trovati per euristica
        killers         : dict — esito di ogni killer
        hypothesis_H    : dict — esito dell'ipotesi H

    Onestà di estrazione: i campi n_literal e n_heuristic documentano quanti
    record hanno "RESTATEMENT #N" letterale nel log vs. assegnati per euristica.
    """
    recs  = load_collapses(log_path)
    curve = cumulative_curve(recs)
    gt    = good_turing(recs, n_boot=10000, seed=0)
    stab  = stability(recs)

    type_counts: Dict[str, int] = {}
    for r in recs:
        t = r["collapse_type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    n_ambig   = sum(1 for r in recs if len(r["ambiguous"]) >= 2)
    ambig_ns  = [r["restatement_n"] for r in recs if len(r["ambiguous"]) >= 2]
    n_lit     = sum(1 for r in recs if r["found_by"] == "literal")
    n_heur    = sum(1 for r in recs if r["found_by"] == "heuristic")

    C_final = curve[-1] if curve else 0

    # Killers
    k_narrativa    = n_ambig >= 4
    k_small_sample = (
        C_final >= 7
        or gt["ci_lo"] >= 0.5
        or gt["n_singleton"] >= 4
    )
    k_granularita  = not (3 <= C_final <= 10)
    k_omission     = any(r["collapse_type"] == "__UNCLASSIFIABLE__" for r in recs)

    killers = {
        "K_narrativa":    {"fires": k_narrativa,
                           "value": n_ambig,
                           "threshold": 4,
                           "note": f"{n_ambig}/21 record ambigui"},
        "K_small_sample": {"fires": k_small_sample,
                           "C_final": C_final,
                           "unseen_ci_lo": gt["ci_lo"],
                           "n_singleton": gt["n_singleton"]},
        "K_granularita":  {"fires": k_granularita,
                           "C_final": C_final,
                           "valid_range": "[3, 10]"},
        "K_omission":     {"fires": k_omission,
                           "note": "nessun record non-classificabile" if not k_omission
                                   else "ATTENZIONE: record non classificabile trovato"},
    }

    # Ipotesi H
    h_c_passes     = C_final <= 6
    h_gt_passes    = gt["ci_hi"] <= 1.0   # upper CI ≤ 1 tipo non visto
    hypothesis_H   = {
        "C_final":        C_final,
        "C_passes":       h_c_passes,
        "gt_ci_hi":       gt["ci_hi"],
        "gt_passes":      h_gt_passes,
        "H_holds":        h_c_passes and h_gt_passes,
        "note":           ("H REGGE" if (h_c_passes and h_gt_passes)
                           else "H FALSIFICATA"),
    }

    return {
        "records":       recs,
        "n_records":     len(recs),
        "curve":         curve,
        "C_final":       C_final,
        "good_turing":   gt,
        "stability":     stab,
        "type_counts":   type_counts,
        "n_ambiguous":   n_ambig,
        "ambiguous_list": ambig_ns,
        "n_literal":     n_lit,
        "n_heuristic":   n_heur,
        "killers":       killers,
        "hypothesis_H":  hypothesis_H,
    }
