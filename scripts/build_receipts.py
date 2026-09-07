#!/usr/bin/env python3
"""Parse the 30 footnotes out of the essay into structured receipts.json (with URLs)."""
import json, re
from pathlib import Path

essay = Path('/home/user/Projects/antiAI/its-2005-all-over-again-v3.md').read_text()

notes = essay.split('### Notes', 1)[1]
fn_re = re.compile(r'<a name="fn(\d+)"></a>\s*(\d+)\.\s*(.*?)(?=\n\n<a name="fn|\n\n\*Note|\n*$)', re.S)
footnotes = {}
for m in fn_re.finditer(notes):
    num = int(m.group(1))
    text = m.group(3).strip().replace('\n', ' ')
    footnotes[num] = text

# meta: type, proves, doi, pmid, url(s). URLs via doi.org/pubmed auto-generated too.
meta = {
 1: dict(type="journal", proves="RAND's $81B/year savings claim (Sept 2005)",
        doi="10.1377/hlthaff.24.5.1103", pmid="16162551"),
 2: dict(type="press-release", proves="RAND admitted evidence didn't exist; used simulation models",
        url="https://www.rand.org/news/press/2005/09/14.html"),
 3: dict(type="journal", proves="Himmelstein & Woolhandler: 'hope and hype' — the objection that lost",
        doi="10.1377/hlthaff.24.5.1121"),
 4: dict(type="journal", proves="Goodman: 'do it for the quality, not the savings'",
        doi="10.1377/hlthaff.24.5.1124"),
 5: dict(type="statute", proves="HITECH passed inside 2009 stimulus (ARRA)",
        url="https://www.congress.gov/bill/111th-congress/house-bill/1"),
 6: dict(type="government", proves="$44,000 Medicare / $63,750 Medicaid incentives; 2016 last start year",
        url="https://www.cms.gov/medicare/medicare-ehr-incentive-program-basics",
        note="archived (National Archives web capture)"),
 7: dict(type="statute", proves="§1848(a)(7) penalty 99/98/97% + rural hardship exception",
        url="https://www.ssa.gov/OP_Home/ssact/title18/1848.htm"),
 8: dict(type="statute", proves="MACRA 2015",
        url="https://www.congress.gov/bill/114th-congress/house-bill/2"),
 9: dict(type="government", proves="Promoting Interoperability = 25% of MIPS; 7 measures/5 objectives",
        url="https://www.ama-assn.org/system/files/medicare-basics-mips.pdf"),
 10: dict(type="government", proves="±9% MIPS adjustment; penalty certain under budget neutrality",
        note="ACS MIPS resource PDF; no stable public URL identified"),
 11: dict(type="news", proves="Anna Konopka case: e-system load-bearing for licensure",
        urls=["https://www.statnews.com/2017/11/27/anna-konopka-new-hampshire-doctor/",
              "https://www.cnn.com/2017/11/28/health/anna-konopka-new-hampshire-doctor/"]),
 12: dict(type="journal", proves="27% face time, 49.2% EHR/desk, 37% screen in exam room",
        doi="10.7326/M16-0961", pmid="27595430"),
 13: dict(type="journal", proves="'Tethered to the EHR' follow-on study",
        url="https://www.annfammed.org/content/15/5/419"),
 14: dict(type="journal", proves="RAND's own reversal: mixed evidence + $800B added spend",
        doi="10.1377/hlthaff.2012.0693"),
 15: dict(type="news", proves="'Death By 1,000 Clicks': $36B, 9%→96% adoption, $13B/yr industry",
        url="https://kffhealthnews.org/health-industry/death-by-a-thousand-clicks/"),
 16: dict(type="industry-data", proves="Epic revenue $1.2B→$6.7B; 43.7% share; 56.9% beds; Oracle/Cerner $28.3B; Cosmos 1.7T events",
        note="KLAS Research market-share via Becker's Hospital Review; no single stable URL"),
 17: dict(type="journal+report", proves="Scribes reduce burnout; financial impact unclear; 'not productivity tools yet'",
        doi="10.1056/AIe2501051",  # Kim/Liu/Singh — ID printed inconsistently (see essay note)
        url="https://petersonhealthtech.org/",
        note="NEJM AI article ID inconsistency flagged in essay (AIe2501175 vs AIe2501051)"),
 18: dict(type="news", proves="$1B funding in 2025; Abridge $250M; Ambience mega-round",
        url="https://www.statnews.com/2025/07/29/ambience-healthcare-ai-scribe-new-fundraise/"),
 19: dict(type="journal", proves="THE ANCHOR: pivot to revenue-cycle language; coding arms race; Riverside/NW/Texas Oncology; Cigna; winners = subscription + data",
        doi="10.1038/s41746-025-02272-z",
        url="https://www.nature.com/articles/s41746-025-02272-z",
        local="npj_ambient_ai_scribes_2025.pdf"),
 20: dict(type="claims-analysis", proves="Six-system claims analysis: high-intensity E/M coding +12-20 pts, 80% at one system",
        note="Trilliant Health / Blue Health Intelligence; no stable public URL"),
 21: dict(type="journal", proves="Holmgren: +1.81 RVU/wk (5.8%), $3,044/yr, +0.80 encounters, no denial rise",
        doi="10.1001/jamanetworkopen.2025.53233", pmid="41511775",
        url="https://pmc.ncbi.nlm.nih.gov/articles/PMC12789954/",
        local="holmgren_fulltext.xml"),
 22: dict(type="journal", proves="ROI commentary: $200-600/clinician/mo subscription; names 'coding arms race'",
        doi="10.1001/jamanetworkopen.2025.53238"),
 23: dict(type="government", proves="CMS Health Tech Ecosystem pledge, 600+ orgs (voluntary)",
        url="https://www.cms.gov/newsroom/press-releases/white-house-tech-leaders-commit-create-patient-centric-healthcare-ecosystem"),
 24: dict(type="news", proves="Industry told CMS: put incentives in fee schedules; 'provider utilization is the last mile'",
        url="https://bipartisanpolicy.org/explainer/medicare-2027-physician-fee-schedule-proposed-rule-policies-with-potential-to-improve-health-care-affordability-for-patients-and-taxpayers/",
        note="Fierce Healthcare, Apr 2026; Bipartisan Policy Center comment on predictable reimbursement pathways"),
 25: dict(type="government", proves="CMS-1848-P RFI: 'AI scribes… 25% penetration' (VERBATIM)",
        url="https://www.federalregister.gov/documents/2026/07/16/2026-14327",
        local="cms_1848_p_fulltext.txt"),
 26: dict(type="government", proves="MIPS sunset CY2029; MVPs mandatory; FHIR dQMs (VERBATIM)",
        url="https://www.federalregister.gov/documents/2026/07/16/2026-14327",
        local="cms_1848_p_fulltext.txt"),
 27: dict(type="journal", proves="Nong/Neprash: billing tools may raise spending; '$300-500/mo → pressure to increase visits'",
        doi="10.1001/jamahealthforum.2025.5771", pmid="41511793",
        url="https://nihcm.org/publications/exclusive-interview-with-the-researcher-hannah-neprash-on-ambient-ai-scribes"),
 28: dict(type="journal", proves="Rotenstein (5 systems, diff-in-diff): ~$167/mo marginal E/M revenue ≈ $2,004/yr — 'conservative lower bound'",
        doi="10.1001/jama.2026.2253", pmid="41920565"),
 29: dict(type="journal", proves="Hallucination risk + null/mixed productivity findings (Elias; Yadav; Olson; Shah)",
        urls=["https://doi.org/10.1056/aip2500788", "https://doi.org/10.1056/aie2500020"],
        note="Multi-citation: Elias NEJM AI 2025;2(11); Yadav/Longhurst NEJM AI 2025;2(3); Olson JAMA Netw Open 2025;8(10):e2534976; Shah JAMIA 2025;32(2):375-80"),
 30: dict(type="journal", proves="Legal landscape: wiretap/eavesdropping statutes independent of HIPAA; retention governed by contract, not law",
        doi="10.1056/AIp2600203"),
}

receipts = []
for n in sorted(footnotes):
    entry = {"n": n, "citation": footnotes[n]}
    entry.update(meta.get(n, {}))
    receipts.append(entry)

out = {
    "_meta": {
        "source": "It's 2005 All Over Again (v2, final)",
        "domain": "antiAI.robbiemed.org",
        "count": len(receipts),
        "notes": "Citations as written in the essay's Notes section. DOIs/PMIDs/verbatim quotes verified against primary sources 2026-09-06.",
    },
    "receipts": receipts
}
Path('/home/user/Projects/antiAI/receipts.json').write_text(json.dumps(out, ensure_ascii=False, indent=2))
print(f"Wrote {len(receipts)} receipts to receipts.json")
print("Footnotes:", sorted(footnotes.keys()))
