# Annotation guide — gold requirements

Version: 0.1 (2026-11-11)
Status: first pass; revise after annotating 10 items.

This guide defines what counts as a gold requirement, how to encode it, and
how to resolve the ambiguities that come up in Spanish grant documents.

The goal is not to produce "correct" annotations in an absolute sense — it's
to produce **consistent** ones, so that when a model's output is compared to
the gold set, the comparison means something.

---

## 1. What counts as a requirement

A **requirement** is a rule stated in the document that constrains one of:

- **Eligibility** — who can apply, who cannot.
- **Deadline** — when to apply, when the result is published, when to
  justify, etc.
- **Amount** — the size of the grant, the cap, the co-funding ratio.
- **Expenditure** — what the money can and cannot be spent on.
- **Documentation** — what must be submitted with the application.
- **Procedure** — how the application is submitted (in person, online,
  through a specific registry).
- **Exceptions** — explicit carve-outs or special cases ("no obstante",
  "excepto", "salvo").

**Not** a requirement:

- Section headings, title pages, table of contents entries.
- Legal citations to the bases reguladoras without stating a rule.
- Boilerplate ("la presente resolución...", "se publicará en el BOE...").
- Definitions of terms (record these in `notes` if they affect how a
  requirement is read, but don't make them a `Requirement`).
- Cross-references to another document that you don't have.

**The test:** could a computer, given only this requirement and an applicant
profile, make a yes/no/unknown judgement? If not, it may be too vague to
encode — but if it's the document's actual rule, still record it with
`status: unknown` and a note.

---

## 2. Granularity: one rule per Requirement

Split compound rules. "Ser mayor de 18 años y estar empadronado en la
Comunitat Valenciana" is **two** requirements, not one. Each has its own
subject, comparator, and value, and each can fail independently.

Exception: when a rule is genuinely atomic ("haber cursado estudios
postobligatorios"), keep it as one.

If the document repeats the same rule in two places (call body + annex), record
it **once**, with the more precise span. Note the duplicate location in
`notes`.

Conditional rules ("si X, entonces Y"):

- If X is itself a requirement, record it separately.
- Record Y as its own `Requirement`, with `applicability` set to the
  condition in free text.
- Do not encode the implication as a single requirement — it isn't one.

---

## 3. Fields

| Field | Rule |
|---|---|
| `requirement_id` | `T1-<n>-<short>` where `<n>` is the document's page number where the requirement appears, and `<short>` is a slug like `deadline`, `income_cap`, `docs_submit`. Must be unique per document. |
| `type` | `boolean` (yes/no), `numeric` (a number with a comparator), `date` (a date), `membership` (an element of a defined set). |
| `subject` | Lowercase, snake_case, stable across documents. Examples: `applicant_age`, `applicant_residence`, `application_deadline`, `max_grant_amount`, `eligible_expenditure`. **Invent subjects deliberately** — if you invent a new one, list it in §7 below. |
| `comparator` | One of: `>=`, `<=`, `==`, `!=`, `in`, `not_in`, `between`, `before`, `after`. `null` for `boolean` and `membership` unless meaningful. |
| `value` | The comparison value. Use the document's own units (euros, years, days). For dates, ISO `YYYY-MM-DD`. For membership, a list. Never write "N/A" — use `null`. |
| `applicability` | Free-text condition, e.g. `"if applicant is a legal entity"`. `null` if unconditional. |
| `jurisdiction` | The issuing jurisdiction's ISO 3166-2 code, e.g. `ES` for state, `ES-VC` for Comunitat Valenciana, `ES-M` for Madrid. |
| `effective_from` | Earliest date the rule applies. `null` if not stated (see §5). |
| `effective_to` | Latest date the rule applies, for deadlines. `null` if no deadline stated. |
| `evidence` | See §4. Required. |
| `exceptions` | Free-text list of explicit exceptions stated in the document. Empty list if none. |
| `status` | `"unknown"` for all gold annotations. Status is what the *evaluator* sets later; in the gold set it records "the rule exists", not "someone meets it". |

---

## 4. Evidence spans

Every `Requirement` must have an `Evidence` whose span, when sliced from the
extracted text (`text[span_start:span_end]`), reproduces the source verbatim.

Rules for choosing the span:

- **Tight:** the smallest span that still contains the rule. Start at the
  subject ("Los solicitantes...") and end at the value ("...18 años").
- **One sentence, if possible.** If the rule spans two sentences because the
  first is a condition, include both.
- **Never include the article heading.** `"Artículo 5. Requisitos. Ser mayor
  de 18 años."` — the span is `"Ser mayor de 18 años."`, not the whole line.
- **Tables:** if the rule lives in a table cell, the span is the cell text.
  Note in `notes` that it came from a table — `pypdf` extraction of tables is
  fragile and the span may not survive a change in extractor.
- **Page breaks:** if the rule sentence continues on the next page, include
  the whole sentence even if it means spanning a page boundary. Record the
  page number of where it *starts*.
- **If `text[span_start:span_end]` doesn't match exactly,** the span is wrong.
  Don't approximate.

---

## 5. Dates without explicit values

- **"Sin plazo de solicitud"** (BDNS status): `effective_from` and
  `effective_to` are both `null`. Note in `notes`: `"BDNS: sin plazo de
  solicitud"`.
- **Deadline stated relative to publication** ("20 días hábiles desde la
  publicación"): set `effective_to: null`, put the relative rule in `value`
  and `notes`. Do not compute a date unless the publication date is also
  in the document.
- **Open-ended** ("hasta agotar presupuesto"): `effective_to: null`,
  `notes: "until budget exhausted"`.
- **Amendments:** if an amendment changes the deadline, record **both**:
  the original requirement with the original span, and a second
  `Requirement` with `requirement_id` suffixed `-amend`, its own span in
  the amendment, and `notes` explaining the relationship. Do not silently
  replace the original — the point of temporal consistency is that both
  exist.

---

## 6. Negative and ambiguous examples

In each document's gold file, include **at least one**:

- **Negative example:** a piece of text that *looks* like a requirement but
  isn't. Encode it with `status: "unknown"` and `notes: "NEGATIVE: not a
  requirement because ..."`. This tests whether the model over-extracts.
- **Ambiguous case:** a rule that could reasonably be read two ways. Pick
  one reading, record why in `notes`, and note the alternative. This tests
  whether the model hallucinates a confident answer where the document is
  genuinely unclear.

---

## 7. Vocabularies

### Subjects used so far

*(Add to this list as you annotate. The goal is to keep `subject` values
stable — a model evaluated on `applicant_age` should never encounter
`applicant_years_old` in the gold set.)*

- `application_deadline`
- `applicant_age`
- `applicant_residence`
- `applicant_income`
- `applicant_study_level`
- `max_grant_amount`
- `eligible_expenditure`
- `required_documents`

### Comparators

`>=`, `<=`, `==`, `!=`, `in`, `not_in`, `between`, `before`, `after`,
`null`.

### Types

`boolean`, `numeric`, `date`, `membership`.

---

## 8. Review checklist (per document)

Before marking a gold file done:

- [ ] Every `Requirement` validates against `schema/requirement.py`.
- [ ] For every `Requirement`, `text[span_start:span_end]` reproduces the
      intended quote (slice and check).
- [ ] `requirement_id`s are unique within the document.
- [ ] At least one negative example.
- [ ] At least one ambiguous case, or a note saying none was found.
- [ ] All `subject` values appear in §7.
- [ ] Document is recorded in `data/splits/split.json` as train/dev or test.

---

## 9. Open questions (to resolve after first 10 annotations)

- Is `requirement_id` too rigid? Page number changes if the extractor changes.
- Do we need a `derived_from` field for requirements that restate a rule
  from the bases reguladoras?
- Should `subject` be a controlled vocabulary enforced in the schema, or
  free text with a list here?
- How do we handle the "both languages" problem: when a Valencian and
  Castellano version of the same sentence exist, which span do we record?
  (Current answer: the Castellano one, since that's the version the
  evaluation corpus will primarily be in.)

---

## Changelog

- 0.1 (2026-11-11): initial version, before first annotations. Decisions in
  §2, §4, §5 are provisional and likely to change.
