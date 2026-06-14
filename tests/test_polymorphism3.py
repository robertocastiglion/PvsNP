"""Direzione B, ciclo TERNARIO — test ESATTI dei politomorfismi su D={0,1,2}.

Fissa i NUMERI misurati del catalogo (g, profilo simmetrico, |Aut|, marker) cosi` sono
rigenerabili, e l'esito dei 3 killer di H. Tutto esatto/deterministico/finito.
"""

import pytest

from pnp_lab.csp.polymorphism3 import (
    CATALOG,
    MAJORITY3,
    MEDIAN3,
    analyze3,
    commutative_idempotent_binary_ops,
    count_wnu_witnesses,
    g,
    has_wnu,
    op_value3,
    preserves3,
    symmetric_idempotent_ops,
    symmetric_profile3,
    unary_automorphisms,
    wnu_witnesses,
    _binary_table_from_offdiag,
)


# --------------------------------------------------------------------------- #
#  Sanity: op_value3 in base 3 e preserves3                                    #
# --------------------------------------------------------------------------- #

def test_op_value3_base3_indexing():
    # tavola identita` sull'indice: op_table[idx] = idx mod 3 e` mal definita; usiamo
    # una tavola esplicita e verifichiamo idx = sum args[i]*3^i.
    # tavola di 9 valori per k=2: idx = x + 3*y
    table = tuple(range(9))  # NB: non in {0,1,2}, ma testa solo l'indicizzazione
    assert op_value3(table, (0, 0)) == 0   # idx 0
    assert op_value3(table, (1, 0)) == 1   # idx 1
    assert op_value3(table, (2, 0)) == 2   # idx 2
    assert op_value3(table, (0, 1)) == 3   # idx 3
    assert op_value3(table, (2, 2)) == 8   # idx 8
    # k=3: idx = a + 3b + 9c
    t3 = tuple(range(27))
    assert op_value3(t3, (1, 2, 1)) == 1 + 3 * 2 + 9 * 1


def test_preserves3_known_polymorphism():
    R = CATALOG["min_graph"]
    # min preserva il proprio grafo (semilattice -> politomorfismo binario di se`)
    min_table = _binary_table_from_offdiag(0, 0, 1)  # min(0,1)=0,min(0,2)=0,min(1,2)=1
    assert preserves3(min_table, 2, R) is True
    # la maggioranza NON preserva il grafo di min (non e` chiuso sotto majority)
    assert preserves3(MAJORITY3, 2, CATALOG["cycle3"]) is False


def test_majority_and_median_preserve_leq():
    # leq e` chiusa sotto la mediana (ordine lineare) -> ha un WNU ternario
    R = CATALOG["leq"]
    assert preserves3(MEDIAN3, 3, R) is True


# --------------------------------------------------------------------------- #
#  Le 27 binarie idempotenti commutative                                       #
# --------------------------------------------------------------------------- #

def test_count_commutative_idempotent_binary_ops_is_27():
    ops = commutative_idempotent_binary_ops()
    assert len(ops) == 27
    # tutte distinte
    assert len(set(ops)) == 27
    # tutte idempotenti (diagonale x->x) e commutative
    for op in ops:
        for x in (0, 1, 2):
            assert op_value3(op, (x, x)) == x
        for x in (0, 1, 2):
            for y in (0, 1, 2):
                assert op_value3(op, (x, y)) == op_value3(op, (y, x))
        # valori in {0,1,2}
        assert all(v in (0, 1, 2) for v in op)


# --------------------------------------------------------------------------- #
#  g calcolato a mano                                                          #
# --------------------------------------------------------------------------- #

def test_g_min_graph_computed_by_hand():
    """min_graph = {(x,y,min(x,y))}. Calcolo A MANO:
    - Automorfismi unari: una permutazione pi fissa il grafo di min sse min(pi x,pi y) =
      pi min(x,y) per ogni x,y, cioe` sse pi e` un automorfismo dell'ORDINE 0<1<2. L'unico
      e` l'identita` -> |Aut| = 1.
    - Testimoni: l'UNICA operazione binaria idempotente commutativa che preserva il grafo
      di min e` min stessa (verificato per enumerazione delle 27) -> 1 testimone.
    - Quoziente per Aut={id} e` banale -> g = 1 testimone = 1.
    """
    R = CATALOG["min_graph"]
    assert unary_automorphisms(R) == [(0, 1, 2)]
    ws = wnu_witnesses(R)
    assert ws == [_binary_table_from_offdiag(0, 0, 1)]  # esattamente min
    assert count_wnu_witnesses(R) == 1
    assert g(R) == 1


def test_g_neq_computed_by_hand():
    """neq = {(x,y): x!=y}. Calcolo A MANO:
    - Automorfismi unari: ogni permutazione di {0,1,2} fissa neq -> |Aut| = 6.
    - Testimoni: nessuna f binaria idempotente commutativa preserva neq (f(0,1)=v deve
      stare in neq con se stessa: (0,1),(1,0) -> (v,v) deve essere in neq, ma (v,v) ha
      componenti uguali -> mai in neq). Quindi 0 testimoni.
    - g = 0 (nessuna orbita).
    """
    R = CATALOG["neq"]
    assert len(unary_automorphisms(R)) == 6
    assert count_wnu_witnesses(R) == 0
    assert g(R) == 0


# --------------------------------------------------------------------------- #
#  Conteggi esatti delle operazioni simmetriche                                #
# --------------------------------------------------------------------------- #

def test_symmetric_idempotent_ops_counts():
    # #op simmetriche idempotenti = 3^(C(k+2,2)-3)
    assert len(symmetric_idempotent_ops(2)) == 3 ** (6 - 3)    # 27
    assert len(symmetric_idempotent_ops(3)) == 3 ** (10 - 3)   # 2187


# --------------------------------------------------------------------------- #
#  TABELLA centrale: i numeri misurati del catalogo (rigenerabili)             #
# --------------------------------------------------------------------------- #

# Atteso ESATTO (rigenera con: py examples/run_polymorphism3.py)
EXPECTED = {
    # name:       (g, sym_profile, n_aut, wnu2, wnu3)
    "alldiff3":   (0, (),       6, False, False),
    "between":    (8, (2, 3),   1, True,  True),
    "cycle3":     (3, (2,),     3, True,  False),
    "leq":        (8, (2, 3),   1, True,  True),
    "lt":         (9, (2, 3),   1, True,  True),
    "min_graph":  (1, (2, 3),   1, True,  False),
    "nae3":       (0, (),       6, False, False),
    "neq":        (0, (),       6, False, False),
}


def test_catalog_exact_table():
    rep = analyze3()
    got = {
        r.name: (r.g_value, r.sym_profile, r.n_aut, r.wnu2, r.wnu3)
        for r in rep.rows
    }
    assert got == EXPECTED


# --------------------------------------------------------------------------- #
#  Esito dei 3 killer                                                          #
# --------------------------------------------------------------------------- #

def test_killers_outcome():
    rep = analyze3()
    # K-marker: esistono coppie marker-identiche ma g-diverse?
    # (between,lt) e (leq,lt): stessa firma marker (wnu2,wnu3,sym,aut)=(True,True,(2,3),1)
    # ma g 8 vs 9 -> g separa DENTRO una classe marker -> K-marker NON collassa.
    assert rep.witness_pairs == [("between", "lt"), ("leq", "lt")]
    assert rep.k_marker_collapses is False
    # K-sigma: g e` funzione del solo profilo simmetrico? NO: profile (2,3) ha g in {1,8,9}.
    assert rep.k_sigma_collapses is False
    # K-aut: g e` funzione di |Aut|? NO: |Aut|=1 ha g in {1,8,9}.
    assert rep.k_aut_collapses is False
    assert rep.verdict.startswith("NESSUN killer")


def test_has_wnu_only_k2_and_k3():
    R = CATALOG["leq"]
    assert has_wnu(R, 2) is True
    assert has_wnu(R, 3) is True
    with pytest.raises(ValueError):
        has_wnu(R, 4)


# --------------------------------------------------------------------------- #
#  Profilo simmetrico ad arieta` 4: ESAUSTIVO/lento -> slow                    #
# --------------------------------------------------------------------------- #

@pytest.mark.slow
@pytest.mark.timeout(600)
def test_symmetric_profile_arity4_slow():
    """k=4: 531441 operazioni simmetriche -> lento. Verifica che leq mantenga un
    simmetrico anche ad arieta` 4 (ordine lineare -> mediana/min-style)."""
    assert symmetric_profile3(CATALOG["leq"], max_arity=4) == (2, 3, 4)
