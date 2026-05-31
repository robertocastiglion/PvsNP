"""La base di conoscenza curata su P vs NP: barriere, approcci, risultati.

Contenuto verificato rispetto alla letteratura standard. Ogni nodo porta i
riferimenti principali. Gli archi codificano le relazioni essenziali — in
particolare CHI blocca CHI e CHI aggira CHI, che è il cuore del perché il
problema resiste.
"""

from __future__ import annotations

from .graph import Edge, Kind, KnowledgeGraph, Node, Reference, Relation


def build_knowledge_graph() -> KnowledgeGraph:
    g = KnowledgeGraph()

    # === PROBLEMI APERTI ===================================================
    g.add_node(Node(
        id="p_vs_np", kind=Kind.OPEN, title="P vs NP", year=1971,
        summary=(
            "I problemi le cui soluzioni si VERIFICANO in tempo polinomiale (NP) "
            "si possono anche RISOLVERE in tempo polinomiale (P)? Congettura "
            "dominante: P ≠ NP. Aperto."
        ),
        references=[
            Reference("Cook, S.", "The complexity of theorem-proving procedures",
                      1971, "STOC"),
            Reference("Levin, L.", "Universal sequential search problems",
                      1973, "Probl. Peredachi Inf."),
        ],
        tags=["centrale"],
    ))
    g.add_node(Node(
        id="np_vs_conp", kind=Kind.OPEN, title="NP vs coNP",
        summary=(
            "Le tautologie hanno dimostrazioni corte? Se NP ≠ coNP allora P ≠ NP. "
            "È il ponte con la proof complexity."
        ),
    ))
    g.add_node(Node(
        id="vp_vs_vnp", kind=Kind.OPEN, title="VP vs VNP (permanente vs determinante)",
        summary=(
            "Versione algebrica di P vs NP (Valiant 1979): il permanente richiede "
            "circuiti aritmetici super-polinomiali? È il bersaglio della GCT."
        ),
        references=[
            Reference("Valiant, L.", "Completeness classes in algebra", 1979, "STOC"),
        ],
    ))

    # === CONCETTI / CLASSI =================================================
    g.add_node(Node(
        id="pspace", kind=Kind.CONCEPT, title="PSPACE",
        summary="Problemi risolvibili in spazio polinomiale. Contiene P e NP.",
    ))
    g.add_node(Node(
        id="p_poly", kind=Kind.CONCEPT, title="P/poly",
        summary=(
            "Problemi con circuiti booleani di taglia polinomiale (non uniformi). "
            "Mostrare NP ⊄ P/poly separerebbe P da NP."
        ),
    ))

    # === BARRIERE ==========================================================
    g.add_node(Node(
        id="relativization", kind=Kind.BARRIER, title="Relativizzazione",
        year=1975, module="Modulo 2",
        summary=(
            "Esistono oracoli A, B con P^A = NP^A e P^B ≠ NP^B. Una dimostrazione "
            "che 'relativizza' (vale rispetto a ogni oracolo) non può quindi "
            "risolvere P vs NP."
        ),
        references=[
            Reference("Baker, T.; Gill, J.; Solovay, R.",
                      "Relativizations of the P =? NP question", 1975, "SIAM J. Comput."),
        ],
    ))
    g.add_node(Node(
        id="natural_proofs", kind=Kind.BARRIER, title="Natural Proofs",
        year=1994, module="Modulo 1",
        summary=(
            "Una proprietà 'costruttiva' e 'larga' delle funzioni booleane non può "
            "dare lower bound super-polinomiali, pena la rottura dei generatori "
            "pseudo-casuali. Blocca quasi tutti i lower bound combinatori sui circuiti."
        ),
        references=[
            Reference("Razborov, A.; Rudich, S.", "Natural proofs", 1997,
                      "J. Comput. Syst. Sci. (STOC 1994)"),
        ],
    ))
    g.add_node(Node(
        id="algebrization", kind=Kind.BARRIER, title="Algebrizzazione",
        year=2008,
        summary=(
            "Estensione della relativizzazione alle tecniche di aritmetizzazione: "
            "anche i metodi algebrici che superano la relativizzazione (come "
            "IP = PSPACE) restano insufficienti per P vs NP."
        ),
        references=[
            Reference("Aaronson, S.; Wigderson, A.", "Algebrization: a new barrier "
                      "in complexity theory", 2009, "ACM Trans. Comput. Theory (STOC 2008)"),
        ],
    ))

    # === TECNICHE / APPROCCI ==============================================
    g.add_node(Node(
        id="diagonalization", kind=Kind.TECHNIQUE, title="Diagonalizzazione",
        summary=(
            "L'arma di Cantor/Turing/Gödel: costruire un oggetto che differisce da "
            "ogni macchina di una lista. Separa i decidibili dagli indecidibili e dà "
            "i teoremi di gerarchia. Ma relativizza."
        ),
    ))
    g.add_node(Node(
        id="circuit_lb", kind=Kind.APPROACH, title="Lower bound combinatori sui circuiti",
        summary=(
            "Dimostrare che una funzione in NP richiede circuiti super-polinomiali "
            "(NP ⊄ P/poly). Approccio diretto ma colpito in pieno da natural proofs."
        ),
    ))
    g.add_node(Node(
        id="arithmetization", kind=Kind.TECHNIQUE, title="Aritmetizzazione",
        year=1990,
        summary=(
            "Trasformare formule booleane in polinomi su un campo, per sfruttare "
            "l'algebra. Ha dato il celebre IP = PSPACE — risultato che NON "
            "relativizza. Ma cade sotto l'algebrizzazione."
        ),
        references=[
            Reference("Lund, C.; Fortnow, L.; Karloff, H.; Nisan, N.",
                      "Algebraic methods for interactive proof systems", 1992, "J. ACM"),
            Reference("Shamir, A.", "IP = PSPACE", 1992, "J. ACM"),
        ],
    ))
    g.add_node(Node(
        id="gct", kind=Kind.APPROACH, title="Geometric Complexity Theory (GCT)",
        year=2001,
        summary=(
            "Programma di Mulmuley–Sohoni: attaccare VP vs VNP con geometria "
            "algebrica e teoria delle rappresentazioni. Progettato esplicitamente "
            "per essere non-naturale e non-relativizzante. Estremamente difficile, "
            "ma è la principale speranza 'che evita le barriere note'."
        ),
        references=[
            Reference("Mulmuley, K.; Sohoni, M.", "Geometric complexity theory I",
                      2001, "SIAM J. Comput."),
        ],
    ))
    g.add_node(Node(
        id="algorithmic_method", kind=Kind.APPROACH,
        title="Metodo algoritmico (Williams)", year=2011,
        summary=(
            "Trasformare algoritmi leggermente non banali (per es. per la "
            "soddisfacibilità di circuiti) in lower bound. Williams provò "
            "NEXP ⊄ ACC0. Tecnica non-relativizzante e non-naturalizzante."
        ),
        references=[
            Reference("Williams, R.", "Non-uniform ACC circuit lower bounds",
                      2011, "CCC / J. ACM 2014"),
        ],
    ))
    g.add_node(Node(
        id="proof_complexity", kind=Kind.APPROACH, title="Proof complexity",
        summary=(
            "Studiare la lunghezza minima delle dimostrazioni di tautologie. Lower "
            "bound forti per ogni sistema proverebbero NP ≠ coNP (Cook–Reckhow), "
            "quindi P ≠ NP."
        ),
        references=[
            Reference("Cook, S.; Reckhow, R.", "The relative efficiency of "
                      "propositional proof systems", 1979, "J. Symb. Logic"),
        ],
    ))

    # === RISULTATI ACQUISITI (lower bound che HANNO funzionato) ===========
    g.add_node(Node(
        id="ac0_parity", kind=Kind.RESULT, title="Parità ∉ AC0", year=1984,
        summary=(
            "I circuiti a profondità costante (AC0) non calcolano la parità "
            "(Furst–Saxe–Sipser; switching lemma di Håstad). Lower bound 'naturale' "
            "che funziona perché AC0 è troppo debole per i generatori pseudo-casuali."
        ),
        references=[
            Reference("Furst, M.; Saxe, J.; Sipser, M.", "Parity, circuits, and the "
                      "polynomial-time hierarchy", 1984, "Math. Syst. Theory"),
            Reference("Håstad, J.", "Almost optimal lower bounds for small depth "
                      "circuits", 1986, "STOC"),
        ],
    ))
    g.add_node(Node(
        id="monotone_clique", kind=Kind.RESULT,
        title="Clique richiede circuiti monotoni esponenziali", year=1985,
        summary=(
            "Razborov: i circuiti MONOTONI per il problema della cricca hanno taglia "
            "esponenziale. Grande risultato, ma la monotonia è essenziale e non si "
            "estende ai circuiti generali."
        ),
        references=[
            Reference("Razborov, A.", "Lower bounds on the monotone complexity of "
                      "some Boolean functions", 1985, "Soviet Math. Dokl."),
        ],
    ))
    g.add_node(Node(
        id="ip_pspace", kind=Kind.RESULT, title="IP = PSPACE", year=1992,
        summary=(
            "Le dimostrazioni interattive catturano esattamente PSPACE. Primo grande "
            "risultato NON relativizzante: dimostra che superare la relativizzazione "
            "è possibile (via aritmetizzazione)."
        ),
        references=[
            Reference("Shamir, A.", "IP = PSPACE", 1992, "J. ACM"),
        ],
    ))
    g.add_node(Node(
        id="nexp_acc0", kind=Kind.RESULT, title="NEXP ⊄ ACC0", year=2011,
        summary=(
            "Williams: il tempo esponenziale nondeterministico non sta nei circuiti "
            "ACC0. Raro lower bound moderno che aggira relativizzazione e natural "
            "proofs (metodo algoritmico)."
        ),
        references=[
            Reference("Williams, R.", "Non-uniform ACC circuit lower bounds",
                      2011, "CCC / J. ACM 2014"),
        ],
    ))
    g.add_node(Node(
        id="cook_levin", kind=Kind.RESULT, title="Teorema di Cook–Levin", year=1971,
        summary="SAT è NP-completo: fonda la teoria della NP-completezza e P vs NP.",
        references=[
            Reference("Cook, S.", "The complexity of theorem-proving procedures",
                      1971, "STOC"),
        ],
    ))

    # === ARCHI =============================================================
    E = lambda s, t, r, note="": g.add_edge(Edge(s, t, r, note))

    # fondamenti
    E("cook_levin", "p_vs_np", Relation.RELATED, "fonda la NP-completezza")
    E("p_vs_np", "np_vs_conp", Relation.RELATED, "NP≠coNP ⇒ P≠NP")
    E("p_vs_np", "vp_vs_vnp", Relation.RELATED, "analogo algebrico (Valiant)")

    # chi blocca chi (il cuore)
    E("relativization", "diagonalization", Relation.BLOCKS,
      "la diagonalizzazione classica relativizza")
    E("natural_proofs", "circuit_lb", Relation.BLOCKS,
      "i lower bound combinatori usano proprietà naturali")
    E("algebrization", "arithmetization", Relation.BLOCKS,
      "anche i metodi algebrici 'algebrizzano' e restano insufficienti")

    # chi aggira chi (la frontiera)
    E("arithmetization", "relativization", Relation.EVADES,
      "IP = PSPACE non relativizza")
    E("gct", "relativization", Relation.EVADES, "approccio algebrico-geometrico")
    E("gct", "natural_proofs", Relation.EVADES, "proprietà non naturali")
    E("gct", "algebrization", Relation.EVADES,
      "progettata per evitare tutte le barriere note")
    E("algorithmic_method", "relativization", Relation.EVADES, "non relativizza")
    E("algorithmic_method", "natural_proofs", Relation.EVADES,
      "non costruisce una proprietà naturale")

    # uso / generalizzazione / istanze
    E("arithmetization", "ip_pspace", Relation.USES, "la tecnica che dà IP=PSPACE")
    E("algorithmic_method", "nexp_acc0", Relation.USES, "ha prodotto NEXP ⊄ ACC0")
    E("ac0_parity", "circuit_lb", Relation.INSTANCE_OF,
      "lower bound su una classe ristretta (AC0)")
    E("monotone_clique", "circuit_lb", Relation.INSTANCE_OF,
      "lower bound sul caso monotono")
    E("circuit_lb", "p_poly", Relation.USES, "mira a NP ⊄ P/poly")
    E("ip_pspace", "pspace", Relation.RELATED, "caratterizza PSPACE")

    # bersagli
    E("circuit_lb", "p_vs_np", Relation.TARGETS, "NP ⊄ P/poly ⇒ P ≠ NP")
    E("gct", "vp_vs_vnp", Relation.TARGETS, "permanente vs determinante")
    E("proof_complexity", "np_vs_conp", Relation.TARGETS, "lower bound sulle prove")
    E("algorithmic_method", "p_vs_np", Relation.TARGETS,
      "lower bound sui circuiti via algoritmi")

    return g
