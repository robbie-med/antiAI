#!/usr/bin/env python3
"""Generate a single self-contained receipts page (no navigation) from receipts.json."""
import json
from pathlib import Path

receipts = json.loads(Path('/home/user/Projects/antiAI/receipts.json').read_text())['receipts']

TYPE = {
    "journal": ("Journal article", "#1d4ed8"),
    "journal+report": ("Journal + report", "#1d4ed8"),
    "statute": ("Statute", "#7c3aed"),
    "government": ("Govt document", "#059669"),
    "press-release": ("Press release", "#0f766e"),
    "news": ("News reporting", "#b45309"),
    "industry-data": ("Industry data", "#be123c"),
    "claims-analysis": ("Claims analysis", "#be123c"),
}

cards = []
for r in receipts:
    n = r['n']
    typ, color = TYPE.get(r.get('type',''), ("Source", "#64748b"))
    citation = r['citation'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    proves = r.get('proves','').replace('&','&amp;').replace('<','&lt;')
    # collect links: explicit url/urls, then doi.org, then pubmed
    links = []
    if r.get('url'):
        links.append(r['url'])
    for u in r.get('urls', []):
        links.append(u)
    doi = r.get('doi'); pmid = r.get('pmid')
    if doi:
        links.append(f"https://doi.org/{doi}")
    if pmid:
        links.append(f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
    links = list(dict.fromkeys(links))
    link_html = ' '.join(
        f'<a href="{u}" target="_blank" rel="noopener">{u}</a>' for u in links
    )
    idrow = ''
    if doi: idrow += f'<span class="id">DOI {doi}</span> '
    if pmid: idrow += f'<span class="id">PMID {pmid}</span> '
    local = ''
    if r.get('local'):
        local = f'<span class="local">📄 local: {r["local"]}</span>'
    note = ''
    if r.get('note'):
        note = f'<div class="note">{r["note"]}</div>'

    cards.append(f'''
<article class="card" id="fn{n}">
  <div class="card-head">
    <span class="num">{n}</span>
    <span class="badge" style="background:{color}">{typ}</span>
    <span class="proves">{proves}</span>
  </div>
  <div class="cite">{citation}</div>
  <div class="ids">{idrow}{local}</div>
  {note}
  <div class="links">{link_html}</div>
</article>''')

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>antiAI — The Receipts</title>
<style>
  :root {{ color-scheme: light dark; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         max-width: 860px; margin: 0 auto; padding: 24px 20px 80px;
         line-height: 1.5; background: #fff; color: #111; }}
  @media (prefers-color-scheme: dark) {{ body {{ background: #0f1115; color: #e5e7eb; }} }}
  h1 {{ font-size: 1.6rem; margin: 0 0 4px; }}
  .sub {{ color: #6b7280; margin: 0 0 28px; font-size: .95rem; }}
  .card {{ border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px 16px; margin: 0 0 12px; }}
  @media (prefers-color-scheme: dark) {{ .card {{ border-color: #2a2e37; }} }}
  .card-head {{ display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 6px; }}
  .num {{ background: #111; color: #fff; border-radius: 50%; width: 22px; height: 22px;
         display: inline-flex; align-items: center; justify-content: center;
         font-size: .8rem; font-weight: 600; flex: 0 0 auto; }}
  @media (prefers-color-scheme: dark) {{ .num {{ background: #e5e7eb; color: #111; }} }}
  .badge {{ color: #fff; font-size: .72rem; padding: 2px 8px; border-radius: 999px; font-weight: 600; }}
  .proves {{ font-size: .9rem; font-weight: 600; color: #b91c1c; }}
  @media (prefers-color-scheme: dark) {{ .proves {{ color: #f87171; }} }}
  .cite {{ font-size: .9rem; color: #374151; margin-bottom: 4px; }}
  @media (prefers-color-scheme: dark) {{ .cite {{ color: #cbd5e1; }} }}
  .ids {{ font-size: .8rem; color: #6b7280; margin-bottom: 4px; }}
  .id {{ background: #f3f4f6; border-radius: 4px; padding: 1px 6px; margin-right: 6px; font-family: ui-monospace, monospace; }}
  @media (prefers-color-scheme: dark) {{ .id {{ background: #1f2937; }} }}
  .local {{ font-family: ui-monospace, monospace; font-size: .8rem; color: #059669; }}
  .note {{ font-size: .78rem; color: #92400e; margin: 4px 0; font-style: italic; }}
  @media (prefers-color-scheme: dark) {{ .note {{ color: #fbbf24; }} }}
  .links a {{ font-size: .8rem; color: #2563eb; text-decoration: none; display: block;
              overflow-wrap: anywhere; margin-top: 2px; }}
  .links a:hover {{ text-decoration: underline; }}
  footer {{ margin-top: 40px; color: #9ca3af; font-size: .85rem; }}
</style>
</head>
<body>
  <h1>antiAI — The Receipts</h1>
  <p class="sub">All 30 sources for "It's 2005 All Over Again," inline — no navigation.
  Each card shows the claim it proves, the full citation, and the source link(s).</p>
  {''.join(cards)}
  <footer>S.D.G. · citations as written in the essay; DOIs/PMIDs/verbatim quotes verified against primary sources.</footer>
</body>
</html>'''

out = Path('/home/user/Projects/antiAI/receipts.html')
out.write_text(html)
print(f"Wrote {len(cards)} cards to {out} ({out.stat().st_size} bytes)")
