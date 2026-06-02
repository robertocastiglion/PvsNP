"""Dal cuore a query all'oracolo per macchine di Turing: una lingua in NP^Ã \\ P^Ã.

Il resto del Modulo 10 esegue la separazione nel MODELLO A QUERY (NP = 1 query,
P ≥ κ via avversario di cancellazione). Qui la SOLLEVIAMO: cabliamo quell'avversario
in una vera **diagonalizzazione** che costruisce un oracolo algebrico O e una
lingua

        L_O = { 1ⁿ : l'oracolo allo stadio n NON è identicamente nullo }

con L_O ∈ NP^Ã (un testimone sul cubo, una sola query) ma L_O ∉ P^Ã (nessuna
macchina deterministica che fa abbastanza poche query algebriche la decide).

Il meccanismo, stadio per stadio (è ESATTAMENTE il cuore a query, ora usato come
gadget di diagonalizzazione):

  • si fa girare la macchina M_i su 1ⁿ contro l'oracolo identicamente nullo (Ã ≡ 0),
    registrando i punti di query R che essa interroga;
  • se M_i ACCETTA pur avendo visto tutti zeri, lasciamo l'oracolo nullo: allora
    1ⁿ ∉ L_O ma M_i accetta → sbaglia;
  • se M_i RIFIUTA, cerchiamo un **nucleo booleano** A ≠ 0 con Ã(r)=0 su tutte le
    query R (è ``boolean_kernel_witness``: esiste finché le query non "uccidono"
    ogni nucleo — garantito se |R| < κ, ma può accadere anche con |R| ≥ κ se le
    query sono mal scelte, p.es. solo sul cubo). Lo piantiamo: Ã resta 0 su tutti
    i punti che M_i ha visto, quindi M_i ripercorre lo stesso cammino e rifiuta —
    ma ora 1ⁿ ∈ L_O → sbaglia.

In entrambi i casi M_i è diagonalizzata. La macchina può salvarsi solo facendo
≥ κ query BEN SCELTE (abbastanza, e nei punti giusti, da uccidere ogni nucleo):
ma κ cresce con N = 2^m, mentre una macchina polinomiale ne fa troppo poche,
definitivamente.

Onestà sul confine. ESEGUIAMO la diagonalizzazione (il gadget per stadio e il
cablaggio su una lista finita e concreta di macchine-oracolo). Il teorema completo
— su TUTTE le macchine poly-time, asintotico — è la diagonalizzazione standard; la
**versione forte** con il lower bound di **communication complexity** è il teorema
di **Aaronson–Wigderson**: quelli li CITIAMO.
"""

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from typing import Callable, Dict, List, Optional, Tuple

from pnp_lab.algebrization import Field, bits

from .separation import (
    BoolVec,
    Point,
    boolean_kernel_witness,
    chi_vector,
    deterministic_lower_bound,
    evaluate,
)

# ── Palette "System Ignition" ────────────────────────────────────────────
_BG = "#0A0502"
_FG = "#FCF2E6"
_ORANGE = "#FF8012"
_GREEN = "#4AF626"
_RED = "#D73434"
_ASH = "#876244"

#: una macchina-oracolo algebrica: decide(n, m, query) -> accetta/rifiuta,
#: interrogando l'estensione Ã in punti di GF(p)^m tramite ``query``.
OracleMachine = Callable[[int, int, Callable[[Point], int]], bool]


@dataclass
class NamedMachine:
    """Una macchina-oracolo con un nome (per i report)."""

    name: str
    decide: OracleMachine


# ── alcune macchine-oracolo concrete (campione del "nemico") ──────────────
def const_machine(value: bool) -> NamedMachine:
    """Risponde sempre ``value``, senza fare query (0 query)."""
    return NamedMachine(
        name=f"const_{'accept' if value else 'reject'}",
        decide=lambda n, m, query: value,
    )


def cube_scan_machine(k: int) -> NamedMachine:
    """Interroga i primi k punti del cubo {0,1}^m e accetta se ne trova uno a 1."""

    def decide(n: int, m: int, query: Callable[[Point], int]) -> bool:
        N = 1 << m
        for z in range(min(k, N)):
            if query(bits(z, m)) == 1:
                return True
        return False

    return NamedMachine(name=f"cube_scan_{k}", decide=decide)


def field_probe_machine(points: List[Point]) -> NamedMachine:
    """Interroga una lista fissa di punti di GF(p)^m e accetta se Ã è non nullo da qualche parte."""

    def decide(n: int, m: int, query: Callable[[Point], int]) -> bool:
        return any(query(r) != 0 for r in points)

    return NamedMachine(name=f"field_probe_{len(points)}", decide=decide)


def default_adversary_machines() -> List[NamedMachine]:
    """Un campione di macchine-oracolo da diagonalizzare (poche query ciascuna)."""
    return [
        const_machine(True),
        const_machine(False),
        cube_scan_machine(1),
        cube_scan_machine(2),
        field_probe_machine([(0, 0), (1, 1)]),
    ]


# ── un singolo stadio di diagonalizzazione ────────────────────────────────
@dataclass
class StageResult:
    machine_name: str
    n: int                      # la lunghezza di input 1ⁿ assegnata allo stadio
    m: int                      # numero di bit dell'oracolo a questa lunghezza (N = 2^m)
    p: int
    queries_made: int           # |R|: quante query algebriche ha fatto la macchina
    kappa: int                  # κ(m,p): quante ne servirebbero per non poter essere ingannata
    machine_answer: bool        # cosa ha risposto la macchina su 1ⁿ (contro Ã ≡ 0)
    planted: Optional[BoolVec]  # il nucleo booleano piantato (None = oracolo lasciato nullo)
    true_membership: bool       # 1ⁿ ∈ L_O dopo aver fissato l'oracolo
    diagonalized: bool          # la macchina sbaglia su 1ⁿ?


def diagonalize_stage(machine: NamedMachine, n: int, m: int, p: int) -> Tuple[StageResult, BoolVec]:
    """Diagonalizza UNA macchina alla lunghezza n con oracolo su m bit.

    Restituisce ``(StageResult, slice)`` dove ``slice`` è l'oracolo booleano da
    fissare a questa lunghezza (tupla di lunghezza 2^m).
    """
    F = Field(p)
    N = 1 << m
    zero: BoolVec = tuple(0 for _ in range(N))

    # 1) gira contro l'oracolo nullo, registrando i punti di query
    seen: List[Point] = []

    def recording_query(r: Point) -> int:
        seen.append(tuple(F.reduce(x) for x in r))
        return evaluate(zero, r, F)  # ≡ 0

    answer = bool(machine.decide(n, m, recording_query))

    # κ esatto del cuore a query (per il report e la spiegazione)
    kappa = deterministic_lower_bound(m, p).det_lower_bound

    if answer:
        # accetta pur avendo visto solo zeri → lasciamo l'oracolo nullo: 1ⁿ ∉ L_O
        slice_: BoolVec = zero
        planted = None
        true_mem = False
    else:
        # rifiuta → pianta un nucleo booleano A ≠ 0 invisibile alle sue query
        witness = boolean_kernel_witness(seen, m, F)
        if witness is not None:
            slice_ = witness
            planted = witness
            true_mem = any(witness)
        else:
            # ha fatto ≥ κ query: non ingannabile a questa lunghezza (oracolo nullo)
            slice_ = zero
            planted = None
            true_mem = False

    diagonalized = (answer != true_mem)
    return (
        StageResult(
            machine_name=machine.name, n=n, m=m, p=p,
            queries_made=len(seen), kappa=kappa,
            machine_answer=answer, planted=planted,
            true_membership=true_mem, diagonalized=diagonalized,
        ),
        slice_,
    )


# ── il cablaggio: costruzione dell'oracolo e della lingua ─────────────────
@dataclass
class LiftResult:
    p: int
    oracle: Dict[int, BoolVec] = dc_field(default_factory=dict)   # n → oracolo booleano (cubo)
    oracle_m: Dict[int, int] = dc_field(default_factory=dict)     # n → m (bit) a quella lunghezza
    stages: List[StageResult] = dc_field(default_factory=list)

    @property
    def all_diagonalized(self) -> bool:
        return all(s.diagonalized for s in self.stages)

    def in_language(self, n: int) -> bool:
        """1ⁿ ∈ L_O ⟺ l'oracolo allo stadio n non è identicamente nullo."""
        return any(self.oracle.get(n, ()))


def build_oracle(
    machines: Optional[List[NamedMachine]] = None, *, p: int = 3, m: int = 2, base_n: int = 2
) -> LiftResult:
    """Costruisce O e L_O diagonalizzando una macchina per lunghezza.

    La macchina i-esima viene diagonalizzata alla lunghezza ``base_n + i`` con un
    oracolo su ``m`` bit (N = 2^m valori). Le altre lunghezze restano nulle.
    """
    machines = machines if machines is not None else default_adversary_machines()
    res = LiftResult(p=p)
    for i, M in enumerate(machines):
        n = base_n + i
        stage, slice_ = diagonalize_stage(M, n, m, p)
        res.oracle[n] = slice_
        res.oracle_m[n] = m
        res.stages.append(stage)
    return res


# ── il lato NP: un testimone, una query ───────────────────────────────────
@dataclass
class NPCertificate:
    n: int
    in_language: bool
    witness: Optional[Point]    # z sul cubo con Ã(z)=1 (se 1ⁿ ∈ L_O)
    queries: int                # = 1 (verifica del testimone)
    verified: bool


def np_certificate(lift: LiftResult, n: int) -> NPCertificate:
    """Certificato NP^Ã per 1ⁿ: un testimone sul cubo, verificato con UNA query.

    Se 1ⁿ ∈ L_O esiste z con A(z)=1; lo si verifica valutando Ã(z) (= A(z) sul
    cubo) in una sola query algebrica. È il lato NP, ora sull'oracolo costruito.
    """
    F = Field(p=lift.p)
    values = lift.oracle.get(n, ())
    m = lift.oracle_m.get(n, 0)
    mem = any(values)
    if not mem:
        return NPCertificate(n=n, in_language=False, witness=None, queries=0, verified=True)
    z = next(a for a, v in enumerate(values) if v == 1)
    point = bits(z, m)
    verified = evaluate(values, point, F) == 1   # una query
    return NPCertificate(
        n=n, in_language=True, witness=point, queries=1, verified=verified
    )


# ── report ────────────────────────────────────────────────────────────────
def ascii_lift(lift: LiftResult) -> str:
    lines = [
        f"  Sollevamento query → oracolo TM — una lingua in NP^Ã \\ P^Ã  (GF({lift.p}))",
        "  " + "─" * 70,
        f"  {'macchina':>16}  {'1^n':>4}  {'query':>6}  {'κ':>3}  {'risposta':>9}  "
        f"{'1^n∈L_O':>8}  esito",
    ]
    for s in lift.stages:
        ans = "accetta" if s.machine_answer else "rifiuta"
        mem = "sì" if s.true_membership else "no"
        out = "DIAGONALIZZATA ✓" if s.diagonalized else "non ingannata"
        lines.append(
            f"  {s.machine_name:>16}  1^{s.n:<2}  {s.queries_made:>6}  {s.kappa:>3}  "
            f"{ans:>9}  {mem:>8}  {out}"
        )
    lines += [
        "  " + "─" * 70,
        f"  Tutte diagonalizzate: {'sì' if lift.all_diagonalized else 'no'}  "
        f"(le query fatte non uccidono ogni nucleo ⇒ resta un avversario che la acceca).",
        "",
        "  Lato NP^Ã: dove 1^n ∈ L_O, un testimone sul cubo basta con UNA query.",
    ]
    for n in sorted(lift.oracle):
        cert = np_certificate(lift, n)
        if cert.in_language:
            lines.append(
                f"    1^{n}: testimone z={cert.witness}, verificato in {cert.queries} query "
                f"→ {'OK' if cert.verified else 'FALLITO'}"
            )
    lines += [
        "  " + "─" * 70,
        "  Onestà: gadget e cablaggio ESEGUITI su macchine concrete; il teorema su",
        "  TUTTE le macchine e la versione forte (communication complexity) =",
        "  Aaronson–Wigderson, CITATI.",
    ]
    return "\n".join(lines)


def to_svg_lift(lift: LiftResult, *, width: int = 900, height: int = 460) -> str:
    """Per ogni stadio: query fatte (verde) contro la soglia κ (linea), con esito."""
    pad_l, pad_r, pad_t, pad_b = 70, 30, 100, 70
    plot_w = width - pad_l - pad_r
    plot_h = height - pad_t - pad_b
    stages = lift.stages or []
    nbar = max(len(stages), 1)
    kappa = max([s.kappa for s in stages] + [1])
    ymax = max([s.queries_made for s in stages] + [kappa, 1])

    def Y(v: float) -> float:
        return pad_t + plot_h * (1 - v / ymax)

    base_y = pad_t + plot_h
    slot = plot_w / nbar
    bw = slot * 0.5
    p: List[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Inter, Segoe UI, system-ui, sans-serif">',
        f'<rect width="{width}" height="{height}" fill="{_BG}"/>',
        f'<text x="{pad_l}" y="40" fill="{_ORANGE}" font-size="13" '
        f'font-family="ui-monospace, Consolas, monospace" letter-spacing="2">'
        f'&gt; LIFT query → oracolo TM // una lingua in NP^A \\ P^A</text>',
        f'<text x="{pad_l}" y="68" fill="{_FG}" font-size="22" font-weight="700">'
        f'Le query lasciano vivo un nucleo — e la macchina viene ingannata</text>',
        f'<line x1="{pad_l}" y1="{base_y}" x2="{pad_l+plot_w}" y2="{base_y}" stroke="{_ASH}"/>',
        f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{base_y}" stroke="{_ASH}"/>',
    ]
    # soglia κ (linea tratteggiata arancione)
    p.append(f'<line x1="{pad_l}" y1="{Y(kappa):.0f}" x2="{pad_l+plot_w}" y2="{Y(kappa):.0f}" '
             f'stroke="{_ORANGE}" stroke-dasharray="6 5"/>')
    p.append(f'<text x="{pad_l+plot_w}" y="{Y(kappa)-6:.0f}" fill="{_ORANGE}" font-size="12" '
             f'text-anchor="end">soglia κ = {kappa}</text>')
    for i, s in enumerate(stages):
        cx = pad_l + slot * (i + 0.5)
        h = base_y - Y(s.queries_made)
        col = _GREEN if s.diagonalized else _RED
        p.append(f'<rect x="{cx-bw/2:.0f}" y="{Y(s.queries_made):.0f}" width="{bw:.0f}" '
                 f'height="{max(h,1):.0f}" fill="{col}" opacity="0.85"/>')
        p.append(f'<text x="{cx:.0f}" y="{base_y+18:.0f}" fill="{_ASH}" font-size="10" '
                 f'text-anchor="middle">{s.machine_name}</text>')
        p.append(f'<text x="{cx:.0f}" y="{Y(s.queries_made)-6:.0f}" fill="{_FG}" font-size="11" '
                 f'text-anchor="middle">{s.queries_made}</text>')
    p.append(f'<text x="{pad_l-50}" y="{pad_t+plot_h/2:.0f}" fill="{_ASH}" font-size="12" '
             f'text-anchor="middle" transform="rotate(-90 {pad_l-50} {pad_t+plot_h/2:.0f})">'
             f'query algebriche fatte</text>')
    p.append(f'<rect x="{pad_l:.0f}" y="{height-20:.0f}" width="12" height="12" fill="{_GREEN}"/>')
    p.append(f'<text x="{pad_l+18:.0f}" y="{height-10:.0f}" fill="{_FG}" font-size="12">'
             f'diagonalizzata (sbaglia su 1ⁿ)</text>')
    p.append("</svg>")
    return "\n".join(p)


def write_svg(content: str, path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def lift_summary() -> str:
    return "\n".join(
        [
            "=" * 72,
            "  DAL CUORE A QUERY ALL'ORACOLO TM  →  NP^Ã \\ P^Ã",
            "=" * 72,
            "  La separazione a query (NP = 1, P ≥ κ) diventa una vera separazione",
            "  relativizzata: l'avversario di cancellazione — il nucleo booleano che",
            "  acceca poche query — è il gadget di una diagonalizzazione che, stadio",
            "  dopo stadio, costruisce un oracolo O e la lingua L_O ∈ NP^Ã \\ P^Ã.",
            "",
            "  Onestà. Eseguiamo il gadget e il cablaggio su macchine concrete (ne",
            "  basta una per lunghezza, ciascuna con poche query). Il teorema su tutte",
            "  le macchine poly-time è la diagonalizzazione standard; la versione forte",
            "  col lower bound di communication complexity è Aaronson–Wigderson:",
            "  quelli li CITIAMO. E, come sempre: questo NON risolve P vs NP — è un",
            "  mondo relativizzato, e proprio per questo non può deciderlo.",
            "=" * 72,
        ]
    )
