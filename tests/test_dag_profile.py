"""
Test del DAG-profile di refutazione Resolution -- Proof-DAG geometry arena.

Struttura
---------
B) Test di INVARIANZA (coppia di controllo): W(F) == W(sigma(F)) esatto.
   Se fallisce => la definizione non e` invariante: kill della DEFINIZIONE.
C) Test di CONSISTENZA: sum(W) == s, w* == max ampiezza nel DAG.
D) Test KILLER: (s, w*, W) per tutte le formule del pool;
   verifica se W e` funzione di (s, w*).
"""
import sys
import pytest

sys.stdout.reconfigure(encoding="utf-8")

from pnp_lab.proof_complexity.formula import CNF, pigeonhole_cnf
from pnp_lab.proof_complexity.dag_profile import (
    width_profile,
    canonical_refutation,
    min_width,
    WidthProfile,
)


# ---------------------------------------------------------------------------
# Pool di formule
# ---------------------------------------------------------------------------

def php21() -> CNF:
    """PHP_2^1: 2 piccioni, 1 buco."""
    return pigeonhole_cnf(2, 1)


def sigma_php21() -> CNF:
    """Rinomina delle variabili di PHP_2^1: var 1 <-> 2.

    PHP_2^1 ha clausole: {1}, {2}, {-1,-2}.
    Dopo sigma (1<->2): {2}, {1}, {-2,-1}  -- stessa formula riordinata.
    """
    clauses = [
        frozenset({2}),
        frozenset({1}),
        frozenset({-2, -1}),
    ]
    return CNF(clauses=clauses, num_vars=2, name="sigma(PHP21)")


def two_col_clash() -> CNF:
    """Formula 2-coloring clash su 2 variabili.

    Clausole: {1,-2}, {-1,2}, {1,2}, {-1,-2}.
    Forza x1=x2 (dalle prime due) e x1!=x2 (dalle ultime due): UNSAT.
    Profilo atteso: s=8, w*=2, W=(4,1,2,1), L=3.
    """
    return CNF(
        clauses=[
            frozenset({1, -2}),
            frozenset({-1, 2}),
            frozenset({1, 2}),
            frozenset({-1, -2}),
        ],
        num_vars=2,
        name="2col_clash",
    )


def diamond() -> CNF:
    """Formula a diamante su 3 variabili.

    Clausole: {1,2}, {-1,3}, {-2,3}, {-3}.
    Struttura: {1,2} si risolve con {-1,3} e {-2,3} per dare {3};
    poi {3} e {-3} danno la clausola vuota. DAG a diamante.
    Profilo atteso: s=8, w*=2, W=(4,2,1,1), L=3.
    """
    return CNF(
        clauses=[
            frozenset({1, 2}),
            frozenset({-1, 3}),
            frozenset({-2, 3}),
            frozenset({-3}),
        ],
        num_vars=3,
        name="f_diamond",
    )


# ---------------------------------------------------------------------------
# B) Test di INVARIANZA
# ---------------------------------------------------------------------------

class TestInvarianza:
    """Coppia di controllo B: W(F) deve essere uguale a W(sigma(F)) esatto."""

    def test_invarianza_W_profile(self):
        """W(PHP21) == W(sigma(PHP21)) -- invarianza per rinomina di variabili."""
        f = php21()
        sf = sigma_php21()
        pf = width_profile(f)
        psf = width_profile(sf)
        assert pf.W == psf.W, (
            f"INVARIANZA FALLITA: W(F)={pf.W} != W(sigma(F))={psf.W}\n"
            "=> La definizione del profilo NON e` invariante per rinomina. "
            "Kill della DEFINIZIONE (non dell'ipotesi)."
        )

    def test_invarianza_w_star(self):
        f = php21()
        sf = sigma_php21()
        assert min_width(f) == min_width(sf)

    def test_invarianza_s(self):
        f = php21()
        sf = sigma_php21()
        pf = width_profile(f)
        psf = width_profile(sf)
        assert pf.s == psf.s

    def test_invarianza_L(self):
        f = php21()
        sf = sigma_php21()
        pf = width_profile(f)
        psf = width_profile(sf)
        assert pf.L == psf.L


# ---------------------------------------------------------------------------
# C) Test di CONSISTENZA
# ---------------------------------------------------------------------------

class TestConsistenza:
    """Invariante: sum(W) == s, w* == max ampiezza nel DAG."""

    def _check_consistency(self, cnf: CNF) -> WidthProfile:
        prof = width_profile(cnf)
        assert sum(prof.W) == prof.s, (
            f"{cnf.name}: sum(W)={sum(prof.W)} != s={prof.s}"
        )
        nodes, edges = canonical_refutation(cnf)
        actual_max_width = max(len(c) for c in nodes)
        assert prof.w_star == actual_max_width, (
            f"{cnf.name}: w*={prof.w_star} != max ampiezza={actual_max_width}"
        )
        assert prof.L >= 0
        assert all(w >= 0 for w in prof.W)
        assert prof.W[prof.L] >= 1
        return prof

    def test_consistenza_php21(self):
        p = self._check_consistency(php21())
        # Valori esatti misurati
        assert p.s == 5
        assert p.w_star == 2
        assert p.W == (3, 1, 1)
        assert p.L == 2

    def test_consistenza_sigma_php21(self):
        p = self._check_consistency(sigma_php21())
        assert p.s == 5
        assert p.w_star == 2
        assert p.W == (3, 1, 1)
        assert p.L == 2

    def test_consistenza_2col_clash(self):
        p = self._check_consistency(two_col_clash())
        assert p.s == 8
        assert p.w_star == 2
        assert p.W == (4, 1, 2, 1)
        assert p.L == 3

    def test_consistenza_diamond(self):
        p = self._check_consistency(diamond())
        assert p.s == 8
        assert p.w_star == 2
        assert p.W == (4, 2, 1, 1)
        assert p.L == 3


# ---------------------------------------------------------------------------
# D) Test KILLER: W e` funzione di (s, w*)?
# ---------------------------------------------------------------------------

class TestKiller:
    """Il killer dell'arena: W e` funzione di (s, w*)?

    Se esistono due formule con (s, w*) uguali e W diverso => CONFERMATO
    (W e` un invariante strettamente piu` fine di (s, w*)).
    Se tutte le coppie iso-(s,w*) hanno W identico => RESTATEMENT.
    """

    def _collect_profiles(self):
        formulas = [
            php21(),
            sigma_php21(),
            two_col_clash(),
            diamond(),
        ]
        return [(f.name, width_profile(f)) for f in formulas]

    def test_killer_distinguishing_pair_exists(self):
        """Coppia (2col_clash, f_diamond): stessi (s=8, w*=2), W diverso.

        2col_clash: W=(4,1,2,1)  -- due clausole a livello 2
        f_diamond:  W=(4,2,1,1)  -- due clausole a livello 1

        => CONFERMATO: W non e` determinato da (s, w*).
        """
        p_clash = width_profile(two_col_clash())
        p_diamond = width_profile(diamond())

        # Stessi (s, w*)
        assert (p_clash.s, p_clash.w_star) == (p_diamond.s, p_diamond.w_star), (
            f"Le due formule non hanno piu` stesso (s,w*): "
            f"clash=({p_clash.s},{p_clash.w_star}), diamond=({p_diamond.s},{p_diamond.w_star})"
        )
        # W diverso => CONFERMATO
        assert p_clash.W != p_diamond.W, (
            f"W identico ({p_clash.W}): la coppia non discrimina. "
            "Estendi il pool."
        )

    def test_killer_verdetto(self, capsys):
        """Stampa il verdetto completo del killer per l'Explorer."""
        profiles = self._collect_profiles()

        groups: dict[tuple[int, int], list[tuple[str, WidthProfile]]] = {}
        for name, p in profiles:
            key = (p.s, p.w_star)
            groups.setdefault(key, []).append((name, p))

        found_distinguishing = False
        for (s, w_star), members in groups.items():
            if len(members) >= 2:
                W_values = [p.W for _, p in members]
                if len(set(W_values)) > 1:
                    found_distinguishing = True

        verdict = (
            "CONFERMATO: W distingue formule iso-(s,w*)"
            if found_distinguishing
            else "RESTATEMENT: W non distingue nel pool corrente"
        )
        print(f"\n[KILLER] {verdict}")
        for name, p in profiles:
            print(f"  {name}: s={p.s}, w*={p.w_star}, W={p.W}, L={p.L}")

        # Il test afferma il verdetto atteso
        assert found_distinguishing, (
            "Pool insufficiente: nessuna coppia iso-(s,w*) con W diverso trovata."
        )
