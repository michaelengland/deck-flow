---
name: craft
description: "This skill should be used when the user asks to plan a presentation structure, create a content outline, organize sections for a deck, or invoke /deck-flow:craft. Use AFTER /deck-flow:narrative. Translates narrative into a structured content outline with sections, key messages, and flow."
---

# Craft

Translate a validated narrative into a structured content outline. This skill organizes the story into logical sections with key messages, supporting content, and flow — without locking in specific slide counts or layouts (those are decided during the present phase based on visual design research).

## Prerequisites

Before using this skill, ensure:
- A narrative document exists (from **/deck-flow:narrative**), OR
- User provides clear presentation goals, audience, and key message

If no narrative exists, suggest: "Would you like to use **/deck-flow:narrative** first to develop your story?"

## Process

### 1. Review the Narrative

Read the narrative document or user-provided context. Identify:
- Total key points to cover
- Logical groupings
- Required evidence/visuals
- Time constraints

### 2. Estimate Duration and Section Count

Estimate total sections based on:

| Presentation Length | Suggested Sections | Approach |
|---------------------|-------------------|----------|
| 5 minutes | 3-4 sections | Tight, focused |
| 10 minutes | 4-6 sections | Room for evidence |
| 20 minutes | 6-10 sections | Can develop arguments |
| 30+ minutes | 8-12 sections | Consider part groupings |

Present recommendation and get user agreement before detailing sections.

### 3. Create Content Outline

For each section, specify:

```markdown
### Section N: [Title — states the takeaway]
**Key message**: [The one thing the audience should take from this section]
**Content**:
- [Supporting point or evidence]
- [Data, example, or proof point]
**Emphasis**: [high / medium / low — how much visual weight this deserves]
**Speaker notes**: [What to say, not what's on screen]
**Transition**: [How this connects to next section]
```

**Emphasis levels guide the present phase:**
- **high** — This section deserves maximum visual impact (could become multiple slides, large typography, dramatic layout)
- **medium** — Standard treatment, clear and clean
- **low** — Brief, transitional, or supporting (could be a simple divider or combined with adjacent content)

### 4. Validate Incrementally

Present the outline in batches. After each batch:
> "Here are sections 1-4. Does this flow work? Any adjustments?"

### 5. Document the Outline

Save the validated outline to: `docs/plans/YYYY-MM-DD-<topic>-content-outline.md`

**Document format:**

```markdown
# [Presentation Title] - Content Outline

> **Next step:** Use **/deck-flow:design** to plan slides and visual direction.

## Overview
- **Estimated duration**: [X minutes]
- **Total sections**: [N]
- **Narrative doc**: [link to narrative if exists]

## Content Outline

### Section 1: [Opening — Title / Hook]
**Key message**: [First impression, context setting]
**Content**:
- [Title, subtitle, presenter info]
**Emphasis**: high
**Speaker notes**: [Introduction context]

### Section 2: [Title — states the takeaway]
**Key message**: [takeaway]
**Content**:
- [supporting details]
**Emphasis**: [high / medium / low]
**Speaker notes**: [talking points]
**Transition**: [connection to next]

[... continue for all sections ...]

## Source References
- [Carried forward from narrative document]

## Design Notes
- **Brand requirements**: [if any — logos, fonts, colors the user specified]
- **Constraints**: [any visual preferences or restrictions mentioned during planning]
```

## Handoff

After outline approval, offer next steps:

> "Your content outline is ready. Next step:
> - Use **/deck-flow:design** to plan slides and visual direction
> - Or refine the outline further"

## Content Principles

Apply these to every section in the outline. If a section violates any of these, restructure it before finalizing.

- **One key message per section** — If a section has two takeaways, split it
- **Headlines state the takeaway** — "Revenue grew 40%" not "Q3 Revenue Data". The headline IS the point.
- **Keep supporting content focused** — 2-3 supporting points max per section. More than that means the section should be split.
- **Prefer evidence over assertion** — Numbers, examples, and comparisons are stronger than bullet-point claims
- **Speaker notes carry the detail** — Dense explanation belongs in notes, not on screen
- **Vary emphasis** — Not every section is high emphasis. Alternating intensity creates rhythm.

### Handling Dense Content

When a narrative point requires complex information:

1. **Split into sub-sections** — Break into 2-3 sections that build on each other
2. **Lead with the insight** — First section states the conclusion, following sections show the evidence
3. **Use the appendix pattern** — Main outline has the simple version, mark detailed backup as appendix material
