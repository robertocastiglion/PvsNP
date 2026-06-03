"""Modulo 15 — Distinguishing Advantage Sandbox (misurazione ESATTA su n=3).

Idea. Nel dibattito sulle barriere abbiamo concluso che una nozione *puramente
informazionale* I(T,f) non unifica i Natural Proofs (che vedono tutta la truth
table ma sono limitati nel CALCOLO). La lente corretta è l'**indistinguibilità
contro un osservatore a risorse limitate**, dove la risorsa varia su DUE assi
ortogonali. Qui rendiamo quell'idea ESEGUIBILE su un'istanza minuscola.

L'osservatore (il "distinguitore") riceve la truth table di una funzione su n=3
variabili — 2^3 = 8 bit — e prova a dire se la funzione è DURA (alta complessità
di formula, istanza MCSP) o FACILE (bassa complessità). Misuriamo il suo
vantaggio di distinzione

    ε(ℓ, s) = max_D | Pr_{f dura}[D(f)=1] − Pr_{f facile}[D(f)=1] |

al variare di due budget ORTOGONALI del distinguitore:

  • Asse INFORMAZIONE  — ℓ: il fan-in locale delle *oracle gate*. Ogni oracle
    gate legge una finestra di ℓ degli 8 bit e ne calcola una funzione
    ARBITRARIA (lookup locale gratuito). ℓ piccolo = ogni sonda vede pochi bit.
  • Asse CALCOLO       — s: il numero di gate binari (∧, ∨; ¬ gratis) con cui le
    oracle gate vengono COMBINATE. s piccolo = poca capacità di combinare.

I due assi sono genuinamente ortogonali: con calcolo illimitato conta solo
QUANTI bit vedi (informazione pura); con informazione illimitata (ℓ=n) conta solo
COME li combini. Il punto interessante è il *confine*: esiste una regione in cui
l'osservatore è costretto ad avere SIMULTANEAMENTE ℓ alto e s alto per mantenere
ε > 0?

Onestà intellettuale (vincolante per questo repo).
  • Questa è una misurazione ESATTA su FINITE SIZE (n=3, 8 bit, 256 funzioni),
    NON la dimostrazione asintotica di una barriera. A n=3 il "muro" non può
    essere visibile: serve n→∞. Qui si VEDE solo la geometria del trade-off su
    un'istanza giocattolo.
  • Le oracle gate usano una famiglia canonica di finestre contigue degli 8 bit
    (non tutte le C(8,ℓ) sottoinsiemi): è una scelta deliberata per tenere il
    calcolo esatto. Ogni cella riporta se la ricerca è stata esaustiva (`exact`).
  • Riusa il motore del Modulo 6 (`min_formula_sizes`, `projection`) e la nozione
    di durezza del Modulo 13 (MCSP). Non riscrive il valutatore di circuiti.
  • NON dimostra (né tocca) P vs NP.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

from pnp_lab.circuits import min_formula_sizes

# n è FISSATO a 3 per vincolo architetturale: truth table di 8 bit, 256 funzioni.
# Salire a n=4 farebbe esplodere il calcolo esatto (il distinguitore avrebbe
# 2^16 input). NON modificare.
N_VARS = 3
TT_BITS = 1 << N_VARS          # 8: i bit della truth table = input del distinguitore
NUM_FUNCS = 1 << TT_BITS       # 256: quante funzioni su 3 variabili esistono


def _popcount(x: int) -> int:
    """Numero di bit a 1 (usa int.bit_count se disponibile)."""
    try:
        return x.bit_count()          # Python 3.10+
    except AttributeError:            # pragma: no cover
        return bin(x).count("1")


# ── Lo split DURE / FACILI (riuso del Modulo 6 = complessità di formula) ──────

@dataclass
class HardEasySplit:
    """Partizione delle 256 funzioni su n=3 in DURE (≥ τ) e FACILI (< τ)."""

    tau: int
    hard: Tuple[int, ...]      # truth table (0..255) delle funzioni dure
    easy: Tuple[int, ...]      # truth table delle funzioni facili
    hard_mask: int             # OR di (1<<f) per f dura  → maschera a 256 bit
    easy_mask: int             # OR di (1<<f) per f facile
    max_cost: int

    @property
    def n_hard(self) -> int:
        return len(self.hard)

    @property
    def n_easy(self) -> int:
        return len(self.easy)


def default_split(tau: Optional[int] = None) -> HardEasySplit:
    """Costruisce lo split DURE/FACILI sulle funzioni su n=3 (Modulo 6).

    `min_formula_sizes(3)` dà la dimensione di formula MINIMA esatta di ognuna
    delle 256 funzioni. Una funzione è DURA se la sua complessità è ≥ τ, FACILE
    altrimenti. Senza τ esplicito si usa la mediana, così le due classi sono
    bilanciate (il caso più informativo per il vantaggio di distinzione).
    """
    ct = min_formula_sizes(N_VARS)
    costs = ct.cost                      # truth table -> complessità
    if tau is None:
        ordered = sorted(costs.values())
        tau = ordered[len(ordered) // 2]  # mediana
    hard, easy = [], []
    hard_mask = easy_mask = 0
    for f in range(NUM_FUNCS):
        if costs[f] >= tau:
            hard.append(f)
            hard_mask |= 1 << f
        else:
            easy.append(f)
            easy_mask |= 1 << f
    return HardEasySplit(
        tau=tau,
        hard=tuple(hard),
        easy=tuple(easy),
        hard_mask=hard_mask,
        easy_mask=easy_mask,
        max_cost=ct.max_cost,
    )


def _advantage(table: int, split: HardEasySplit) -> float:
    """|Pr_dure[D=1] − Pr_facili[D=1]| per il distinguitore con truth table `table`.

    `table` è una funzione degli 8 bit (intero a 256 bit): il suo bit f dice se
    il distinguitore accetta la funzione la cui truth table è f. L'accuratezza è
    quindi due popcount di interi a 256 bit — costo trascurabile per candidato.
    """
    p_hard = _popcount(table & split.hard_mask) / split.n_hard
    p_easy = _popcount(table & split.easy_mask) / split.n_easy
    return abs(p_hard - p_easy)


# ── Le oracle gate: famiglia canonica di finestre di ampiezza ℓ ──────────────

def _windows(ell: int) -> List[Tuple[int, ...]]:
    """Le finestre contigue di ampiezza ℓ sugli 8 bit della truth table.

    ℓ=1 → 8 finestre, ℓ=2 → 7, ℓ=3 → 6. Scelta canonica e piccola per tenere il
    calcolo ESATTO (non tutte le C(8,ℓ) sottoinsiemi).
    """
    return [tuple(range(start, start + ell)) for start in range(TT_BITS - ell + 1)]


def build_local_basis(ell: int) -> List[int]:
    """Le funzioni a 256 bit calcolabili da UNA oracle gate di fan-in ≤ ℓ.

    Repertorio canonico delle oracle gate: per ogni finestra di ampiezza w ≤ ℓ,
    TUTTE le funzioni SIMMETRICHE di quei bit — cioè le feature di CONTEGGIO (il
    valore dipende solo da quanti dei w bit sono a 1). Includono i mattoni
    naturali di un'oracle gate locale: ∧ (tutti 1), ∨ (almeno un 1), ⊕ (parità),
    maggioranza, soglie. La famiglia è chiusa per complemento e contiene le
    costanti 0/1 (quindi ¬ è gratis sulle foglie).

    Fan-in ≤ ℓ (non = ℓ) ⇒ base(1) ⊆ base(2) ⊆ base(3): la classe C(ℓ,s) è quindi
    MONOTÒNA in ℓ (più informazione non può che aiutare), come dev'essere.

    Perché simmetriche e non TUTTE le 2^(2^ℓ) funzioni locali: con i lookup
    arbitrari la chiusura sotto ≤ s gate esplode (milioni di funzioni a 256 bit,
    out-of-memory già a ℓ=2). Le simmetriche tengono la misura ESATTA e minuscola
    e restano una nozione basis-free di "feature locale". È una restrizione
    DELIBERATA del sandbox, documentata: misuriamo la geometria del trade-off,
    non la barriera asintotica.
    """
    basis: set[int] = set()
    for w in range(1, ell + 1):
        for win in _windows(w):
            # popcount della finestra per ogni input i ∈ 0..255
            win_pop = [sum((i >> p) & 1 for p in win) for i in range(NUM_FUNCS)]
            for accept in range(1 << (w + 1)):    # sottoinsieme dei pesi accettati
                table = 0
                for i in range(NUM_FUNCS):
                    if (accept >> win_pop[i]) & 1:
                        table |= 1 << i
                basis.add(table)
    return sorted(basis)


# ── Il cuore: vantaggio massimo della classe C(ℓ, s) ─────────────────────────

@dataclass
class CellResult:
    """Una cella della matrice ε al budget (ℓ, s)."""

    ell: int
    s: int
    epsilon: float
    exact: bool                # la ricerca nella classe è stata esaustiva?
    explored: int              # numero di distinguitori DISTINTI esaminati


@dataclass
class AdvantageMatrix:
    split: HardEasySplit
    ells: Tuple[int, ...]
    ss: Tuple[int, ...]
    cells: Dict[Tuple[int, int], CellResult] = field(default_factory=dict)

    def get(self, ell: int, s: int) -> CellResult:
        return self.cells[(ell, s)]


def advantage_column(
    split: HardEasySplit,
    ell: int,
    ss: Sequence[int],
    *,
    guard: int = 150_000,
) -> List[CellResult]:
    """Vantaggio cumulativo ε(ℓ, s) per s crescente, con UNA sola DP per colonna.

    Programmazione dinamica per dimensione di formula crescente (come il Modulo
    6) sopra la base delle oracle gate di fan-in ℓ. A ogni livello di dimensione
    teniamo le funzioni DISTINTE realizzabili (dedup sulle truth table a 256
    bit) e aggiorniamo il massimo vantaggio CUMULATIVO (su tutte le funzioni con
    ≤ s gate). `guard` limita le funzioni trattenute per livello: se superato, il
    livello viene troncato e la cella è segnata `exact=False` (cota inferiore).

    Monotonìa: C(ℓ,s) ⊆ C(ℓ,s+1), quindi ε è non-decrescente in s; se ε tocca
    1.0 (separazione perfetta) ci fermiamo, non si può fare meglio.
    """
    max_s = max(ss)
    base = build_local_basis(ell)

    by_cost: List[List[int]] = [base[:]]      # by_cost[0] = oracle gate (0 gate binari)
    seen: set[int] = set(base)
    best = max((_advantage(t, split) for t in base), default=0.0)
    cum_best: List[float] = [best]            # cum_best[size] = ε con ≤ size gate
    exact_upto: List[bool] = [True]

    for size in range(1, max_s + 1):
        if best >= 1.0:                       # già perfetto: nulla da guadagnare
            cum_best.append(best)
            exact_upto.append(exact_upto[-1])
            by_cost.append([])
            continue
        found: List[int] = []
        truncated = False
        for i in range(size):                 # partizione i + (size-1-i) + 1 gate
            left = by_cost[i]
            right = by_cost[size - 1 - i]
            for a in left:
                for b in right:
                    for t in (a & b, a | b):  # ∧ e ∨ (¬ è gratis nella base)
                        if t not in seen:
                            seen.add(t)
                            found.append(t)
                            adv = _advantage(t, split)
                            if adv > best:
                                best = adv
                            if len(seen) >= guard:
                                truncated = True
                                break
                    if truncated:
                        break
                if truncated:
                    break
            if truncated:
                break
        by_cost.append(found)
        cum_best.append(best)
        exact_upto.append(exact_upto[-1] and not truncated)

    out: List[CellResult] = []
    for s in ss:
        out.append(CellResult(
            ell=ell, s=s,
            epsilon=cum_best[s],
            exact=exact_upto[s],
            explored=len(seen),
        ))
    return out


def advantage_matrix(
    split: Optional[HardEasySplit] = None,
    ells: Sequence[int] = (1, 2, 3),
    ss: Sequence[int] = (1, 2, 3),
    *,
    guard: int = 150_000,
) -> AdvantageMatrix:
    """La matrice completa ε(ℓ, s) per ℓ, s ∈ {1,2,3} (vincolo architetturale).

    Le celle troppo grandi per la ricerca esaustiva (corner ad alto ℓ e s) sono
    cote INFERIORI certificate, segnate `exact=False`. Applichiamo poi un
    *tightening monotòno*: poiché C(ℓ',s') ⊆ C(ℓ,s) per ℓ'≤ℓ, s'≤s, ogni cella
    vale almeno quanto le sue vicine in basso/sinistra — alziamo le cote inferiori
    a quel massimo (resta una cota inferiore valida, e la matrice è monotòna).
    """
    if split is None:
        split = default_split()
    ells_t, ss_t = tuple(ells), tuple(ss)
    m = AdvantageMatrix(split=split, ells=ells_t, ss=ss_t)
    for ell in ells_t:
        for cell in advantage_column(split, ell, ss_t, guard=guard):
            m.cells[(ell, cell.s)] = cell
    # tightening monotòno (su ε crescente per ℓ e per s)
    for ell in ells_t:
        for s in ss_t:
            cur = m.cells[(ell, s)]
            lo = cur.epsilon
            if (ell - 1, s) in m.cells:
                lo = max(lo, m.cells[(ell - 1, s)].epsilon)
            if (ell, s - 1) in m.cells:
                lo = max(lo, m.cells[(ell, s - 1)].epsilon)
            if lo > cur.epsilon:
                m.cells[(ell, s)] = CellResult(
                    ell=ell, s=s, epsilon=lo, exact=cur.exact, explored=cur.explored
                )
    return m


def frontier_note(m: AdvantageMatrix) -> str:
    """Legge la matrice e dice se i DUE assi sono entrambi necessari.

    Confronta gli "spigoli" (ℓ alto da solo, s alto da solo) con l'angolo
    (entrambi alti) per vedere se esiste un trade-off reale su questa istanza.
    """
    ell_lo, ell_hi = min(m.ells), max(m.ells)
    s_lo, s_hi = min(m.ss), max(m.ss)
    corner = m.get(ell_hi, s_hi).epsilon
    info_only = m.get(ell_hi, s_lo).epsilon       # tanta informazione, poco calcolo
    comp_only = m.get(ell_lo, s_hi).epsilon       # poca informazione, tanto calcolo
    floor = m.get(ell_lo, s_lo).epsilon
    gain_info = corner - comp_only                # quanto aggiunge alzare ℓ
    gain_comp = corner - info_only                # quanto aggiunge alzare s
    lines = [
        f"  Lettura del confine (n={N_VARS}, ricerca esatta su finite size):",
        f"    ε minimo  (ℓ={ell_lo}, s={s_lo}) = {floor:.3f}",
        f"    solo info (ℓ={ell_hi}, s={s_lo}) = {info_only:.3f}",
        f"    solo calc (ℓ={ell_lo}, s={s_hi}) = {comp_only:.3f}",
        f"    entrambi  (ℓ={ell_hi}, s={s_hi}) = {corner:.3f}",
    ]
    if gain_info > 1e-9 and gain_comp > 1e-9:
        lines.append("  → ENTRAMBI gli assi contribuiscono: né informazione né calcolo")
        lines.append("    da soli saturano il vantaggio. Trade-off ℓ↔s presente.")
    elif gain_info > 1e-9:
        lines.append("  → conta soprattutto l'INFORMAZIONE (ℓ): a parità di ℓ, più gate")
        lines.append("    aggiungono poco su questa istanza.")
    elif gain_comp > 1e-9:
        lines.append("  → conta soprattutto il CALCOLO (s): a parità di s, finestre più")
        lines.append("    larghe aggiungono poco su questa istanza.")
    else:
        lines.append("  → a n=3 il vantaggio satura già nell'angolo basso: l'istanza è")
        lines.append("    troppo piccola per separare gli assi (atteso — serve n→∞).")
    lines.append("  NB: misura ESATTA su finite size, NON la barriera asintotica.")
    return "\n".join(lines)


def distinguishing_summary() -> str:
    return "\n".join([
        "  Distinguishing Advantage Sandbox — ε(ℓ, s) su n=3 (8 bit, 256 funzioni).",
        "  Osservatore = distinguitore DURE vs FACILI (istanze MCSP, Modulo 6/13).",
        "    • asse INFORMAZIONE ℓ = fan-in delle oracle gate (bit per blocco)",
        "    • asse CALCOLO      s = numero di gate binari che le combinano",
        "  ε = massimo vantaggio di distinzione della classe C(ℓ, s).",
        "  Onestà: misura ESATTA su finite size; NON è la barriera asintotica; non",
        "  tocca P vs NP. La famiglia di oracle gate è canonica (finestre contigue).",
    ])
