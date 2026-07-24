# Stop prompting. Start writing procedures.

### The full workings behind Case Study 004: how twelve plain-English skills replaced a days-long compliance run, what one costs to build, and why "stop and ask" is the line that matters most.

<!--
NOT PUBLISHED — metadata for posting.
Read time:     8 min
Word count:    ~1,450
Suggested tags: practical AI, agentic workflows, AI skills, business analysis, AI governance
Site article:  https://ai-sustained.com/case-studies/teach-it-once/
Substack slug: stop-prompting-start-writing-procedures
-->

There is a category of AI user who gets exceptional output on Monday and mediocre output on Thursday, and the difference is not the model. It's that Monday's context died with Monday's chat. Every session starts from a blank context window, and whatever rules, exceptions and formatting standards you loaded into the last one are gone.

The fix is not a better prompt. It's not putting the rules in a prompt at all. This is the long version of how I moved my repeat work into reusable skills: what a skill actually is under the hood, what one costs to build, the compliance job that went from days to minutes, and the run where the guardrail earned its keep.

## What a skill actually is

Strip the branding and a skill is a Markdown file. It contains a description of a job, the rules that govern it, the exceptions to those rules, the order of operations, references to any assets it needs (templates, connection details, example files), and explicit stop conditions. The model loads it when the job comes up, either because you invoked it by name or because your request matched its description.

That's it. No code in the load-bearing sense. Some of mine carry a helper script; most are pure written instruction.

Two properties fall out of this that a chat prompt never gives you:

**Determinism of intent.** The rules are versioned text in a file, not a memory of what you typed last time. When the output is wrong, you don't re-prompt harder, you edit the procedure. Corrections compound instead of evaporating.

**Auditability.** For regulated work this is the quiet superpower. If anyone asks "what rules does the AI apply to this document?", the answer is a file you can print, not a vibe. Your compliance rules become documentation as a side effect.

Vendor mapping, for completeness: this pattern is custom GPTs in ChatGPT, Gems in Gemini, and skills in Claude, which is where I build. The portable asset is the written procedure. If you change vendor, you take the text with you.

> When the output is wrong, you don't re-prompt harder. You edit the procedure.

## The build loop, honestly costed

Every skill in my library was built the same way, and the loop matters more than any individual trick:

1. **Write the job description as if for a competent new starter.** Not for a machine, for a person. If a temp with domain knowledge could follow it, the model can. If a temp would ask a clarifying question, the model needs that answer written down.
2. **Attach a real artefact.** A real source file with the real mess in it. Skills built against idealised descriptions fail on contact with actual data; the edge cases are the job.
3. **Run it. Mark the errors. Fold every correction back into the instructions.** This is the step people skip and then blame the model. Two or three iterations is typical.
4. **Add the stop conditions.** The list of situations where the skill must halt and ask a human rather than proceed. More on why below.

Elapsed time per skill: 30 to 60 minutes, measured across the twelve I've built. That is the entire capital cost. There is no deployment, no environment, no release process. The marginal cost of the thirteenth skill is another spare hour.

The eval discipline is informal but real: each skill gets re-run against known-good historical outputs before I trust it. Where a skill touches warehouse data, it reads from governed marts, so the master data it enriches against is the same data the business reports on. Grounding against your single source of truth is what separates "AI guessed the product attributes" from "AI looked them up".

## The worked example: days to minutes

The flagship is a safety-critical compliance document produced on a rolling cycle. Keeping it deliberately generic: the source system exports a report, and before publication that report needs a specific class of false positives corrected against a house rule set, a re-pagination pass so no logical section splits across a page boundary, a date stamp in a fixed position on every page, and a branded cover sheet with the same date written into it.

Done by hand, that run took several days. Not because any single step is hard, but because the checking is dense, the rules have exceptions, the exceptions have exceptions, and the person doing it is also doing a full-time job. Under time pressure, applied from memory, an eleven-rule procedure gets ten rules on a bad day. On this document, a bad day is not acceptable.

The skill encodes the full rule set, including the exception logic that made the job slow. A run now takes about five minutes: upload the export, invoke the skill, review what it flags, sign off. The days-to-minutes arithmetic is not the model being fast; it's the checking being moved from human working memory into written procedure, where it executes completely every time.

Same library, different shape: a chain of skills that takes a working spreadsheet, flattens it to row-per-item format, enriches every line against product master data in the warehouse via its key, generates the import file for a downstream system in that system's template, and produces the branded customer-facing output from the same source. Four tools' worth of manual rekeying, gone. The chain matters because the enrichment step means the downstream files inherit warehouse truth rather than whatever was typed into the spreadsheet.

## The run where it argued back

One cycle, I fed the compliance skill a source document and told it which of two rule modes to apply. The document's own labelling said otherwise, on an indicator I'd missed. The failure mode writes itself: automation applies the wrong rule set, output looks immaculate, three line items are wrong in a document where wrong has consequences.

It didn't happen, because the skill contains a stop condition: *if the source contradicts the operator's instruction, halt, report, change nothing.* The skill flagged the conflict, named the three exact line items that would differ under the other mode, and asked. I checked, confirmed the right mode, re-ran. Total cost of the guardrail: one message and thirty seconds.

Two things about that moment are worth being precise about.

First, **the guardrail was authored**. The model didn't spontaneously develop caution; I wrote the sentence that told it when to stop. Agentic safety in this pattern is a writing task. If you didn't write the stop condition, you don't have one, and the fluency of the output will hide that from you until it matters.

Second, **the human stayed accountable**. The skill's job ends at the flag; the decision was mine, on the record. That division of labour, machine carries the checklist, human owns the judgement, is the honest answer to "can you trust AI with regulated work?" You don't trust it. You instrument it, and you keep the sign-off.

## The caveats

Where this argument is weakest, so you can weigh it:

**The numbers are one practitioner's.** Days-to-minutes is a real measured delta on my document, my rule set, my mess. Your job may be less rule-dense, in which case your delta will be smaller and a skill may be overkill. The pattern pays where rules are many, stable and boring.

**Skills rot.** When the house rules change, someone must edit the file. An out-of-date skill fails more dangerously than no skill, because its output still looks authoritative. Treat the library like documentation: owned, dated, reviewed. (My covers carry the update date for exactly this reason.)

**The stop conditions are only as good as your imagination.** My skill caught the mismatch because I'd anticipated that class of conflict. The failure I haven't imagined is not covered. Human review of the output remains mandatory; the skill narrows the review, it does not replace it.

**Twelve skills is a library, not a platform.** This scales to a person or a small team beautifully. Scaling it to an enterprise raises the questions you'd expect: who owns skills, who approves changes, what's the test process. Those are governance problems, and they're the same governance problems as any SOP estate, which is rather the point.

## What this means if you're building

Start with an inventory, not a tool. List the jobs you have explained to an AI more than twice. Rank them by rule density times frequency times cost-of-error. The top of that list is your first skill, and the rules you keep re-typing are its first draft; you have already written most of it, one disposable prompt at a time.

Then, before you run it in anger, write the stop conditions. Ask yourself what the worst plausible silent failure looks like, and write the sentence that makes it loud instead.

The prompt was never the asset. The procedure is.

---

*The shorter version of this piece is on the site: [Prompts forget. Skills remember.](https://ai-sustained.com/case-studies/teach-it-once/)*
