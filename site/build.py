"""Build persistencedynamics.com from the repo's Markdown.

Usage: python3 site/build.py [outdir]   (default: _site)
Needs: pip install markdown
Pages: home, the theory (theory/01 to 07 on one page), the persistor, and what came before.
"""
import html, re, shutil, sys
from pathlib import Path
import markdown

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from figures import FIGS, waves, phase  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"
SITE = "https://persistencedynamics.com"
THEORY = ["01-the-two-operations", "02-the-two-crossed-dimensions", "03-the-four-regimes",
          "04-why-this-order", "05-the-cycle-closes", "06-the-fractal-recursion", "07-the-five-dimensions"]
NAV = [("/theory/", "The theory"), ("/persistor/", "The persistor"), ("/lineage/", "What came before")]
LINKS = {"theory/03-the-four-regimes.md": "/theory/#s3"}
LINKS.update({f"theory/{s}.md": f"/theory/#s{i+1}" for i, s in enumerate(THEORY)})
LINKS.update({"persistor/README.md": "/persistor/", "theory/08-what-came-before.md": "/lineage/"})

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400'
         '&amp;display=swap" rel="stylesheet">')
BAR = '<div class="bar" aria-hidden="true"><i style="background:#1B5BD8"></i><i style="background:#B77800"></i><i style="background:#D63A1F"></i><i style="background:#924D35"></i></div>'
CITE = ('<p>Cite as: van der Klein, R. (2026). <i>Persistence Dynamics: the study of the structural conditions '
        'under which systems persist.</i> persistencedynamics.com</p><p style="margin:0">Text and figures are licensed CC BY 4.0.</p>')


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


def render(md_text, src, figs):
    htm = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    htm = re.sub(r"<!-- fig:(\w+) -->", lambda m: FIGS[m.group(1)](figs.next()), htm)
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
        body = render(rest, f"theory/{s}.md", figs)
        toc.append((i, title))
        sections.append(f'<section id="s{i}"><h2 data-num="{i}">{html.escape(title)}</h2>{body}</section>')
    side = "".join(f'<li><span>{i}</span><a href="#s{i}">{html.escape(t)}</a></li>' for i, t in toc)
    main = f"""<article class="page row">
<div></div>
<div class="body">
<h1>The theory</h1>
<p class="lede" style="margin-top:0">Two operations, each active or latent, give four regimes. The regimes run in one forced order, the cycle closes, and every closed cycle is part of a larger one. Seven steps, each building on the last.</p>
{''.join(sections)}
<nav class="pager"><span></span><a href="/persistor/">The persistor →</a></nav>
</div>
<aside class="side"><div class="sticky"><p class="sc muted" style="margin:0">Contents</p><ol>{side}</ol></div></aside>
</article>"""
    write("/theory/", page("/theory/", "The theory", "The theory in seven steps: two operations, two dimensions, four regimes, one forced order, closure, recursion and five dimensions.", main))
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


def home(toc):
    steps = {1: "Every persisting system holds and crosses, and each operation is active or latent.",
             2: "Two dimensions cross at the centre: transactional, which spans space, and generational, which spans time.",
             3: "Two operations with two states give four regimes: capacitor, factory, reactor, homeostat.",
             4: "The regimes run in one forced order, flipping one bit at each threshold.",
             5: "A round closes when Conservation feeds the next Potentiality, and closure fixes the scale: d = 1/φ.",
             6: "Seen from one level up, a closed cycle is a single axis. Every cycle sits inside a larger one.",
             7: "Identity, other, occurrence, closure and recursion: each rests on the ones below it."}
    items = "".join(f'<li><span>{i}</span><div><a href="/theory/#s{i}">{html.escape(t)}</a><br><span style="font-style:normal;color:var(--soft)">{steps[i]}</span></div></li>' for i, t in toc)
    main = f"""<section class="sec row" style="padding-top:96px">
<div></div>
<div>
<h1 class="thesis">Anything that uses energy to maintain itself runs one cycle.</h1>
<p class="lede">Persistence Dynamics is a theory of what makes things last. Two operations, hold and cross, are each active or latent. That gives four regimes, which run in one forced order. A round closes when Conservation hands its residue to the next Potentiality, and every closed cycle is one part of a larger cycle.</p>
</div>
<div></div>
</section>
<section style="padding-top:40px">
<div class="duo">
{waves(1, interactive=True).replace('<figcaption>', '<figcaption hidden>')}
{phase(2, interactive=True).replace('<figcaption>', '<figcaption hidden>')}
</div>
<div class="row"><div></div><p class="note" style="max-width:640px"><span class="fn">Figures 1 and 2.</span> One round of the cycle, twice. Left: hold (solid) and cross (dashed) are the same wave a quarter of a period apart, each active above the midline. Right: plotted against each other, hold active to the left and cross active at the top, they trace a circle, and the four regimes are its quadrants. The dots move together.</p><div></div></div>
</section>
<section class="rule">
<div class="row sec" style="padding-top:64px">
<div></div>
<div><h2 style="font-size:32px;margin-bottom:18px">The theory in seven steps</h2><ol class="steps">{items}</ol></div>
<div></div>
</div>
</section>
<section class="rule">
<div class="row sec" style="padding-top:64px">
<div></div>
<div>
<h2 style="font-size:32px;margin-bottom:18px">The persistor</h2>
<p style="font-size:25px;line-height:1.38;color:var(--ink)">One cycle that creates the structure for the next cycle to build on.</p>
<p>The persistor is the unit of the theory. In Koestler's word it is a holon: a whole to the parts below it and a part of the whole above it.</p>
<p><a href="/persistor/">The persistor</a></p>
</div>
<div></div>
</div>
</section>
<section class="rule">
<div class="row sec" style="padding-top:64px">
<div></div>
<div>
<h2 style="font-size:32px;margin-bottom:18px">What came before</h2>
<p>The theory stands on Cannon, Schrödinger, Gray, Ashby, Koestler, Bertalanffy, Prigogine, Maturana and Varela, and Holling. Each gave it one piece. <a href="/lineage/">Where each one connects</a></p>
</div>
<div></div>
</div>
</section>"""
    script = """<script>
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
    write("/", page("/", "Persistence Dynamics", "A theory of what makes things last: two operations, four regimes in one forced order, and the persistor, one cycle that creates the structure for the next.", main, script))


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    toc = theory_page()
    home(toc)
    doc("persistor/README.md", "/persistor/", prev=("/theory/", "The theory"), nxt=("/lineage/", "What came before"))
    doc("theory/08-what-came-before.md", "/lineage/", prev=("/persistor/", "The persistor"))
    shutil.copy(HERE / "style.css", OUT / "style.css")
    shutil.copy(HERE / "favicon.svg", OUT / "favicon.svg")
    (OUT / "CNAME").write_text("persistencedynamics.com\n")
    urls = ["/", "/theory/", "/persistor/", "/lineage/"]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    (OUT / "llms.txt").write_text(
        "# Persistence Dynamics\n\n> A theory of what makes things last. Two operations (hold, cross), each active or latent, give four regimes "
        "(Potentiality, Construction, Encounter, Conservation) in one forced order. The unit is the persistor, "
        "a holon in Koestler's sense: one cycle that creates the structure for the next. Every closed cycle is one part of a larger one.\n\n"
        f"- [The theory]({SITE}/theory/): seven steps\n- [The persistor]({SITE}/persistor/): the unit, axioms, formal core, thresholds\n"
        f"- [What came before]({SITE}/lineage/): the traditions the theory builds on\n")
    (OUT / "404.html").write_text(page("/404/", "Not found", "Page not found.",
        '<section class="sec row"><div></div><div><h1 class="thesis">This page does not persist.</h1>'
        '<p class="lede"><a href="/">Back to the start</a></p></div><div></div></section>'))
    print(f"built {OUT}")


if __name__ == "__main__":
    main()
