# Caveats and Discrepancies — YipitData Signal Validation

## Discrepancies between challenge-doc formats

The challenge brief is provided in three formats inside `challange_docs/`:

| File | Type | Content hash (Markdown-extracted text) |
|---|---|---|
| `take_home_exam_candidate.md`        | Markdown   | canonical |
| `take_home_exam_candidate.docx`      | Word 2007+ | byte-identical to `take_home_exam_candidate(1).docx`; text content matches the `.md` modulo Markdown formatting |
| `take_home_exam_candidate(1).docx`   | Word 2007+ | byte-identical to `take_home_exam_candidate.docx` |
| `take_home_exam_candidate.pdf`       | PDF 1.7    | text content matches the `.md` modulo Markdown formatting |

**Verified**: a line-by-line diff of the `.docx` plain-text against the `.md` (after stripping
the line-number prefixes the `.md` carries) shows only formatting differences (heading hashes,
backticks for code spans, bullet markers, blockquote `>`). The two `.docx` files have identical
SHA-256 hashes. The PDF text-extraction confirms the same paragraphs. **There are no content
discrepancies between the three formats. The duplicate `.docx` is just a copy.**

The lockfile `challange_docs/~$ke_home_exam_candidate.docx` is a Word editing-session lock
file (created by Microsoft Word when a document is opened) and contains no challenge content.
It should be ignored. (Optional follow-up: add it to `.gitignore`.)

## Open caveats from the brief itself

These are points where the brief leaves the candidate to make a defensible call. They are
listed here so the Director and Reviewer can keep them visible.

1. **Choice of YoY vs. levels.** The brief's first-pass code uses YoY growth. The team will
   stay with YoY for the headline because (a) it is what consumers of the memo will compare
   across firms, and (b) it removes most seasonality and trend before any modelling. Caveat:
   YoY is unstable when the year-ago denominator is small (e.g., the 2021 base after 2020).
2. **Calendar quarter vs. Walmart fiscal quarter.** Walmart's fiscal year ends late January.
   Aggregating FRED months on a *calendar*-quarter basis introduces a one-month misalignment.
   The methodology mandates Walmart-fiscal alignment for this reason.
3. **FRED publication lag.** FRED RSXFS is released approximately 6 weeks after the reference
   month ends. The methodology codifies the publication-lag rule; the actual lag in days will
   be checked against the FRED release calendar where it matters for the most recent quarter.
4. **Walmart 10-Q filing lag.** Walmart files its 10-Q ~30–45 days after the fiscal-quarter
   end. Mid-Q4 falls comfortably after the fiscal-Q3 file date for most years; the rule still
   requires per-quarter checking.
5. **2020 disruption window.** The brief says "do not blindly fit a line through 2020." We
   define the disruption window as `2020Q1`–`2021Q1` (5 quarters) for the headline-cut
   reporting. This is a defensible default; the Reviewer may push back and the Director will
   document any change here.
6. **"Baseline" definition.** The brief shows two equivalent baseline formulations
   (`Q(t-4)` plain vs. plus-average-growth). The methodology adopts SN-A by default and
   reports SN-B as a robustness check.

## Discrepancies between the brief and the mission directive

These are the **non-negotiable overrides** the Director enforces.

| Brief permits | Directive forbids | Resolution |
|---|---|---|
| "If you would rather pull fresher data ... walks you through the free APIs" | No APIs of any kind | Use only the local CSVs |
| "Use any LLM coding assistant" | Specific 3-tier persona model with named LLM profiles | Follow `docs/team/roles.md` and `docs/llm-roster.md` |
| Implicit: candidate works solo | 3-persona Director / Lead Quant / Reviewer team | Follow `docs/team/roles.md` |

## Open questions logged for HITL

(none at scaffolding time; populated as Tasks progress)
