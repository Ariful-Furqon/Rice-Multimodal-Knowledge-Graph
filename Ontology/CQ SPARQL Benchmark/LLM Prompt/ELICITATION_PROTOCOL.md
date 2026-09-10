# Elicitation Protocol

How the competency questions in this directory were obtained from large
language models, and how to obtain another set the same way.

This document exists because an LLM elicitation is not reproducible in the
sense a script is, and saying so plainly is better than implying otherwise.
What can be reproduced is stated below; what cannot is stated too.

---

## What is and is not reproducible here

**Reproducible.** The prompt. It is one file, frozen, hashed, and provably
unchanged since the day it was written. Anyone can send exactly the same text
to a model of their choice and compare what comes back.

**Reproducible.** The screening. Everything downstream of the six model
outputs — pool construction, the scope gate, the grouping, the questionnaire,
the agreement statistics — is deterministic Python over files in this
repository, and re-running it reproduces every number byte for byte. The human
decisions inside it are recorded as tables, not recomputed, so they can be
inspected and disagreed with.

**Not reproducible.** The model outputs themselves. Commercial chat models are
sampled, they are updated without notice, and the interfaces used here expose
no temperature or seed control. Sending the same prompt tomorrow returns a
different set of competency questions. This is a property of the instrument,
not a defect in the procedure, and no amount of documentation removes it.

The honest response to that last point is to measure it rather than hide it.
That is what Stage 7 does: send the prompt again — as run, four further trials
each for five of the six models — and report how often each canonical
requirement comes back, and whether run-to-run variation differs from
model-to-model variation. See
`../CQ Screening/scripts/stage7_stability.py`.

---

## The frozen prompt

| | |
|---|---|
| Source file | `rice_mmkg_cq_prompt.md` |
| Text actually sent | `rice_mmkg_cq_prompt.payload.txt` |
| SHA-256 of the sent text | `0e3207a14a18dd777a704068a208333c1ac538dd50e3007600c414faddaddd78` |
| Length | 8,364 characters, 134 lines |
| First and only commit | `97d2986`, 2026-09-03 |

The payload file is **generated**, never edited: it is the contents of the
fenced block inside `rice_mmkg_cq_prompt.md`, which is what an operator was
instructed to copy. The surrounding prose in the markdown file is guidance to
the operator and was never sent, so hashing the whole file would hash text the
models never saw. Regenerate and verify with:

```bash
python "../CQ Screening/scripts/stage0a_provenance.py"
```

Hashing normalises CRLF to LF first. This repository is checked out on Windows
with `core.autocrlf=true`, so a fresh clone can rewrite line endings; without
normalisation the digest would depend on which machine did the checkout, which
would make it useless as evidence.

### The placeholders are deliberate

The prompt contains bracketed placeholders — `[E.G., PLANT PATHOLOGY
RESEARCHERS...]`, `[LIST, OR "USE COMMON MAJOR RICE PESTS/DISEASES"]`, and
others — and they were **not** filled in before sending. That is not an
oversight. The prompt's final instruction is:

> If any of the above INPUT fields are left as bracketed placeholders, proceed
> using the stated defaults and clearly mark any assumption you make.

So the unfilled prompt is a complete, self-contained protocol, and every model
recorded its own assumptions in its answer — visible as the "Assumptions"
sections in the Claude Fable 5.1 and GPT-6 Astra outputs. Filling the
placeholders in now would be a **different protocol**, and any run of it would
not be a replication of what produced the current pool. Do not do it. If a
future study wants a more constrained prompt, that is a new prompt file with
its own hash, run as its own round.

### Both rounds received the same bytes

The pool was built in two sittings: five models on or before 2026-09-03, and
GPT-6 Astra on or before 2026-09-08. The claim that the sixth model received
the same prompt as the first five is **verifiable, not asserted** — the prompt
file was committed once and never modified:

```bash
git rev-parse 97d2986:"Ontology/CQ SPARQL Benchmark/LLM Prompt/rice_mmkg_cq_prompt.md"
git rev-parse   HEAD:"Ontology/CQ SPARQL Benchmark/LLM Prompt/rice_mmkg_cq_prompt.md"
# both print 7332baabe6bfc6b6f8354dde2bd09e6977ffea46
```

---

## The run manifest

`runs/run_manifest.csv` has one row per model run. Every output file in this
directory is accounted for by exactly one row, and the digests are checked by
`stage0a_provenance.py`, which exits non-zero if any output has been edited
since it was recorded.

| Column | Meaning |
|---|---|
| `run_id` | stable handle, e.g. `r1-gpt-6-astra` |
| `round` | `1a` five models, `1b` GPT-6 Astra, `2` the stability replication |
| `replicate` | the trial number in the filename; `round` says whether it is a reference run or a replicate |
| `elicited_on` | date the prompt was sent |
| `model_label` | model name as it should appear in the paper |
| `model_version_reported` | the exact version string the interface showed |
| `interface` | `chat-ui`, or the API and endpoint if one was used |
| `operator` | who ran it |
| `prompt_sha256` | digest of the payload, identical for every row by design |
| `prompt_source_commit` | commit the prompt was read from |
| `output_file` | the answer, saved verbatim |
| `output_sha256` | digest of that file when it was recorded |
| `settings` | temperature, seed, system prompt, tools — or `not-recorded` |

### What round 1 does not record

Three facts about the original six runs were never captured and **cannot be
recovered**: the exact date each prompt was sent, the model version string the
interface displayed, and whether any interface-level features (web search,
memory, custom instructions) were active. Those cells read `not-recorded`, and
they must stay that way. Reconstructing them from commit dates would turn a
bound into a fabricated observation; the commit dates are recorded in the
`notes` column instead, where they are what they are — an upper bound on when
the run happened.

Write this limitation into the paper. It is the price of having run the first
round through chat interfaces without a protocol, it is not fixable after the
fact, and a reviewer who notices it before the authors do will trust the rest
of the pipeline less.

---

## Running the prompt again: the replication matrix

**Design: each model repeatedly, so that runs and models can be told apart.**
As actually run on 2026-09-10: trials 2-5 for Claude Opus 5, Claude Fable 5.1,
GPT-5.6 Sol, Gemini Pro 3.1 and Gemini Flash 3.8 — **20 replication runs**.
GPT-6 Astra was not repeated, so `G24` and `G25`, the two groups it founded
alone, have no model in round 2 that had proposed them before; a miss on those
two cannot be told apart from the model's absence.

Several runs per model is what makes the exercise worth the effort. A single
replication round confounds two things — the same model answering differently
twice, and different models answering differently at all. A run × model matrix
separates them, and that separation is the finding. If runs of one model
resemble each other no more than runs of different models, then "which model
you ask" carries no information, and the six-model pool was buying spread that
five runs of one model would have bought just as well. That would not
invalidate the canonical set, but it would change what `n_models` can be
claimed to show.

Fix the design before looking at any output. Deciding how many runs to do after
seeing how the first ones turned out converts a stability estimate into a
selected one.

**Round 1 is not one of the five.** The grouping vocabulary G01–G25 was derived
*from* the round-1 outputs, so round 1 re-proposes 100% of it by construction
and including it would be circular. It stays in the manifest under `round` 1a/1b, and
Stage 7 reads only `round` 2, which excludes it from every rate.

### 1. Fix the conditions

For every run, open a **fresh conversation** with no prior turns. Turn off
anything that makes the context non-standard: custom instructions or
"personalisation", stored memory, project/workspace context, web search or
browsing, file attachments, and any connected tools. Record what you turned off
in `settings`. If the interface will not let you disable something, record that
instead of pretending it was off.

Two things that look like shortcuts and are not:

- **Do not use "regenerate"** on an existing answer. It reuses the conversation
  and, in several interfaces, conditions on the answer it is replacing. Open a
  new conversation each time.
- **Do not ask the model to "do it again" or "give me another set."** That is a
  different prompt, and one that explicitly invites the model to differ from
  what it just wrote.

Record `model_version_reported` for every run — whatever version string the
interface displays. Thirty runs will not be simultaneous, and commercial models
are updated without notice. Where this column reads `not-recorded`,
run-to-run variation and version drift cannot be told apart afterwards, and the
whole measurement is weaker for it. This is the one column that round 1 lost
and that round 2 has no excuse to lose.

### 2. Send the prompt

Paste the entire contents of `rice_mmkg_cq_prompt.payload.txt` as the first and
only message. Do not introduce it, do not add a greeting, do not translate or
reformat it. If a model asks a clarifying question, do not supply new
information — its own instructions tell it to proceed with defaults, so reply
only with `Proceed with the stated defaults.` and record in `notes` that you
did.

### 3. Save the answer verbatim

One file per run in this directory, named `<Model> trial <N> CQ.md`:

```
Claude Opus 5 trial 1 CQ.md      <- round 1, the reference run
Claude Opus 5 trial 2 CQ.md      <- replication
...
Gemini Pro 3.1 trial 5 CQ.md
```

**`trial 1` is the round-1 output**, renamed on 2026-09-10 when the replication
trials arrived — a rename only, each file byte-identical to what was committed
under its old name in `a084b91`. So the trial numbers run 1-5 while the
*replicates* are trials 2-5: trial 1 is the reference the canonical set was
derived from and is excluded from every rate. The manifest encodes that with
`round` (`1a`/`1b` for trial 1, `2` for the rest) and never by shifting the
number, so a row's `replicate` always equals the trial number in its filename.

Filenames must match their round-1 counterpart exactly apart from the trial
number, so every run is comparable file for file. Note GPT-5.6 Sol's files
carry a dash the others do not (`GPT-5.6 Sol - trial 2 CQ.md`); the manifest
names each file explicitly, so that is harmless — but do not "tidy" it, because
`stage0_build_pool.py` maps the exact string.

Save the model's markdown as it came out: do not fix its tables, renumber its
CQs, delete a preamble, or tidy its headings. If an answer was truncated and
continued, save the concatenation and say so in `notes`. Every edit you make to
an output is an edit to the data.

**Do not reformat a table to help the parser.** Fix the parser instead. On
2026-09-10 four trials parsed to zero CQs because the reader required the
second header cell to read exactly `Question` while those trials wrote
`Natural-Language Question` — the prompt's own term. Worse, three further
trials silently lost *every cross-modal row*, the category the prompt weights
most heavily, because their id cells read `CQ-MM-01 (T x I)` and the id pattern
was anchored at the end of the cell. That loss looked exactly like a model
writing fewer CQs. Both patterns were loosened, and re-parsing trial 1 through
them returns the same 213 rows with identical ids and text — check that
invariant whenever the reader changes.

If a run produces something unusable — the model ignored the table format
entirely, or refused — **keep the file and record the run anyway**, with the
problem in `notes`. Silently discarding the runs that went badly is how a
stability rate becomes an overestimate.

### 4. Record the runs

One manifest row per run, with `round` = `2`, `replicate` = the trial number,
`output_file` as the filename relative to this directory (`Claude Opus 5 trial
3 CQ.md`), and `prompt_sha256` / `output_sha256` left as `pending`. Then:

```bash
python "../CQ Screening/scripts/stage0a_provenance.py" --update
```

This fills the digests and verifies the whole manifest. From then on it detects
any later edit to any output file.

### 5. Adjudicate

```bash
cd "../CQ Screening/scripts"
python stage7_stability.py --checklist    # -> data/cq_stage7_checklist.csv
```

The checklist is 30 runs × 25 groups = 750 rows. Work **one run at a time**:
read that run's output once, then go down its 25 rows and mark `proposed` as
`yes` or `no`. For every `yes`, put the model's own CQ id in `evidence_cq` —
the script rejects an unsupported `yes`, because a claim that cannot be audited
is not a measurement. When a run states a Tier A requirement that no canonical
group covers, add a row to `cq_stage7_new_requirements.csv`.

Why a checklist rather than labelling each CQ: thirty runs produce roughly a
thousand CQs, and labelling each one against 25 groups is both slower and less
consistent than reading one output and ticking the groups it covers. The
checklist is also exactly the quantity being measured. The per-CQ worksheet
remains available for **auditing a sample** of runs against the checklist:

```bash
python stage7_stability.py --worksheet    # -> data/cq_stage7_worksheet.csv
```

It prints three ranked candidate groups per CQ. **They are a reading aid with
no authority.** Stage 2 of this pipeline tried exactly that kind of lexical
similarity as a decision procedure and it failed at every threshold tried —
*which pathogen causes blast* and *which symptoms does blast show* score alike.
The decision is human and is recorded rather than computed, for the same reason
every other decision in this pipeline is.

Decide the boundary cases **before** you start, and write them down. In
particular: does a CQ that covers part of a group count as proposing it, and
does a CQ that merges two groups count for both? Whatever you choose, the
answer has to be the same at run 30 as at run 1, because drift in the rule
looks exactly like instability in the models.

### 6. Report

```bash
python stage7_stability.py                # -> reports/cq_stage7_stability.md
```

It reports the per-group re-proposal rate with 95% Wilson intervals, the
within-model versus between-model Jaccard comparison with a permutation test,
and Spearman's rho between round-1 `n_models` and the re-proposal rate. The
permutation shuffles the *model label across runs*, not across pairs: every run
appears in many pairs, so pairwise Jaccards are not independent and a
pair-level shuffle would produce a p-value that means nothing.

At 30 runs the Wilson intervals are wide — a group seen in 15 of 30 runs is
compatible with a true rate from roughly a third to two thirds. Report the
ordering of the groups, not the individual percentages.

## Things this protocol forbids

**Do not merge round 2 into the pool.** The 213-CQ pool and the 25 canonical
CQs are the adjudicated product of 2026-09-03 and 2026-09-08. Folding a
replication into them would discard that adjudication and would settle
nothing, since a third round would immediately raise the same question about
the merged set. Round 2 is a measurement over the canonical set.

**Do not edit a competency question because a round-2 run did not re-propose
it.** Convergence is the signal being tested against expert ratings, not a
criterion being applied in advance; using it to prune the set makes the Stage 5
hypothesis unfalsifiable. Ten of the 25 canonical CQs come from a single model
and are kept deliberately for exactly this reason. Only the expert ratings
justify changing the set.

**Do not report a stability rate without its caveat.** Round-2 adjudication is
done against a grouping vocabulary that already exists, which makes it easier
for a CQ to land in an existing group than to found a new one. The re-proposal
rate is therefore an upper bound and the count of newly raised requirements a
lower one — the same bias the README records for GPT-6 Astra.

**Do not describe any of this as an automatic result.** The grouping was
drafted by Claude Opus 5, which is also one of the source models, and approved
by M. A. Furqon. It is an LLM-assisted first pass, human-adjudicated.
