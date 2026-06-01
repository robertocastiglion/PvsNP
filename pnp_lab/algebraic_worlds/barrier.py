"""La morale: i due mondi algebrici e la barriera dell'algebrizzazione."""

from __future__ import annotations


def algebraic_worlds_summary() -> str:
    return "\n".join(
        [
            "=" * 72,
            "  I MONDI ALGEBRICI  →  la barriera dell'algebrizzazione (Aaronson–Wigderson)",
            "=" * 72,
            "  La relativizzazione (Modulo 2) usa oracoli BOOLEANI. L'algebrizzazione li",
            "  estende a polinomi a basso grado Ã: l'algoritmo può interrogare Ã in",
            "  qualunque punto del campo, non solo sul cubo 0/1. Abbiamo reso eseguibili i",
            "  due effetti opposti di questo accesso.",
            "",
            "  MONDO 1 — POTENZA. Rilevare un bit piantato costa fino a 2^m query",
            "  booleane, ma UNA sola query algebrica con probabilità (1−1/p)^m. Questo",
            "  potere è ciò che ha permesso ad arithmetization di dimostrare IP = PSPACE,",
            "  un risultato che NON relativizza: la barriera della relativizzazione, da",
            "  sola, non lo coglie. (È il motore del sum-check, Modulo 7.)",
            "",
            "  MONDO 2 — LIMITE. Eppure determinare l'oracolo richiede ~2^m query anche",
            "  algebriche: è un lower bound di interpolazione ESATTO (l'estensione ha 2^m",
            "  coefficienti; con meno valutazioni il sistema su GF(p) è sotto-determinato).",
            "  L'avversario tiene in vita due estensioni indistinguibili. Il metodo dei",
            "  polinomi (Schwartz–Zippel) misura esattamente quanto l'accesso algebrico",
            "  può e non può fare.",
            "",
            "  Aaronson–Wigderson combinano i due effetti per costruire mondi algebrici",
            "  con esiti OPPOSTI su P vs NP: nessuna tecnica algebrizzante, da sola, può",
            "  risolverlo. ONESTÀ: qui ESEGUIAMO il motore (Schwartz–Zippel, potenza e",
            "  limite delle query algebriche); la costruzione completa dei due oracoli",
            "  P^Ã = NP^Ã e P^Ã ≠ NP^Ã resta il teorema che CITIAMO — eccede questo",
            "  toolkit, ma ora se ne vedono girare gli ingranaggi.",
            "=" * 72,
        ]
    )
