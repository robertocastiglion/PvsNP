"""La morale: lo switching lemma e perché la parità sta fuori da AC0."""

from __future__ import annotations


def switching_summary() -> str:
    """Testo che lega l'esperimento al teorema parità ∉ AC0."""
    return "\n".join(
        [
            "=" * 72,
            "  LO SWITCHING LEMMA  (Håstad, 1986)  →  parità ∉ AC0",
            "=" * 72,
            "  Un circuito AC0 ha profondità costante d e porte ∧/∨ di fan-in qualunque:",
            "  ogni livello è, in piccolo, una DNF o una CNF di larghezza limitata.",
            "",
            "  Lo switching lemma dice che sotto una restrizione casuale (ogni variabile",
            "  resta libera con prob. p) una DNF di larghezza w 'switcha' a un albero di",
            "  decisione di profondità ≥ s solo con prob. ≤ (5 p w)^s. Scegliendo p",
            "  piccolo, ogni livello del circuito si appiattisce: applicando la",
            "  restrizione d-1 volte, l'intero AC0 collassa a una funzione che dipende da",
            "  pochissime variabili — quindi quasi costante.",
            "",
            "  Ma la PARITÀ ristretta resta la parità delle variabili libere. Il suo",
            "  albero di decisione ha profondità ESATTAMENTE pari al numero di variabili",
            "  libere: per decidere la parità le devi leggere tutte. Finché restano",
            "  abbastanza variabili libere, la parità non è affatto costante.",
            "",
            "  Contraddizione: se la parità fosse in AC0, dopo le restrizioni dovrebbe",
            "  appiattirsi come ogni AC0 — ma non lo fa. Dunque parità ∉ AC0.",
            "",
            "  In questo modulo lo VEDIAMO: la profondità della DNF resta bassa e piatta",
            "  al crescere delle variabili libere, mentre quella della parità segue la",
            "  diagonale. È il caso esatto del 'muro della parità' del Modulo 6, ora",
            "  spiegato dal meccanismo che lo produce.",
            "=" * 72,
        ]
    )
