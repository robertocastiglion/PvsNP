"""Refutazione resolution con DAG + estrazione dell'interpolante (Krajíček/Pudlák).

Una formula **split** è A(p, z) ∧ B(q, z) dove:
  * `z`  = variabili CONDIVISE (shared),
  * `p`  = variabili private di A,
  * `q`  = variabili private di B,
e nessuna clausola mescola `p` con `q` (è la condizione di split).

Teorema (feasible interpolation, Krajíček 1997 / Pudlák 1997): da una refutazione
resolution di A∧B si estrae, in tempo lineare nella taglia della refutazione, un
circuito I(z) tale che per ogni assegnamento α a z:
    I(α) = 0  ⟹  A(p, α) è INSODDISFACIBILE
    I(α) = 1  ⟹  B(q, α) è INSODDISFACIBILE

Costruzione (caso booleano). Ad ogni clausola C della refutazione si associa una
funzione h_C(z) (un gate del circuito):
  * C assioma di A           → h_C = 0
  * C assioma di B           → h_C = 1
  * C risolvente su w∈z      → h_C = MUX(z_w, h_{C⁻}, h_{C⁺})   (un gate per pivot shared)
  * C risolvente su w∈p (A)  → h_C = OR(h_{C⁺}, h_{C⁻})
  * C risolvente su w∈q (B)  → h_C = AND(h_{C⁺}, h_{C⁻})
dove C⁺ è il genitore con +w e C⁻ quello con ¬w. L'interpolante è h_∅ (clausola vuota).

Qui NON ci fidiamo della costruzione a parole: `verify_interpolant` controlla la
proprietà semantica su TUTTI gli α ∈ {0,1}^|z| per forza bruta (le private sono poche).
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product

from pnp_lab.proof_complexity.formula import CNF, Clause
from pnp_lab.proof_complexity.resolution import resolve


# --------------------------------------------------------------------------- #
#  Split formula                                                              #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Split:
    """Una formula split A(p,z) ∧ B(q,z)."""

    a_clauses: tuple[Clause, ...]
    b_clauses: tuple[Clause, ...]
    shared: frozenset[int]      # variabili z (interi positivi)
    a_private: frozenset[int]   # variabili p
    b_private: frozenset[int]   # variabili q

    def all_clauses(self) -> list[Clause]:
        return list(self.a_clauses) + list(self.b_clauses)

    def check_split(self) -> None:
        """Verifica che nessuna clausola mescoli p con q e che i tag siano coerenti."""
        for c in self.a_clauses:
            vs = {abs(l) for l in c}
            if vs & self.b_private:
                raise ValueError(f"clausola A tocca variabili B-private: {c}")
            if not vs <= (self.shared | self.a_private):
                raise ValueError(f"clausola A con variabili ignote: {c}")
        for c in self.b_clauses:
            vs = {abs(l) for l in c}
            if vs & self.a_private:
                raise ValueError(f"clausola B tocca variabili A-private: {c}")
            if not vs <= (self.shared | self.b_private):
                raise ValueError(f"clausola B con variabili ignote: {c}")


# --------------------------------------------------------------------------- #
#  Refutazione con DAG                                                        #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class DagNode:
    """Nodo del DAG di refutazione: clausola + provenienza."""

    clause: Clause
    side: str | None        # 'A' o 'B' se assioma, None se risolvente
    parents: tuple[Clause, Clause] | None  # (C⁺, C⁻) se risolvente
    pivot: int | None       # variabile di risoluzione (>0)


@dataclass(frozen=True)
class DagRefutation:
    found_empty: bool
    nodes: dict[Clause, DagNode]   # clausola -> come è stata ottenuta (prima derivazione)
    steps: int                     # numero di passi di risoluzione registrati
    capped: bool


def dag_refute(split: Split, max_clauses: int = 20000) -> DagRefutation:
    """Saturazione con sussunzione che REGISTRA il DAG (genitori + pivot).

    A differenza di `resolution.refute`, qui teniamo per ogni clausola la sua
    prima derivazione, così da poter ricostruire l'interpolante.
    """
    nodes: dict[Clause, DagNode] = {}
    clauses: set[Clause] = set()

    def add(new: Clause, node: DagNode) -> bool:
        # niente sussunzione "distruttiva" sul DAG: registriamo la prima derivazione
        # ma per il controllo di crescita usiamo comunque la sussunzione sull'insieme attivo.
        for c in clauses:
            if c <= new:
                return False
        to_drop = {c for c in clauses if new < c}
        clauses.difference_update(to_drop)
        clauses.add(new)
        if new not in nodes:
            nodes[new] = node
        return True

    for c in split.a_clauses:
        add(c, DagNode(c, "A", None, None))
    for c in split.b_clauses:
        add(c, DagNode(c, "B", None, None))

    empty: Clause = frozenset()
    if empty in clauses:
        return DagRefutation(True, nodes, 0, False)

    steps = 0
    changed = True
    while changed:
        changed = False
        snapshot = list(clauses)
        for a in snapshot:
            for b in snapshot:
                if a is b:
                    continue
                for lit in a:
                    if lit > 0 and -lit in b:
                        r = resolve(a, b, lit)
                        if r is None:
                            continue
                        steps += 1
                        node = DagNode(r, None, (a, b), lit)  # a=C⁺ (+lit), b=C⁻ (-lit)
                        if not r:
                            nodes.setdefault(r, node)
                            return DagRefutation(True, nodes, steps, False)
                        if add(r, node):
                            changed = True
                        if len(clauses) + steps > max_clauses:
                            return DagRefutation(False, nodes, steps, True)
    return DagRefutation(False, nodes, steps, False)


# --------------------------------------------------------------------------- #
#  Circuito interpolante                                                      #
# --------------------------------------------------------------------------- #
# Un gate è una tupla con structural sharing (memoizzazione per identità di sotto-circuito):
#   ('const', 0|1)
#   ('mux', var, g_low, g_high)   # var∈z: se z_var=0 -> g_low, se =1 -> g_high
#   ('or',  g1, g2)
#   ('and', g1, g2)
Gate = tuple


@dataclass(frozen=True)
class Interpolant:
    root: Gate
    gate_count: int           # gate non-const distinti (con sharing)
    mux_gates: int            # quanti MUX (= passi su variabili shared)
    bool_gates: int           # quanti AND/OR


def build_interpolant(split: Split, ref: DagRefutation) -> Interpolant:
    """Costruisce h_∅ via la costruzione booleana, con structural sharing."""
    if not ref.found_empty:
        raise ValueError("nessuna refutazione: niente interpolante")

    memo: dict[Clause, Gate] = {}
    seen_gates: set[Gate] = set()   # per contare gate distinti

    def reg(g: Gate) -> Gate:
        if g[0] != "const":
            seen_gates.add(g)
        return g

    def h(clause: Clause) -> Gate:
        if clause in memo:
            return memo[clause]
        node = ref.nodes[clause]
        if node.side == "A":
            g: Gate = ("const", 0)
        elif node.side == "B":
            g = ("const", 1)
        else:
            assert node.parents is not None and node.pivot is not None
            c_plus, c_minus = node.parents
            w = node.pivot
            hp, hm = h(c_plus), h(c_minus)
            if w in split.shared:
                # invariante Krajíček: z_w=0 → ramo del genitore con +w (C⁺), z_w=1 → C⁻
                g = reg(("mux", w, hp, hm))
            elif w in split.a_private:
                g = reg(("or", hp, hm))
            elif w in split.b_private:
                g = reg(("and", hp, hm))
            else:
                raise ValueError(f"pivot {w} non classificato")
        memo[clause] = g
        return g

    root = h(frozenset())
    mux = sum(1 for g in seen_gates if g[0] == "mux")
    boolg = sum(1 for g in seen_gates if g[0] in ("and", "or"))
    return Interpolant(root, len(seen_gates), mux, boolg)


def build_interpolant_swapped(split: Split, ref: DagRefutation) -> Interpolant:
    """IDENTICA a build_interpolant ma con la REGOLA PRIVATA SCAMBIATA:
        pivot A-privato → AND   (invece di OR)
        pivot B-privato → OR    (invece di AND)

    Serve al test "buco-2": se l'istanza FORZA davvero la regola corretta, allora
    verify_interpolant su questo interpolante-scambiato DEVE fallire su almeno un α.
    """
    if not ref.found_empty:
        raise ValueError("nessuna refutazione: niente interpolante")

    memo: dict[Clause, Gate] = {}
    seen_gates: set[Gate] = set()

    def reg(g: Gate) -> Gate:
        if g[0] != "const":
            seen_gates.add(g)
        return g

    def h(clause: Clause) -> Gate:
        if clause in memo:
            return memo[clause]
        node = ref.nodes[clause]
        if node.side == "A":
            g: Gate = ("const", 0)
        elif node.side == "B":
            g = ("const", 1)
        else:
            assert node.parents is not None and node.pivot is not None
            c_plus, c_minus = node.parents
            w = node.pivot
            hp, hm = h(c_plus), h(c_minus)
            if w in split.shared:
                g = reg(("mux", w, hp, hm))
            elif w in split.a_private:
                g = reg(("and", hp, hm))   # SCAMBIO: era OR
            elif w in split.b_private:
                g = reg(("or", hp, hm))    # SCAMBIO: era AND
            else:
                raise ValueError(f"pivot {w} non classificato")
        memo[clause] = g
        return g

    root = h(frozenset())
    mux = sum(1 for g in seen_gates if g[0] == "mux")
    boolg = sum(1 for g in seen_gates if g[0] in ("and", "or"))
    return Interpolant(root, len(seen_gates), mux, boolg)


def eval_gate(g: Gate, z: dict[int, int]) -> int:
    if g[0] == "const":
        return g[1]
    if g[0] == "mux":
        _, var, glow, ghigh = g
        return eval_gate(ghigh, z) if z[var] else eval_gate(glow, z)
    if g[0] == "or":
        return eval_gate(g[1], z) | eval_gate(g[2], z)
    if g[0] == "and":
        return eval_gate(g[1], z) & eval_gate(g[2], z)
    raise ValueError(g)


# --------------------------------------------------------------------------- #
#  Semantica esatta (forza bruta sulle private) per la verifica               #
# --------------------------------------------------------------------------- #
def _restrict_sat(clauses: tuple[Clause, ...], shared: frozenset[int],
                  private: frozenset[int], z: dict[int, int]) -> bool:
    """C'è un assegnamento delle private che soddisfa `clauses` dato z fissato?"""
    priv = sorted(private)
    for bits in product((0, 1), repeat=len(priv)):
        assign = dict(z)
        assign.update(dict(zip(priv, bits)))
        ok = True
        for c in clauses:
            if not any((lit > 0 and assign.get(abs(lit), 0) == 1) or
                       (lit < 0 and assign.get(abs(lit), 0) == 0) for lit in c):
                ok = False
                break
        if ok:
            return True
    return False


def verify_interpolant(split: Split, interp: Interpolant) -> dict:
    """Controlla la proprietà di interpolazione su TUTTI gli α ∈ {0,1}^|z|.

    Ritorna {'ok': bool, 'truth_table': {alpha_tuple: I(alpha)}, 'violations': [...]}.
    """
    zs = sorted(split.shared)
    tt: dict[tuple[int, ...], int] = {}
    violations = []
    for bits in product((0, 1), repeat=len(zs)):
        z = dict(zip(zs, bits))
        val = eval_gate(interp.root, z)
        tt[bits] = val
        a_sat = _restrict_sat(split.a_clauses, split.shared, split.a_private, z)
        b_sat = _restrict_sat(split.b_clauses, split.shared, split.b_private, z)
        # I=0 deve garantire A insodd; I=1 deve garantire B insodd
        if val == 0 and a_sat:
            violations.append((bits, "I=0 ma A è SODD"))
        if val == 1 and b_sat:
            violations.append((bits, "I=1 ma B è SODD"))
    return {"ok": not violations, "truth_table": tt, "violations": violations}


# --------------------------------------------------------------------------- #
#  Interpolante MINIMO sulla tavola di verità (forza bruta su z piccoli)       #
# --------------------------------------------------------------------------- #
def min_interpolant_dt_size(split: Split) -> dict:
    """Calcola, su z piccoli, l'INSIEME degli interpolanti ammessi e la taglia
    minima di un albero di decisione (numero di foglie) che li realizza.

    Un α è 'don't care' se sia A|α che B|α sono insodd (l'interpolante può valere
    0 o 1); altrimenti è forzato. Restituisce la taglia DT minima sul miglior
    completamento dei don't care (programmazione dinamica esatta su {0,1}^|z|).
    """
    zs = sorted(split.shared)
    n = len(zs)
    # forced[bits] ∈ {0,1,None(=don't care)}
    forced: dict[tuple[int, ...], int | None] = {}
    for bits in product((0, 1), repeat=n):
        z = dict(zip(zs, bits))
        a_sat = _restrict_sat(split.a_clauses, split.shared, split.a_private, z)
        b_sat = _restrict_sat(split.b_clauses, split.shared, split.b_private, z)
        if not a_sat and not b_sat:
            forced[bits] = None        # don't care
        elif not a_sat:
            forced[bits] = 0           # A insodd -> I deve poter essere 0 (forzato 0)
        elif not b_sat:
            forced[bits] = 1           # B insodd -> forzato 1
        else:
            # A sodd e B sodd contemporaneamente per questo α: A∧B non sarebbe unsat
            forced[bits] = -1          # impossibile da interpolare

    if any(v == -1 for v in forced.values()):
        return {"interpolatable": False, "min_leaves": None}

    # DT minimo per foglie su un sottocubo (subset di indici già fissati).
    # Stato: dict var->bit dei vincoli; valutiamo su tutti i 2^n con maschera.
    from functools import lru_cache

    cells = list(product((0, 1), repeat=n))

    @lru_cache(maxsize=None)
    def best(mask: tuple, fixed: tuple) -> int:
        # mask: tuple di n elementi in {0,1,None}; cella appartiene al sottocubo se
        # combacia con tutti i bit non-None. fixed = stessa cosa (passiamo mask).
        sub = [c for c in cells
               if all(mask[i] is None or mask[i] == c[i] for i in range(n))]
        vals = {forced[c] for c in sub if forced[c] is not None}
        if len(vals) <= 1:
            return 1  # una foglia basta (costante ammessa)
        bestcost = None
        for i in range(n):
            if mask[i] is not None:
                continue
            m0 = tuple(0 if j == i else mask[j] for j in range(n))
            m1 = tuple(1 if j == i else mask[j] for j in range(n))
            cost = best(m0, m0) + best(m1, m1)
            if bestcost is None or cost < bestcost:
                bestcost = cost
        return bestcost

    start = tuple([None] * n)
    leaves = best(start, start)
    return {"interpolatable": True, "min_leaves": leaves, "n_shared": n}
