"""Proof-search su Lean VERO (stile LeanDojo) — la stessa policy, un verificatore reale.

Il resto del Modulo 11 fa proof-search su un mini-prover giocattolo. Qui colleghiamo
la STESSA idea di policy a **Lean 4 reale**: una policy propone tattiche, e a
verificarle è il kernel di Lean (via `lake env lean`). La policy non dimostra nulla
da sola — propone solo blocchi `by …`; l'unica autorità è Lean. Una policy migliore
si misura nello stesso modo onesto del modulo: in **numero di verifiche** (meno
chiamate al verificatore = policy migliore).

Architettura (e onestà):
  • `LeanGoal`          — un lemma da dimostrare (solo Lean core, niente mathlib).
  • `CheckFn`           — `(goal, block) -> bool`: prova un blocco di tattiche. È
                          INIETTABILE: i test usano un checker FINTO e deterministico
                          (niente Lean richiesto, suite veloce e portabile), come
                          l'LLM del modulo non è mai usato nei test.
  • `LeanChecker`       — l'implementazione REALE: scrive un file temporaneo e lo
                          fa verificare a `lake env lean`. Sound per costruzione.
  • policy              — `exhaustive_lean_policy` (ordine fisso, baseline) e
                          `heuristic_lean_policy` (ordina i candidati in base alla
                          forma del goal), più `LLMLeanPolicy` OPZIONALE (mai nel
                          percorso verificato: Lean ha l'ultima parola).
  • `prove_with_lean`   — il loop: prova i blocchi nell'ordine della policy finché
                          uno è accettato da Lean; conta le verifiche.

Non dimostra P vs NP: è la tecnica AlphaProof/LeanDojo resa onesta e misurabile,
ora su un verificatore vero invece che giocattolo.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple


def _elan_env() -> Dict[str, str]:
    """Ambiente con `~/.elan/bin` in testa al PATH (per trovare lake/lean)."""
    env = os.environ.copy()
    env["PATH"] = str(Path.home() / ".elan" / "bin") + os.pathsep + env.get("PATH", "")
    return env


def _find_lake(env: Dict[str, str]) -> Optional[str]:
    """Risolve l'eseguibile `lake` (su Windows è `lake.exe`)."""
    return shutil.which("lake", path=env.get("PATH"))

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_ASH = "#876244"


@dataclass(frozen=True)
class LeanGoal:
    """Un lemma da dimostrare in Lean core (niente mathlib)."""

    name: str
    statement: str
    preamble: str = ""


#: un checker prova un blocco di tattiche su un goal e dice se Lean lo accetta.
CheckFn = Callable[[LeanGoal, str], bool]


# ── il pool di tattiche candidate (blocchi `by …`) ────────────────────────
#: blocchi generici, ognuno una stringa che va nel corpo di `by`.
DEFAULT_TACTICS: Tuple[str, ...] = (
    "rfl",
    "decide",
    "omega",
    "simp",
    "intros\nrfl",
    "intros\nomega",
    "intros\nsimp",
    "intros\ndecide",
    "intro a b h\nexact ⟨h.2, h.1⟩",
    "intro h\nexact h",
)


def _has(statement: str, *needles: str) -> bool:
    return any(s in statement for s in needles)


def _heuristic_order(goal: LeanGoal, tactics: Tuple[str, ...]) -> List[str]:
    """Ordina i candidati in base alla forma sintattica del goal.

    Trasparente e testabile: è un punteggio, non magia. Goal con quantificatori/
    implicazioni → prima i blocchi che fanno `intros`; uguaglianze → prima
    `rfl`/`omega`; congiunzioni → prima il costruttore; ⊤/→ identità → `exact h`.
    """
    s = goal.statement
    binder = _has(s, "∀", "→", "->")
    eq = _has(s, "=")
    arith = _has(s, "≤", "<", "≥", ">") or eq
    conj = _has(s, "∧")

    def score(t: str) -> int:
        sc = 0
        ti = t.replace("\n", " ")
        if binder and "intro" in ti:
            sc -= 4
        if not binder and "intro" in ti:
            sc += 4  # inutile fare intros senza binder
        if conj and "h.2, h.1" in ti:
            sc -= 6
        if arith and ("omega" in ti or "decide" in ti):
            sc -= 2
        if eq and "rfl" in ti:
            sc -= 3
        if "simp" in ti:
            sc += 1  # ultima spiaggia (può chiudere ma è più costosa)
        return sc

    return sorted(tactics, key=score)


def exhaustive_lean_policy(tactics: Tuple[str, ...] = DEFAULT_TACTICS) -> Callable[[LeanGoal], List[str]]:
    """Baseline: prova i blocchi nell'ordine fisso, senza guardare il goal."""
    def policy(_goal: LeanGoal) -> List[str]:
        return list(tactics)
    return policy


def heuristic_lean_policy(tactics: Tuple[str, ...] = DEFAULT_TACTICS) -> Callable[[LeanGoal], List[str]]:
    """Policy trasparente: riordina i candidati in base alla forma del goal."""
    def policy(goal: LeanGoal) -> List[str]:
        return _heuristic_order(goal, tactics)
    return policy


# ── interfaccia opzionale per un modello esterno (LLM) ────────────────────
def build_prompt(goal: LeanGoal, tactics: Tuple[str, ...] = DEFAULT_TACTICS) -> str:
    """Prompt per il modello (PURO, testabile): elenca goal e blocchi numerati."""
    lines = [
        "Sei una policy di proof-search per Lean 4.",
        f"Obiettivo: {goal.statement}",
        "Blocchi di tattiche disponibili:",
    ]
    for i, t in enumerate(tactics):
        lines.append(f"  [{i}] {t.replace(chr(10), ' ; ')}")
    lines.append("Rispondi con gli indici dei blocchi migliori, uno per riga (es. '0').")
    return "\n".join(lines)


def parse_indices(response: str, tactics: Tuple[str, ...] = DEFAULT_TACTICS) -> List[str]:
    """Interpreta la risposta del modello in blocchi (PURO, testabile)."""
    out: List[str] = []
    for line in response.splitlines():
        token = line.strip().split()[0] if line.strip() else ""
        key = token.lstrip("[").rstrip("]")
        if key.isdigit():
            idx = int(key)
            if 0 <= idx < len(tactics) and tactics[idx] not in out:
                out.append(tactics[idx])
    return out


class LLMLeanPolicy:
    """Policy guidata da un modello esterno. OPZIONALE e onesta.

    `call_fn : str -> str` è fornita dall'utente. Il toolkit non include chiavi né
    dipendenze di rete; se `call_fn` fallisce o non propone nulla, si ripiega
    sull'euristica. **Mai nel percorso verificato**: a dire l'ultima parola è Lean.
    I test non usano un modello reale.
    """

    def __init__(self, call_fn: Callable[[str], str], *, tactics: Tuple[str, ...] = DEFAULT_TACTICS):
        self.call_fn = call_fn
        self.tactics = tactics
        self._fallback = heuristic_lean_policy(tactics)

    def __call__(self, goal: LeanGoal) -> List[str]:
        try:
            proposed = parse_indices(self.call_fn(build_prompt(goal, self.tactics)), self.tactics)
            if not proposed:
                return self._fallback(goal)
            # le proposte del modello prima, poi il resto come rete di sicurezza
            rest = [t for t in self._fallback(goal) if t not in proposed]
            return proposed + rest
        except Exception:
            return self._fallback(goal)


# ── il loop di ricerca (verificatore iniettabile) ─────────────────────────
@dataclass
class LeanProofResult:
    goal: str
    proved: bool
    winning_block: Optional[str]
    checks: int                 # numero di verifiche Lean fatte (la metrica onesta)
    tried: List[str] = field(default_factory=list)


def prove_with_lean(
    goal: LeanGoal,
    policy: Callable[[LeanGoal], List[str]],
    check: CheckFn,
    *,
    budget: Optional[int] = None,
) -> LeanProofResult:
    """Prova i blocchi nell'ordine della policy finché Lean ne accetta uno.

    `check` è iniettabile: in produzione è `LeanChecker` (Lean vero), nei test un
    checker finto e deterministico. La metrica onesta è `checks` = quante volte
    abbiamo dovuto interrogare il verificatore.
    """
    tried: List[str] = []
    for block in policy(goal):
        if budget is not None and len(tried) >= budget:
            break
        tried.append(block)
        if check(goal, block):
            return LeanProofResult(goal.name, True, block, len(tried), tried)
    return LeanProofResult(goal.name, False, None, len(tried), tried)


# ── il verificatore REALE: Lean via lake ──────────────────────────────────
class LeanChecker:
    """Verifica un blocco di tattiche con Lean 4 reale (`lake env lean`).

    Scrive un file temporaneo `theorem … := by <block>` e lo fa controllare al
    kernel di Lean. Sound per costruzione: accettiamo un blocco solo se Lean
    compila senza errori. I risultati sono memorizzati per non ripetere chiamate.
    """

    def __init__(self, formalization_dir: Optional[str] = None, *, timeout: float = 60.0):
        if formalization_dir is None:
            formalization_dir = str(Path(__file__).resolve().parents[2] / "formalization")
        self.dir = formalization_dir
        self.timeout = timeout
        self._cache: Dict[Tuple[str, str, str], bool] = {}
        self.env = _elan_env()
        self.lake = _find_lake(self.env)

    @staticmethod
    def available(formalization_dir: Optional[str] = None) -> bool:
        """True se `lake` è raggiungibile (per saltare i test quando Lean manca)."""
        if formalization_dir is None:
            formalization_dir = str(Path(__file__).resolve().parents[2] / "formalization")
        env = _elan_env()
        lake = _find_lake(env)
        if lake is None:
            return False
        try:
            r = subprocess.run([lake, "--version"], cwd=formalization_dir, env=env,
                               capture_output=True, timeout=60)
            return r.returncode == 0
        except Exception:
            return False

    def _source(self, goal: LeanGoal, block: str) -> str:
        body = "\n".join("  " + ln for ln in block.splitlines())
        pre = (goal.preamble + "\n") if goal.preamble else ""
        return f"{pre}theorem pnp_search_goal : {goal.statement} := by\n{body}\n"

    def __call__(self, goal: LeanGoal, block: str) -> bool:
        key = (goal.statement, goal.preamble, block)
        if key in self._cache:
            return self._cache[key]
        if self.lake is None:
            return False
        ok = False
        with tempfile.NamedTemporaryFile("w", suffix=".lean", delete=False, encoding="utf-8") as f:
            f.write(self._source(goal, block))
            path = f.name
        try:
            r = subprocess.run([self.lake, "env", "lean", path], cwd=self.dir, env=self.env,
                               capture_output=True, timeout=self.timeout, text=True,
                               encoding="utf-8", errors="replace")
            ok = (r.returncode == 0)
        except Exception:
            ok = False
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass
        self._cache[key] = ok
        return ok


# ── benchmark di goal (Lean core) ─────────────────────────────────────────
def benchmark_lean_goals() -> List[LeanGoal]:
    """Un piccolo benchmark di lemmi veri, chiudibili in Lean core (no mathlib)."""
    return [
        LeanGoal("add_zero", "∀ n : Nat, n + 0 = n"),
        LeanGoal("zero_add", "∀ n : Nat, 0 + n = n"),
        LeanGoal("succ_eq", "∀ n : Nat, n + 1 = Nat.succ n"),
        LeanGoal("two_two", "2 + 2 = 4"),
        LeanGoal("le_refl", "∀ n : Nat, n ≤ n"),
        LeanGoal("and_comm", "∀ p q : Prop, p ∧ q → q ∧ p"),
    ]


# ── confronto fra policy ───────────────────────────────────────────────────
@dataclass
class PolicyComparison:
    goal: str
    results: Dict[str, LeanProofResult]  # nome policy → risultato


def compare_lean_policies(
    goals: List[LeanGoal],
    policies: Dict[str, Callable[[LeanGoal], List[str]]],
    check: CheckFn,
    *,
    budget: Optional[int] = None,
) -> List[PolicyComparison]:
    """Esegue ogni policy su ogni goal con lo STESSO verificatore; raccoglie i `checks`."""
    out: List[PolicyComparison] = []
    for g in goals:
        res = {name: prove_with_lean(g, pol, check, budget=budget) for name, pol in policies.items()}
        out.append(PolicyComparison(goal=g.name, results=res))
    return out


def ascii_comparison(comp: List[PolicyComparison], policy_names: List[str]) -> str:
    lines = [
        "  Proof-search su Lean VERO — verifiche per chiudere ogni lemma (meno = meglio)",
        "  " + "─" * 66,
        "  " + f"{'lemma':>12}  " + "  ".join(f"{n:>14}" for n in policy_names),
    ]
    totals = {n: 0 for n in policy_names}
    for c in comp:
        cells = []
        for n in policy_names:
            r = c.results[n]
            totals[n] += r.checks
            mark = "✓" if r.proved else "✗"
            cells.append(f"{r.checks:>2} {mark:>1} ({(r.winning_block or '—').splitlines()[0][:6]:>6})")
        lines.append(f"  {c.goal:>12}  " + "  ".join(f"{c:>14}" for c in cells))
    lines += [
        "  " + "─" * 66,
        "  " + f"{'TOTALE':>12}  " + "  ".join(f"{str(totals[n])+' verifiche':>14}" for n in policy_names),
        "  L'euristica chiude con MENO verifiche: stessa metrica onesta del Modulo 11,",
        "  ma il verificatore ora è Lean vero. (La policy propone, Lean dispone.)",
    ]
    return "\n".join(lines)


def to_svg_comparison(comp: List[PolicyComparison], policy_names: List[str],
                      *, width: int = 900, height: int = 460) -> str:
    """Verifiche totali per policy (barre): meno = policy migliore."""
    pad_l, pad_r, pad_t, pad_b = 70, 30, 100, 70
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    totals = {n: sum(c.results[n].checks for c in comp) for n in policy_names}
    ymax = max(list(totals.values()) + [1])
    base_y = pad_t + plot_h
    slot = plot_w / max(len(policy_names), 1)
    bw = slot * 0.45

    def Y(v: float) -> float:
        return pad_t + plot_h * (1 - v / ymax)

    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; PROOF-SEARCH su LEAN VERO // la policy propone, Lean verifica</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Verifiche Lean per chiudere il benchmark — meno = policy migliore</text>',
        f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>',
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>',
    ]
    for i, n in enumerate(policy_names):
        cx = pad_l + slot * (i + 0.5)
        v = totals[n]
        col = _GREEN if v == min(totals.values()) else _ORANGE
        p.append(f'<rect x="{cx-bw/2:.0f}" y="{Y(v):.0f}" width="{bw:.0f}" '
                 f'height="{base_y-Y(v):.0f}" fill="{col}" opacity="0.85"/>')
        p.append(f'<text x="{cx:.0f}" y="{Y(v)-8:.0f}" fill="{_FG}" font-size="13" '
                 f'text-anchor="middle">{v}</text>')
        p.append(f'<text x="{cx:.0f}" y="{base_y+22:.0f}" fill="{_ASH}" font-size="12" '
                 f'text-anchor="middle">{n}</text>')
    p.append(f'<text x="{pad_l-50}" y="{pad_t+plot_h/2:.0f}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle" transform="rotate(-90 {pad_l-50} {pad_t+plot_h/2:.0f})">'
             f'verifiche Lean totali</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def lean_bridge_summary() -> str:
    return "\n".join(
        [
            "=" * 72,
            "  PROOF-SEARCH SU LEAN VERO  (stile LeanDojo)",
            "=" * 72,
            "  Stessa idea del Modulo 11 — una policy propone tattiche — ma il",
            "  verificatore non è più un giocattolo: è Lean 4, col suo kernel. La",
            "  policy ordina i blocchi `by …`; Lean li accetta o li rifiuta. La metrica",
            "  resta onesta: una policy migliore chiude i lemmi con MENO verifiche.",
            "",
            "  Onestà. (1) La policy non dimostra nulla: a verificare è SEMPRE Lean.",
            "  (2) L'LLM è una policy OPZIONALE e pluggable, mai nel percorso sound; i",
            "  test usano un checker finto e non invocano Lean (suite veloce). (3) Questo",
            "  NON dimostra P vs NP: è la tecnica AlphaProof/LeanDojo resa misurabile.",
            "=" * 72,
        ]
    )
