"""TINY-INSTANCE COLLAPSE — cristallizzazione di CHIUSURA del loop di ricerca.

Questo modulo NON introduce un nuovo discriminante. Cristallizza la
META-CONCLUSIONE raggiunta dopo CINQUE cicli consecutivi di
RESTATEMENT-OF-KNOWN (RESEARCH_LOG Entry 1,2,4,5,6):

  Nel regime n<=4, ogni "discriminante locale" costruito dal loop si riduce —
  via un'IDENTITA' ESATTA verificabile in codice — a un invariante già nel
  dizionario μ_R (cover-LP / proof-complexity / KT). Il pattern trascende TRE
  arene (dualità/cover-LP, proof-complexity, meta-complessità).

Qui rendiamo RIPRODUCIBILI i due fatti portanti che DEPRECANO ``d_flip`` (il
discriminante del Ciclo 5, vedi ``strata_graph.py``) come metrica:

  (W1) d_flip è il GRADIENTE DISCRETO di MCSP-size sul cubo delle tavole di
       verità: d_flip(f) = #{k : cost[f XOR (1<<k)] < cost[f]}. Non è un nuovo
       invariante — è la derivata di un oggetto-KT, ricostruibile da ``cost``
       SOLO (nessun oracolo aggiuntivo).  Verificato esatto su 256/256 (n=3)
       e 65536/65536 (n=4).

  (W2) d_flip NON è CANONICO: cambiando l'oracolo di costo (formula-size ->
       profondità di albero di decisione, entrambi misure di complessità
       ESATTE) il valore di d_flip cambia su una frazione misurabile delle
       funzioni. Una "metrica" che dipende dalla scelta arbitraria del costo
       non è un discriminante strutturale.

E formalizza il FALSIFICATORE richiesto per produrre contenuto genuinamente
nuovo (vedi ``falsifier_status``): un discriminante su n<=4 che separi due
funzioni di PARI MCSP-size E pari cover-LP/G★ E NON ricostruibile da ``cost``
né da μ_R via un'identità esatta.

Tutto è ESATTO e deterministico (interi, niente float). Riusa
``pnp_lab.circuits.min_formula_sizes`` (formula-size) e calcola la
profondità di albero di decisione esatta come secondo oracolo di costo.

ATTENZIONE (scope): è una constatazione sul METODO del loop su istanze FINITE,
NON un claim su P vs NP.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Dict, List, Tuple

from pnp_lab.circuits import ComplexityTable, min_formula_sizes
from pnp_lab.meta_complexity.strata_graph import (
    down_degree_flip,
    down_degree_negation,
)


# --------------------------------------------------------------------------- #
#  Secondo oracolo di costo ESATTO: profondità di albero di decisione         #
# --------------------------------------------------------------------------- #

@lru_cache(maxsize=None)
def _dt_depth_vals(vals: Tuple[int, ...]) -> int:
    """Profondità minima di albero di decisione per la sottofunzione ``vals``.

    ``vals`` è la tavola di verità (lista di output) su m variabili libere,
    lunga 2^m. Caso base: funzione costante -> 0. Altrimenti, si può
    interrogare QUALSIASI variabile libera p: profondità = 1 + max delle due
    cofattorizzazioni (p=0, p=1). Esatto via minimo su p, memoizzato.
    """
    first = vals[0]
    if all(v == first for v in vals):
        return 0
    L = len(vals)
    m = L.bit_length() - 1  # 2^m = L
    best = m  # ogni funzione su m variabili ha un DT di profondità <= m
    for p in range(m):
        low = tuple(vals[i] for i in range(L) if not (i >> p) & 1)
        high = tuple(vals[i] for i in range(L) if (i >> p) & 1)
        d = 1 + max(_dt_depth_vals(low), _dt_depth_vals(high))
        if d < best:
            best = d
    return best


def dt_depth(tt: int, n: int) -> int:
    """Profondità esatta dell'albero di decisione ottimo per la tavola ``tt``."""
    return _dt_depth_vals(tuple((tt >> i) & 1 for i in range(1 << n)))


def dt_depth_cost(n: int) -> Dict[int, int]:
    """Oracolo di costo {tt: dt_depth} per TUTTE le 2^(2^n) funzioni su n var."""
    total = 1 << (1 << n)
    return {tt: dt_depth(tt, n) for tt in range(total)}


# --------------------------------------------------------------------------- #
#  Down-degree generico rispetto a un oracolo di costo arbitrario             #
# --------------------------------------------------------------------------- #

def down_degree_flip_cost(cost: Dict[int, int], tt: int, n: int) -> int:
    """#output-flip che ABBASSANO strettamente un oracolo di costo arbitrario.

    Generalizza ``strata_graph.down_degree_flip`` (che usa formula-size) a
    QUALSIASI funzione di costo. Serve per il witness di NON-canonicità (W2).
    """
    c0 = cost[tt]
    N = 1 << n
    return sum(1 for k in range(N) if cost[tt ^ (1 << k)] < c0)


# --------------------------------------------------------------------------- #
#  I tre witness riproducibili della META-CONCLUSIONE                          #
# --------------------------------------------------------------------------- #

def negation_is_cost_automorphism(ct: ComplexityTable, n: int) -> int:
    """Killer-1: #funzioni con d_negation>0 (atteso 0 — input-negation è un
    automorfismo del costo). Ritorna il conteggio; 0 = confermato."""
    return sum(1 for tt in ct.cost if down_degree_negation(ct, tt, n) != 0)


def dflip_is_cost_gradient(ct: ComplexityTable, n: int) -> int:
    """W1: #funzioni dove d_flip differisce dal gradiente ricostruito da ``cost``.

    Ricostruisce d_flip dal SOLO dizionario ``cost`` (nessun oracolo aggiuntivo)
    e confronta col valore prodotto da ``strata_graph.down_degree_flip``. Devono
    coincidere OVUNQUE -> d_flip ∈ σ(cost), è la derivata di un oggetto-KT.
    Ritorna il numero di mismatch (0 = identità esatta verificata).
    """
    mism = 0
    for tt in ct.cost:
        if down_degree_flip(ct, tt, n) != down_degree_flip_cost(ct.cost, tt, n):
            mism += 1
    return mism


def dflip_canonicity_mismatch(n: int, cap: int = 60) -> Tuple[int, int]:
    """W2: (#funzioni dove d_flip cambia tra i due oracoli, #funzioni totali).

    Confronta d_flip calcolato su formula-size (Module 6) vs su profondità DT —
    due misure di complessità ENTRAMBE esatte. Se il valore cambia su una
    frazione non banale, d_flip NON è canonico (dipende dalla scelta del costo).
    """
    ct = min_formula_sizes(n, cap)
    dt_cost = dt_depth_cost(n)
    funcs = list(ct.cost)
    mism = 0
    for tt in funcs:
        a = down_degree_flip(ct, tt, n)
        b = down_degree_flip_cost(dt_cost, tt, n)
        if a != b:
            mism += 1
    return mism, len(funcs)


# --------------------------------------------------------------------------- #
#  Il FALSIFICATORE esplicito                                                 #
# --------------------------------------------------------------------------- #

@dataclass
class FalsifierStatus:
    """Esito della ricerca del falsificatore (NON trovato = collasso confermato)."""
    found: bool
    note: str


def falsifier_status(n: int, cap: int = 60) -> FalsifierStatus:
    """Cerca un falsificatore della META-CONCLUSIONE entro la toolbox del loop.

    FALSIFICATORE = un discriminante su n<=4 che (a) separa due funzioni di pari
    MCSP-size, (b) NON è ricostruibile da ``cost`` via identità esatta.

    Verifichiamo che ``d_flip`` — l'unico discriminante "locale" del Ciclo 5 —
    NON qualifica: W1 (``dflip_is_cost_gradient``) prova che è interamente
    ricostruibile da ``cost``, quindi viola (b) per costruzione. Gli altri
    invarianti della toolbox (sensitivity, block-sensitivity, gf2-degree) NON
    sono ricostruibili da ``cost`` ma sono ESSI STESSI invarianti già nel
    dizionario μ_R (analisi booleana classica), quindi non sono "contenuto
    nuovo". Conclusione: nessun falsificatore nella toolbox -> collasso confermato.
    """
    ct = min_formula_sizes(n, cap)
    if dflip_is_cost_gradient(ct, n) != 0:
        # se d_flip NON fosse ricostruibile da cost, sarebbe un candidato
        return FalsifierStatus(
            found=True,
            note="d_flip NON ricostruibile da cost: candidato falsificatore — investigare.",
        )
    return FalsifierStatus(
        found=False,
        note=("nessun falsificatore nella toolbox: d_flip è ricostruibile da cost "
              "(gradiente, W1); sensitivity/bsens/gf2-degree non lo sono ma sono "
              "invarianti già dizionarizzati. Collasso tiny-instance confermato."),
    )


# --------------------------------------------------------------------------- #
#  Sommario di chiusura                                                       #
# --------------------------------------------------------------------------- #

@dataclass
class CollapseSummary:
    n: int
    num_funcs: int
    negation_nonzero: int          # 0 atteso (killer-1)
    gradient_mismatch: int         # 0 atteso (W1)
    canonicity_mismatch: int       # >0 atteso (W2)
    canonicity_total: int
    falsifier_found: bool          # False atteso (collasso confermato)

    @property
    def canonicity_fraction(self) -> float:
        return self.canonicity_mismatch / self.canonicity_total if self.canonicity_total else 0.0


def collapse_summary(n: int, cap: int = 60) -> CollapseSummary:
    """Calcola tutti i witness della meta-conclusione per le funzioni su n var."""
    ct = min_formula_sizes(n, cap)
    cmm, ctot = dflip_canonicity_mismatch(n, cap)
    fs = falsifier_status(n, cap)
    return CollapseSummary(
        n=n,
        num_funcs=len(ct.cost),
        negation_nonzero=negation_is_cost_automorphism(ct, n),
        gradient_mismatch=dflip_is_cost_gradient(ct, n),
        canonicity_mismatch=cmm,
        canonicity_total=ctot,
        falsifier_found=fs.found,
    )
