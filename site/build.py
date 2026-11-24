"""Build persistencedynamics.com from the repo's Markdown.

Usage: python3 site/build.py [outdir]   (default: _site)
Needs: pip install markdown
"""
import html, os, re, shutil, sys
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"
SITE = "https://persistencedynamics.com"
REPO = "https://github.com/raimovanderklein/persistencedynamics"

THEORY = [
    ("01-the-two-operations", "1"), ("02-the-two-crossed-dimensions", "2"),
    ("03-the-four-regimes", "3"), ("04-why-this-order", "4"),
    ("05-the-cycle-closes", "5"), ("06-the-fractal-recursion", "6"),
    ("07-the-five-dimensions", "7"), ("08-what-came-before", "8"),
    ("09-what-this-is-for", "9"),
]
# theory/10 (how the lab uses it) is about Encounter, not PD, so it is left off the site.

# source file (relative to ROOT) -> URL path
PAGES = {"theory/README.md": "/theory/", "theory/00-introduction.md": "/theory/",
         "persistor/README.md": "/persistor/", "persistor/spec.md": "/persistor/spec/",
         "persistor/HISTORY.md": "/persistor/history/", "claims.md": "/claims/",
         "papers/README.md": "/papers/", "README.md": "/"}
for slug, _ in THEORY:
    PAGES[f"theory/{slug}.md"] = f"/theory/{slug}/"

NAV = [("/theory/", "0 THEORY"), ("/persistor/", "1 PERSISTOR"), ("/claims/", "2 CLAIMS"),
       ("/persistor/history/", "3 HISTORY"), ("/papers/", "4 PAPERS")]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400'
         '&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">')
KATEX = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.css">'
         '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>'
         '<script>addEventListener("DOMContentLoaded",function(){document.querySelectorAll(".math").forEach(function(e){'
         'try{katex.render(e.textContent,e,{displayMode:true,throwOnError:false})}catch(x){}})})</script>')

STATUS = {"structural": "derived", "derived": "deriv", "tested": "tested", "open": "open", "falsified": "false"}


def page(url, title, desc, main, crumbs="", math=False):
    nav = "".join(
        f'<a href="{u}"{" aria-current=\"page\"" if url.startswith(u) and not (u == "/persistor/" and url.startswith("/persistor/history/")) else ""}>{l}</a>'
        for u, l in NAV)
    full_title = "Persistence Dynamics" if url == "/" else f"{title} · Persistence Dynamics"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{SITE}{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/style.css">
{KATEX if math else ""}
</head>
<body>
<div class="wrap">
<header class="head mono">
<a class="mark" href="/">PERSISTENCE DYNAMICS</a>
<nav aria-label="Main">{nav}<a href="{REPO}">SOURCE ↗</a></nav>
</header>
{crumbs}
<main>
{main}
</main>
<footer class="foot">
<div class="row">
<div class="addr">Colophon</div>
<div class="note" style="font-size:15px">
<p>Cite as: van der Klein, R. (2026). <i>Persistence Dynamics: the study of the structural conditions under which systems persist.</i> persistencedynamics.com</p>
<p>Text and figures CC BY 4.0. Code MIT. The source of every page, and every change to it, is public on <a href="{REPO}">GitHub</a>.</p>
</div>
<div></div>
</div>
</footer>
</div>
</body>
</html>
"""


def rewrite_links(htm, src):
    """Point .md links at site URLs and anything else in the repo at GitHub."""
    base = (ROOT / src).parent

    def fix(m):
        href = m.group(1)
        if re.match(r"^(https?:|mailto:|#|/)", href):
            return m.group(0)
        path, _, frag = href.partition("#")
        target = (base / path).resolve()
        try:
            rel = target.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        frag = f"#{frag}" if frag else ""
        if rel in PAGES:
            return f'href="{PAGES[rel]}{frag}"'
        if rel.startswith("papers/") and rel.endswith(".pdf"):
            return f'href="/{rel}"'
        kind = "tree" if target.is_dir() else "blob"
        return f'href="{REPO}/{kind}/main/{rel}{frag}"'

    htm = re.sub(r'href="([^"]+)"', fix, htm)
    for a, b in ((">HISTORY.md<", ">the history<"), (">claims.md<", ">the claims ledger<"),
                 (">archive/<", ">the archive<"), (">spec.md<", ">the specification<")):
        htm = htm.replace(a, b)
    return htm


def addr_for(text):
    m = re.match(r"^(\d+(?:\.\d+)*)\.?\s", text)
    if m:
        n = m.group(1)
        return "§" + n, "s" + n.replace(".", "-")
    m = re.match(r"^Part ([A-Z])\b", text)
    if m:
        return "Part " + m.group(1), "part-" + m.group(1).lower()
    return None, None


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def render(md_text, src, addr_prefix=""):
    md_text = re.sub(r"```latex\n(.*?)\n```", lambda m: f'<div class="math">{html.escape(m.group(1))}</div>',
                     md_text, flags=re.S)
    htm = markdown.markdown(md_text, extensions=["tables", "sane_lists", "attr_list"])
    # status labels like [structural] or [derived; empirical fit open]
    def lab(m):
        inner = m.group(1)
        first = inner.split(";")[0].split(":")[0].strip().lower()
        cls = STATUS.get(first)
        if not cls:
            return m.group(0)
        if "open" in inner.lower() and cls != "false":
            cls = cls if cls in ("derived",) else cls
        return f'<span class="st {cls}"><i></i>{html.escape(inner)}</span>'
    htm = re.sub(r"\[((?:structural|derived|tested|open|falsified)[^\]]*)\]", lab, htm)

    # status cells in tables
    def cell(m):
        txt = m.group(1)
        first = re.split(r"[;\s(]", re.sub(r"<[^>]+>", "", txt).strip().lower())[0]
        cls = STATUS.get(first)
        if not cls:
            return m.group(0)
        return f'<td><span class="st {cls}"><i></i>{txt}</span></td>'
    htm = re.sub(r"<td>((?:<strong>)?(?:structural|derived|tested|open|falsified)\b[^<]*(?:</strong>[^<]*)?)</td>", cell, htm)
    htm = htm.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")

    toc = []

    def head(m):
        lvl, text = m.group(1), m.group(2)
        plain = re.sub(r"<[^>]+>", "", text)
        a, i = addr_for(plain)
        if a:
            shown = re.sub(r"^(\d+(?:\.\d+)*)\.?\s+", "", text) if a.startswith("§") else text
            shown = re.sub(r"^Part [A-Z]:\s*", "", shown) if a.startswith("Part") else shown
            toc.append((lvl, i, a, re.sub(r"<[^>]+>", "", shown)))
            return f'<h{lvl} id="{i}" data-addr="{addr_prefix}{a}">{shown}</h{lvl}>'
        i = slug(plain)
        toc.append((lvl, i, "", plain))
        return f'<h{lvl} id="{i}">{text}</h{lvl}>'
    htm = re.sub(r"<h([234])>(.*?)</h\1>", head, htm)
    return rewrite_links(htm, src), toc


def split_title(md_text):
    m = re.match(r"\s*#\s+(.+?)\n(.*)", md_text, flags=re.S)
    return (m.group(1).strip(), m.group(2)) if m else ("", md_text)


def lede(md_text):
    for para in md_text.split("\n\n"):
        p = para.strip()
        if p and not p.startswith(("#", "|", "-", "```", "<")):
            return re.sub(r"[*_`\[\]]|\(.*?\)", "", p)[:200]
    return ""


def doc_page(src, url, crumbs, addr="", side_toc=True, prev=None, nxt=None, extra_side=""):
    raw = (ROOT / src).read_text()
    title, rest = split_title(raw)
    body, toc = render(rest, src)
    sects = [t for t in toc if t[0] in ("2", "3")]
    side = ""
    if side_toc and len(sects) >= 4:
        items = "".join(
            f'<li class="l{l}"><a href="#{i}">{(a + " ") if a.startswith("§") else ""}{html.escape(t)}</a></li>'
            for l, i, a, t in sects)
        side = f'<p class="mono muted" style="margin:0">ON THIS PAGE</p><ol>{items}</ol>'
    side = f'<aside class="side"><div class="sticky">{extra_side}{side}</div></aside>'
    pager = ""
    if prev or nxt:
        p = f'<a href="{prev[0]}">← {prev[1]}</a>' if prev else "<span></span>"
        n = f'<a href="{nxt[0]}">{nxt[1]} →</a>' if nxt else "<span></span>"
        pager = f'<nav class="pager" aria-label="Previous and next">{p}{n}</nav>'
    main = f"""<article class="doc row">
<div class="addr">{addr}</div>
<div class="body">
<h1>{html.escape(title)}</h1>
{body}
{pager}
</div>
{side}
</article>"""
    write(url, page(url, title, lede(rest), main, crumbs, math='class="math"' in body))


def crumb(*parts):
    bits = [f'<a href="{u}">{html.escape(t)}</a>' if u else html.escape(t) for t, u in parts]
    return f'<p class="crumbs">{" &nbsp;/&nbsp; ".join(bits)}</p>'


def write(url, text):
    path = OUT / url.strip("/") / "index.html" if url != "/" else OUT / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    here = Path(__file__).parent

    # home
    write("/", page("/", "Persistence Dynamics",
                    "A theory of what makes things last: two operations, four regimes in one forced order, "
                    "and the persistor, one cycle that creates the structure for the next.",
                    (here / "home.html").read_text()))

    # theory index = introduction + contents
    intro_title, intro = split_title((ROOT / "theory/00-introduction.md").read_text())
    intro_html, _ = render(intro, "theory/00-introduction.md")
    titles = {}
    for s, n in THEORY:
        t, _ = split_title((ROOT / f"theory/{s}.md").read_text())
        titles[s] = t or s
    items = "".join(f'<li><span>{n}</span><a href="/theory/{s}/">{html.escape(titles[s])}</a></li>' for s, n in THEORY)
    main_html = f"""<article class="doc row">
<div class="addr">§0</div>
<div class="body">
<h1>The theory</h1>
{intro_html}
<h2>Contents</h2>
<div class="toc" style="grid-template-columns:1fr"><ol>{items}</ol></div>
<nav class="pager"><span></span><a href="/theory/{THEORY[0][0]}/">1 {html.escape(titles[THEORY[0][0]])} →</a></nav>
</div>
<aside class="side"><div class="sticky"><p class="mono muted" style="margin:0 0 8px">VERSION 2 · 27 MAY 2026</p>
<p>The canonical text, one page per section. Its quantitative claims are tracked in the <a href="/claims/">ledger</a>.</p></div></aside>
</article>"""
    write("/theory/", page("/theory/", "The theory", lede(intro), main_html))

    for k, (s, n) in enumerate(THEORY):
        prev = ("/theory/", "Contents") if k == 0 else (f"/theory/{THEORY[k-1][0]}/", f"{THEORY[k-1][1]} {titles[THEORY[k-1][0]]}")
        nxt = (f"/theory/{THEORY[k+1][0]}/", f"{THEORY[k+1][1]} {titles[THEORY[k+1][0]]}") if k + 1 < len(THEORY) else None
        doc_page(f"theory/{s}.md", f"/theory/{s}/", crumb(("The theory", "/theory/"), (f"§{n}", None)),
                 addr=f"§{n}", prev=prev, nxt=nxt)

    doc_page("persistor/README.md", "/persistor/", "", addr="Unit",
             nxt=("/persistor/spec/", "The specification"),
             extra_side='<p style="margin:0 0 18px"><b>Three names, one concept.</b> Persistor is the public term. '
                        'Change Unit and Quadragen are the same concept in other shapes.</p>')
    doc_page("persistor/spec.md", "/persistor/spec/",
             crumb(("The persistor", "/persistor/"), ("Specification v1.0", None)), addr="Spec",
             prev=("/persistor/", "The persistor"), nxt=("/persistor/history/", "History"))
    doc_page("persistor/HISTORY.md", "/persistor/history/",
             crumb(("The persistor", "/persistor/"), ("History", None)), addr="Record",
             prev=("/persistor/spec/", "The specification"))
    doc_page("claims.md", "/claims/", "", addr="Ledger")
    doc_page("papers/README.md", "/papers/", "", addr="Papers")
    for pdf in (ROOT / "papers").glob("*.pdf"):
        (OUT / "papers").mkdir(exist_ok=True)
        shutil.copy(pdf, OUT / "papers" / pdf.name)

    # static files
    shutil.copy(here / "style.css", OUT / "style.css")
    shutil.copy(here / "favicon.svg", OUT / "favicon.svg")
    shutil.copy(ROOT / "llms.txt", OUT / "llms.txt")
    (OUT / "CNAME").write_text("persistencedynamics.com\n")
    urls = ["/", "/theory/"] + [f"/theory/{s}/" for s, _ in THEORY] + \
           ["/persistor/", "/persistor/spec/", "/persistor/history/", "/claims/", "/papers/"]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    (OUT / "404.html").write_text(page("/404/", "Not found", "Page not found.",
        '<section class="sec row"><div class="addr">404</div><div><h1 class="thesis">This page does not persist.</h1>'
        '<p style="margin-top:28px"><a href="/">Back to the start</a></p></div><div></div></section>'))
    print(f"built {OUT}")


if __name__ == "__main__":
    main()
