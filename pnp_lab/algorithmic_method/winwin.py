"""La catena "win-win": come uno speedup di SAT diventa un lower bound.

Lo scheletro dell'argomento di Williams (NEXP ⊄ ACC⁰, 2011), reso esplicito.
Supponiamo, per assurdo, NEXP ⊆ C (C = una classe di circuiti piccoli):

  1.  Easy Witness Lemma: allora i testimoni dei problemi in NTIME[2^n] hanno
      circuiti C piccoli (li si può "indovinare").
  2.  Con un algoritmo di C-SAT più veloce della forza bruta (tempo 2^n / g(n)),
      si decide NTIME[2^n] indovinando il piccolo circuito-testimone e verificando
      con quell'algoritmo: tempo ≈ 2^n / g(n) + poly.
  3.  Se g(n) è SUPER-POLINOMIALE, questo batte 2^n di un fattore super-poly e
      contraddice il Teorema di Gerarchia dei Tempi Nondeterministici (vero senza
      ipotesi: NTIME[2^n] ⊄ NTIME[2^n / n^{ω(1)}]).
  4.  Contraddizione ⇒ NEXP ⊄ C.

La SOGLIA è dunque: speedup super-polinomiale. È il senso preciso di «anche solo
un po' più veloce della forza bruta»: basta un fattore n^{ω(1)}.

NOTA DI ONESTÀ. «Super-polinomiale» è una proprietà ASINTOTICA della funzione di
speedup, non qualcosa che un campione finito possa decidere (es. 2^{√n} supera
n^8 solo per n enormi). Perciò dichiariamo la classe di crescita per quello che
è — un fatto matematico noto — e usiamo la tabella dei rapporti solo per
ILLUSTRARE. Gli ingredienti profondi (Easy Witness Lemma, PCP, gerarchia) sono
CITATI: qui rendiamo esplicita solo la *soglia* e la *struttura logica*.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class SpeedupClass:
    label: str
    g: Callable[[int], float]      # fattore di speedup g(n)  (tempo SAT = 2^n / g(n))
    superpolynomial: bool          # classe di crescita NOTA (non campionata)


def standard_speedups() -> List[SpeedupClass]:
    """I regimi tipici di speedup, dal nessun guadagno all'esponenziale."""
    return [
        SpeedupClass("nessuno  (g = 1)", lambda n: 1.0, superpolynomial=False),
        SpeedupClass("polinomiale  (g = n^3)", lambda n: float(n) ** 3, superpolynomial=False),
        SpeedupClass("quasi-poly  (g = n^{log n})",
                     lambda n: float(n) ** max(1, n.bit_length()), superpolynomial=True),
        SpeedupClass("Williams ACC⁰  (g = 2^{n^0.5})",
                     lambda n: 2.0 ** (n ** 0.5), superpolynomial=True),
    ]


def ratio_table(s: SpeedupClass, ns: List[int], k: int) -> List[float]:
    """g(n)/n^k per n nel range: ILLUSTRA la crescita relativa a un polinomio di grado k.
    (Per i super-poly il rapporto tende a +∞, ma può servire n grande per vederlo.)"""
    return [s.g(n) / (float(n) ** k) for n in ns]


@dataclass
class WinWin:
    speedup: SpeedupClass
    lower_bound: bool       # lo speedup implica un lower bound (NEXP ⊄ C)?
    reason: str


def win_win(speedup: SpeedupClass) -> WinWin:
    """Applica la catena: lo speedup fa scattare la contraddizione (⇒ lower bound)?

    La contraddizione con la gerarchia scatta se e solo se lo speedup è
    super-polinomiale (gli altri passi sono ipotesi citate).
    """
    if speedup.superpolynomial:
        return WinWin(speedup, True,
                      "super-poly ⇒ batte la gerarchia NTIME ⇒ NEXP ⊄ C")
    return WinWin(speedup, False,
                  "non super-poly ⇒ nessuna contraddizione (il lower bound non segue)")


def analyze_all() -> List[WinWin]:
    return [win_win(s) for s in standard_speedups()]
