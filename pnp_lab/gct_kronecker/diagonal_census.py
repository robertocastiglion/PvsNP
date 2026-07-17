"""Censimento dei vanishing DIAGONALI g(lambda,lambda,lambda)=0 e loro classificazione
(Entry 40).

Per ogni partizione lambda |- d (d=1..d_max) calcola g_fast(lam,lam,lam) e classifica
ogni zero contro le famiglie note (sign, two_row, hook, two_col, hook_conj, two_row_conj,
orbit_covered) riportando senza manipolazioni i casi 'uncovered'.

Struttura del modulo
--------------------
  diagonal_zeros(d_max) -> lista [(d, lam, g_val)]
      Tutte le terne (d, lambda, g) con g_fast(lam,lam,lam)==0.

  classify_diag(d, lam) -> str
      Classificazione del vanishing diagonale:
        'sign'          - lam = (1^d) (rappresentazione segno)
        'two_row'       - ell(lam) <= 2 (forma a due righe)
        'hook'          - lam = (a, 1^b) (forma ad uncino)
        'two_col'       - lam[0] <= 2 (forma a due colonne)
        'two_row_conj'  - la trasposta lam' e' two_row (=> lam e' two_col, step
                          ridondante ma esplicito per onesta')
        'hook_conj'     - la trasposta lam' e' hook
        'orbit_covered' - covered((lam,lam,lam)) == True (copertura da letteratura
                          via rappresentante nell'orbita g-simmetrica con >=2
                          argomenti di forma speciale)
        'uncovered'     - nessuna delle precedenti

  stretch_diagonal(lam, N=2) -> int o None
      g_fast(N*lam, N*lam, N*lam) se sum(lam)*N <= STRETCH_MAX_D, altrimenti None.
      Usato per verificare: g=0 con stretch>0 => HOLE (non-saturazione di Kronecker).

  summary(d_max=12) -> dict
      Stampa tabella e restituisce conteggi per categoria + lista 'uncovered'.

Confine di onesta':
    Il calcolo e' ESATTO (g_fast usa aritmetica intera pura via tavola dei caratteri
    di Murnaghan-Nakayama).  'covered' verifica la PRECONDIZIONE STRUTTURALE (>=2
    argomenti special_shape in un rappresentante g-simmetrico), non ricalcola i valori
    delle formule chiuse di Rosas / Bessenrodt-Bowman (quelli restano CITATI).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .fast import g_fast
from .kronecker import partitions, transpose
from .coverage import is_two_row, is_two_column, is_hook, covered

Partition = Tuple[int, ...]

# Limite superiore per il calcolo del tratto: sum(lam)*N <= STRETCH_MAX_D
# p(18)=385 e' ancora fattibile; p(20)~627 comincia ad essere lento.
STRETCH_MAX_D: int = 24


# --------------------------------------------------------------------------------------
#  Enumerazione degli zeri diagonali
# --------------------------------------------------------------------------------------
def diagonal_zeros(d_max: int = 12) -> List[Tuple[int, Partition, int]]:
    """Tutte le terne (d, lambda, g) con g_fast(lam,lam,lam)==0 per d=1..d_max.

    Per ogni d pre-calcola la tavola dei caratteri UNA volta (via g_fast -> character_table
    con memoizzazione), poi scorre le p(d) partizioni di d.

    Ritorna lista ordinata per d crescente, poi per ordine decrescente-lessicografico
    di lambda (l'ordine di partitions(d)).
    """
    result: List[Tuple[int, Partition, int]] = []
    for d in range(1, d_max + 1):
        for lam in partitions(d):
            g = g_fast(lam, lam, lam)
            if g == 0:
                result.append((d, lam, g))
    return result


# --------------------------------------------------------------------------------------
#  Classificazione di un vanishing diagonale
# --------------------------------------------------------------------------------------
def classify_diag(d: int, lam: Partition) -> str:
    """Classifica il vanishing diagonale g(lam,lam,lam)=0 contro le famiglie note.

    Gerarchia di test (nell'ordine, primo che scatta vince):
      1. sign          : lam == (1^d)
      2. two_row       : ell(lam) <= 2
      3. hook          : lam = (a, 1^b)
      4. two_col       : lam[0] <= 2  (parti massima <= 2)
      5. two_row_conj  : lam' e' two_row  (ridondante con step 4, ma esplicito)
      6. hook_conj     : lam' e' hook
      7. orbit_covered : covered((lam,lam,lam)) == True
      8. uncovered     : nessuna delle precedenti

    Nota: i passi 5/6 sono RIDONDANTI con 4 e 7 rispettivamente (is_two_column(lam)
    iff is_two_row(transpose(lam)), e i hook sono sempre covered), ma li teniamo
    espliciti per tracciabilita'.
    """
    # 1. Rappresentazione segno
    if lam == tuple([1] * d):
        return "sign"

    # 2. Two-row: al piu' due righe nel diagramma di Young
    if is_two_row(lam):
        return "two_row"

    # 3. Hook: (a, 1, 1, ..., 1)
    if is_hook(lam):
        return "hook"

    # 4. Two-column: parte massima <= 2
    if is_two_column(lam):
        return "two_col"

    # 5. Trasposta two-row (=> lam two-col; ridondante con step 4)
    lam_t = transpose(lam)
    if is_two_row(lam_t):
        return "two_row_conj"

    # 6. Trasposta hook
    if is_hook(lam_t):
        return "hook_conj"

    # 7. Copertura strutturale via orbita g-simmetrica
    if covered((lam, lam, lam)):
        return "orbit_covered"

    # 8. Genuinamente non coperto dalle famiglie note
    return "uncovered"


# --------------------------------------------------------------------------------------
#  Tratto diagonale
# --------------------------------------------------------------------------------------
def stretch_diagonal(lam: Partition, N: int = 2) -> Optional[int]:
    """g_fast(N*lam, N*lam, N*lam) se sum(lam)*N <= STRETCH_MAX_D, altrimenti None.

    Interpretazione:
      - None  : calcolo non eseguito (troppo lento / fuori soglia)
      - 0     : zero anche al tratto => possibile vanishing strutturale
      - > 0   : HOLE (g(lam,lam,lam)=0 ma g(N*lam,N*lam,N*lam)>0):
                restates la non-saturazione di Kronecker
                (Stembridge; Burgisser-Christandl-Ikenmeyer).
    """
    d = sum(lam)
    if d * N > STRETCH_MAX_D:
        return None
    scaled: Partition = tuple(x * N for x in lam)
    return g_fast(scaled, scaled, scaled)


# --------------------------------------------------------------------------------------
#  Sommario
# --------------------------------------------------------------------------------------
def summary(d_max: int = 12) -> Dict:
    """Enumera i vanishing diagonali g(lam,lam,lam)=0 per d=1..d_max, classifica
    ciascuno e stampa una tabella.

    Ritorna dict con chiavi:
      'd_max'         : d_max usato
      'total_zeros'   : numero totale di vanishing diagonali trovati
      'by_category'   : {categoria: conteggio}
      'uncovered'     : lista di (d, lam, stretch_g_or_None) per i casi 'uncovered'
      'all_zeros'     : lista di (d, lam, categoria, stretch_g_or_None)
    """
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    zeros = diagonal_zeros(d_max)
    rows = []
    for d, lam, _g in zeros:
        cat = classify_diag(d, lam)
        stretch = stretch_diagonal(lam, N=2)
        rows.append((d, lam, cat, stretch))

    # Conteggi per categoria
    by_cat: Dict[str, int] = {}
    for _d, _lam, cat, _s in rows:
        by_cat[cat] = by_cat.get(cat, 0) + 1

    uncovered_list = [
        (d, lam, stretch)
        for d, lam, cat, stretch in rows
        if cat == "uncovered"
    ]

    # Stampa tabella
    print("=" * 72)
    print(f"Censimento vanishing DIAGONALI g(lam,lam,lam)=0  (d=1..{d_max})")
    print("=" * 72)
    print(f"{'d':>3}  {'lambda':<30}  {'categoria':<16}  {'g(2lam,2lam,2lam)'}")
    print("-" * 72)
    prev_d = None
    for d, lam, cat, stretch in rows:
        if prev_d is not None and d != prev_d:
            print()
        stretch_str = str(stretch) if stretch is not None else "None (d*2>18)"
        marker = " <-- UNCOVERED" if cat == "uncovered" else ""
        print(f"{d:>3}  {str(lam):<30}  {cat:<16}  {stretch_str}{marker}")
        prev_d = d

    print("-" * 72)
    print(f"\nTotale vanishing diagonali: {len(rows)}")
    print("\nConteggi per categoria:")
    for cat, cnt in sorted(by_cat.items()):
        print(f"  {cat:<20}: {cnt}")

    print(f"\nZeri UNCOVERED ({len(uncovered_list)}):")
    if uncovered_list:
        for d, lam, stretch in uncovered_list:
            stretch_str = str(stretch) if stretch is not None else "None (d*2>18)"
            print(f"  d={d}  lam={lam}  g(2lam,2lam,2lam)={stretch_str}")
    else:
        print("  (nessuno)")

    print("\nConfine di onesta':")
    print(
        "  g_fast = ESATTO (aritmetica intera pura, Murnaghan-Nakayama).\n"
        "  'covered' verifica la precondizione strutturale (>=2 argomenti special_shape\n"
        "  in un rappresentante g-simmetrico) ma NON ricalcola i valori di Rosas /\n"
        "  Bessenrodt-Bowman (restano CITATI).  'uncovered' = genuinamente fuori\n"
        "  dalle famiglie note esplorate."
    )
    print("=" * 72)

    return {
        "d_max": d_max,
        "total_zeros": len(rows),
        "by_category": by_cat,
        "uncovered": uncovered_list,
        "all_zeros": rows,
    }
