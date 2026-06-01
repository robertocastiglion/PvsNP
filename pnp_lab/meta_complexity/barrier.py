"""La morale: la meta-complessità chiude il cerchio del progetto."""

from __future__ import annotations


def meta_complexity_summary() -> str:
    return "\n".join(
        [
            "=" * 72,
            "  META-COMPLESSITÀ: MCSP & HARDNESS MAGNIFICATION  —  la frontiera viva",
            "=" * 72,
            "  MCSP = «quanto è complessa questa funzione?» reso un problema. È in NP",
            "  (il testimone è il circuito piccolo), e la sua durezza è il crocevia di",
            "  tutto: lo calcoliamo ESATTAMENTE su funzioni piccole (riuso del Modulo 6).",
            "",
            "  IL CERCHIO SI CHIUDE.",
            "    • Modulo 6 (Shannon): quasi tutte le funzioni sono dure — ma nessuna",
            "      esplicita è dimostrabilmente dura. È il muro dei lower bound.",
            "    • Modulo 1 (Natural Proofs): la proprietà 'f è dura' è utile e larga;",
            "      renderla COSTRUTTIVA = risolvere MCSP efficientemente = rompere i PRG",
            "      (Razborov–Rudich). La barriera È la durezza di MCSP. Lo verifichiamo.",
            "    • Modulo 12 (metodo algoritmico): l'unico ad aver aggirato le barriere.",
            "",
            "  HARDNESS MAGNIFICATION (il filo più vivo, 2018+). Lower bound MINUSCOLI",
            "  (n^{1+ε}) per problemi specifici come gap-MCSP si AMPLIFICANO in P ≠ NP.",
            "  La soglia è a un soffio dai lower bound noti (~n·polylog) — eppure resta",
            "  fuori portata, perché quei LB sembrano richiedere tecniche non-naturali:",
            "  la 'barriera di magnificazione'. Si torna alle barriere di sempre.",
            "",
            "  ONESTÀ. Calcoliamo MCSP e il legame con Natural Proofs in modo ESATTO; i",
            "  teoremi di amplificazione e lo status di MCSP (NP-hard? in P?) li CITIAMO.",
            "  E, ancora una volta: questo NON risolve P vs NP. Ma mostra dove i fili si",
            "  annodano — la meta-complessità è il punto in cui il problema guarda sé stesso.",
            "=" * 72,
        ]
    )
