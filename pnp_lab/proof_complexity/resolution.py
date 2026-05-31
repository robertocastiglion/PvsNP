"""
La **regola di resolution** e una refutazione verificata per i casi piccoli.

Resolution è il sistema di prova più studiato per le formule in CNF. Ha **una
sola regola**:

    da   (A ∨ x)   e   (B ∨ ¬x)   deduci   (A ∨ B)

Una *refutazione* è una sequenza di risoluzioni che, partendo dalle clausole
della formula, arriva alla **clausola vuota** (la contraddizione). Una formula
in CNF è insoddisfacibile se e solo se ha una refutazione per resolution
(completezza).

La saturazione completa esplode in fretta (è proprio il punto del teorema di
Haken), quindi qui la usiamo solo per **esibire una prova vera** sulle istanze
piccole, con un tetto esplicito al numero di clausole generate. La misura su
istanze grandi avviene invece via DPLL (vedi `dpll.py`).
"""
from __future__ import annotations

from dataclasses import dataclass

from .formula import CNF, Clause


def resolve(c1: Clause, c2: Clause, var: int) -> Clause | None:
    """Risolve `c1` e `c2` sulla variabile `var` (>0).

    Richiede `+var ∈ c1` e `-var ∈ c2`. Restituisce il risolvente, oppure
    `None` se il risolvente è una **tautologia** (contiene sia `w` sia `-w`):
    le tautologie sono inutili e si scartano.
    """
    if var <= 0 or var not in c1 or -var not in c2:
        raise ValueError("resolve: la variabile non compare con i segni giusti")
    resolvent = (c1 - {var}) | (c2 - {-var})
    for lit in resolvent:
        if -lit in resolvent:
            return None  # tautologia
    return frozenset(resolvent)


@dataclass(frozen=True)
class RefutationResult:
    """Esito di una ricerca di refutazione per resolution."""

    found_empty: bool
    generated: int
    capped: bool
    detail: str


def refute(cnf: CNF, max_clauses: int = 20000) -> RefutationResult:
    """Cerca la clausola vuota per **saturazione** con sussunzione.

    Genera risolventi finché trova la clausola vuota o raggiunge il tetto
    `max_clauses`. La sussunzione (scarto delle clausole sovrainsieme di una già
    presente) tiene a bada la crescita quanto basta per i casi piccoli.

    NB: è volutamente limitata — su PHP grande NON termina entro il tetto, ed è
    *esattamente* la lezione del teorema di Haken resa tangibile.
    """
    # insieme delle clausole correnti, tenuto minimale per sussunzione
    clauses: set[Clause] = set()

    def add_subsuming(new: Clause) -> bool:
        """Aggiunge `new` se non è sussunta; rimuove quelle che `new` sussume.
        Ritorna True se `new` è stata effettivamente aggiunta."""
        for c in clauses:
            if c <= new:  # esiste già una clausola più forte
                return False
        to_drop = {c for c in clauses if new < c}
        clauses.difference_update(to_drop)
        clauses.add(new)
        return True

    for c in cnf.clauses:
        if not c:
            return RefutationResult(True, 0, False, "clausola vuota già presente")
        add_subsuming(c)

    generated = 0
    # saturazione a punto fisso
    changed = True
    while changed:
        changed = False
        snapshot = list(clauses)
        for a in snapshot:
            for b in snapshot:
                if a is b:
                    continue
                # cerca una variabile su cui risolvere
                for lit in a:
                    if lit > 0 and -lit in b:
                        r = resolve(a, b, lit)
                        if r is None:
                            continue
                        generated += 1
                        if not r:
                            return RefutationResult(
                                True, generated, False,
                                "clausola vuota derivata: formula INSODD.",
                            )
                        if add_subsuming(r):
                            changed = True
                        if len(clauses) + generated > max_clauses:
                            return RefutationResult(
                                False, generated, True,
                                f"tetto di {max_clauses} clausole raggiunto "
                                "senza clausola vuota (saturazione troppo grande)",
                            )
    return RefutationResult(
        False, generated, False,
        "saturazione completata senza clausola vuota: formula SODDISFACIBILE",
    )
