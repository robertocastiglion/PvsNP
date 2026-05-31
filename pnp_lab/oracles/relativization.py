"""La conclusione: la barriera della relativizzazione."""

from __future__ import annotations


def relativization_summary() -> str:
    """Testo riassuntivo che lega i due oracoli alla barriera."""
    return "\n".join(
        [
            "=" * 72,
            "  LA BARRIERA DELLA RELATIVIZZAZIONE  (Baker–Gill–Solovay, 1975)",
            "=" * 72,
            "  Abbiamo costruito due mondi con oracolo, entrambi coerenti:",
            "",
            "    • Mondo B (separation):  P^B ≠ NP^B   — diagonalizzazione, eseguita.",
            "    • Mondo A (collapse):    P^A = NP^A   — oracolo PSPACE-completo (TQBF).",
            "",
            "  Una dimostrazione si dice che 'relativizza' se vale identica rispetto a",
            "  QUALSIASI oracolo. Ma allora dovrebbe dare la STESSA risposta in A e in B",
            "  — impossibile, perché lì P vs NP ha esiti opposti.",
            "",
            "  Conseguenza: nessuna tecnica che relativizza può risolvere P vs NP.",
            "  E la diagonalizzazione classica (l'arma con cui Turing separò i problemi",
            "  decidibili da quelli indecidibili) relativizza. Per questo da sola non",
            "  basta: serve una tecnica 'non relativizzante'. È la prima delle tre",
            "  grandi barriere — insieme a natural proofs (Modulo 1) e algebrizzazione.",
            "=" * 72,
        ]
    )
