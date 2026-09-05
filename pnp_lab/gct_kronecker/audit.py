"""Audit meccanico dei valori Kronecker hardcoded nel corpus (STATE.md).

Per ogni voce del corpus estrae:
  - partizione lambda
  - valore scritto (stated)
  - fonte (Entry/Congettura in STATE.md)

Ricalcola tramite g_fast (aritmetica intera esatta, Murnaghan-Nakayama)
e riporta MATCH / MISMATCH.

Scope:
  - d <= 21 : sempre audited
  - d == 24 : audited se il calcolo termina in < 120 s (incluso qui)
  - d >= 25  : NON-AUDITED (annotato con motivo)

Per R = g * d! / f^3 usa Fraction esatta (frame_robinson_thrall disponibile
in crossing.py).

Struttura del modulo:
  CORPUS     : lista dichiarativa di AuditEntry
  audit_all  : ricalcola ogni entry e ritorna AuditResult per ciascuna
  tabella    : stampa la tabella formattata su stdout
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from math import factorial
from typing import List, Optional, Tuple

from .crossing import frame_robinson_thrall
from .fast import g_fast

Partition = Tuple[int, ...]

# ---------------------------------------------------------------------------
# Costanti
# ---------------------------------------------------------------------------
MAX_SCOPE_D: int = 24   # d <= 24 audited; d >= 25 NON-AUDITED
TIMEOUT_SEC: float = 120.0  # timeout per singolo calcolo (g_fast d=24)


# ---------------------------------------------------------------------------
# Strutture dati
# ---------------------------------------------------------------------------

@dataclass
class AuditEntry:
    """Una voce hardcoded nel corpus STATE.md da verificare.

    Campi:
      fonte        : identificatore nel corpus (es. 'C49 c=2', 'STAIRCASE k=4')
      lam          : partizione lambda (tupla di interi)
      stated_g     : valore g dichiarato in STATE.md (None se ambiguo)
      stated_R     : valore R dichiarato (float approssimato, se presente)
      is_R_entry   : True se il valore da verificare e' R = g*d!/f^3, non g diretto
      ambiguo      : True se la partizione o il valore non e' identificabile con certezza
      nota         : nota libera (spiegazione ambiguita', NON-AUDITED ecc.)
    """
    fonte: str
    lam: Optional[Partition]
    stated_g: Optional[int]
    stated_R: Optional[float] = None
    is_R_entry: bool = False
    ambiguo: bool = False
    nota: str = ""


@dataclass
class AuditResult:
    """Risultato di un'audit su una AuditEntry."""
    entry: AuditEntry
    computed_g: Optional[int]         # g_fast ricomputato (None se non audited)
    computed_R: Optional[Fraction]    # R ricomputato (None se non R-entry o non audited)
    stato: str                        # 'MATCH', 'MISMATCH', 'NON-AUDITED', 'AMBIGUO'
    elapsed_sec: float = 0.0


# ---------------------------------------------------------------------------
# Corpus dichiarativo — tutti i valori hardcoded di g in STATE.md d<=21
# ---------------------------------------------------------------------------

def _build_corpus() -> List[AuditEntry]:
    """Costruisce la lista dichiarativa delle voci del corpus STATE.md.

    Ogni voce corrisponde a un valore numerico esplicito di g o R
    nel testo di STATE.md (sezione 'Sequenze chiave', 'Spettro', 'Congetture').

    Convenzione notazione STATE.md:
      (c^2)  = partizione (c, c)
      (c^3)  = partizione (c, c, c)
      (c^4)  = partizione (c, c, c, c)
      (k^k)  = partizione (k, k, ..., k) con k parti
      (3^k)  = partizione (3, 3, ..., 3) con k parti di 3
      delta_k = staircase (k, k-1, ..., 2, 1)
      s_3(k) = lim_{a->inf} g((a, 3^k)^3) = lim g((a, 3, 3, ..., 3)^3) k volte 3
    """
    entries: List[AuditEntry] = []

    # ------------------------------------------------------------------
    # C49: g((c^2)^3) = 0 c dispari, 1 c pari   (verificato c=1..13)
    # Fonte: STATE riga 39, 53
    # d = 2c, scope: d<=21 => c<=10; c=11 d=22 > 21 -> NON-AUDITED
    # ------------------------------------------------------------------
    for c in range(1, 11):  # c=1..10, d=2..20 <=21
        lam = (c, c)
        exp = 0 if c % 2 == 1 else 1
        entries.append(AuditEntry(
            fonte=f"C49 c={c}",
            lam=lam,
            stated_g=exp,
            nota=f"g(({c}^2)^3); d={2*c}",
        ))
    # c=11..13 d=22..26 fuori scope <=21; c=14 wall (indicato in STATE)
    for c in [11, 12, 13]:
        entries.append(AuditEntry(
            fonte=f"C49 c={c}",
            lam=(c, c),
            stated_g=0 if c % 2 == 1 else 1,
            nota=f"d={2*c} > 21 -> NON-AUDITED (scope limit)",
        ))

    # ------------------------------------------------------------------
    # C50: g((c^3)^3) = floor(c/3) dispari, c/2 pari   (c=1..9, wall c=10)
    # Fonte: STATE riga 40, 54
    # d = 3c, scope: d<=21 => c<=7
    # ------------------------------------------------------------------
    c50_stated = {1: 0, 2: 1, 3: 1, 4: 2, 5: 1, 6: 3, 7: 2}
    for c in range(1, 8):  # d=3..21
        lam = (c, c, c)
        exp = c // 3 if c % 2 == 1 else c // 2
        entries.append(AuditEntry(
            fonte=f"C50 c={c}",
            lam=lam,
            stated_g=c50_stated[c],
            nota=f"g(({c}^3)^3); d={3*c}; formula predice {exp}",
        ))
    # c=8 d=24: incluso (scope d<=24)
    entries.append(AuditEntry(
        fonte="C50 c=8",
        lam=(8, 8, 8),
        stated_g=4,   # formula c/2=4 per c=8 pari
        nota="d=24 incluso (<=24); C50 predice c/2=4",
    ))
    # c=9 d=27 e c=10 d=30: fuori scope
    for c in [9, 10]:
        entries.append(AuditEntry(
            fonte=f"C50 c={c}",
            lam=(c, c, c),
            stated_g=c // 3 if c % 2 == 1 else c // 2,
            nota=f"d={3*c} > 24 -> NON-AUDITED",
        ))

    # ------------------------------------------------------------------
    # C51: g((3^k)^3): 1,0,1,1,2,1,0,1,1  (k=1..9)
    # (3^k) = partizione con k parti uguali a 3; d = 3k
    # Fonte: STATE riga 41, 56
    # d<=21 => k<=7; k=8 d=24 incluso; k=9 d=27 fuori
    # ------------------------------------------------------------------
    c51_stated = {1: 1, 2: 0, 3: 1, 4: 1, 5: 2, 6: 1, 7: 0, 8: 1, 9: 1}
    for k in range(1, 8):  # k=1..7 d=3..21
        lam = (3,) * k
        entries.append(AuditEntry(
            fonte=f"C51 k={k}",
            lam=lam,
            stated_g=c51_stated[k],
            nota=f"g((3^{k})^3); d={3*k}; C51 zeri a k=2,7 (k≡2 mod 5)",
        ))
    # k=8 d=24 incluso
    entries.append(AuditEntry(
        fonte="C51 k=8",
        lam=(3,) * 8,
        stated_g=c51_stated[8],
        nota="d=24 incluso (<=24)",
    ))
    # k=9 d=27 fuori scope
    entries.append(AuditEntry(
        fonte="C51 k=9",
        lam=(3,) * 9,
        stated_g=c51_stated[9],
        nota="d=27 > 24 -> NON-AUDITED",
    ))

    # ------------------------------------------------------------------
    # C53: g((k^k)^3) = F(3k-7) per k>=2:  sequenza 1,1,5,21 per k=2..5
    # Fonte: STATE riga 43, 52
    # k=2: d=4, k=3: d=9, k=4: d=16, k=5: d=25 (>21; fuori scope)
    # ------------------------------------------------------------------
    # Fibonacci: F(-1)=1,F(0)=1,F(1)=1,F(2)=1,F(3)=2,F(4)=3,F(5)=5,F(6)=8,F(7)=13,F(8)=21
    fib_vals = {-1: 1, 0: 1, 1: 1, 2: 1, 3: 2, 4: 3, 5: 5, 6: 8, 7: 13, 8: 21}
    c53_stated = {2: 1, 3: 1, 4: 5, 5: 21}
    for k in [2, 3, 4]:  # d=4,9,16 <=21
        lam = (k,) * k
        n = 3 * k - 7
        entries.append(AuditEntry(
            fonte=f"C53 k={k}",
            lam=lam,
            stated_g=c53_stated[k],
            nota=f"g(({k}^{k})^3); d={k*k}; C53: F({n})={fib_vals.get(n, '?')}",
        ))
    # k=5 d=25 fuori scope
    entries.append(AuditEntry(
        fonte="C53 k=5",
        lam=(5,) * 5,
        stated_g=21,
        nota="d=25 > 24 -> NON-AUDITED (C53 verificata da Entry 59; valore 21=F(8))",
    ))

    # ------------------------------------------------------------------
    # Staircase delta_k: g(delta_k^3): 1,1,5,117,18269,24891165 (k=1..6)
    # Fonte: STATE riga 64, 86
    # delta_k = (k, k-1, ..., 1), d = k*(k+1)/2
    # k=1:d=1, k=2:d=3, k=3:d=6, k=4:d=10, k=5:d=15, k=6:d=21 <=21 tutti ok
    # ------------------------------------------------------------------
    stair_stated = {1: 1, 2: 1, 3: 5, 4: 117, 5: 18269, 6: 24891165}
    for k in range(1, 7):
        lam = tuple(range(k, 0, -1))
        d_k = k * (k + 1) // 2
        entries.append(AuditEntry(
            fonte=f"STAIRCASE delta_{k}",
            lam=lam,
            stated_g=stair_stated[k],
            nota=f"g(delta_{k}^3); d={d_k}",
        ))

    # ------------------------------------------------------------------
    # C52 (FALSIFICATA F68): serie (c^4) dispari c=1,3,5: 0,1,4
    # g((7^4)^3)=21 (il valore falsificante) - d=28 NON-AUDITED
    # Fonte: STATE riga 42, 66
    # ------------------------------------------------------------------
    c52_c_vals = {1: 0, 3: 1, 5: 4}  # d=4,12,20
    for c, gval in c52_c_vals.items():
        entries.append(AuditEntry(
            fonte=f"C52/F68 c={c} (c^4)",
            lam=(c,) * 4,
            stated_g=gval,
            nota=f"serie dispari g(({c}^4)^3); d={4*c}; C52 falsificata da F68",
        ))
    # c=7 d=28 NON-AUDITED
    entries.append(AuditEntry(
        fonte="C52/F68 c=7 (7^4)",
        lam=(7,) * 4,
        stated_g=21,
        nota="d=28 >= 25 -> NON-AUDITED (valore falsificante di C52)",
    ))

    # ------------------------------------------------------------------
    # Spettro d=10 (STATE righe 102-103): R per 2 shape SC
    # ------------------------------------------------------------------
    # (5,2,1,1,1): hooks {9,1}, R=0.8475 = 21*10!/448^3
    entries.append(AuditEntry(
        fonte="SPETTRO d=10 (5,2,1,1,1)",
        lam=(5, 2, 1, 1, 1),
        stated_g=21,
        stated_R=0.8475,
        is_R_entry=True,
        nota="d=10; g=21 e R=0.8475 (arrotondato 4 dec)",
    ))
    # (4,3,2,1) = delta_4: hooks {7,3}, R=0.9373 = 117*10!/768^3
    entries.append(AuditEntry(
        fonte="SPETTRO d=10 delta_4=(4,3,2,1)",
        lam=(4, 3, 2, 1),
        stated_g=117,
        stated_R=0.9373,
        is_R_entry=True,
        nota="d=10; delta_4; g=117 e R=0.9373",
    ))

    # ------------------------------------------------------------------
    # Spettro d=13 (STATE righe 104-106): R per 3 shape
    # ------------------------------------------------------------------
    # (7,1^6): hooks {13}, R=7.8934
    entries.append(AuditEntry(
        fonte="SPETTRO d=13 (7,1^6)",
        lam=(7, 1, 1, 1, 1, 1, 1),
        stated_g=1,
        stated_R=7.8934,
        is_R_entry=True,
        nota="d=13; g=1; R=7.8934",
    ))
    # (5,3,3,1,1): hooks {9,3,1}, R=1.0019
    entries.append(AuditEntry(
        fonte="SPETTRO d=13 (5,3,3,1,1)",
        lam=(5, 3, 3, 1, 1),
        stated_g=661,
        stated_R=1.0019,
        is_R_entry=True,
        nota="d=13; g=661; R=1.0019",
    ))
    # (4,4,3,2): hooks {7,5,1}, R=0.8380 (CORRETTO da F64)
    entries.append(AuditEntry(
        fonte="SPETTRO d=13 (4,4,3,2)",
        lam=(4, 4, 3, 2),
        stated_g=85,
        stated_R=0.8380,
        is_R_entry=True,
        nota="d=13; R=0.8380; corretto da F64",
    ))

    # ------------------------------------------------------------------
    # Spettro d=15 (STATE righe 107-110): R per 4 shape
    # ------------------------------------------------------------------
    # (8,1^7): hooks {15}, R=32.3488
    entries.append(AuditEntry(
        fonte="SPETTRO d=15 (8,1^7)",
        lam=(8, 1, 1, 1, 1, 1, 1, 1),
        stated_g=1,
        stated_R=32.3488,
        is_R_entry=True,
        nota="d=15; g=1; R=32.3488",
    ))
    # (6,3,3,1,1,1): hooks {11,3,1}, R=0.9924 (CORRETTO da F64)
    entries.append(AuditEntry(
        fonte="SPETTRO d=15 (6,3,3,1,1,1)",
        lam=(6, 3, 3, 1, 1, 1),
        stated_g=2881,
        stated_R=0.9924,
        is_R_entry=True,
        nota="d=15; g=2881; R=0.9924; corretto da F64",
    ))
    # (5,4,3,2,1) = delta_5: hooks {9,5,1}, R=0.9511
    entries.append(AuditEntry(
        fonte="SPETTRO d=15 delta_5=(5,4,3,2,1)",
        lam=(5, 4, 3, 2, 1),
        stated_g=18269,
        stated_R=0.9511,
        is_R_entry=True,
        nota="d=15; delta_5; g=18269; R=0.9511",
    ))
    # (4,4,4,3): hooks {7,5,3}, R=0.8488 (CORRETTO da F64)
    entries.append(AuditEntry(
        fonte="SPETTRO d=15 (4,4,4,3)",
        lam=(4, 4, 4, 3),
        stated_g=9,
        stated_R=0.8488,
        is_R_entry=True,
        nota="d=15; g=9; R=0.8488; corretto da F64",
    ))

    # ------------------------------------------------------------------
    # Spettro d=21 self-conjugate (STATE righe 88-97): R per 8 shape
    # ------------------------------------------------------------------
    # (11,1^10): hooks {21}, R=8101.18
    entries.append(AuditEntry(
        fonte="SPETTRO d=21 (11,1^10)",
        lam=(11,) + (1,) * 10,
        stated_g=1,
        stated_R=8101.18,
        is_R_entry=True,
        nota="d=21; 1-hook SC; g=1; R=8101.18 (2 dec)",
    ))
    # hooks {17,3,1} -> (9,3,3,1,1,1,1,1,1): R=1.93
    entries.append(AuditEntry(
        fonte="SPETTRO d=21 hooks{17,3,1}",
        lam=(9, 3, 3, 1, 1, 1, 1, 1, 1),
        stated_g=8013,
        stated_R=1.93,
        is_R_entry=True,
        nota="d=21; hooks {17,3,1}; g=8013; R=1.93 (2 dec)",
    ))
    # hooks {15,5,1} -> (8,4,3,2,1,1,1,1): R=1.04
    entries.append(AuditEntry(
        fonte="SPETTRO d=21 hooks{15,5,1}",
        lam=(8, 4, 3, 2, 1, 1, 1, 1),
        stated_g=3759213,
        stated_R=1.04,
        is_R_entry=True,
        nota="d=21; hooks {15,5,1}; R=1.04 (2 dec arrotondato da 1.0352)",
    ))
    # hooks {13,7,1} -> (7,5,3,2,2,1,1): R=0.997
    entries.append(AuditEntry(
        fonte="SPETTRO d=21 hooks{13,7,1}",
        lam=(7, 5, 3, 2, 2, 1, 1),
        stated_g=27329601,
        stated_R=0.997,
        is_R_entry=True,
        nota="d=21; hooks {13,7,1}; R=0.997 (3 dec)",
    ))
    # hooks {13,5,3} -> (7,4,4,3,1,1,1): R=0.998
    entries.append(AuditEntry(
        fonte="SPETTRO d=21 hooks{13,5,3}",
        lam=(7, 4, 4, 3, 1, 1, 1),
        stated_g=4420601,
        stated_R=0.998,
        is_R_entry=True,
        nota="d=21; hooks {13,5,3}; R=0.998 (3 dec)",
    ))
    # hooks {11,9,1} -> (6,6,3,2,2,2): R=0.993
    entries.append(AuditEntry(
        fonte="SPETTRO d=21 hooks{11,9,1}",
        lam=(6, 6, 3, 2, 2, 2),
        stated_g=411081,
        stated_R=0.993,
        is_R_entry=True,
        nota="d=21; hooks {11,9,1}; R=0.993 (3 dec)",
    ))
    # hooks {11,7,3} = delta_6 -> (6,5,4,3,2,1): R=0.954
    entries.append(AuditEntry(
        fonte="SPETTRO d=21 hooks{11,7,3}=delta_6",
        lam=(6, 5, 4, 3, 2, 1),
        stated_g=24891165,
        stated_R=0.954,
        is_R_entry=True,
        nota="d=21; delta_6 staircase; g=24891165; R=0.954 (3 dec)",
    ))
    # hooks {9,7,5} -> (5,5,5,3,3): R=0.838
    entries.append(AuditEntry(
        fonte="SPETTRO d=21 hooks{9,7,5}",
        lam=(5, 5, 5, 3, 3),
        stated_g=5453,
        stated_R=0.838,
        is_R_entry=True,
        nota="d=21; hooks {9,7,5}; R=0.838 (3 dec)",
    ))

    # ------------------------------------------------------------------
    # s_3(k) = lim_{a->inf} g((a,3^k)^3) — valori stabili per a grande
    # Fonte: STATE riga 57; verificati con a=10..12 (stabili)
    # s_3(1)=2, s_3(2)=14, s_3(3)=158
    # Usare a=10 come proxy del limite (stabile già da a~7)
    # ------------------------------------------------------------------
    # Nota: qui audito il VALORE LIMITE, non un singolo g(lam,lam,lam).
    # Uso (a=10, 3^k) come partizione rappresentativa.
    s3_stated = {1: 2, 2: 14, 3: 158}
    for k, val in s3_stated.items():
        a = 10
        lam = (a,) + (3,) * k
        entries.append(AuditEntry(
            fonte=f"s3({k}) stabile a=10",
            lam=lam,
            stated_g=val,
            nota=f"s_3({k})=lim g((a,3^{k})^3); verifica con a={a}, d={a+3*k}",
        ))
    # s_3(4)=1497: d=a+12; a=10 -> d=22 > 21 ma <=24 -> includo
    entries.append(AuditEntry(
        fonte="s3(4) stabile a=10",
        lam=(10,) + (3,) * 4,
        stated_g=1497,
        nota="s_3(4)=1497; a=10, d=22 incluso (<=24)",
    ))
    # s_3(5)~10826: speculativo, d=a+15 a=10->d=25 > 24 -> NON-AUDITED
    entries.append(AuditEntry(
        fonte="s3(5) stabile",
        lam=None,
        stated_g=None,
        ambiguo=True,
        nota="s_3(5)~10826 SPECULATIVO (C54, non verificato); d>=25 -> NON-AUDITED",
    ))

    return entries


# Corpus globale
CORPUS: List[AuditEntry] = _build_corpus()


# ---------------------------------------------------------------------------
# Funzione di audit singolo
# ---------------------------------------------------------------------------

def _audit_entry(entry: AuditEntry) -> AuditResult:
    """Ricalcola g_fast per una AuditEntry e restituisce AuditResult.

    Gestione dei casi:
      - ambiguo=True     -> stato='AMBIGUO', no calcolo
      - lam None         -> stato='AMBIGUO'
      - d > MAX_SCOPE_D  -> stato='NON-AUDITED'
      - otherwise        -> calcola g_fast, confronta stated_g e stated_R
    """
    if entry.ambiguo or entry.lam is None:
        return AuditResult(entry=entry, computed_g=None, computed_R=None,
                           stato="AMBIGUO")

    d = sum(entry.lam)
    if d > MAX_SCOPE_D:
        return AuditResult(entry=entry, computed_g=None, computed_R=None,
                           stato="NON-AUDITED")

    # Calcolo g_fast con timeout empirico tramite misurazione time
    t0 = time.perf_counter()
    computed_g = g_fast(entry.lam, entry.lam, entry.lam)
    elapsed = time.perf_counter() - t0

    # Calcolo R se richiesto
    computed_R: Optional[Fraction] = None
    if entry.is_R_entry:
        f_lam = frame_robinson_thrall(entry.lam)
        d_fact = factorial(d)
        computed_R = Fraction(computed_g * d_fact, f_lam ** 3)

    # Confronto
    g_ok = (entry.stated_g is None) or (computed_g == entry.stated_g)

    if entry.is_R_entry and entry.stated_R is not None:
        # Tolleranza: STATE usa arrotondamento 2-4 decimali.
        # Consideriamo MATCH se |R_stated - R_computed| <= 0.5 * 10^{-decimals}
        # Dove decimals = len di cifre dopo la virgola nel valore stated
        r_stated_str = str(entry.stated_R)
        decimals = len(r_stated_str.split(".")[-1]) if "." in r_stated_str else 0
        tol = 0.5 * (10 ** (-decimals))
        r_ok = abs(float(computed_R) - entry.stated_R) <= tol
    else:
        r_ok = True

    stato = "MATCH" if (g_ok and r_ok) else "MISMATCH"
    return AuditResult(entry=entry, computed_g=computed_g, computed_R=computed_R,
                       stato=stato, elapsed_sec=elapsed)


# ---------------------------------------------------------------------------
# Audit completo
# ---------------------------------------------------------------------------

def audit_all() -> List[AuditResult]:
    """Esegue l'audit su tutte le voci del CORPUS.

    Ritorna la lista di AuditResult nell'ordine del CORPUS.
    """
    results: List[AuditResult] = []
    for entry in CORPUS:
        result = _audit_entry(entry)
        results.append(result)
    return results


# ---------------------------------------------------------------------------
# Stampa tabella
# ---------------------------------------------------------------------------

def tabella(results: Optional[List[AuditResult]] = None) -> None:
    """Stampa la tabella di audit su stdout (utf-8 riconfigurato).

    Colonne: fonte | partizione | d | scritto_g | ricomputato_g | R_stated | R_comp | STATO
    """
    sys.stdout.reconfigure(encoding="utf-8")
    if results is None:
        results = audit_all()

    # Intestazione
    sep = "-" * 110
    print("=" * 110)
    print("AUDIT coefficienti Kronecker — corpus STATE.md")
    print(f"Scope: d <= {MAX_SCOPE_D} audited | d > {MAX_SCOPE_D} -> NON-AUDITED")
    print("=" * 110)
    fmt = "{:<35} {:>3}  {:>12}  {:>12}  {:>10}  {:>10}  {:>10}"
    print(fmt.format("fonte", "d", "stated_g", "comput_g", "R_stated", "R_comput", "STATO"))
    print(sep)

    match_count = 0
    mismatch_count = 0
    non_audited = 0
    ambiguo_count = 0

    for r in results:
        d = sum(r.entry.lam) if r.entry.lam is not None else -1
        d_str = str(d) if d >= 0 else "?"

        sg = str(r.entry.stated_g) if r.entry.stated_g is not None else "?"
        cg = str(r.computed_g) if r.computed_g is not None else "-"

        sr = f"{r.entry.stated_R:.4g}" if r.entry.stated_R is not None else "-"
        cr = f"{float(r.computed_R):.4g}" if r.computed_R is not None else "-"

        stato = r.stato
        marker = " <== MISMATCH!" if stato == "MISMATCH" else ""

        print(fmt.format(
            r.entry.fonte[:35], d_str, sg, cg, sr, cr, stato
        ) + marker)

        if stato == "MATCH":
            match_count += 1
        elif stato == "MISMATCH":
            mismatch_count += 1
        elif stato == "NON-AUDITED":
            non_audited += 1
        elif stato == "AMBIGUO":
            ambiguo_count += 1

    print(sep)
    print(f"\nRiepilogo:")
    print(f"  MATCH        : {match_count}")
    print(f"  MISMATCH     : {mismatch_count}")
    print(f"  NON-AUDITED  : {non_audited}")
    print(f"  AMBIGUO      : {ambiguo_count}")
    print(f"  TOTALE       : {len(results)}")

    if mismatch_count == 0:
        print(f"\n>>> corpus d<={MAX_SCOPE_D} VALIDATO (zero mismatch) <<<")
    else:
        print(f"\n>>> ATTENZIONE: {mismatch_count} MISMATCH trovati <<<")
        print("\nDettaglio mismatch:")
        for r in results:
            if r.stato == "MISMATCH":
                print(f"  {r.entry.fonte}")
                print(f"    lam={r.entry.lam}  d={sum(r.entry.lam)}")
                print(f"    stated_g={r.entry.stated_g}  computed_g={r.computed_g}")
                if r.computed_R is not None:
                    print(f"    stated_R={r.entry.stated_R}  computed_R={float(r.computed_R):.6f}")
                print(f"    nota: {r.entry.nota}")

    if non_audited > 0:
        print(f"\nVoci NON-AUDITED ({non_audited}):")
        for r in results:
            if r.stato == "NON-AUDITED":
                d = sum(r.entry.lam)
                print(f"  {r.entry.fonte}  d={d}  nota: {r.entry.nota}")

    print("=" * 110)
