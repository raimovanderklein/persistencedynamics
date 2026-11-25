"""Inline SVG figures for the site. Every figure is computed, not drawn by hand."""
import math

INK, SOFT, MUTED, LINE, HAIR, PAPER, FAINT = "#161513", "#4D4843", "#6B655B", "#D5CFC2", "#E4DFD4", "#F7F5F0", "#B9B2A5"
POT, CON, ENC, COS = "#1B5BD8", "#B77800", "#D63A1F", "#924D35"
REG = [("Potentiality", POT), ("Construction", CON), ("Encounter", ENC), ("Conservation", COS)]
FONT = "Source Serif 4, Georgia, serif"
PHI = (1 + 5 ** .5) / 2


def svg(w, h, body, label, cls=""):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img" aria-label="{label}" class="{cls}" '
            f'font-family="{FONT}">{body}</svg>')


def fig(body, caption, n):
    return f'<figure class="figure">{body}<figcaption><span class="fn">Figure {n}.</span> {caption}</figcaption></figure>'


def hold(p):  # p: phase in degrees, 0 = start of Potentiality, runs clockwise through the regimes
    return (1 + math.cos(math.radians(p))) / 2


def cross(p):
    return (1 + math.sin(math.radians(p))) / 2


def waves(n, interactive=False):
    W, H, x0, x1, top, bot = 760, 300, 70, 740, 48, 218
    X = lambda p: x0 + (x1 - x0) * p / 360
    Y = lambda v: bot - (bot - top) * v
    out = []
    for i, (name, c) in enumerate(REG):
        a, b = X(90 * i), X(90 * i + 90)
        out.append(f'<rect x="{a+1:.1f}" y="{top-30}" width="{b-a-2:.1f}" height="3" fill="{c}"/>')
        out.append(f'<text x="{(a+b)/2:.1f}" y="{top-38}" text-anchor="middle" font-size="15" fill="{INK}" class="rname" data-i="{i}">{name}</text>')
    for p in (0, 90, 180, 270, 360):
        out.append(f'<line x1="{X(p):.1f}" y1="{top-24}" x2="{X(p):.1f}" y2="{bot+6}" stroke="{LINE}"/>')
    out.append(f'<line x1="{x0}" y1="{Y(.5)}" x2="{x1}" y2="{Y(.5)}" stroke="{MUTED}" stroke-dasharray="2 4"/>')
    out.append(f'<text x="{x0-10}" y="{Y(.5)-6}" text-anchor="end" font-size="12.5" font-style="italic" fill="{MUTED}">active</text>')
    out.append(f'<text x="{x0-10}" y="{Y(.5)+16}" text-anchor="end" font-size="12.5" font-style="italic" fill="{MUTED}">latent</text>')
    for f, col, w, lab, dash in ((hold, INK, 2.2, "hold", ""), (cross, INK, 2.2, "cross", ' stroke-dasharray="7 5"')):
        pts = " ".join(f"{X(p):.1f},{Y(f(p)):.1f}" for p in range(0, 361, 3))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}"{dash}/>')
    out.append(f'<text x="{X(8):.1f}" y="{Y(hold(8))-10:.1f}" font-size="16" font-style="italic" fill="{INK}">hold</text>')
    out.append(f'<text x="{X(84):.1f}" y="{Y(cross(90))-10:.1f}" font-size="16" font-style="italic" fill="{INK}" text-anchor="end">cross</text>')
    # threshold crossings
    names = {90: "Activation", 180: "Egress", 270: "Drain", 360: "Suppression"}
    for p, nm in names.items():
        out.append(f'<circle cx="{X(p):.1f}" cy="{Y(.5):.1f}" r="4" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
        out.append(f'<text x="{X(p):.1f}" y="{bot+28}" text-anchor="{"end" if p == 360 else "middle"}" font-size="13.5" fill="{SOFT}">{nm}</text>')
    out.append(f'<text x="{x0}" y="{bot+54}" font-size="12.5" font-style="italic" fill="{MUTED}">one round of the cycle</text>')
    out.append(f'<text x="{x1}" y="{bot+54}" text-anchor="end" font-size="12.5" font-style="italic" fill="{MUTED}">a quarter of a period apart</text>')
    if interactive:
        out.append(f'<line class="cursor" x1="{x0}" y1="{top-24}" x2="{x0}" y2="{bot+6}" stroke="{INK}" stroke-width="1" opacity=".55"/>')
        out.append(f'<circle class="dot-h" cx="{x0}" cy="{Y(1)}" r="5" fill="{INK}"/>')
        out.append(f'<circle class="dot-c" cx="{x0}" cy="{Y(.5)}" r="5" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>')
    body = svg(W, H, "".join(out), "Hold and cross drawn as two waves of the same period, a quarter of a period apart, over one round of the cycle.", "waves")
    return fig(body, "Hold and cross over one round. Hold (solid) and cross (dashed) are the same wave, a quarter of a period apart. Each operation is active above the midline and latent below it. Each regime is one quarter of the round, and each threshold is the moment one of the two waves crosses the midline.", n)


def phase(n, interactive=False):
    W, H, s0, s1 = 520, 460, 100, 420
    c, r = (s0 + s1) / 2, (s1 - s0) / 2
    PX = lambda h: s0 + (1 - h) * (s1 - s0)   # hold active on the left
    PY = lambda k: s0 + (1 - k) * (s1 - s0) - 20  # cross active at the top
    cy = c - 20
    out = [f'<rect x="{s0}" y="{s0-20}" width="{s1-s0}" height="{s1-s0}" fill="none" stroke="{LINE}"/>',
           f'<line x1="{c}" y1="{s0-20}" x2="{c}" y2="{s1-20}" stroke="{LINE}"/>',
           f'<line x1="{s0}" y1="{cy}" x2="{s1}" y2="{cy}" stroke="{LINE}"/>',
           f'<circle cx="{c}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="2"/>']
    # arrowheads, clockwise
    for p in (45, 135, 225, 315):
        x, y = PX(hold(p)), PY(cross(p))
        ang = math.degrees(math.atan2(PY(cross(p + 1)) - y, PX(hold(p + 1)) - x))
        out.append(f'<path d="M0 0 L-11 -5 L-11 5 Z" fill="{INK}" transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})"/>')
    ytop, ybot = s0 - 20 - 12, s1 - 20 + 26
    corners = [(s0, ytop, "start"), (s1, ytop, "end"), (s1, ybot, "end"), (s0, ybot, "start")]
    for i, ((x, y, a), (name, col)) in enumerate(zip(corners, REG)):
        sq = x if a == "start" else x - 10
        out.append(f'<rect x="{sq}" y="{y-10}" width="10" height="10" fill="{col}"/>')
        tx = x + 16 if a == "start" else x - 16
        out.append(f'<text x="{tx}" y="{y}" text-anchor="{a}" font-size="16" fill="{INK}" class="rname" data-i="{i}">{name}</text>')
    thr = [(c, s0 - 52, "middle", "Activation"), (s1 + 12, cy + 5, "start", "Egress"),
           (c, s1 + 26, "middle", "Drain"), (s0 - 12, cy + 5, "end", "Suppression")]
    for x, y, a, nm in thr:
        out.append(f'<text x="{x}" y="{y}" text-anchor="{a}" font-size="13.5" fill="{SOFT}">{nm}</text>')
    for p in (0, 90, 180, 270):
        out.append(f'<circle cx="{PX(hold(p)):.1f}" cy="{PY(cross(p)):.1f}" r="4" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>')
    if interactive:
        out.append(f'<circle class="dot-p" cx="{PX(hold(0))}" cy="{PY(cross(0))}" r="7" fill="{INK}"/>')
    body = svg(W, H, "".join(out), "Hold plotted against cross traces a circle. The four regimes are its quadrants and the four thresholds its cardinal points.", "phase")
    return fig(body, "The same round as a circle. Plot hold (active to the left) against cross (active at the top) and the two waves trace a circle, clockwise. The four regimes are its quadrants, and the four thresholds are the points where it crosses an axis.", n)


def dimensions(n):
    W, H = 520, 440
    a, b = 90, 430
    t, u = 40, 380
    out = [f'<rect x="{a}" y="{t}" width="{b-a}" height="{u-t}" fill="none" stroke="{LINE}"/>',
           f'<line x1="{(a+b)/2}" y1="{t}" x2="{(a+b)/2}" y2="{u}" stroke="{HAIR}"/>',
           f'<line x1="{a}" y1="{(t+u)/2}" x2="{b}" y2="{(t+u)/2}" stroke="{HAIR}"/>']
    pad = 70
    out.append(f'<line x1="{a+pad}" y1="{t+pad}" x2="{b-pad}" y2="{u-pad}" stroke="{INK}" stroke-width="2"/>')
    out.append(f'<line x1="{b-pad}" y1="{t+pad}" x2="{a+pad}" y2="{u-pad}" stroke="{INK}" stroke-width="2" stroke-dasharray="7 5"/>')
    cx, cy = (a + b) / 2, (t + u) / 2
    ang = math.degrees(math.atan2(u - t, b - a))
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    out.append(f'<text transform="translate({cx+95*ca+8:.1f} {cy+95*sa-8:.1f}) rotate({ang:.1f})" text-anchor="middle" font-size="14" font-style="italic" fill="{INK}">transactional · space</text>')
    out.append(f'<text transform="translate({cx-95*ca-8:.1f} {cy+95*sa-8:.1f}) rotate({-ang:.1f})" text-anchor="middle" font-size="14" font-style="italic" fill="{INK}">generational · time</text>')
    spots = [(a + 18, t + 32, "start", "receives"), (b - 18, t + 32, "end", "spends"),
             (b - 18, u - 22, "end", "gives"), (a + 18, u - 22, "start", "carries forward")]
    for (x, y, al, verb), (name, col) in zip(spots, REG):
        sq = x if al == "start" else x - 10
        out.append(f'<rect x="{sq}" y="{y-11}" width="10" height="10" fill="{col}"/>')
        tx = x + 16 if al == "start" else x - 16
        out.append(f'<text x="{tx}" y="{y}" text-anchor="{al}" font-size="16" fill="{INK}">{name}</text>')
        out.append(f'<text x="{x}" y="{y+20}" text-anchor="{al}" font-size="13.5" font-style="italic" fill="{SOFT}">{verb}</text>')
    body = svg(W, H, "".join(out), "The transactional dimension joins Potentiality and Encounter; the generational dimension joins Construction and Conservation.")
    return fig(body, "The two crossed dimensions. The transactional dimension (solid) joins Potentiality, which receives, to Encounter, which gives. The generational dimension (dashed) joins Construction, which spends, to Conservation, which carries forward.", n)


def order(n):
    W, H = 760, 170
    states = [("1", "1"), ("0", "1"), ("0", "0"), ("1", "0"), ("1", "1")]
    flips = [None, 0, 1, 0, 1]
    thr = ["Activation", "Egress", "Drain", "Suppression"]
    cols = [POT, CON, ENC, COS, POT]
    out = []
    xs = [60 + i * 160 for i in range(5)]
    for i, (x, (h, c)) in enumerate(zip(xs, states)):
        f = flips[i]
        hc = INK if f == 0 or i == 0 else FAINT
        cc = INK if f == 1 or i == 0 else FAINT
        out.append(f'<rect x="{x-36}" y="22" width="72" height="3" fill="{cols[i]}"/>')
        out.append(f'<text x="{x-14}" y="82" text-anchor="middle" font-size="44" fill="{hc}">{h}</text>')
        out.append(f'<text x="{x+14}" y="82" text-anchor="middle" font-size="44" fill="{cc}">{c}</text>')
        out.append(f'<text x="{x}" y="108" text-anchor="middle" font-size="12.5" font-style="italic" fill="{MUTED}">hold · cross</text>')
        if i < 4:
            out.append(f'<line x1="{x+44}" y1="66" x2="{x+112}" y2="66" stroke="{INK}"/><path d="M{x+116} 66 l-9 -4.5 v9 z" fill="{INK}"/>')
            out.append(f'<text x="{x+80}" y="140" text-anchor="middle" font-size="13.5" fill="{SOFT}">{thr[i]}</text>')
    labels = ["Potentiality", "Construction", "Encounter", "Conservation", "Potentiality"]
    for x, l in zip(xs, labels):
        out.append(f'<text x="{x}" y="16" text-anchor="middle" font-size="13.5" fill="{INK}">{l}</text>')
    body = svg(W, H, "".join(out), "The order as two bits: 11, 01, 00, 10, back to 11. One bit flips at each threshold.")
    return fig(body, "The order as two bits, hold first and cross second. At each threshold exactly one bit flips, shown dark, and the flips alternate between hold and cross.", n)


def closure(n):
    W, H = 760, 300
    out = []
    x0, L, y = 60, 300, 70
    d = 1 / PHI
    out.append(f'<line x1="{x0}" y1="{y}" x2="{x0+L}" y2="{y}" stroke="{INK}" stroke-width="2"/>')
    for x in (x0, x0 + L * d, x0 + L):
        out.append(f'<line x1="{x:.1f}" y1="{y-9}" x2="{x:.1f}" y2="{y+9}" stroke="{INK}" stroke-width="1.5"/>')
    out.append(f'<text x="{x0+L*d/2:.1f}" y="{y-16}" text-anchor="middle" font-size="17" font-style="italic" fill="{INK}">d</text>')
    out.append(f'<text x="{x0+L*d+L*(1-d)/2:.1f}" y="{y-16}" text-anchor="middle" font-size="17" font-style="italic" fill="{INK}">d²</text>')
    out.append(f'<text x="{x0+L/2}" y="{y+34}" text-anchor="middle" font-size="15" fill="{SOFT}">d + d² = 1</text>')
    out.append(f'<text x="{x0}" y="{y+90}" font-size="14" font-style="italic" fill="{MUTED}">The whole splits into the next level, d,</text>')
    out.append(f'<text x="{x0}" y="{y+112}" font-size="14" font-style="italic" fill="{MUTED}">and the level after it, d². Only d = 1/φ does this</text>')
    out.append(f'<text x="{x0}" y="{y+134}" font-size="14" font-style="italic" fill="{MUTED}">at every level.</text>')
    cx, cy, R = 560, 150, 125
    labs = [("level N", 40), ("N + 1", 10), ("N + 2", -22)]
    for k in range(6):
        r = R * d ** k
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{INK if k == 0 else SOFT}" stroke-width="{2 if k == 0 else 1.2}"/>')
    for k, (lab, a) in enumerate(labs):
        r = R * d ** k
        x, y = cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))
        out.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{cx+R+18}" y2="{y:.1f}" stroke="{LINE}"/>')
        out.append(f'<text x="{cx+R+24}" y="{y+4:.1f}" font-size="13" font-style="italic" fill="{MUTED}">{lab}</text>')
    body = svg(W, H, "".join(out), "A unit split into d and d squared, and nested cycles shrinking by 1 over phi at each level.")
    return fig(body, "Closure fixes the scale. If every level has the same shape, each level is the one above it scaled by d, and d² + d = 1 gives d = 1/φ ≈ 0.618.", n)


def recursion(n):
    W, H = 760, 330
    out = []
    # child cycle, level N
    cx, cy, r = 130, 165, 70
    for i, (name, col) in enumerate(REG):
        a0 = 180 - 90 * i
        a1 = a0 - 90
        p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
        out.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{col}" stroke-width="4"/>')
    out.append(f'<text x="{cx}" y="{cy+r+34}" text-anchor="middle" font-size="14" font-style="italic" fill="{MUTED}">a closed cycle, level N</text>')
    # arrow
    out.append(f'<line x1="232" y1="{cy}" x2="318" y2="{cy}" stroke="{INK}"/><path d="M324 {cy} l-10 -5 v10 z" fill="{INK}"/>')
    out.append(f'<text x="278" y="{cy-12}" text-anchor="middle" font-size="13.5" fill="{SOFT}">seen from above</text>')
    # parent, level N+1
    px, py, R = 560, 165, 120
    out.append(f'<circle cx="{px}" cy="{py}" r="{R}" fill="none" stroke="{INK}" stroke-width="2"/>')
    # two axes, each a flattened child cycle
    for rot in (0, 90):
        out.append(f'<g transform="rotate({rot} {px} {py})">'
                   f'<ellipse cx="{px}" cy="{py}" rx="{R}" ry="7" fill="none" stroke="{SOFT}" stroke-width="1.2"/>'
                   f'<line x1="{px-R}" y1="{py}" x2="{px+R}" y2="{py}" stroke="{INK}" stroke-width="1.5"/></g>')
    out.append(f'<path d="M{px+R} {py} l-11 -5 v10 z" fill="{INK}"/>')
    out.append(f'<path d="M{px} {py+R} l-5 -11 h10 z" fill="{INK}"/>')
    out.append(f'<text x="{px}" y="{py+R+34}" text-anchor="middle" font-size="14" font-style="italic" fill="{MUTED}">the cycle at level N+1: two directed axes</text>')
    body = svg(W, H, "".join(out), "A closed four-regime cycle, seen from one level up, collapses into one directed axis; two such axes cross to make the next cycle.")
    return fig(body, "One level up. A closed cycle collapses into a single directed axis. Two axes cross to make the cycle at the next level, and each axis, opened up, is a whole cycle again.", n)


def five(n):
    W, H = 760, 240
    names = ["Identity", "Other", "Occurrence", "Closure", "Recursion"]
    out = []
    base, step, h = 230, 120, 36
    for i, nm in enumerate(names):
        x = 60 + i * step
        y = base - (i + 1) * h
        out.append(f'<rect x="{x}" y="{y}" width="{W-60-x}" height="{h}" fill="none" stroke="{INK if i == 3 else LINE}" stroke-width="{1.6 if i == 3 else 1}"/>')
        out.append(f'<text x="{x+14}" y="{y+24}" font-size="16" fill="{INK}">{i+1}. {nm}</text>')
    body = svg(W, H, "".join(out), "Five dimensions stacked: identity, other, occurrence, closure, recursion.")
    return fig(body, "The five dimensions build on each other. Closure, the fourth, is where a single round becomes a cycle.", n)


def quadragen(n):
    W, H = 520, 390
    s0, s = 100, 320
    out = []
    for i, (name, col) in enumerate(REG):
        x = s0 + (s / 2) * (1 if i in (1, 2) else 0)
        y = 40 + (s / 2) * (1 if i in (2, 3) else 0)
        out.append(f'<rect x="{x}" y="{y}" width="{s/2}" height="{s/2}" fill="none" stroke="{INK}" stroke-width="1"/>')
        out.append(f'<rect x="{x+16}" y="{y+16}" width="10" height="10" fill="{col}"/>')
        out.append(f'<text x="{x+16}" y="{y+52}" font-size="17" fill="{INK}">{name}</text>')
        bits = ["11", "01", "00", "10"][i]
        out.append(f'<text x="{x+16}" y="{y+s/2-18}" font-size="26" fill="{INK}">{bits}</text>')
    c = s0 + s / 2
    out.append(f'<circle cx="{c}" cy="{40+s/2}" r="6" fill="{INK}"/>')
    body = svg(W, H, "".join(out), "The quadragen: four faces of one moment, around the crossing of two dimensions.")
    return fig(body, "The quadragen. The four regimes are four faces of one moment, around the point where the two dimensions cross.", n)


FIGS = {"waves": waves, "phase": phase, "dimensions": dimensions, "order": order,
        "closure": closure, "recursion": recursion, "five": five, "quadragen": quadragen}


def lineage(n):
    rows = [("1932", "Cannon", "homeostasis", "Conservation"),
            ("1944", "Schrödinger", "order from order", "the question"),
            ("1947", "Gray", "one-bit code", "the forced order"),
            ("1952", "Ashby", "the homeostat", "the regime types"),
            ("1967", "Koestler", "the holon", "the persistor"),
            ("1968", "Bertalanffy", "open systems", "hold and cross"),
            ("1977", "Prigogine", "dissipative structures", "the persisting system"),
            ("1980", "Maturana, Varela", "autopoiesis", "closure"),
            ("1986", "Holling", "the adaptive cycle", "nested regimes")]
    W, rh, top = 760, 38, 30
    H = top + rh * len(rows) + 20
    out = [f'<text x="40" y="16" font-size="13" font-style="italic" fill="{MUTED}">who, and the idea</text>',
           f'<text x="{W-20}" y="16" text-anchor="end" font-size="13" font-style="italic" fill="{MUTED}">where it lives in Persistence Dynamics</text>']
    for i, (yr, who, idea, pd) in enumerate(rows):
        y = top + i * rh + 22
        out.append(f'<text x="40" y="{y}" font-size="14" fill="{MUTED}">{yr}</text>')
        out.append(f'<text x="92" y="{y}" font-size="16" fill="{INK}">{who}</text>')
        out.append(f'<text x="232" y="{y}" font-size="15" font-style="italic" fill="{SOFT}">{idea}</text>')
        out.append(f'<line x1="410" y1="{y-5}" x2="560" y2="{y-5}" stroke="{LINE}"/><circle cx="560" cy="{y-5}" r="3" fill="{INK}"/>')
        out.append(f'<text x="{W-20}" y="{y}" text-anchor="end" font-size="16" fill="{INK}">{pd}</text>')
        if i:
            out.append(f'<line x1="40" y1="{y-rh+9}" x2="{W-20}" y2="{y-rh+9}" stroke="{HAIR}"/>')
    body = svg(W, H, "".join(out), "Nine predecessors and the part of Persistence Dynamics each one feeds.")
    return fig(body, "Where each tradition connects. Each line runs from an idea to the part of the theory it lives on in.", n)


FIGS["lineage"] = lineage
