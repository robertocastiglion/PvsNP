"""Modulo 17 — rendering testuale: la tabella del survival test e il verdetto.

Nessuna logica nuova: legge le misure di `survival.py` e le presenta come una
tabella dei due poli (relativizzazione vs natural proofs) sotto il criterio
Δ(𝒭=∞) ≷ 1, con il verdetto sulla famiglia di ciascuna barriera.
"""

from __future__ import annotations

from .survival import (
    natural_proofs_curve,
    survival_results,
)


def survival_report(*, n: int = 8, t: int = 2) -> str:
    """Tabella del survival test (misure esatte su istanze minuscole)."""
    results = survival_results(n=n, t=t)
    curve = natural_proofs_curve((1, 2, 3))

    lines = ["  SURVIVAL TEST — Δ a calcolo illimitato 𝒭=∞", ""]

    lines.append("  (1) RELATIVIZZAZIONE   asse 𝒜 (informazione)")
    lines.append(f"      needle su N={n}, budget t={t} query booleane, 𝒭 = ∞ (g arbitraria)")
    rel = results[0]
    lines.append(f"      Δ(𝒭=∞) = {rel.delta_compute_unbounded:.3f} = t/N  →  il calcolo è INERTE")
    lines.append(f"      margine = 1 − Δ = {rel.margin:.3f} > 0   ⟹  SOPRAVVIVE")
    lines.append(f"      VERDETTO: {rel.kind.upper()} (bound incondizionato sull'interfaccia)")
    lines.append("")

    lines.append("  (2) NATURAL PROOFS     asse 𝒭 (calcolo)")
    lines.append("      informazione satura ℓ=3; Δ(ℓ=3, s) al crescere del calcolo s:")
    lines.append("      " + "   ".join(f"s={s}: Δ={d:.3f}" for s, d in curve))
    npr = results[1]
    lines.append(f"      s=∞: Δ = {npr.delta_compute_unbounded:.3f}  (indicatore del predicato 'duro')")
    lines.append(f"      margine = 1 − Δ = {npr.margin:.3f} = 0   ⟹  NON sopravvive")
    lines.append(f"      VERDETTO: {npr.kind.upper()} (= ipotesi di pseudocasualità)")
    return "\n".join(lines)


def verdict_note() -> str:
    """Il verdetto del criterio e cosa ri-deriva (e cosa NO)."""
    return "\n".join([
        "  VERDETTO",
        "  • UN test scalare classifica ogni barriera: si misura Δ con 𝒭 = ∞.",
        "    Δ(𝒭=∞) < 1 ⟹ information-theoretic (relativizzazione, algebrizzazione:",
        "    bound sull'interfaccia 𝒜, un TEOREMA incondizionato — hai mancato l'ago).",
        "    Δ(𝒭=∞) = 1 ⟹ computational (natural proofs, proof complexity: il bound",
        "    evapora a calcolo illimitato, esisteva solo perché 'duro' sembra 'facile'",
        "    al calcolo limitato — cioè la PSEUDOCASUALITÀ).",
        "",
        "  • Le due genericità NON sono la stessa cosa: una è informazione-teorica e",
        "    incondizionata, l'altra è computazionale e condizionata. Il test le separa.",
        "",
        "  Onestà: NON è un nuovo lower bound. È il criterio operativo che ri-deriva i",
        "  due assi ortogonali del Modulo 15 (informazione × calcolo) come un singolo",
        "  numero misurabile. Niente qui tocca P vs NP.",
    ])
