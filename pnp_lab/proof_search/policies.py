"""Le policy: come si propongono le tattiche da uno stato di ricerca.

Tre livelli, dal "nessuna intelligenza" all'opzionale modello esterno:

  • ``exhaustive_policy``  — propone TUTTE le tattiche applicabili (baseline cieca).
  • ``heuristic_policy``   — le ordina per quanto avvicinano al target e ne tiene
                             le migliori top_k (una policy trasparente e testabile).
  • ``LLMPolicy``          — interfaccia per un modello esterno (stile AlphaProof):
                             costruisce un prompt, lo manda a un `call_fn` fornito
                             dall'utente, e interpreta la risposta. OPZIONALE: il
                             core del toolkit non ne dipende e i test non lo usano.

Onestà: la policy non "dimostra" nulla da sola — propone solo MOSSE; è il motore
(sound) a verificare. Una policy migliore si misura in NODI ESPANSI, non in
promesse.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from .engine import Rule, Tactic, apply_tactic, applicable_tactics, distance, show
from .search import SearchState


def exhaustive_policy(allow_reverse: bool = True):
    """Baseline: tutte le tattiche applicabili, senza ordinamento utile."""
    def policy(state: SearchState) -> List[Tactic]:
        return applicable_tactics(state.rules, state.term, allow_reverse=allow_reverse)  # type: ignore[arg-type]
    return policy


def heuristic_policy(top_k: int = 4, allow_reverse: bool = True):
    """Policy trasparente: ordina le tattiche per distanza-al-target del risultato,
    e tiene solo le `top_k` più promettenti (taglia il fattore di ramificazione)."""
    def policy(state: SearchState) -> List[Tactic]:
        scored = []
        for tac in applicable_tactics(state.rules, state.term, allow_reverse=allow_reverse):  # type: ignore[arg-type]
            nxt = apply_tactic(state.rules, state.term, tac)  # type: ignore[arg-type]
            if nxt is None:
                continue
            scored.append((distance(nxt, state.target), tac))  # type: ignore[arg-type]
        scored.sort(key=lambda s: s[0])
        return [tac for _, tac in scored[:top_k]]
    return policy


# ── interfaccia opzionale per un modello esterno (LLM) ────────────────────

def build_prompt(state: SearchState) -> str:
    """Costruisce il prompt per il modello (funzione PURA, testabile).

    Elenca obiettivo, target e le tattiche applicabili numerate; chiede di
    restituire gli indici delle mosse più promettenti, una per riga.
    """
    tactics = applicable_tactics(state.rules, state.term)  # type: ignore[arg-type]
    lines = [
        "Sei una policy di proof-search per riscrittura equazionale.",
        f"Termine corrente: {show(state.term)}",        # type: ignore[arg-type]
        f"Obiettivo (target): {show(state.target)}",    # type: ignore[arg-type]
        "Tattiche applicabili:",
    ]
    for i, t in enumerate(tactics):
        lines.append(f"  [{i}] {t.show()}")
    lines.append("Rispondi con gli indici delle mosse migliori, una per riga (es. '0').")
    return "\n".join(lines)


def parse_tactics(response: str, state: SearchState) -> List[Tactic]:
    """Interpreta la risposta del modello in una lista di tattiche (PURA, testabile).

    Accetta righe con un indice intero; ignora il resto. Indici fuori range o non
    validi vengono scartati: il motore resta l'unica autorità.
    """
    tactics = applicable_tactics(state.rules, state.term)  # type: ignore[arg-type]
    out: List[Tactic] = []
    for line in response.splitlines():
        token = line.strip().split()[0] if line.strip() else ""
        if token.lstrip("[").rstrip("]").isdigit():
            idx = int(token.lstrip("[").rstrip("]"))
            if 0 <= idx < len(tactics) and tactics[idx] not in out:
                out.append(tactics[idx])
    return out


class LLMPolicy:
    """Policy guidata da un modello esterno. OPZIONALE e onesta.

    `call_fn` è fornito dall'utente: una funzione `str -> str` che manda il prompt
    al modello (Anthropic, OpenAI, locale…) e restituisce il testo. Il toolkit NON
    include chiavi né dipendenze di rete; se `call_fn` fallisce, si ripiega sulla
    policy euristica, così la ricerca non si rompe mai. I test non usano mai un
    modello reale: validano solo `build_prompt`/`parse_tactics` (puri).
    """

    def __init__(self, call_fn: Callable[[str], str], *, fallback_top_k: int = 4):
        self.call_fn = call_fn
        self._fallback = heuristic_policy(top_k=fallback_top_k)

    def __call__(self, state: SearchState) -> List[Tactic]:
        try:
            response = self.call_fn(build_prompt(state))
            tactics = parse_tactics(response, state)
            return tactics if tactics else self._fallback(state)
        except Exception:
            return self._fallback(state)
