---
name: narrative
description: "This skill should be used when the user asks to brainstorm a presentation, develop a story for slides, plan a talk, or invoke /deckwright:narrative. Use BEFORE creating any slides. Explores audience, purpose, and story arc through sequential questioning. Produces a validated narrative document."
---

# Narrative

Develop the story and message before thinking about slides. This skill converts rough presentation ideas into validated narrative documents through collaborative dialogue.

## Prerequisites

- User has a presentation idea, topic, or goal, OR
- A PptxGenJS generation script exists from a previous import or creation (edit mode)

## Process

### Edit Mode Check

Before starting, check: does a deck folder in `decks/` contain a PptxGenJS generation script (a `.js` file containing `require("pptxgenjs")`)?

- **If no**: This is a new presentation. Follow the standard process below.
- **If yes**: This is an edit. Read the generation script to understand the current slides, then:
  1. Summarize the narrative you see in the deck — audience, purpose, key message, and story arc as you interpret them from the slide content and speaker notes
  2. Present this to the user as your interpretation:
     > "Based on the current deck, here's the narrative I see:
     > - **Audience**: [inferred]
     > - **Key message**: [inferred]
     > - **Arc**: [slide-by-slide summary of the story flow]
     >
     > What would you like to change about the story?"
  3. Focus questioning only on what the user wants to change — skip settled topics
  4. Produce a narrative document as usual, noting which parts are unchanged vs. reworked

### 1. Understand the Context

Before asking questions, review any existing context:
- User's initial request and goals
- Any documents, data, or materials they've shared
- Prior conversation context

### 2. Sequential Questioning

Ask ONE question at a time. Favor multiple-choice when possible.

**Core questions to explore (adapt based on context):**

1. **Audience**: Who will see this? What do they already know? What do they care about?
2. **Purpose**: What should the audience think, feel, or do after seeing this?
3. **Key message**: If they remember only ONE thing, what should it be?
4. **Constraints**: Time limit? Existing template or brand guidelines?
5. **Content**: What evidence, data, or examples support the message?
6. **Sources**: What source materials, documents, reports, or data back up the claims?

Stop questioning when you have enough clarity to propose a narrative arc.

### 3. Explore Story Frameworks

Present 2-3 narrative frameworks that fit the content. Lead with your recommendation.

**For detailed framework guidance**, read `${CLAUDE_PLUGIN_ROOT}/references/narrative-frameworks.md`.

**Quick reference:**

| Framework | Best for |
|-----------|----------|
| Problem → Solution → Impact | Pitches, proposals |
| Situation → Complication → Resolution | Strategic updates, analysis |
| What → So What → Now What | Data presentations, reports |
| Before → After → Bridge | Transformations, case studies |
| Hook → Build → Payoff | Persuasive, storytelling |

Discuss trade-offs conversationally. Get user agreement before proceeding.

### 4. Present the Narrative

Once the framework is chosen, present the narrative in **200-300 word sections**:

1. **Opening hook** - How will you grab attention in the first 30 seconds?
2. **Core argument** - What's the logical flow of your message?
3. **Supporting evidence** - What proof points back up each claim?
4. **Conclusion & call-to-action** - What do you want them to do next?

After each section, pause for validation:
> "Does this capture what you're going for? Anything to adjust?"

### 5. Track Source References

Throughout the narrative process, actively build a source list. Sources are critical — they carry forward through craft, design, and into the final `.pptx` and `.pdf` as clickable links.

**Push for research.** When the user makes claims without backing data, proactively search for supporting evidence — statistics, studies, reports, benchmarks. Offer what you find:
> "You mentioned adoption is growing fast. I found [specific stat] from [source with URL] — want to use that?"

**Every source must include a URL where possible.** For every claim, data point, or key argument in the narrative:
- URLs to articles, reports, research, or data sources (preferred — these become clickable links in the final output)
- Documents or files the user shared (note the filename and relevant page/section)
- Internal data or metrics (note the system or report they come from)
- Quotes with attribution and source URL

If a claim has no source, flag it:
> "This claim doesn't have a source yet. Should we find one, or mark it as the presenter's own assertion?"

Include all sources in the narrative document so they carry forward into slide creation.

### 6. Document the Narrative

Save the validated narrative to `decks/<name>/narrative.md` (create the deck folder if it doesn't exist).

**Document format:**

```markdown
# [Presentation Title] - Narrative

> **Next step:** Use **/deckwright:craft** to structure this narrative into a content outline.

## Overview
- **Audience**: [who]
- **Purpose**: [what they should think/feel/do]
- **Key message**: [one sentence]
- **Framework**: [chosen framework]

## Narrative Arc

### Opening
[Hook and context-setting]

### Core Argument
[Main points in logical sequence]

### Evidence
[Supporting data, examples, proof points]

### Conclusion
[Summary and call-to-action]

## Source References
- [Short label](https://url) — brief description of what this supports
- [Gartner 2025 Report](https://example.com/report) — market size and growth projections (slides 3-4)
- [Internal Q3 data] — revenue figures, no public URL (presenter's source)

## Notes
[Any constraints, open questions, or considerations for downstream phases]
```

## Handoff

After narrative approval, offer next steps:

> "Your narrative is ready. Next step:
> - Use **/deckwright:craft** to structure this into a content outline
> - Or refine this narrative further"

## Principles

- **One question at a time** - Don't overwhelm
- **Multiple-choice when possible** - Reduces cognitive load
- **Ruthless focus** - Cut anything that doesn't serve the key message (YAGNI for presentations)
- **Validate incrementally** - Check understanding after each section
- **Stay flexible** - Revisit earlier decisions if new information emerges
- **Cite sources with URLs** — Every claim needs a source. Proactively research backing data.
