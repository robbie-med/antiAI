#!/usr/bin/env python3
"""Back-port prose edits made directly in index.html into the markdown source.

index.html is a generated file. When it gets edited in place (e.g. on GitHub),
the .md falls behind and the next build silently reverts the edits. This walks
the <article> back into markdown so the source becomes authoritative again.

The Notes section is preserved verbatim from the existing .md — it never
appears in <article>, so there is nothing to recover for it.

    python3 scripts/backport_html_to_md.py [--check]

--check reports what would change without writing.
"""

import html as html_mod
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
MD = ROOT / "its-2005-all-over-again-v3.md"


def inline(s):
    """HTML inline markup -> markdown."""
    # Footnote markers become <sup>[18](#fn18)</sup>. They are parked in
    # placeholders first: the generic tag-strip below would otherwise eat the
    # <sup> we just wrote, leaving a bare [14](#fn14) — which markdown then
    # reads as a link, or as an *image* when the preceding character is '!'.
    held = []

    def marks(m):
        refs = re.findall(r'data-ref="(\d+)"', m.group(1))
        if not refs:
            return ""
        held.append("<sup>" + ",".join(f"[{r}](#fn{r})" for r in refs) + "</sup>")
        return f"\x00SUP{len(held) - 1}\x00"

    s = re.sub(r'<span class="marks">(.*?)</span>', marks, s, flags=re.S)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<b>(.*?)</b>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<(?:em|i)>(.*?)</(?:em|i)>", r"*\1*", s, flags=re.S)
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', r"[\2](\1)", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html_mod.unescape(s)
    s = re.sub(r"[ \t]+", " ", s).strip()
    for i, sup in enumerate(held):
        s = s.replace(f"\x00SUP{i}\x00", sup)
    return s


def html_to_md_body(doc):
    art = re.search(r"<article>(.*?)</article>", doc, re.S).group(1)
    blocks, pos = [], 0
    pat = re.compile(
        r"<h2[^>]*>(?P<h2>.*?)</h2>"
        r"|<blockquote>(?P<bq>.*?)</blockquote>"
        r"|<p>(?P<p>.*?)</p>"
        r"|<hr\s*/?>(?P<hr>)",
        re.S,
    )
    for m in pat.finditer(art, pos):
        if m.group("h2") is not None:
            blocks.append("## " + inline(m.group("h2")))
        elif m.group("bq") is not None:
            inner = [
                inline(x) for x in re.findall(r"<p>(.*?)</p>", m.group("bq"), re.S)
            ] or [inline(m.group("bq"))]
            blocks.append("\n>\n".join("> " + t for t in inner if t))
        elif m.group("p") is not None:
            t = inline(m.group("p"))
            if t:
                blocks.append(t)
        else:
            blocks.append("---")
    return blocks


def main():
    check = "--check" in sys.argv
    doc = HTML.read_text()
    old = MD.read_text()

    title = re.search(r"\A(#\s+.*?)\n", old).group(1)
    notes = old.split("### Notes", 1)
    if len(notes) != 2:
        sys.exit("could not find '### Notes' in the markdown; aborting")
    tail = "### Notes" + notes[1]

    body = html_to_md_body(doc)
    new = title + "\n\n" + "\n\n".join(body) + "\n\n---\n\n" + tail

    if new == old:
        print("markdown already matches index.html — nothing to do")
        return
    old_paras = [p for p in old.split("### Notes")[0].split("\n\n") if p.strip()]
    new_paras = [p for p in new.split("### Notes")[0].split("\n\n") if p.strip()]
    print(f"blocks recovered from index.html : {len(body)}")
    print(f"markdown body blocks  {len(old_paras)} -> {len(new_paras)}")
    if check:
        print("(--check: not written)")
        return
    MD.write_text(new)
    print(f"wrote {MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
