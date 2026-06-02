"""Le tre lenti come realizzazioni dello STESSO predicato di durezza H_s(f).

Fissiamo la verità di base (la lente "calcolare", esatta) e poi vediamo se le
altre due la riproducono. H_s(f) := [ complessità(f) > s ]  (f è "dura").

  • CALCOLARE  (V_time)   — χ_comp(f) = costo MCSP esatto > s. Per definizione
    corretta; costo = enumerare le formule (esponenziale). È il riferimento.
  • RICONOSCERE (V_sample) — χ_recog(f) = verdetto di una proprietà COSTRUTTIVA
    (Razborov–Rudich): una statistica cheap (influenza totale) sopra una soglia θ.
    Larga e costruttiva, ma può SBAGLIARE rispetto al costo esatto: lo scarto è la
    perdita (la barriera natural-proofs / di località in miniatura).
  • DIMOSTRARE (V_proof)   — χ_prove(f) = "il lower bound costo>s è certificabile
    entro un budget di prova B". Il certificato per esaustione deve escludere tutte
    le formule di taglia ≤ s; la loro quantità è la LUNGHEZZA della prova. Se il
    budget non basta, il lower bound resta non dimostrato (proof complexity).

Tutte e tre agiscono sugli stessi oggetti di ``category.Category``. La domanda del
Modulo 14 è: queste realizzazioni COINCIDONO (equivalenza stretta) o lasciano un
difetto (relazione lassa)?
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import Dict, List

from pnp_lab.circuits import ComplexityTable


# ── lente CALCOLARE: il costo esatto (riferimento) ────────────────────────

def chi_compute(ct: ComplexityTable, tt: int, s: int) -> bool:
    """χ_comp(f): la funzione è dura (costo esatto > s)? Esatto, costoso."""
    return ct.cost[tt] > s


# ── lente RICONOSCERE: una proprietà costruttiva (influenza totale) ────────

def total_influence(tt: int, n: int) -> int:
    """Influenza totale (non normalizzata): Σ_x Σ_j [ f(x) ≠ f(x ⊕ e_j) ].

    Statistica COSTRUTTIVA classica (Fourier / sensitività): O(N·n), nessuna
    enumerazione di circuiti. È il tipo di proprietà "naturale" di Razborov–Rudich.
    """
    N = 1 << n
    total = 0
    for x in range(N):
        fx = (tt >> x) & 1
        for j in range(n):
            y = x ^ (1 << j)
            if fx != ((tt >> y) & 1):
                total += 1
    return total


def chi_recognize(tt: int, n: int, theta: int) -> bool:
    """χ_recog(f): la proprietà costruttiva dichiara f dura (influenza > θ)?"""
    return total_influence(tt, n) > theta


def best_recognize_threshold(ct: ComplexityTable, s: int) -> int:
    """Sceglie θ che meglio approssima H_s con la statistica costruttiva.

    È la versione più CARITATEVOLE della lente "riconoscere": le diamo la soglia
    ottimale. Se anche così resta un difetto, quello è irriducibile per una
    proprietà naturale di questa famiglia (il cuore della barriera).
    """
    n = ct.n
    infl = {t: total_influence(t, n) for t in ct.cost}
    candidates = sorted(set(infl.values()))
    best_theta, best_err = candidates[0] if candidates else 0, len(ct.cost) + 1
    for theta in candidates + [candidates[-1] + 1] if candidates else [0]:
        err = sum(1 for t in ct.cost if (infl[t] > theta) != (ct.cost[t] > s))
        if err < best_err:
            best_err, best_theta = err, theta
    return best_theta


# ── lente DIMOSTRARE: la lunghezza di prova del lower bound ────────────────

def _catalan(k: int) -> int:
    """Numero di forme d'albero binario con k nodi interni."""
    return comb(2 * k, k) // (k + 1)


def formulas_of_size(s: int, n: int) -> int:
    """Quante formule sintattiche hanno taglia (= n. di gate) esattamente s.

    Un albero con s gate ha s+1 foglie; ogni gate sceglie ∧/∨ (2 modi), ogni
    foglia un letterale tra 2n. Forme d'albero = Catalan(s).
    """
    return _catalan(s) * (2 ** s) * ((2 * n) ** (s + 1))


def proof_length_for_threshold(s: int, n: int) -> int:
    """Lunghezza della prova-per-esaustione del lower bound 'costo > s'.

    Per certificare che f NON ha formule di taglia ≤ s bisogna escluderle tutte:
    la prova ha lunghezza = numero di formule candidate di taglia ≤ s. Cresce
    super-esponenzialmente — è il costo di *dimostrare* la durezza.
    """
    return sum(formulas_of_size(k, n) for k in range(s + 1))


def chi_prove(ct: ComplexityTable, tt: int, s: int, budget: int) -> bool:
    """χ_prove(f): il lower bound 'f è dura' è certificabile entro ``budget``?

    Vero sse f è davvero dura E il budget copre l'enumerazione necessaria. Se il
    budget non basta, il lower bound c'è ma resta NON dimostrato (è esattamente la
    situazione della proof complexity: il fatto è vero ma la prova è troppo lunga).
    """
    if not chi_compute(ct, tt, s):
        return False
    return proof_length_for_threshold(s, ct.n) <= budget


@dataclass
class LensVerdicts:
    """I tre verdetti su tutti gli oggetti, per una soglia s fissata."""

    s: int
    compute: Dict[int, bool]
    recognize: Dict[int, bool]
    prove: Dict[int, bool]
    theta: int
    proof_budget: int
    proof_length_needed: int


def evaluate_lenses(ct: ComplexityTable, s: int, proof_budget: int,
                    theta: int | None = None) -> LensVerdicts:
    """Calcola i tre verdetti χ_comp, χ_recog, χ_prove su tutte le funzioni."""
    n = ct.n
    if theta is None:
        theta = best_recognize_threshold(ct, s)
    compute = {t: chi_compute(ct, t, s) for t in ct.cost}
    recognize = {t: chi_recognize(t, n, theta) for t in ct.cost}
    prove = {t: chi_prove(ct, t, s, proof_budget) for t in ct.cost}
    return LensVerdicts(
        s=s,
        compute=compute,
        recognize=recognize,
        prove=prove,
        theta=theta,
        proof_budget=proof_budget,
        proof_length_needed=proof_length_for_threshold(s, n),
    )
