"""Modulo 16 — rendering testuale: la tabella unificata e il verdetto.

Nessuna logica nuova: legge le misure di `observer.py` e le presenta come una
tabella delle quattro barriere sotto l'unico template Δ(𝒞; D0, D1) ≤ ε, con il
PUNTO ESATTO in cui la proof complexity esce dal template.
"""

from __future__ import annotations

from .observer import (
    algebrization_one_query_advantage,
    natural_proofs_advantage,
    proof_complexity_probe,
    relativization_advantage,
)


def unified_report(*, n: int = 8) -> str:
    """Tabella delle quattro barriere come Δ ≤ ε (misure esatte su istanze tiny)."""
    # (1) relativizzazione: Δ = t/N, decresce col dominio → ε → 0
    rel = [(t, relativization_advantage(n, t)) for t in (0, 1, 2)]
    # (2) algebrizzazione: una query algebrica vs una booleana
    adv_alg, adv_bool = algebrization_one_query_advantage(k=3, p=5)
    # (3) natural proofs: corner del Modulo 15 (informazione satura, calcolo s)
    np_adv = natural_proofs_advantage(s=3)
    # (4) proof complexity: la sonda del fallimento
    probe = proof_complexity_probe()

    lines = ["  Δ(𝒞; D0, D1) ≤ ε — misure esatte su istanze minuscole", ""]

    lines.append("  (1) RELATIVIZZAZIONE  𝒜=query booleane, 𝒭 illimitata, budget t")
    lines.append(f"      needle su N={n} punti:  Δ(t) = t/N")
    lines.append("      " + "   ".join(f"t={t}: Δ={d:.3f}" for t, d in rel))
    lines.append(f"      → ε = t/N: con t=poly e N=2^m esponenziale, Δ → 0.  RIENTRA.")
    lines.append("")

    lines.append("  (2) ALGEBRIZZAZIONE   𝒜=query alla estensione di basso grado")
    lines.append(f"      1 query ALGEBRICA: Δ={adv_alg:.3f}   1 query BOOLEANA: Δ={adv_bool:.3f}")
    lines.append("      → STESSO template, 𝒜_alg ⊋ 𝒜_rel (interfaccia più ricca).")
    lines.append("        Il bound poggia su Schwartz–Zippel (vedi test).  RIENTRA.")
    lines.append("")

    lines.append("  (3) NATURAL PROOFS    𝒜=truth table SATURA, 𝒭 limitata (Modulo 15)")
    lines.append(f"      Δ con informazione satura (ℓ=n=3) e calcolo s=3: Δ={np_adv:.3f}")
    lines.append("      → bound dall'asse ORTOGONALE (calcolo), non informazione. RIENTRA.")
    lines.append("")

    lines.append("  (4) PROOF COMPLEXITY  tentativo: D0=SAT, D1=UNSAT, t=profondità refut.")
    lines.append(f"      lato D0 (formule soddisfacibili): Pr[decide=1] = {probe.d0_acceptance:.3f}")
    lines.append("      " + "   ".join(f"t={t}: Δ={d:.3f}" for t, d in probe.delta_by_budget))
    lengths = ", ".join("∞" if m is None else str(m) for m in probe.min_lengths)
    lines.append(f"      min |Π| sui mondi UNSAT (profondità): [{lengths}]")
    lines.append("      → il lato D0 è IDENTICAMENTE 0 (sanità): NON c'è un ε bilaterale.")
    lines.append("        La quantità reale è min|Π| ∈ ℕ∪{∞}, non sup|E1−E0| ∈ [0,1]. NON RIENTRA.")
    return "\n".join(lines)


def verdict_note() -> str:
    """Il verdetto e il PRIMO punto matematico in cui Δ ≤ ε fallisce."""
    return "\n".join([
        "  VERDETTO",
        "  • Barriere 1–2–3: un SOLO template Δ(𝒞; D0, D1) ≤ ε. 𝒞 varia su due assi",
        "    ortogonali (interfaccia 𝒜, calcolo 𝒭). Relativizzazione e algebrizzazione",
        "    differiscono SOLO in 𝒜; natural proofs satura 𝒜 e limita 𝒭.",
        "  • Barriera 4 (proof complexity): NON rientra.",
        "",
        "  PRIMO PUNTO DI FALLIMENTO — la costruzione di Δ stessa (il passo 'advantage'):",
        "    per scrivere Δ = |E_{D1}[T] − E_{D0}[T]| servono (i) due mondi e (ii) un",
        "    osservatore a singolo input. Un sistema di prova è SANO ⇒ sul mondo D0",
        "    (formule vere/soddisfacibili) la probabilità di refutare è ≡ 0: il lato D0",
        "    è costante, niente ε. E la regola di decisione NON è funzione del solo",
        "    mondo: prende un certificato Π extra, con un ∃ (|Π| ≤ t). Quindi la",
        "    quantità dura è min|Π| ∈ ℕ∪{∞} (lunghezza di testimone), di TIPO diverso",
        "    da un sup di differenza di medie ∈ [0,1].",
        "",
        "  Si può 'salvare' solo aggiungendo pseudocasualità (generatori di proof",
        "  complexity / interpolazione fattibile): ma così si RIDUCE la barriera 4 alla",
        "  3, a costo di un'ipotesi non dimostrata — una riduzione con debito, non",
        "  un'unificazione.",
    ])
