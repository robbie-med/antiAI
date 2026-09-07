#!/usr/bin/env python3
"""Build index.html — the essay with every receipt inline.

    essay markdown + receipts.json + archive/ + sources/  ->  index.html

The page is self-contained (no external requests) except for links into the
archived source files, which are served from the same static root.
"""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ESSAY = ROOT / "its-2005-all-over-again-v3.md"
RECEIPTS = ROOT / "receipts.json"
OUT = ROOT / "index.html"

# Directories scanned for archived copies, in preference order. Files are matched
# to footnotes by their fnNN_ prefix (fn25_26_ maps to both 25 and 26).
ARCHIVE_DIRS = [
    ("archive/public_domain", "public domain"),
    ("archive/open_access", "open access"),
    ("archive/paywalled_screenshots", "paywalled"),
    ("sources", "source file"),
]

# Files here are gitignored and never deployed. We still record that a capture
# exists so the page can say so plainly instead of silently omitting the source.
NOT_REDISTRIBUTABLE = "archive/paywalled_screenshots"

TYPE_LABELS = {
    "journal": "Journal article",
    "press-release": "Press release",
    "statute": "Statute",
    "government": "Government",
    "report": "Report",
    "news": "News reporting",
    "regulation": "Regulation",
    "interview": "Interview",
    "other": "Source",
}


def find_local_copies():
    """Map footnote number -> list of (relpath, provenance, redistributable)."""
    copies = {}
    for subdir, provenance in ARCHIVE_DIRS:
        d = ROOT / subdir
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if not f.is_file():
                continue
            m = re.match(r"(?:fn|ref)((?:\d+_)*\d+)_", f.name)
            if not m:
                continue
            nums = [int(x) for x in m.group(1).split("_")]
            rel = f"{subdir}/{f.name}"
            ok = not rel.startswith(NOT_REDISTRIBUTABLE)
            for n in nums:
                copies.setdefault(n, []).append((rel, provenance, ok))
    return copies


def links_for(r):
    """Publisher-side links for a receipt, de-duplicated, in a sensible order."""
    out = []
    if r.get("doi"):
        out.append(("DOI", f"https://doi.org/{r['doi']}"))
    if r.get("pmid"):
        out.append(("PubMed", f"https://pubmed.ncbi.nlm.nih.gov/{r['pmid']}/"))
    if r.get("url"):
        out.append(("Publisher", r["url"]))
    seen, uniq = set(), []
    for label, href in out:
        if href not in seen:
            seen.add(href)
            uniq.append((label, href))
    return uniq


def render_citation(text):
    """The citations carry markdown emphasis and bare URLs. Render both."""
    t = html.escape(text)
    t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
    t = re.sub(
        r"(?<![\">])(https?://[^\s<)]+[^\s<).,;])",
        r'<a href="\1">\1</a>',
        t,
    )
    return t


def receipt_html(r, copies):
    n = r["n"]
    parts = [f'<div class="receipt" id="r{n}" role="note">']
    parts.append(f'<div class="r-num">{n}</div>')
    parts.append('<div class="r-body">')

    kind = TYPE_LABELS.get(r.get("type", "other"), "Source")
    parts.append(f'<p class="r-kind">{html.escape(kind)}</p>')

    if r.get("proves"):
        parts.append(
            '<p class="r-proves"><span class="r-lede">Proves</span> '
            f"{html.escape(r['proves'])}</p>"
        )

    parts.append(f'<p class="r-cite">{render_citation(r["citation"])}</p>')

    ids = []
    if r.get("doi"):
        ids.append(f"doi:{r['doi']}")
    if r.get("pmid"):
        ids.append(f"PMID {r['pmid']}")
    if ids:
        parts.append(f'<p class="r-ids">{html.escape("  ·  ".join(ids))}</p>')

    if r.get("note"):
        parts.append(f'<p class="r-note">{html.escape(r["note"])}</p>')

    rows = []
    for rel, provenance, ok in copies.get(n, []):
        name = rel.rsplit("/", 1)[-1]
        if ok:
            rows.append(
                f'<a class="r-file" href="{html.escape(rel)}">'
                f'<span class="r-file-name">{html.escape(name)}</span>'
                f'<span class="r-file-tag">archived copy · {provenance}</span></a>'
            )
        else:
            rows.append(
                '<span class="r-file r-file-off">'
                f'<span class="r-file-name">{html.escape(name)}</span>'
                '<span class="r-file-tag">captured, not republished · '
                "copyrighted</span></span>"
            )
    for label, href in links_for(r):
        rows.append(
            f'<a class="r-file" href="{html.escape(href)}" '
            'target="_blank" rel="noopener">'
            f'<span class="r-file-name">{html.escape(href)}</span>'
            f'<span class="r-file-tag">{label.lower()}</span></a>'
        )
    if rows:
        parts.append('<div class="r-files">' + "".join(rows) + "</div>")

    parts.append("</div></div>")
    return "".join(parts)


# A plate whose icon is this sentinel renders as a full-bleed photograph
# instead of an icon on a colour field.
PHOTO = ("photo", "assets/robbiemed-2005.jpg", "The author, 2005")

# One plate per section: a nuoveXT2 desktop icon centred on a solid field.
# Keyed by section heading; the empty key is the untitled opening.
# Icons are nuoveXT2 by Alexandre Moore, LGPL-3+ — see assets/icons/.
PLATES = {
    "": ("#8e8b83", "01-folder.png"),
    # The promise runs on a photo instead of an icon: the author in 2005.
    "The promise": ("#6b7f99", PHOTO),
    "The staircase": ("#7f7a92", "03-up.png"),
    "The bill": ("#9a6f5c", "04-clock.png"),
    "5:40": ("#6f8a72", "05-home.png"),
    "The check that has to clear": ("#8a7a4f", "06-warning.png"),
    "Who pays the difference": ("#9c6f72", "07-users.png"),
    "It's 2005 all over again": ("#5f7078", "08-audio.png"),
    "Where this goes": ("#7a6a86", "09-next.png"),
}


def plate_html(heading):
    if heading not in PLATES:
        return ""
    colour, icon = PLATES[heading]
    if isinstance(icon, tuple) and icon[0] == "photo":
        _, src, alt = icon
        return (
            f'<div class="plate plate-photo" style="background:{colour}">'
            f'<img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy">'
            "</div>"
        )
    return (
        f'<div class="plate" style="background:{colour}">'
        f'<img src="assets/icons/{icon}" width="128" height="128" alt="">'
        "</div>"
    )


def markers(sup_inner):
    """<sup>[18](#fn18),[19](#fn19)</sup> -> one button per reference."""
    nums = [int(x) for x in re.findall(r"\[(\d+)\]\(#fn\d+\)", sup_inner)]
    if not nums:
        return ""
    btns = "".join(
        f'<button class="mark" data-ref="{n}" aria-expanded="false" '
        f'aria-controls="r{n}" title="Show source {n}">{n}</button>'
        for n in nums
    )
    return f'<span class="marks">{btns}</span>'


def build_body(md_text):
    """Essay markdown -> HTML. The Notes section is dropped; it lives inline now."""
    body = md_text.split("### Notes")[0]
    body = re.sub(r"\n---\s*$", "", body.rstrip())
    # The masthead already carries the title; drop the essay's own H1.
    body = re.sub(r"\A#\s+.*?\n", "", body, count=1)

    # Protect footnote markers from the markdown pass.
    slots = []

    def stash(m):
        slots.append(markers(m.group(1)))
        return f"\x00MARK{len(slots) - 1}\x00"

    body = re.sub(r"<sup>(.*?)</sup>", stash, body, flags=re.S)

    import markdown as md

    out = md.markdown(body, extensions=["extra", "sane_lists"])

    for i, s in enumerate(slots):
        out = out.replace(f"\x00MARK{i}\x00", s)

    # A plate before every section heading, and one opening the essay.
    def put_plate(m):
        heading = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        heading = html.unescape(heading)
        return plate_html(heading) + m.group(0)

    out = re.sub(r"<h2[^>]*>(.*?)</h2>", put_plate, out, flags=re.S)
    out = plate_html("") + out

    unplated = [
        re.sub(r"<[^>]+>", "", h).strip()
        for h in re.findall(r"<h2[^>]*>(.*?)</h2>", out, flags=re.S)
    ]
    for h in unplated:
        if html.unescape(h) not in PLATES:
            print(f"  WARNING: no plate defined for section {h!r}")
    return out


CSS = """
:root{
  --measure:48rem; --size:1.15rem;
  --paper:#fdfdfb; --ink:#16161a; --muted:#5c5c66; --rule:#d6d4cd;
  --rule-hard:#16161a; --link:#1a3fa0; --flag:#8a2b1f; --panel:#f4f2ec;
}
@media (prefers-color-scheme:dark){
  :root{
    --paper:#131316; --ink:#e6e5e1; --muted:#9a99a2; --rule:#33333a;
    --rule-hard:#e6e5e1; --link:#8fb0ff; --flag:#e08a7d; --panel:#1b1b20;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font:var(--size)/1.6 Charter,"Bitstream Charter",Georgia,"Times New Roman",serif;
}
/* Column width and body size are the two knobs worth touching. Keep them in
   proportion: --measure 48rem at --size 1.15rem reads about 80 characters. */
.wrap{max-width:var(--measure); margin:0 auto; padding:0 1.5rem 6rem}

/* masthead */
header{border-bottom:2px solid var(--rule-hard); margin-bottom:2.5rem; padding:3rem 0 1rem}
h1{font-size:2.35rem; line-height:1.1; margin:0; font-weight:600; letter-spacing:-.01em}

/* the tool bar */
.tools{
  display:flex; flex-wrap:wrap; gap:.5rem 1.25rem; align-items:baseline;
  border-bottom:1px solid var(--rule); padding:.85rem 0; margin-bottom:2.5rem;
  position:sticky; top:0; background:var(--paper); z-index:5
}
.tools p{
  margin:0; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.72rem; color:var(--muted); letter-spacing:.04em
}
.tools button{
  font:inherit; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.72rem; letter-spacing:.04em;
  background:none; border:0; border-bottom:1px solid var(--ink); color:var(--ink);
  padding:0 0 1px; cursor:pointer; text-transform:uppercase
}
.tools button:hover{background:var(--panel)}

/* essay */
h2{
  font-size:.78rem; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  letter-spacing:.16em; text-transform:uppercase; color:var(--ink);
  margin:3.25rem 0 1.1rem; padding-top:.9rem; border-top:1px solid var(--rule); font-weight:600
}
/* section plates */
.plate{
  display:flex; align-items:center; justify-content:center;
  height:11rem; margin:3.5rem 0 1.6rem
}
.plate:first-child{margin-top:0}
.plate img{width:128px; height:128px; display:block}
/* the photo plate sizes to the image, not the icon band */
.plate-photo{height:auto}
.plate-photo img{width:100%; height:auto; max-width:100%}
/* the plate is the section break, so the heading drops its rule */
.plate + h2{margin-top:1.2rem; padding-top:0; border-top:0}
p{margin:0 0 1.15rem}
strong{font-weight:600}
a{color:var(--link)}
blockquote{
  margin:1.6rem 0; padding:0 0 0 1.15rem; border-left:2px solid var(--rule-hard);
  font-size:1rem; color:var(--ink)
}
blockquote p:last-child{margin-bottom:0}
hr{border:0; border-top:1px solid var(--rule); margin:2.5rem 0}

/* footnote markers */
.marks{white-space:nowrap}
.mark{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.68rem; line-height:1; vertical-align:.42em;
  background:none; border:0; border-bottom:1px solid var(--link); color:var(--link);
  padding:0 .05em 1px; margin:0 .04em; cursor:pointer
}
.mark:hover,.mark:focus-visible{background:var(--link); color:var(--paper); outline:0}
.mark[aria-expanded="true"]{background:var(--link); color:var(--paper)}

/* receipts */
.receipt{
  display:none; grid-template-columns:2.25rem 1fr; gap:0 .5rem;
  border-top:1px solid var(--rule-hard); border-bottom:1px solid var(--rule);
  background:var(--panel); margin:1.35rem 0; padding:.9rem 1rem .95rem .75rem;
}
.receipt.open{display:grid}
.r-num{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.9rem; font-weight:600; text-align:right; padding-top:.05rem
}
.r-kind{
  margin:0 0 .4rem; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.65rem; letter-spacing:.14em; text-transform:uppercase; color:var(--muted)
}
.r-proves{margin:0 0 .5rem; font-size:.95rem}
.r-lede{
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.65rem; letter-spacing:.12em; text-transform:uppercase;
  color:var(--flag); margin-right:.45rem
}
.r-cite{margin:0 0 .45rem; font-size:.88rem; line-height:1.5; color:var(--muted)}
.r-cite a{overflow-wrap:anywhere}
.r-ids,.r-note{
  margin:0 0 .45rem; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.7rem; color:var(--muted)
}
.r-note{color:var(--flag)}
.r-files{border-top:1px solid var(--rule); margin-top:.6rem}
.r-file{
  display:flex; flex-wrap:wrap; gap:0 .6rem; align-items:baseline;
  padding:.32rem 0; border-bottom:1px solid var(--rule);
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:.72rem;
  text-decoration:none
}
a.r-file:hover .r-file-name{text-decoration:underline}
.r-file-name{color:var(--link); overflow-wrap:anywhere; flex:1 1 12rem}
.r-file-off .r-file-name{color:var(--muted); text-decoration:line-through}
.r-file-tag{color:var(--muted); letter-spacing:.04em; white-space:nowrap}

/* index */
.index h2{border-top:2px solid var(--rule-hard)}
.index .receipt{display:grid; background:none; border-bottom:1px solid var(--rule);
  border-top:0; margin:0; padding:.9rem .25rem}
.index .receipt:first-of-type{border-top:1px solid var(--rule)}
footer{
  margin-top:3rem; padding-top:1rem; border-top:1px solid var(--rule);
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:.7rem; line-height:1.7; color:var(--muted)
}
@media (max-width:34rem){
  h1{font-size:1.85rem}
  .wrap{padding:0 1rem 4rem}
  .receipt{grid-template-columns:1.5rem 1fr}
}
@media print{
  .tools{display:none}
  .receipt{display:grid !important; background:none; break-inside:avoid}
}
"""

JS = """
(function(){
  var bank = document.getElementById('bank');
  var article = document.querySelector('article');
  var marks = document.querySelectorAll('.mark');

  // Each marker gets its own copy of the receipt, opened in place.
  function panelFor(btn){
    var n = btn.dataset.ref;
    if (btn._panel) return btn._panel;
    var src = bank.querySelector('#r' + n);
    if (!src) return null;
    var p = src.cloneNode(true);
    p.id = 'r' + n + '-' + (btn.dataset.slot);
    btn.setAttribute('aria-controls', p.id);
    // Place it after the OUTERMOST block the marker sits in. Climbing to a direct
    // child of <article> keeps a receipt from landing inside a blockquote, where
    // it would read as part of the quotation.
    var block = btn.closest('p, blockquote, li') || btn.parentNode;
    while (block.parentNode && block.parentNode !== article) block = block.parentNode;
    block.parentNode.insertBefore(p, block.nextSibling);
    btn._panel = p;
    return p;
  }

  function toggle(btn, force){
    var p = panelFor(btn);
    if (!p) return;
    var open = (force === undefined) ? !p.classList.contains('open') : force;
    p.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  marks.forEach(function(btn, i){
    btn.dataset.slot = i;
    btn.addEventListener('click', function(){ toggle(btn); });
  });

  function all(open){
    marks.forEach(function(btn){ toggle(btn, open); });
  }
  document.getElementById('open-all').addEventListener('click', function(){ all(true); });
  document.getElementById('close-all').addEventListener('click', function(){ all(false); });
})();
"""


def main():
    receipts = json.loads(RECEIPTS.read_text())["receipts"]
    copies = find_local_copies()
    body = build_body(ESSAY.read_text())

    n_archived = sum(
        1 for r in receipts if any(ok for _, _, ok in copies.get(r["n"], []))
    )

    bank = "".join(receipt_html(r, copies) for r in receipts)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>It's 2005 All Over Again</title>
<meta name="description" content="Ambient AI scribes, the coding arms race, and the
CY 2027 Physician Fee Schedule. Every source inline.">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>It&rsquo;s 2005 All Over Again</h1>
</header>

<div class="tools">
  <p>Click any <span style="color:var(--link)">number</span> to open its source in place.</p>
  <button id="open-all" type="button">Open all</button>
  <button id="close-all" type="button">Close all</button>
</div>

<article>
{body}
</article>

<section class="index">
  <h2>All sources</h2>
  {bank.replace('class="receipt"', 'class="receipt open"')}
</section>

<footer>
  <p>Sources are archived on this server where licensing permits. Paywalled articles
  are cited and linked to the publisher but not republished here.
  Redactions to archived captures are logged in
  <a href="archive/REDACTIONS.md">archive/REDACTIONS.md</a>;
  verification against primary documents is in
  <a href="sources/VERIFICATION.md">sources/VERIFICATION.md</a>.</p>
  <p>Source and build scripts: <a href="https://github.com/robbie-med/antiAI">github.com/robbie-med/antiAI</a></p>
  <p>Section icons from the nuoveXT2 theme by Alexandre Moore,
  <a href="assets/icons/LGPL-3.txt">LGPL-3+</a>.</p>
</footer>

</div>

<div id="bank" hidden>{bank}</div>
<script>{JS}</script>
</body>
</html>
"""
    OUT.write_text(page)
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(page):,} bytes)")
    print(f"  {len(receipts)} receipts, {n_archived} with a redistributable local copy")
    missing = [r["n"] for r in receipts if r["n"] not in copies]
    if missing:
        print(f"  no local capture at all for: {missing}")


if __name__ == "__main__":
    main()
