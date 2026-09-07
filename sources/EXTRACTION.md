# antiAI — Source extraction

Working notes and verbatim primary-source pulls for the ambient-AI-scribe / coding-arms-race
piece. All quotes below are copied from the original documents; nothing is paraphrased
from memory.

---

## 1. The peer-reviewed anchor — npj Digital Medicine policy brief

**Full citation**

> Dai, T., Kvedar, J.C. & Polsky, D. *Policy brief: ambient AI scribes and the coding
> arms race.* **npj Digital Medicine** 8, 780 (2025).
> https://doi.org/10.1038/s41746-025-02272-z — published 2025-12-24 — open access, CC BY.

**Authors (Johns Hopkins + Harvard, as you said):**
- Tinglong Dai — Johns Hopkins University, Carey Business School (and npj Digit. Med. Editor)
- Joseph C. Kvedar — Harvard Medical School / Mass General Brigham
- Daniel Polsky — Johns Hopkins University, Bloomberg School of Public Health

**Files on disk:** `sources/npj_ambient_ai_scribes_2025.pdf` (4-page PDF, 394 KB).

### The pivot from time-saving to revenue-cycle language (verbatim)

> "The business case increasingly centers on revenue capture through more intensive
> coding. Ambience Healthcare's July 2025 funding announcement, for instance, described
> its platform as 'the leading ambient AI system for documentation, coding, and clinical
> documentation integrity,' highlighting how it 'drives revenue-cycle performance.' This
> language marks a clear pivot from earlier messaging about saving doctors time."

### The coding arms race, named (verbatim)

> "If revenue optimization becomes its defining purpose, we risk repeating a familiar
> cycle—an arms race that ends with higher administrative friction, payer pushback, and
> little improvement at the bedside."

### The winners' profit model (verbatim)

> "Vendors will have winners and losers; the winners will profit from subscription
> revenue and accumulated data assets."

### The primary-source chain (all footnoted inside the brief)

| System | Finding | Brief's citation # |
|---|---|---|
| **Riverside Health** (Abridge) | 11% rise in wRVUs; 14% increase in documented HCC diagnoses per encounter | ref 5 → Abridge blog |
| **Northwestern Medicine** (Nuance DAX) | clinicians billed more high-level E/M visits on average | ref 6 → Microsoft/NM white paper |
| **Texas Oncology** (2024) | documented diagnoses rose 3.0 → 4.1 per encounter | ref 7 |
| **Cigna** (Oct 2025) | began auto-reducing many level 4–5 E/M claims by one level unless documentation shows higher complexity | ref 10 |
| **Aetna Better Health** | similar downcoding reviews | ref 11 |
| **Doximity** free scribe | signals basic transcription is commoditizing; differentiation moves "after the transcript" | ref 4 |

---

## 2. CMS-1848-P — the CY 2027 Physician Fee Schedule proposed rule

**Document facts**

- Citation: **91 FR 43842** — Federal Register document number **2026-14327**
- Published: **2026-07-16**
- **Comments close: 2026-09-14** (the "eight days out" date as of your note)
- Full text on disk: `sources/cms_1848_p_fulltext.txt` (2.8 MB, 46,912 lines)

### The RFI that names ambient AI scribes

Section **"E. Request for Information: Redesigning Primary Care To Make America Healthy
Again"** (Federal Register page 43936) — subsection **"4. Payment Implications of
Technology Enablement of Primary Care / a. Changes to Primary Care and Care Management
Due to Technology and Clinical AI"**.

**Verbatim passage (the one to quote):**

> "…as of this request for information, clinician-facing AI tools that are currently in
> widespread use are more focused on administrative burden reduction and clinical
> decision-support. For example, tools focused on reducing clinician documentation
> burden (e.g. AI scribes), have perhaps been the most widely taken up by clinicians,
> with an estimated 25% penetration among all US physicians. Early system-level
> evaluations demonstrate generally increased productivity among adopters along with
> decreases in perceived documentation burden."

Then CMS solicits comments on, among other things:
- whether "clinical documentation and clinical decision-support tools" being the most
  common AI applications "reflect[s] current practice"
- how AI tools "impacted the resource costs associated with primary care practice"
- how to "develop a comprehensive and consistent approach to payment for
  technology-enabled care"

### The RFI's own footnote 73 — a second primary source (bonus find)

CMS cites, for the "increased productivity" claim, a JAMA Network Open paper whose
**title alone** is your thesis:

> Holmgren AJ, Fenton CL, Thombley R, et al. **Ambient Artificial Intelligence Scribes
> and Physician Financial Productivity.** *JAMA Network Open*. 2026;9(1):e2553233.
> doi:10.1001/jamanetworkopen.2025.53233.

That is a peer-reviewed, named-source empirical study of ambient scribes' effect on
**financial** productivity — pull it next; it is the strongest citable primary source
and it postdates the npj brief.

### The vehicle: MIPS sunset → MVP mandate (verbatim, page 44143)

> "…we are proposing the traditional MIPS reporting option would be sunset and that MVPs
> will be the only reporting option for MIPS beginning with the CY 2029 performance
> period/2031 MIPS payment year. Traditional MIPS would continue to be an available
> reporting option until the CY 2029 performance period/2031 MIPS payment year, when
> sunsetting occurs."

So: traditional MIPS runs through **CY 2028**, MVPs become mandatory in **CY 2029**
(2031 payment year), and the same rule pushes **FHIR-based digital quality measures**
(dQM) across Shared Savings / MIPS (pages ~44100+, see "digital quality measurement"
passages). This is the published-timetable vehicle: ambient-scribe documentation is
being wired into the same measurement apparatus that is being forcibly digitized.

---

## 3. Timeline (the action hook)

| Date | Event |
|---|---|
| 2025-07 | Ambience funding round — "revenue-cycle performance" language |
| 2025-10 | Cigna auto-downcoding of L4–5 E/M goes live |
| 2025-12-24 | npj brief published (Dai, Kvedar, Polsky) |
| 2026-01 | Holmgren et al., *JAMA Netw Open* — ambient scribes & **financial** productivity |
| 2026-07-16 | CMS-1848-P published (91 FR 43842) |
| **2026-09-14** | **CMS comment deadline** (8 days from your note) |
| CY 2028 | last year of traditional MIPS |
| CY 2029 | MVPs mandatory; dQM transition underway |

---

## 4. Next pulls (not yet done)

1. **Holmgren et al., *JAMA Network Open* 2026;9(1):e2553233** — the "financial
   productivity" study. This is the strongest primary source and is currently missing.
2. The **Abridge / Riverside** and **Microsoft / Northwestern** white papers (refs 5 & 6
   in the npj brief) — already cited in the brief but worth holding as primary copies.
3. The **Texas Oncology 2024** study (ref 7).
4. The **Cigna downcoding** policy language (ref 10) — confirm the October 2025 effective
   date against a primary Cigna/announcement source, not just the brief.

*Note: the Nixon Law Group summary that surfaced in search returned a network-block error
when fetched directly — not relied upon; everything above comes from the Federal Register
full text and the npj article itself.*
