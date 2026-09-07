# Verification log — antiAI receipts

What I checked against primary sources (2026-09-06), and the result.

## Load-bearing quotes — VERBATIM ✓

Both CMS quotes were checked against the full CMS-1848-P text on disk
(`sources/cms_1848_p_fulltext.txt`, footnote markers stripped).

| Quote | Status |
|---|---|
| RFI "…AI scribes… 25% penetration among all US physicians…" | **verbatim** ✓ |
| "…traditional MIPS reporting option would be sunset… CY 2029 performance period/2031 MIPS payment year" | **verbatim** ✓ |
| RFI title "Redesigning Primary Care To Make America Healthy Again" | **verbatim** ✓ |

## Holmgren study (ref 21) — all key figures verified against full text ✓

Source: full JATS XML pulled via Europe PMC (`sources/holmgren_fulltext.xml`).

| Figure in essay | In primary text | |
|---|---|---|
| ~1.2 million ambulatory encounters | 182,617 encounters = 15.2% of total → ~1.20M total | ✓ |
| 1,565 physicians | "1 565" present | ✓ |
| 698 adopters (44.6%) | "698 (44.6%) were AI scribe adopters and 867 were nonadopters" | ✓ |
| +1.81 RVUs/week | "1.81 (95% CI, 0.86–2.75) greater RVUs per week" | ✓ |
| 5.8% increase | matches UCSF release + commentary | ✓ |
| $3,044 annual | "1.81 RVUs per week increase translates to $3044 annually per physician, using the 2025 Medicare Physician Fee Schedule" | ✓ |
| +0.80 encounters/week | "0.80 (95% CI, 0.05–1.56) more encounters per week" | ✓ |
| no denial increase | "no difference in claim denial proportion" (abstract/commentary) | ✓ |

## Nong & Neprash (ref 27) — verified ✓

- **$300–$500/mo** subscription — in the article ✓
- Recoupment math: "A $500/month ambient scribe payment can be recouped in roughly
  4 additional level-4 established patient Medicare office visits per month." ✓
- **Published 2026 Jan 2** (PubMed issue date) — same issue as Holmgren (ref 21), so
  the essay's "same day as ref. 21" holds at the citation level. ✓

## Shah ROI commentary (ref 22) — verified ✓

- **$200–$600/clinician/mo** subscription ✓
- "…could collectively offset subscription fees" ✓
- Independently names the "coding arms race": "Recent downcoding policies by Aetna
  and Cigna may signal a 'coding arms race'…" ✓ (this is a *second* source naming it,
  beyond the npj brief)

## Minor flags (not errors, but note)

1. **ref 17 (NEJM AI article ID).** The essay cites "NEJM AI 2025;2:AIe2501175" while
   the npj brief's own reference list prints the DOI as `10.1056/AIe2501051`. This is
   an internal inconsistency in the *npj* article that the essay inherited. Verify the
   article ID before print if you rely on the exact volume/issue string.
2. **ref 19 date.** Essay body says npj brief "dated 24DEC2025" — correct
   (Nature publication date 2025-12-24).

## Blocked / not-yet-fetched

- **PMC direct HTML** for Holmgren is reCAPTCHA-walled (bot detection) — but the full
  text was retrieved via Europe PMC, so nothing is missing.
- **refs 20, 23, 24** (Trilliant/Blue Health claims analysis; CMS Health Tech pledge;
  Fierce Healthcare piece) are industry/news items without stable public URLs in the
  essay; the footnotes describe them but don't link. Left as-is; worth adding links
  when you have them.
