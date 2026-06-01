"""Perché il metodo algoritmico AGGIRA tutte e tre le barriere."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class BarrierEvasion:
    barrier: str
    evaded: bool
    why: str


def evasion_report() -> List[BarrierEvasion]:
    """Il metodo di Williams contro le tre barriere note (cfr. Moduli 1, 2, 7-10)."""
    return [
        BarrierEvasion(
            "Relativizzazione (Modulo 2)", True,
            "Usa il Teorema di Gerarchia dei Tempi e l'Easy Witness Lemma in modo "
            "NON relativizzante (dipendono dalla struttura della macchina, non valgono "
            "rispetto a ogni oracolo)."),
        BarrierEvasion(
            "Natural Proofs (Modulo 1)", True,
            "Non è una 'proprietà naturale' delle funzioni: non è né costruttiva né "
            "larga. È una CONVERSIONE algoritmo→lower bound, fuori dallo schema "
            "Razborov–Rudich."),
        BarrierEvasion(
            "Algebrizzazione (Moduli 7-10)", True,
            "Aaronson–Wigderson lo notano esplicitamente: il risultato di Williams "
            "NON algebrizza. Sfugge anche alla terza barriera."),
    ]


def algorithmic_method_summary() -> str:
    return "\n".join(
        [
            "=" * 72,
            "  IL METODO ALGORITMICO  (Ryan Williams, 2011)  →  NEXP ⊄ ACC⁰",
            "=" * 72,
            "  «Un algoritmo di SAT più veloce della forza bruta per una classe di",
            "  circuiti C ⇒ un lower bound contro C.»",
            "",
            "  Perché è IL candidato più solido: è l'unico approccio che ha davvero",
            "  rotto TUTTE e tre le barriere e prodotto separazioni nuove.",
            "",
            "    • Relativizzazione: aggirata (gerarchia + easy witness non relativizzano).",
            "    • Natural Proofs:   aggirata (non è una proprietà naturale, è una",
            "                        conversione algoritmo→lower bound).",
            "    • Algebrizzazione:  aggirata (Aaronson–Wigderson: non algebrizza).",
            "",
            "  Cosa abbiamo reso ESEGUIBILE qui:",
            "    • lo SPEEDUP: circuiti strutturati hanno polinomi sparsi ⇒ si conta",
            "      su tutti i 2^n input senza enumerarli (esatto e verificato).",
            "    • la SOGLIA win-win: serve uno speedup super-polinomiale perché la",
            "      catena 'speedup + NEXP⊆C ⇒ contraddizione con la gerarchia' scatti.",
            "",
            "  ONESTÀ SUL CONFINE. Eseguiamo il motore (lo speedup) e la struttura",
            "  logica (la soglia). Gli ingredienti profondi — Easy Witness Lemma, PCP",
            "  succinti, il teorema di gerarchia, e l'algoritmo ACC⁰ vero (2^{n-n^δ} via",
            "  Beigel–Tarui + moltiplicazione veloce di matrici) — li CITIAMO.",
            "",
            "  E, come sempre: questo NON risolve P vs NP. È l'unica crepa nota nel muro",
            "  delle barriere — la direzione dove la ricerca prova davvero a spingere.",
            "=" * 72,
        ]
    )
