"""La conclusione: la barriera dell'algebrizzazione (Aaronson–Wigderson 2008)."""

from __future__ import annotations


def algebrization_summary() -> str:
    """Testo che lega arithmetization e sum-check alla terza barriera."""
    return "\n".join(
        [
            "=" * 72,
            "  LA BARRIERA DELL'ALGEBRIZZAZIONE  (Aaronson–Wigderson, 2008)",
            "=" * 72,
            "  La relativizzazione (Modulo 2) sembrava chiudere la porta: ogni tecnica",
            "  che vale rispetto a OGNI oracolo non può risolvere P vs NP. Poi è arrivata",
            "  l'arithmetization — sollevare le formule a polinomi su un campo — che ha",
            "  dimostrato IP = PSPACE. E quel risultato NON relativizza: la porta non era",
            "  del tutto chiusa.",
            "",
            "  Cosa abbiamo reso eseguibile qui:",
            "    • estensione multilineare f~  — l'oggetto algebrico: un oracolo booleano",
            "      f visto come polinomio, valutabile in tutto GF(p)^n, non solo su 0/1.",
            "    • sum-check  — il verificatore controlla Σ_{x∈{0,1}^n} g(x) con UNA sola",
            "      valutazione di g. È il motore di IP = PSPACE, e qui gira davvero.",
            "",
            "  La mossa di Aaronson–Wigderson: definire un oracolo 'algebrico' come una",
            "  qualunque estensione polinomiale a basso grado Ã di un oracolo A. Una",
            "  dimostrazione 'algebrizza' se vale rispetto a tali Ã. L'arithmetization",
            "  algebrizza. Ma loro costruiscono mondi algebrici con esiti OPPOSTI su",
            "  P vs NP: quindi nemmeno le tecniche algebrizzanti, da sole, possono",
            "  risolverlo.",
            "",
            "  Morale: serve una tecnica NON-algebrizzante. Le tre barriere note —",
            "  relativizzazione, natural proofs, algebrizzazione — restano tutte in piedi.",
            "  Onestà: l'estensione e il sum-check li ESEGUIAMO; la separazione tramite",
            "  oracoli algebrici è il teorema che CITIAMO (la sua costruzione completa",
            "  eccede questo toolkit).",
            "=" * 72,
        ]
    )
