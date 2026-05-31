"""
Formule in CNF e codifica del **principio della piccionaia** (pigeonhole).

Rappresentazione minimale, zero dipendenze:
  * un **letterale** è un intero con segno: `+k` = variabile k vera, `-k` = falsa;
  * una **clausola** è un `frozenset` di letterali (una disgiunzione OR);
  * una **CNF** è una congiunzione AND di clausole.

Il cuore del modulo è `pigeonhole_cnf(pigeons, holes)`. Il principio della
piccionaia dice che non puoi sistemare `pigeons` piccioni in `holes` buche, uno
per buca, se `pigeons > holes`. Tradotto in CNF diventa **insoddisfacibile**
esattamente in quel caso — ed è la formula più famosa della *proof complexity*,
perché ogni refutazione per resolution della versione PHP^(n+1)_n ha dimensione
**esponenziale** (teorema di Haken, 1985).
"""
from __future__ import annotations

from dataclasses import dataclass, field

# Una clausola è un insieme di letterali interi con segno.
Clause = frozenset[int]


@dataclass
class CNF:
    """Una formula in forma normale congiuntiva, con un po' di metadati."""

    clauses: list[Clause]
    num_vars: int
    name: str = ""
    var_label: dict[int, str] = field(default_factory=dict)

    @property
    def num_clauses(self) -> int:
        return len(self.clauses)

    @property
    def width(self) -> int:
        """Larghezza = numero massimo di letterali in una clausola."""
        return max((len(c) for c in self.clauses), default=0)

    def describe(self) -> str:
        return (
            f"{self.name or 'CNF'}: {self.num_vars} variabili, "
            f"{self.num_clauses} clausole, larghezza {self.width}"
        )


def pigeonhole_cnf(pigeons: int, holes: int) -> CNF:
    """Codifica PHP: `pigeons` piccioni in `holes` buche.

    Variabile x(i, j) = "il piccione i sta nella buca j", con
    indice = (i - 1) * holes + j  (numerazione 1-based).

    Clausole:
      * **piccione** — ogni piccione sta in almeno una buca:
        per ogni i,  (x(i,1) ∨ x(i,2) ∨ … ∨ x(i,holes)).
        Sono `pigeons` clausole, ciascuna di larghezza `holes`.
      * **buca** — nessuna buca ospita due piccioni:
        per ogni buca j e ogni coppia i < i',  (¬x(i,j) ∨ ¬x(i',j)).

    La formula è **insoddisfacibile** se e solo se `pigeons > holes`.
    """
    if pigeons < 1 or holes < 1:
        raise ValueError("servono almeno 1 piccione e 1 buca")

    def var(i: int, j: int) -> int:
        return (i - 1) * holes + j

    clauses: list[Clause] = []

    # ogni piccione in almeno una buca
    for i in range(1, pigeons + 1):
        clauses.append(frozenset(var(i, j) for j in range(1, holes + 1)))

    # nessuna buca con due piccioni
    for j in range(1, holes + 1):
        for i in range(1, pigeons + 1):
            for i2 in range(i + 1, pigeons + 1):
                clauses.append(frozenset({-var(i, j), -var(i2, j)}))

    labels = {
        var(i, j): f"x[{i}->{j}]"
        for i in range(1, pigeons + 1)
        for j in range(1, holes + 1)
    }
    sat = "SODD." if pigeons <= holes else "INSODD."
    return CNF(
        clauses=clauses,
        num_vars=pigeons * holes,
        name=f"PHP {pigeons} piccioni / {holes} buche [{sat}]",
        var_label=labels,
    )


def horn_chain_cnf(length: int) -> CNF:
    """Una catena di implicazioni soddisfacibile e *facile* — per contrasto.

    x1, e x1→x2, x2→x3, …, e infine ¬x_length. È soddisfacibile? No: la catena
    forza x_length vero, ma l'ultima clausola lo nega → INSODD., però con una
    refutazione **lineare** (la propagazione unitaria basta). Serve a mostrare il
    contrasto con la piccionaia: stessa "insoddisfacibilità", costo del tutto
    diverso.
    """
    if length < 1:
        raise ValueError("length >= 1")
    clauses: list[Clause] = [frozenset({1})]  # x1
    for k in range(1, length):
        clauses.append(frozenset({-k, k + 1}))  # x_k -> x_{k+1}
    clauses.append(frozenset({-length}))  # ¬x_length
    return CNF(
        clauses=clauses,
        num_vars=length,
        name=f"Catena di Horn ({length}) [INSODD., facile]",
        var_label={k: f"x{k}" for k in range(1, length + 1)},
    )
