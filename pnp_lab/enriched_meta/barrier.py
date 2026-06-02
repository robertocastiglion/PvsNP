"""La morale del Modulo 14: cosa dice (onestamente) l'esperimento sul difetto.

Traduce i numeri in un verdetto sulla tesi forte di Roberto — "le tre lenti sono
gli stessi morfismi visti tramite tre arricchimenti incompatibili" — restando
nei limiti di ciò che è ESEGUITO vs ciò che è CITATO.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Citation:
    claim: str
    reference: str


def framework_citations() -> List[Citation]:
    """I risultati noti che il modulo rende eseguibili o cita."""
    return [
        Citation(
            "Stesse frecce, metriche incompatibili = categoria arricchita su quantali",
            "Lawvere 1973, 'Metric spaces, generalized logic, and closed categories'"),
        Citation(
            "Riconoscere ⟺ apprendere (l'isola di equivalenza stretta, difetto 0)",
            "Carmosino–Impagliazzo–Kabanets–Kolokolova 2016"),
        Citation(
            "Proprietà costruttiva+larga ⇒ niente PRG (perché 'riconoscere' è lossy)",
            "Razborov–Rudich 1994"),
        Citation(
            "Il difetto residuo non chiudibile = barriera di località",
            "Chen–Hirahara–Oliveira–Pich 2020"),
        Citation(
            "Calcolare → dimostrare (algoritmo ⇒ lower bound), freccia non invertibile",
            "Williams 2011 (NEXP ⊄ ACC⁰)"),
        Citation(
            "Invariante di sistema NON-scalare condiviso dalle tre lenti = esistenza OWF",
            "Razborov–Rudich 1994 + Kabanets–Cai 2000 + Razborov 1995"),
        Citation(
            "Scheletro qualitativo dell'auto-referenza (punto fisso)",
            "Lawvere 1969; Yanofsky 2003"),
    ]


@dataclass
class Verdict:
    headline: str
    cikk_island: str
    prove_axis: str
    recognize_axis: str
    conclusion: str
    honesty: str


def enriched_metacategory_summary() -> Verdict:
    """Il verdetto del Modulo 14 sulla tesi forte (A-condizionato)."""
    return Verdict(
        headline="Le tre lenti NON arricchiscono on-the-nose la stessa C: una sola "
                 "coppia coincide, le altre due restano lasse.",
        cikk_island="riconoscere ⟺ apprendere: difetto 0 (equivalenza stretta, CIKK). "
                    "Qui la tesi forte è letteralmente vera.",
        prove_axis="calcolare ↔ dimostrare: difetto CHIUDIBILE pagando budget di prova "
                   "(→0 sopra la lunghezza necessaria). Soglia netta = proof complexity.",
        recognize_axis="calcolare ↔ riconoscere: difetto residuo > 0 anche con la soglia "
                       "ottimale, NON chiudibile restando costruttivi (barriera di "
                       "località / Razborov–Rudich).",
        conclusion="Tesi forte = (A) CONDIZIONATO: diventerebbe 'una sola C arricchita "
                   "tre volte' se e solo se il difetto residuo riconoscere↔calcolare "
                   "collassasse — esattamente il programma Hirahara / barriera di "
                   "località. Oggi: struttura lassa con un'isola di equivalenza.",
        honesty="ESEGUITO: invarianza su C, i tre verdetti, i difetti, l'isola CIKK, la "
                "curva del budget, il gap residuo — tutti esatti su n piccolo. CITATO: "
                "le riduzioni generali, i teoremi di equivalenza/barriera asintotici, "
                "l'invariante OWF. NON risolve P vs NP.",
    )
