"""Build persistencedynamics.com from the repo's Markdown.

Usage: python3 site/build.py [outdir]   (default: _site)
Needs: pip install markdown
Pages: home, the persistor, the theory (theory/01 to 07 and 09 on one page), what came before, and about.
"""
import html, re, shutil, sys
from pathlib import Path
import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from figures import FIGS  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"
SITE = "https://persistencedynamics.com"
THEORY = ["01-the-two-operations", "02-the-two-crossed-dimensions", "03-the-four-regimes",
          "04-why-this-order", "05-the-cycle-closes", "06-the-fractal-recursion", "07-the-five-dimensions", "09-how-it-could-be-wrong"]
NAV = [("/persistor/", "The persistor"), ("/theory/", "The theory"), ("/lineage/", "What came before"), ("/about/", "About")]
LINKS = {"theory/03-the-four-regimes.md": "/theory/#s3"}
LINKS.update({f"theory/{s}.md": f"/theory/#s{i+1}" for i, s in enumerate(THEORY)})
LINKS.update({"persistor/README.md": "/persistor/", "theory/08-what-came-before.md": "/lineage/", "about/README.md": "/about/"})

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400'
         '&amp;display=swap" rel="stylesheet">')
BAR = '<div class="bar" aria-hidden="true"><i style="background:#1B5BD8"></i><i style="background:#B77800"></i><i style="background:#D63A1F"></i><i style="background:#924D35"></i></div>'
CITE = ('<p>Cite as: van der Klein, R. (2026). <i>Persistence Dynamics: The Internal Geometry of Dissipative-Autopoietic Systems.</i> '
        'Zenodo. <a href="https://doi.org/10.5281/zenodo.20415561">doi:10.5281/zenodo.20415561</a></p><p style="margin:0">Text and figures are licensed CC BY 4.0.</p>')


def page(url, title, desc, main, script=""):
    nav = "".join(f'<a href="{u}"{" aria-current=\"page\"" if url == u else ""}>{l}</a>' for u, l in NAV)
    full = "Persistence Dynamics" if url == "/" else f"{title} · Persistence Dynamics"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/style.css">
</head>
<body>
{BAR}
<div class="wrap">
<header class="head">
<a class="mark" href="/">Persistence Dynamics</a>
<nav aria-label="Main">{nav}</nav>
</header>
<main>
{main}
</main>
<footer class="foot"><div class="row"><div></div><div class="note">{CITE}</div><div></div></div></footer>
</div>
{script}
</body>
</html>
"""


class Counter:
    def __init__(self):
        self.n = 0

    def next(self):
        self.n += 1
        return self.n


def render(md_text, src, figs, live=False):
    htm = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    def figure(name):
        if live and name in ("waves", "phase"):
            return FIGS[name](figs.next(), interactive=True)
        return FIGS[name](figs.next())
    htm = re.sub(r"<!-- fig:(\w+) -->", lambda m: figure(m.group(1)), htm)
    htm = re.sub(r"<!-- eq: (.*?) -->", lambda m: f'<div class="math">{m.group(1)}</div>', htm, flags=re.S)
    htm = re.sub(r"<p>(<figure.*?</figure>)</p>", r"\1", htm, flags=re.S)
    htm = re.sub(r"<p>(<div class=\"math\">.*?</div>)</p>", r"\1", htm, flags=re.S)
    htm = htm.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")
    base = (ROOT / src).parent

    def fix(m):
        href = m.group(1)
        if re.match(r"^(https?:|#|/)", href):
            return m.group(0)
        rel = (base / href.split("#")[0]).resolve().relative_to(ROOT).as_posix()
        return f'href="{LINKS.get(rel, "/")}"'
    return re.sub(r'href="([^"]+)"', fix, htm)


def split_title(text):
    m = re.match(r"\s*#\s+(.+?)\n(.*)", text, flags=re.S)
    return m.group(1).strip(), m.group(2)


def write(url, text):
    path = OUT / "index.html" if url == "/" else OUT / url.strip("/") / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def theory_page():
    figs, sections, toc = Counter(), [], []
    for i, s in enumerate(THEORY, 1):
        title, rest = split_title((ROOT / f"theory/{s}.md").read_text())
        body = render(rest, f"theory/{s}.md", figs, live=True)
        toc.append((i, title))
        sections.append(f'<section id="s{i}"><h2 data-num="{i}">{html.escape(title)}</h2>{body}</section>')
    side = "".join(f'<li><span>{i}</span><a href="#s{i}">{html.escape(t)}</a></li>' for i, t in toc)
    main = f"""<article class="page row">
<div></div>
<div class="body">
<h1>The theory</h1>
<p class="lede" style="margin-top:0">How a persistor works, in eight steps. Each answers one question and builds on the one before: what a persisting system does, what phases that gives, why they come in one order, why the cycle closes, how cycles stack, what has to be in place, and how the theory could be shown wrong.</p>
{''.join(sections)}
<nav class="pager"><a href="/persistor/">← The persistor</a><a href="/lineage/">What came before →</a></nav>
</div>
<aside class="side"><div class="sticky"><p class="sc muted" style="margin:0">Contents</p><ol>{side}</ol></div></aside>
</article>"""
    write("/theory/", page("/theory/", "The theory", "How a persistor works, in eight steps: two operations, two dimensions, four regimes, one forced order, closure, cycles inside cycles, five conditions, and how the theory could be wrong.", main, SYNC))
    return toc


def doc(src, url, prev=None, nxt=None):
    title, rest = split_title((ROOT / src).read_text())
    body = render(rest, src, Counter())
    body = re.sub(r"<h2>(.*?)</h2>", r'</section><section><h2>\1</h2>', body)
    body = f"<section>{body}</section>"
    p = f'<a href="{prev[0]}">← {prev[1]}</a>' if prev else "<span></span>"
    n = f'<a href="{nxt[0]}">{nxt[1]} →</a>' if nxt else "<span></span>"
    main = f"""<article class="page row">
<div></div>
<div class="body">
<h1>{html.escape(title)}</h1>
{body}
<nav class="pager">{p}{n}</nav>
</div>
<div></div>
</article>"""
    desc = re.sub(r"[*_\[\]]|\(.*?\)", "", rest.strip().split("\n\n")[0])[:200]
    write(url, page(url, title, desc, main))


SYNC = """<script>
(function(){
var w=document.querySelector('svg.waves'),p=document.querySelector('svg.phase');if(!w||!p)return;
var cur=w.querySelector('.cursor'),dh=w.querySelector('.dot-h'),dc=w.querySelector('.dot-c'),dp=p.querySelector('.dot-p');
var names=[].slice.call(document.querySelectorAll('.rname'));
function H(a){return(1+Math.cos(a*Math.PI/180))/2}function C(a){return(1+Math.sin(a*Math.PI/180))/2}
function draw(a){var x=70+670*a/360;cur.setAttribute('x1',x);cur.setAttribute('x2',x);
dh.setAttribute('cx',x);dh.setAttribute('cy',218-170*H(a));dc.setAttribute('cx',x);dc.setAttribute('cy',218-170*C(a));
dp.setAttribute('cx',100+(1-H(a))*320);dp.setAttribute('cy',80+(1-C(a))*320);
var r=Math.floor(a/90)%4;names.forEach(function(n){n.classList.toggle('on',+n.getAttribute('data-i')===r)})}
if(matchMedia('(prefers-reduced-motion: reduce)').matches){draw(45);return}
var t0=null;function step(t){if(t0===null)t0=t;draw(((t-t0)/16000*360)%360);requestAnimationFrame(step)}requestAnimationFrame(step);
})();
</script>"""

REGS = [("Potentiality", "var(--pot)", "hold active · cross active"),
        ("Construction", "var(--con)", "hold latent · cross active"),
        ("Encounter", "var(--enc)", "hold latent · cross latent"),
        ("Conservation", "var(--cons)", "hold active · cross latent")]

EXAMPLES = [
    ("An immune response", "over days to weeks", [
        "A lymph node gathers antigen until it crosses the threshold for priming T-cells.",
        "One T-cell clone is selected and expands into an army of the same specificity.",
        "The T-cells meet the tumour at many sites at once. Nothing is held back and nothing more is reached for: the meeting is the work.",
        "The tumour is cleared. A memory population is kept; the rest is released. Memory is the starting material of the next response."]),
    ("A neuron", "in a few milliseconds", [
        "The membrane charges as inputs arrive, until it reaches the firing threshold.",
        "The neuron fires. One spike is built and travels down the axon.",
        "Transmitter meets receptors at many synapses at once.",
        "During the refractory period the neuron restores its resting state and cannot fire. Then it charges again."]),
]


def section(title, inner, first=False):
    pad = "padding-top:96px" if first else "padding-top:64px"
    wrap_open = "" if first else '<section class="rule">'
    wrap_close = "" if first else "</section>"
    return f"""{wrap_open}<div class="row sec" style="{pad}"><div></div><div>{f'<h2 class="h2">{title}</h2>' if title else ''}{inner}</div><div></div></div>{wrap_close}"""


def home(toc):
    heads = "".join(f'<div class="cy-h" style="border-color:{c}"><span class="cy-n">{n}</span><span class="cy-b">{b}</span></div>' for n, c, b in REGS)
    grids = ""
    for name, span, steps in EXAMPLES:
        cells = "".join(f'<div class="cy-c" style="border-color:{c}"><span class="cy-n cy-m">{n}</span>{t}</div>' for (n, c, _), t in zip(REGS, steps))
        grids += f'<p class="cy-t"><b>{name}</b>, {span}</p><div class="cycle">{cells}</div>'
    square_fig = FIGS["square"](1)
    main = f"""<section class="sec row" style="padding-top:96px">
<div></div>
<div>
<h1 class="thesis">Why does anything last?</h1>
<p class="lede">A cell, a flame, an immune response, a team: each keeps its shape while the world around it runs down. Erwin Schrödinger asked how in 1944. Ilya Prigogine and then Humberto Maturana and Francisco Varela showed which kinds of system can do it. None of them described the cycle that runs inside such a system. Persistence Dynamics does.</p>
</div>
<div></div>
</section>
{section("Anything that persists by running is a persistor", '''<p class="big">A cell, a flame, an immune response, a team: each keeps its shape the same way. It runs one cycle that creates the structure for its next cycle to build on.</p>
<p>That cycle is the <b>persistor</b>, the unit of the theory. Persistors sit inside persistors, from a molecule to an institution. It is a large claim, and the theory is built so that it can be tested and could fail.</p>
<p><a href="/persistor/">The persistor →</a></p>''')}
{section("Two operations, four regimes, one order", f'''<p>A persistor does two things. It <b>holds</b>: it keeps what it has gathered. It <b>crosses</b>: it reaches beyond itself to engage something else. At any moment each operation is either active or latent. That gives four combinations, the four <b>regimes</b>, and a persistor always runs through them in the same order. Here is the same cycle in two systems that run at very different speeds.</p>
</div><div></div></div><div class="row"><div></div><div class="cywrap">{grids}<p class="note" style="margin-top:6px">Encounter, with both operations latent, is not idle: the system is no longer gathering or building, because it is in contact. Between each regime and the next, exactly one of the two operations switches. After Conservation the round closes, and what it releases becomes the material of the next Potentiality.</p></div><div></div></div><div class="row"><div></div><div>
<p style="margin-top:24px"><a href="/theory/">How it works, step by step →</a></p>''')}
{section("Why this order and no other", f'''<p class="big">The order of the regimes is not observed and then named. It follows from the two operations.</p>
<p>Write each regime as two bits, hold first and cross second, with 1 for active and 0 for latent. The four regimes become the four corners of a square. Each corner is joined to the two corners that differ from it by one switch, and not to the corner opposite, which would need both operations to switch at once.</p>
{square_fig}
<p>A cycle has to pass through all four regimes and come back. On the square there is only one path that does this: round the edge. Any other order would switch both operations in at least one step, which, in the paper's words, &ldquo;skips a regime instead of passing through it&rdquo;. So the steps alternate, hold then cross then hold then cross.</p>
<p>A second argument, independent of the first, gives the same order. Each regime produces what the next one consumes. Potentiality gathers the material that Construction builds from. Construction delivers the forms that Encounter brings into contact. Encounter leaves the outcomes that Conservation keeps, and Conservation releases the material the next Potentiality gathers.</p>
<p>This is also where the theory is most exposed. A persisting system seen to switch both operations at once, cutting across the square, would disprove it.</p>
<p><a href="/theory/#s4">Why this order, in full →</a></p>''')}
{section("What it is for", '''<p class="big">Its first use is reading where a system is stuck. Because the order is fixed, a system that stops running stops at a particular threshold. You can ask which regime it is in, which threshold it cannot cross, and what has to be in place underneath before it can.</p>
<p>That reading works the same way in a cell, a team or a market, which gives it two further uses.</p>
<ol class="steps">
<li><span>1</span><div><b>One vocabulary across fields.</b> A finding in one field gets a form that can be read in another.</div></li>
<li><span>2</span><div><b>A theory that can fail.</b> Its predictions are numbers. Adjacent nested levels should contract by the same ratio, <i>d</i> = 1/φ ≈ 0.618. A cycling system fitted as a damped oscillator should lose amplitude at γ<i>T</i> ≈ 1.924 per cycle when it has four nested levels. Both hold if the levels are self-similar, and a robust measurement of another value disproves them. <a href="/theory/#s8">How it could be wrong</a></div></li>
</ol>''')}
{section("Who", '''<p>Persistence Dynamics is developed by Raimo van der Klein at <a href="https://encounter.bio">Encounter</a>, which applies it to cancer. It was first published as a preprint on <a href="https://doi.org/10.5281/zenodo.20415561">Zenodo</a> in May 2026. It builds on a line of thinkers from Walter Cannon to C. S. Holling: <a href="/lineage/">what came before</a>.</p>
<p><a href="/about/">About the author and the paper →</a></p>''')}"""
    write("/", page("/", "Persistence Dynamics", "Why does anything last? Persistence Dynamics: anything that persists by running is a persistor, one cycle of four regimes in a forced order that creates the structure for the next.", main))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    toc = theory_page()
    home(toc)
    doc("persistor/README.md", "/persistor/", prev=("/", "Home"), nxt=("/theory/", "How it works: the theory"))
    doc("theory/08-what-came-before.md", "/lineage/", prev=("/theory/", "The theory"), nxt=("/about/", "About"))
    doc("about/README.md", "/about/", prev=("/lineage/", "What came before"), nxt=("/persistor/", "Start with the persistor"))
    shutil.copy(HERE / "style.css", OUT / "style.css")
    shutil.copy(HERE / "favicon.svg", OUT / "favicon.svg")
    (OUT / "CNAME").write_text("persistencedynamics.com\n")
    urls = ["/", "/persistor/", "/theory/", "/lineage/", "/about/"]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    (OUT / "llms.txt").write_text(
        "# Persistence Dynamics\n\n> A theory of what makes things last. Two operations (hold, cross), each active or latent, give four regimes "
        "(Potentiality, Construction, Encounter, Conservation) in one forced order. The unit is the persistor, "
        "a holon in Koestler's sense: one cycle that creates the structure for the next. Every closed cycle is one part of a larger one.\n\n"
        f"- [The persistor]({SITE}/persistor/): the unit of the theory; anything that persists by running is a persistor\n- [The theory]({SITE}/theory/): how a persistor works, in eight steps, and how it could be wrong\n"
        f"- [What came before]({SITE}/lineage/): the traditions the theory builds on\n- [About]({SITE}/about/): Raimo van der Klein, Encounter, and the paper (Zenodo, doi:10.5281/zenodo.20415561)\n")
    (OUT / "404.html").write_text(page("/404/", "Not found", "Page not found.",
        '<section class="sec row"><div></div><div><h1 class="thesis">This page does not persist.</h1>'
        '<p class="lede"><a href="/">Back to the start</a></p></div><div></div></section>'))
    print(f"built {OUT}")


if __name__ == "__main__":
    main()
