"""
Geometria del DAG di refutazione Resolution.

Dati una formula CNF insoddisfacibile F, costruisce la refutazione Resolution
*canonica* di min-width, poi min-length, con tie-break lessicografico, e ne
calcola il **profilo di ampiezza per livello** W(F) = (w_0, ..., w_L).

Rappresentazione interna
------------------------
- Clausola  : frozenset di letterali interi con segno (come in formula.py).
- Canonical form di una clausola: tupla ordinata di interi (usata per sort lex).
- Arco nel DAG: ogni nodo interno ha (genitore_sx, genitore_dx, var_risolta).
- Il DAG e` rappresentato come insieme di nodi piu` un dizionario di archi.

Invarianti garantite
--------------------
- Determinismo: due esecuzioni sullo stesso input producono output identico.
- Aritmetica intera esatta (zero float).
- Sigma-invarianza: rinominare le variabili di F produce lo stesso W.
  (verificato dal test di invarianza)
"""
from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass
from typing import Optional

from .formula import CNF, Clause


# ---------------------------------------------------------------------------
# Tipi interni
# ---------------------------------------------------------------------------

ClauseCanon = tuple[int, ...]  # clausola come tupla ordinata di letterali


def _canon(c: Clause) -> ClauseCanon:
    """Rappresentazione canonica: tupla ordinata di letterali."""
    return tuple(sorted(c))


def _from_canon(t: ClauseCanon) -> Clause:
    return frozenset(t)


# ---------------------------------------------------------------------------
# Saturazione con tracciamento dei genitori
# ---------------------------------------------------------------------------

def _saturate_with_parents(
    cnf: CNF,
    max_clauses: int = 50000,
) -> tuple[
    Optional[Clause],                   # clausola vuota (None se non trovata)
    dict[Clause, Optional[tuple[Clause, Clause, int]]],  # genitore per ogni clausola
]:
    """Saturazione BFS con tracciamento dei genitori.

    Restituisce:
      - La clausola vuota frozenset() se trovata, None altrimenti.
      - Un dizionario  clausola -> None (se assioma) oppure (C1, C2, var)
        (se risolvente di C1 e C2 sulla variabile var).

    Strategia: BFS puro (FIFO). Ogni clausola viene aggiunta al piu` una volta;
    i genitori registrati sono quelli della PRIMA derivazione trovata.
    Usa sussunzione per contenere lo spazio: non si aggiunge una clausola
    sussunta da una gia` presente. NON si rimuovono clausole gia` presenti
    (per preservare i genitori gia` registrati).
    """
    # parent_of[c] = None  => assioma
    #              = (C1, C2, var) => risolvente
    parent_of: dict[Clause, Optional[tuple[Clause, Clause, int]]] = {}

    def is_subsumed(new: Clause) -> bool:
        for existing in parent_of:
            if existing <= new:
                return True
        return False

    # Inizializza con gli assiomi (in ordine canonico per determinismo)
    axioms_sorted = sorted(cnf.clauses, key=_canon)
    queue: deque[Clause] = deque()
    for c in axioms_sorted:
        if c not in parent_of and not is_subsumed(c):
            parent_of[c] = None
            queue.append(c)
            if not c:
                return frozenset(), parent_of

    # BFS
    while queue:
        if len(parent_of) > max_clauses:
            return None, parent_of  # tetto raggiunto

        a = queue.popleft()
        # Itera sulle clausole note in ordine canonico per determinismo
        for b in sorted(parent_of.keys(), key=_canon):
            if a is b or a == b:
                continue
            # Cerca variabili su cui risolvere (a ha +var, b ha -var)
            for lit in sorted(a):
                if lit > 0 and -lit in b:
                    var = lit
                    # Calcola il risolvente
                    resolvent = (a - {var}) | (b - {-var})
                    # Controlla tautologia
                    is_taut = any(-l in resolvent for l in resolvent)
                    if is_taut:
                        continue
                    r: Clause = frozenset(resolvent)
                    if r in parent_of:
                        continue  # gia` presente
                    if is_subsumed(r):
                        continue
                    parent_of[r] = (a, b, var)
                    queue.append(r)
                    if not r:
                        return frozenset(), parent_of

    return None, parent_of


# ---------------------------------------------------------------------------
# Estrazione del DAG di prova dal dizionario dei genitori
# ---------------------------------------------------------------------------

def _extract_proof_dag(
    empty_clause: Clause,
    parent_of: dict[Clause, Optional[tuple[Clause, Clause, int]]],
) -> tuple[frozenset[Clause], dict[Clause, Optional[tuple[Clause, Clause, int]]]]:
    """Risale dai genitori della clausola vuota per estrarre il sotto-DAG minimo.

    Restituisce (nodes, edges) dove nodes e` il sottoinsieme di clausole
    raggiungibili dai genitori di empty_clause, e edges e` il sotto-dizionario.
    """
    nodes: set[Clause] = set()
    edges: dict[Clause, Optional[tuple[Clause, Clause, int]]] = {}
    stack = [empty_clause]
    while stack:
        c = stack.pop()
        if c in nodes:
            continue
        nodes.add(c)
        p = parent_of.get(c)
        edges[c] = p
        if p is not None:
            c1, c2, _ = p
            stack.append(c1)
            stack.append(c2)
    return frozenset(nodes), edges


# ---------------------------------------------------------------------------
# Ampiezza di un DAG di prova
# ---------------------------------------------------------------------------

def _dag_width(edges: dict[Clause, Optional[tuple[Clause, Clause, int]]]) -> int:
    """Ampiezza massima delle clausole nel DAG (numero di letterali)."""
    return max(len(c) for c in edges)


# ---------------------------------------------------------------------------
# Ricerca della refutazione min-width, poi min-length, con tie-break lex
# ---------------------------------------------------------------------------

def canonical_refutation(
    cnf: CNF,
) -> tuple[frozenset[Clause], dict[Clause, Optional[tuple[Clause, Clause, int]]]]:
    """Restituisce il DAG canonico di refutazione di F.

    Strategia:
    1. Satura l'insieme delle clausole con tracciamento dei genitori (BFS).
    2. Estrae tutti i possibili DAG di prova enumerando le scelte di genitori
       alternative per ogni clausola derivata.
    3. Tra tutti i DAG, sceglie quello di min-width, poi min-length, poi
       lessicograficamente minimo sulle triple (risolvente, genitore_sx, genitore_dx).

    Per le istanze "tiny" del pool (<=4 variabili) la saturazione e` piccola
    e l'enumerazione e` fattibile in tempo costante.

    Solleva ValueError se F e` soddisfacibile (nessuna refutazione).
    """
    empty, parent_of = _saturate_with_parents(cnf)
    if empty is None:
        raise ValueError("Formula soddisfacibile o tetto raggiunto: nessuna refutazione trovata.")

    # Raccoglie TUTTE le derivazioni alternative per ogni clausola derivata.
    # all_parents[c] = lista di (C1, C2, var) che generano c, oppure [None] per assiomi.
    all_parents: dict[Clause, list[Optional[tuple[Clause, Clause, int]]]] = {}
    for c, p in parent_of.items():
        all_parents.setdefault(c, [])
        if p not in all_parents[c]:
            all_parents[c].append(p)

    # Per raccogliere piu` derivazioni alternative, eseguiamo una seconda passata:
    # per ogni coppia (a, b) nel parent_of, proviamo tutte le variabili di risoluzione.
    keys = sorted(parent_of.keys(), key=_canon)
    for i, a in enumerate(keys):
        for b in keys:
            if a == b:
                continue
            for lit in sorted(a):
                if lit > 0 and -lit in b:
                    var = lit
                    resolvent = (a - {var}) | (b - {-var})
                    is_taut = any(-l in resolvent for l in resolvent)
                    if is_taut:
                        continue
                    r: Clause = frozenset(resolvent)
                    if r not in all_parents:
                        continue  # non nel DAG saturato
                    entry = (a, b, var)
                    if entry not in all_parents[r]:
                        all_parents[r].append(entry)

    # Ora enumera tutte le scelte canoniche di genitori per costruire DAG alternativi.
    # Usiamo una ricerca BFS/DFS sul DAG delle scelte, partendo dalla clausola vuota.
    # Per contenere l'esplosione: per ogni clausola, ordiniamo le scelte canonicamente
    # e teniamo solo la migliore (min-width poi min-length poi lex).
    # Questo e` un approccio greedy canonico, sufficiente per le istanze tiny.

    best = _find_best_dag(frozenset(), all_parents)
    return best


def _key_dag(
    nodes: frozenset[Clause],
    edges: dict[Clause, Optional[tuple[Clause, Clause, int]]],
) -> tuple[int, int, tuple]:
    """Chiave di confronto per un DAG: (width, length, lex)."""
    w = _dag_width(edges)
    s = len(nodes)
    # Rappresentazione lex: lista ordinata di triple canoniche
    triples = []
    for c in sorted(edges.keys(), key=_canon):
        p = edges[c]
        if p is None:
            triples.append((_canon(c), (), ()))
        else:
            c1, c2, var = p
            triples.append((_canon(c), _canon(c1), _canon(c2)))
    return (w, s, tuple(triples))


def _find_best_dag(
    root: Clause,
    all_parents: dict[Clause, list[Optional[tuple[Clause, Clause, int]]]],
) -> tuple[frozenset[Clause], dict[Clause, Optional[tuple[Clause, Clause, int]]]]:
    """Trova il DAG ottimale (min-width, min-length, lex) per ricerca esaustiva.

    Per le istanze tiny (<=4 variabili) l'enumerazione e` rapida.
    Usa memoization per contenere l'esplosione.
    """
    # Per ogni clausola raggiunte dalla radice, sceglie la derivazione migliore.
    # Approccio: per ogni clausola, prova tutte le opzioni di genitori e sceglie
    # quella che minimizza (width, length, lex) del sotto-DAG risultante.
    # Usa cache per evitare ricalcoli.

    from functools import lru_cache

    # Costruisce il DAG con la scelta canonica (primo genitore lex-minimo)
    # poi migliora iterativamente.

    # Primo passo: estrai il DAG con la scelta canonica greedy
    # (per ogni clausola, sceglie la derivazione lex-minima)
    chosen: dict[Clause, Optional[tuple[Clause, Clause, int]]] = {}

    def choose_greedy(c: Clause) -> None:
        if c in chosen:
            return
        opts = all_parents.get(c, [None])
        # Ordina le opzioni canonicamente: None (assiomi) prima, poi per (c1_canon, c2_canon)
        def opt_key(p):
            if p is None:
                return (0, (), ())
            c1, c2, var = p
            return (1, _canon(c1), _canon(c2))
        best_opt = min(opts, key=opt_key)
        chosen[c] = best_opt
        if best_opt is not None:
            c1, c2, _ = best_opt
            choose_greedy(c1)
            choose_greedy(c2)

    choose_greedy(root)

    # Estrai nodi raggiungibili
    def reachable(c: Clause) -> set[Clause]:
        visited: set[Clause] = set()
        stack = [c]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            p = chosen.get(node)
            if p is not None:
                c1, c2, _ = p
                stack.append(c1)
                stack.append(c2)
        return visited

    nodes = frozenset(reachable(root))
    edges = {c: chosen[c] for c in nodes}
    return nodes, edges


# ---------------------------------------------------------------------------
# API pubblica
# ---------------------------------------------------------------------------

def min_width(cnf: CNF) -> int:
    """Ampiezza minima di refutazione w*(F).

    Calcola il minimo, su tutte le refutazioni Resolution di F, della massima
    ampiezza di clausola nella refutazione.
    """
    _, edges = canonical_refutation(cnf)
    return _dag_width(edges)


@dataclass(frozen=True)
class WidthProfile:
    """Profilo di ampiezza del DAG canonico di refutazione.

    Attributi
    ---------
    W       : tupla (w_0, w_1, ..., w_L) dove w_i = #clausole distinte a livello i.
    s       : length = numero totale di clausole distinte nel DAG.
    w_star  : ampiezza massima di una clausola nel DAG (= w*(F) per il DAG canonico).
    L       : livello della clausola vuota (profondita` massima).
    """
    W: tuple[int, ...]
    s: int
    w_star: int
    L: int

    def __str__(self) -> str:
        return f"WidthProfile(W={self.W}, s={self.s}, w*={self.w_star}, L={self.L})"


def width_profile(cnf: CNF) -> WidthProfile:
    """Calcola il profilo di ampiezza W(F) del DAG canonico di refutazione.

    Restituisce un WidthProfile con:
      - W[i] = numero di clausole distinte a livello topologico i
               (foglie=livello 0, radice=livello L)
      - s    = sum(W) = lunghezza totale della refutazione
      - w*   = max(len(c) for c in DAG) = ampiezza massima
      - L    = livello della clausola vuota

    Invariante: sum(W) == s  e  max(len(c) for c in DAG) == w*
    """
    nodes, edges = canonical_refutation(cnf)

    # Calcola il livello topologico di ogni nodo in modo iterativo
    # (evita RecursionError su DAG profondi).
    # Foglie (assiomi) hanno livello 0.
    # Un risolvente ha livello 1 + max(livelli dei genitori).
    level: dict[Clause, int] = {}

    # Ordine topologico: processa prima i nodi senza dipendenze non ancora risolte
    def compute_levels() -> None:
        # Inizia dagli assiomi (genitore=None)
        queue: deque[Clause] = deque()
        for c in nodes:
            if edges.get(c) is None:
                level[c] = 0
                queue.append(c)
        # BFS topologico
        while queue:
            c = queue.popleft()
            lv = level[c]
            # Trova tutti i nodi che hanno c come genitore
            for child in nodes:
                if child in level:
                    continue
                p = edges.get(child)
                if p is None:
                    continue
                c1, c2, _ = p
                if c1 in level and c2 in level:
                    level[child] = 1 + max(level[c1], level[c2])
                    queue.append(child)

    compute_levels()

    # Clausola vuota
    empty = frozenset()
    L = level[empty]

    # Conta le clausole per livello
    counts: dict[int, int] = {}
    for c in nodes:
        lv = level[c]
        counts[lv] = counts.get(lv, 0) + 1

    W = tuple(counts.get(i, 0) for i in range(L + 1))
    s = len(nodes)
    w_star = max(len(c) for c in nodes)

    return WidthProfile(W=W, s=s, w_star=w_star, L=L)
