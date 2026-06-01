"""La morale: la separazione P^Ã ≠ NP^Ã e il suo confine onesto."""

from __future__ import annotations


def separation_summary() -> str:
    return "\n".join(
        [
            "=" * 72,
            "  LA SEPARAZIONE  P^Ã ≠ NP^Ã  —  il cuore di query complexity",
            "=" * 72,
            "  Il Modulo 2 separa P^B ≠ NP^B con oracoli BOOLEANI (relativizzazione).",
            "  Qui facciamo la stessa cosa con oracoli ALGEBRICI: l'algoritmo può valutare",
            "  l'estensione Ã in qualunque punto del campo, non solo sul cubo. È il modello",
            "  in cui vive la barriera dell'algebrizzazione.",
            "",
            "  Problema OR: «esiste un 1 nell'oracolo A?»",
            "",
            "  LATO NP — basta UNA query. Si indovina un testimone z e si verifica",
            "  Ã(z) = A(z) = 1. Complessità a query nondeterministica = 1.",
            "",
            "  LATO P — l'avversario risponde sempre 0. Finché le query algebriche sono",
            "  poche, esiste un oracolo booleano NON nullo i cui valori, combinati dai",
            "  funzionali di valutazione χ_·(r), si CANCELLANO su ogni query: dà le stesse",
            "  risposte del tutto-zero. L'algoritmo non distingue «ci sono 1» da «niente",
            "  1». Servono almeno κ query per spezzare ogni cancellazione, e κ cresce con",
            "  N = 2^m (quando il campo è piccolo rispetto a N — il regime di AW).",
            "",
            "  → NP a query = 1, P a query ≥ κ ≫ 1: la separazione, nel suo cuore.",
            "",
            "  ONESTÀ SUL CONFINE. ESEGUIAMO la separazione a query (testimone + avversario",
            "  di cancellazione, esatti). Il sollevamento a un oracolo per macchine di",
            "  Turing — costruire una vera lingua in NP^Ã \\ P^Ã — è la diagonalizzazione",
            "  standard; la versione forte, con il lower bound di communication complexity,",
            "  è il teorema di Aaronson–Wigderson (2008). Quelli li CITIAMO: ne abbiamo",
            "  reso eseguibile il motore, non la macchina completa.",
            "=" * 72,
        ]
    )
