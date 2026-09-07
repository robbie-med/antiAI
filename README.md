# antiAI

Research project on ambient AI scribes and the coding arms race in US healthcare
(FFS + Medicare Advantage). Thesis: ambient-scribe adoption pivoted from burnout relief
to revenue-cycle optimization, driving a documentation/coding arms race that payers are
already answering with downcoding — and the CY 2027 PFS rule (CMS-1848-P) is the vehicle
CMS is using to formalize the response on a published timetable.

The long-form essay is **"It's 2005 All Over Again"** (v2). Its source material lives
here, structured for the web page **antiAI.robbiemed.org** — an article that is also a
receipts tool (every source inline, no navigation).

## Layout

```
antiAI/
├── README.md            # this file
├── receipts.json        # 27 references, structured (machine-readable)
├── receipts.html        # self-contained receipts page (the web tool shell)
├── scripts/
│   ├── build_receipts.py         # parse essay → receipts.json
│   └── build_receipts_page.py    # receipts.json → receipts.html
└── sources/             # primary-source materials (nothing paraphrased)
    ├── VERIFICATION.md            # what was checked against primary sources + result
    ├── EXTRACTION.md              # citations + verbatim quotes + timeline (earlier pass)
    ├── npj_ambient_ai_scribes_2025.pdf   # Dai/Kvedar/Polsky, npj Digit Med (2025) — THE ANCHOR
    ├── cms_1848_p_fulltext.txt           # 91 FR 43842, full proposed-rule text
    ├── holmgren_fulltext.xml             # Holmgren et al. JAMA Netw Open 2026 (Europe PMC JATS)
    ├── ref22_shah_roi.md                 # Shah & Garcia ROI commentary — key quotes
    ├── ref27_nong_neprash.md             # Nong & Neprash viewpoint — key quotes
    └── fr_doc_meta.json                  # Federal Register API metadata
```

## The anchor source

Dai, T., Kvedar, J.C. & Polsky, D. *Policy brief: ambient AI scribes and the coding
arms race.* npj Digital Medicine 8, 780 (2025). https://doi.org/10.1038/s41746-025-02272-z

## The vehicle

CMS-1848-P (CY 2027 Physician Fee Schedule, 91 FR 43842). Comments close **2026-09-14**.
Traditional MIPS sunsets after CY 2028; MVPs mandatory CY 2029; FHIR-based dQM transition
underway. Both quotes used in the essay are **verbatim** (see `sources/VERIFICATION.md`).

## Verified

- Both CMS quotes verbatim ✓
- Holmgren study figures (1.81 RVU, 5.8%, $3,044, 0.80 encounters, 698/44.6%) ✓
- Nong/Neprash ($300–500/mo) + Shah ROI ($200–600/mo) ✓
- "Same-day" publication of Holmgren + Nong/Neprash (both 2026 Jan 2, PubMed) ✓

## Regenerating

```bash
cd ~/Projects/antiAI
python3 scripts/build_receipts.py        # essay → receipts.json
python3 scripts/build_receipts_page.py   # receipts.json → receipts.html
```

The essay source is read from the cached document path in `scripts/build_receipts.py` —
update that path if the essay moves.
