"""Il cuore del Natural Proofs Analyzer.

Razborov–Rudich definiscono una proprietà delle funzioni booleane come
*naturale* se soddisfa due condizioni (qui controllabili):

  1. COSTRUTTIVITÀ — la proprietà è decidibile in tempo polinomiale nella
     dimensione della truth table, cioè poly(N) con N = 2^n. (Equivalente a
     tempo 2^(O(n)).)
  2. LARGHEZZA — la proprietà vale per almeno una frazione 2^(−O(n)) di tutte
     le funzioni su n variabili.

(Una terza condizione, l'UTILITÀ — la proprietà implica un lower bound sui
circuiti — non è verificabile automaticamente e non è coperta qui.)

Il teorema di Razborov–Rudich: se esistono i generatori pseudo-casuali (cosa
ampiamente creduta vera), allora NESSUNA proprietà naturale può dimostrare
lower bound super-polinomiali — e quindi non può separare P da NP. Perciò,
se questo tool dice "la tua proprietà è naturale", ti sta dicendo che quella
strada è uno dei vicoli ciechi già noti.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field
from typing import Callable, Sequence

from .boolean import BooleanFunction, all_functions, num_functions, random_function


# Soglia di default: sopra questo numero di funzioni passiamo al campionamento
# invece dell'enumerazione esatta. 2^20 ~ 1M -> copre n <= 4 (65 536 funzioni).
DEFAULT_MAX_EXACT = 1 << 20


@dataclass
class Property:
    """Una proprietà candidata delle funzioni booleane.

    ``predicate(f)`` deve restituire True/False. ``name`` e ``description``
    servono solo per la reportistica.
    """

    name: str
    predicate: Callable[[BooleanFunction], bool]
    description: str = ""

    def __call__(self, f: BooleanFunction) -> bool:
        return bool(self.predicate(f))


@dataclass
class LargenessResult:
    n: int
    method: str  # "exact" oppure "sampled"
    fraction: float
    # campi diagnostici (a seconda del metodo)
    count: int | None = None
    total: int | None = None
    samples: int | None = None
    ci95: tuple[float, float] | None = None

    @property
    def log2_fraction(self) -> float:
        """log2 della frazione; -inf se la frazione osservata è 0."""
        return math.log2(self.fraction) if self.fraction > 0 else float("-inf")

    def __str__(self) -> str:
        if self.method == "exact":
            return (
                f"n={self.n}: frazione esatta = {self.count}/{self.total} "
                f"= {self.fraction:.3e}  (log2 = {self.log2_fraction:.2f})"
            )
        lo, hi = self.ci95 or (float("nan"), float("nan"))
        return (
            f"n={self.n}: frazione stimata = {self.fraction:.3e} "
            f"[CI95 {lo:.2e}, {hi:.2e}] su {self.samples} campioni "
            f"(log2 = {self.log2_fraction:.2f})"
        )


@dataclass
class ConstructivenessResult:
    ns: list[int]
    seconds: list[float]          # tempo medio per valutazione, per ciascun n
    table_sizes: list[int]        # N = 2^n corrispondenti
    exponent: float | None        # esponente stimato: tempo ~ N^exponent
    verdict: str                  # "plausibilmente costruttiva" / "probabilmente NON costruttiva" / "indeterminato"

    def __str__(self) -> str:
        rows = "\n".join(
            f"    n={n} (N={N}): {s*1e6:8.2f} µs/valutazione"
            for n, N, s in zip(self.ns, self.table_sizes, self.seconds)
        )
        exp = "n/d" if self.exponent is None else f"{self.exponent:.2f}"
        return (
            f"  Scaling del tempo di valutazione:\n{rows}\n"
            f"  Esponente stimato (tempo ~ N^k, N=2^n): k = {exp}\n"
            f"  Verdetto costruttività: {self.verdict}"
        )


@dataclass
class AnalysisReport:
    property_name: str
    largeness: list[LargenessResult]
    largeness_decay_slope: float | None  # pendenza di log2(frazione) vs n
    is_large: bool | None
    constructiveness: ConstructivenessResult | None
    is_constructive: bool | None
    verdict: str
    notes: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        lines = [
            "=" * 68,
            f"  NATURAL PROOFS ANALYZER — proprietà: {self.property_name!r}",
            "=" * 68,
            "",
            "  [1] LARGHEZZA (frazione di funzioni che soddisfano la proprietà)",
        ]
        for lr in self.largeness:
            lines.append(f"      {lr}")
        if self.largeness_decay_slope is not None:
            lines.append(
                f"      Pendenza log2(frazione) vs n: "
                f"{self.largeness_decay_slope:.2f} bit per variabile"
            )
        lines.append(
            f"      -> Larga (decadimento 2^(-O(n)))? "
            f"{_tri(self.is_large)}"
        )
        lines.append("")
        lines.append("  [2] COSTRUTTIVITÀ")
        if self.constructiveness is not None:
            lines.append(str(self.constructiveness))
        lines.append(f"      -> Costruttiva? {_tri(self.is_constructive)}")
        lines.append("")
        lines.append("  [VERDETTO]")
        lines.append(f"      {self.verdict}")
        if self.notes:
            lines.append("")
            lines.append("  Note:")
            for note in self.notes:
                lines.append(f"      - {note}")
        lines.append("=" * 68)
        return "\n".join(lines)


def _tri(value: bool | None) -> str:
    if value is True:
        return "SÌ"
    if value is False:
        return "NO"
    return "indeterminato"


# ---------------------------------------------------------------------------
# Larghezza
# ---------------------------------------------------------------------------

def measure_largeness(
    prop: Property,
    n: int,
    *,
    max_exact: int = DEFAULT_MAX_EXACT,
    samples: int = 200_000,
    rng: random.Random | None = None,
) -> LargenessResult:
    """Misura la frazione di funzioni su n variabili che soddisfano ``prop``.

    Se il numero totale di funzioni 2^(2^n) è <= ``max_exact`` viene calcolata
    in modo ESATTO per enumerazione; altrimenti viene STIMATA con un
    campionamento Monte Carlo uniforme di ``samples`` funzioni.
    """
    total = num_functions(n)
    if total <= max_exact:
        count = sum(1 for f in all_functions(n) if prop(f))
        return LargenessResult(
            n=n, method="exact", fraction=count / total, count=count, total=total
        )

    r = rng or random.Random(0xC0FFEE + n)
    hits = sum(1 for _ in range(samples) if prop(random_function(n, r)))
    p = hits / samples
    # intervallo di confidenza al 95% (approssimazione di Wald, con clamp)
    se = math.sqrt(max(p * (1 - p), 0.0) / samples)
    lo = max(0.0, p - 1.96 * se)
    hi = min(1.0, p + 1.96 * se)
    return LargenessResult(
        n=n, method="sampled", fraction=p, samples=samples, ci95=(lo, hi)
    )


def _largeness_slope(results: Sequence[LargenessResult]) -> float | None:
    """Stima la pendenza di log2(frazione) rispetto a n (regressione lineare).

    Una proprietà è 'larga' nel senso di Razborov–Rudich se la frazione decade
    al più come 2^(-O(n)), cioè se log2(frazione) decresce in modo
    approssimativamente LINEARE in n (pendenza limitata). Un decadimento
    super-lineare (es. 2^(-n^2)) segnala invece una proprietà NON larga.
    """
    pts = [(r.n, r.log2_fraction) for r in results if math.isfinite(r.log2_fraction)]
    if len(pts) < 2:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom


# ---------------------------------------------------------------------------
# Costruttività (euristica, basata sullo scaling empirico)
# ---------------------------------------------------------------------------

def measure_constructiveness(
    prop: Property,
    ns: Sequence[int],
    *,
    trials_per_n: int = 400,
    rng: random.Random | None = None,
) -> ConstructivenessResult:
    """Misura come cresce il tempo di valutazione di ``prop`` al crescere di n.

    NON è una prova di costruttività (indecidibile in generale): misura lo
    scaling empirico e stima l'esponente k tale che tempo ~ N^k con N = 2^n.
    - k piccolo (<= ~3): coerente con poly(N) -> 'plausibilmente costruttiva'.
    - tempo che esplode (super-polinomiale in N): 'probabilmente NON costruttiva'.
    """
    r = rng or random.Random(0xBEEF)
    seconds: list[float] = []
    sizes: list[int] = []
    for n in ns:
        funcs = [random_function(n, r) for _ in range(trials_per_n)]
        t0 = time.perf_counter()
        for f in funcs:
            prop(f)
        elapsed = (time.perf_counter() - t0) / trials_per_n
        seconds.append(elapsed)
        sizes.append(1 << n)

    exponent = _fit_loglog_exponent(sizes, seconds)
    if exponent is None:
        verdict = "indeterminato (dati insufficienti)"
    elif exponent <= 3.0:
        verdict = "plausibilmente costruttiva (scaling ~ poly(N))"
    elif exponent <= 6.0:
        verdict = "incerta (scaling polinomiale alto)"
    else:
        verdict = "probabilmente NON costruttiva (scaling super-polinomiale)"

    return ConstructivenessResult(
        ns=list(ns),
        seconds=seconds,
        table_sizes=sizes,
        exponent=exponent,
        verdict=verdict,
    )


def _fit_loglog_exponent(
    sizes: Sequence[int], seconds: Sequence[float]
) -> float | None:
    """Stima k nella relazione tempo ~ N^k via regressione lineare in scala log-log."""
    pts = [
        (math.log(N), math.log(s))
        for N, s in zip(sizes, seconds)
        if N > 0 and s > 0
    ]
    if len(pts) < 2:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom


# ---------------------------------------------------------------------------
# Analisi completa + verdetto
# ---------------------------------------------------------------------------

def analyze(
    prop: Property,
    *,
    largeness_ns: Sequence[int] = (2, 3, 4),
    constructiveness_ns: Sequence[int] = (3, 4, 5, 6, 7),
    max_slope: float = 2.5,
    samples: int = 200_000,
) -> AnalysisReport:
    """Esegue l'analisi completa e produce un verdetto sulla barriera Razborov–Rudich.

    ``max_slope`` è la massima pendenza ammessa per log2(frazione) vs n perché
    la proprietà sia considerata 'larga' (decadimento 2^(-O(n))).
    """
    largeness = [measure_largeness(prop, n, samples=samples) for n in largeness_ns]
    slope = _largeness_slope(largeness)

    if slope is None:
        # tutte le frazioni nulle (proprietà mai soddisfatta) o dati insufficienti
        all_zero = all(lr.fraction == 0 for lr in largeness)
        is_large = False if all_zero else None
    else:
        is_large = slope >= -max_slope  # decadimento non troppo rapido

    constructiveness = measure_constructiveness(prop, constructiveness_ns)
    if constructiveness.exponent is None:
        is_constructive = None
    else:
        is_constructive = constructiveness.exponent <= 3.0

    verdict, notes = _make_verdict(is_large, is_constructive)
    return AnalysisReport(
        property_name=prop.name,
        largeness=largeness,
        largeness_decay_slope=slope,
        is_large=is_large,
        constructiveness=constructiveness,
        is_constructive=is_constructive,
        verdict=verdict,
        notes=notes,
    )


def _make_verdict(
    is_large: bool | None, is_constructive: bool | None
) -> tuple[str, list[str]]:
    notes = [
        "La costruttività non è decidibile in generale: il verdetto è euristico, "
        "basato sullo scaling empirico del tempo di valutazione.",
        "L'utilità (la proprietà implica un lower bound) NON è verificata qui: "
        "è la terza condizione di Razborov–Rudich e va argomentata a parte.",
    ]
    if is_large and is_constructive:
        return (
            "⚠️  PROPRIETÀ NATURALE (costruttiva + larga). Per il teorema di "
            "Razborov–Rudich, se esistono i generatori pseudo-casuali, questa "
            "proprietà NON può dimostrare lower bound super-polinomiali sui "
            "circuiti — quindi NON può separare P da NP. Vicolo cieco noto.",
            notes,
        )
    if is_large is False and is_constructive:
        return (
            "✅  Costruttiva ma NON larga: evita la barriera Razborov–Rudich sul "
            "fronte della larghezza. Una proprietà 'rara' può in linea di "
            "principio essere utile per un lower bound. (Resta da verificare "
            "l'utilità.)",
            notes,
        )
    if is_large and is_constructive is False:
        return (
            "✅  Larga ma NON costruttiva: evita la barriera Razborov–Rudich sul "
            "fronte della costruttività — esattamente il tipo di proprietà 'non "
            "naturale' che servirebbe a una vera separazione. (Promettente in "
            "linea di principio, ma di solito difficilissima da rendere utile.)",
            notes,
        )
    if is_large is False and is_constructive is False:
        return (
            "✅  Né larga né costruttiva: fuori dal raggio d'azione della barriera "
            "Razborov–Rudich su entrambi i fronti.",
            notes,
        )
    return (
        "❓  Verdetto indeterminato su almeno una condizione: vedi i dati sopra "
        "e/o aumenta il range di n.",
        notes,
    )
