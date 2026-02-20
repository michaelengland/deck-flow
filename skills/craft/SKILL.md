---
name: craft
description: "This skill should be used when the user asks to plan slides, create a deck outline, design slide layouts, or invoke /deck-flow:craft. Use AFTER /deck-flow:narrative. Translates narrative into slide-by-slide outline with layout recommendations."
---

# Craft

Translate a validated narrative into a concrete slide-by-slide plan. This skill creates a detailed deck outline that can be executed by the pptx skill.

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
- Time/slide constraints

### 2. Propose Slide Count

Estimate total slides based on:

| Presentation Length | Suggested Slides | Pace |
|---------------------|------------------|------|
| 5 minutes | 5-7 slides | ~1 min/slide |
| 10 minutes | 8-12 slides | ~1 min/slide |
| 20 minutes | 15-20 slides | ~1 min/slide |
| 30+ minutes | 20-30 slides | Consider sections |

Present recommendation and get user agreement before detailing slides.

### 3. Create Slide-by-Slide Plan

For each slide, specify:

```markdown
### Slide N: [Title]
**Layout**: [layout type - see options below]
**Content**:
- [Headline or key point]
- [Supporting details]
- [Visual element if any]
**Speaker notes**: [What to say, not what's on the slide]
**Transition**: [How this connects to next slide]
```

### Layout Options

**For detailed layout guidance**, read `${CLAUDE_PLUGIN_ROOT}/references/slide-patterns.md`.

**Common layouts:** Title slide, Section header, Single message, Bullet list, Two-column, Three-column, Full-bleed image, Image + text, Image grid, Single chart, Chart + interpretation, Comparison table, Big number, Quote, Timeline, Steps, Cycle, Summary, Call to action, Q&A. See reference for full catalog with usage guidance.

### 4. Validate Incrementally

Present the plan in batches (5-7 slides at a time). After each batch:
> "Here are slides 1-6. Does this flow work? Any adjustments?"

### 5. Document the Plan

Save the validated plan to: `docs/plans/YYYY-MM-DD-<topic>-deck-plan.md`

**Document format:**

```markdown
# [Presentation Title] - Deck Plan

## Overview
- **Total slides**: [N]
- **Estimated duration**: [X minutes]
- **Narrative doc**: [link to narrative if exists]

## Slide Plan

### Slide 1: [Title]
**Layout**: Title slide
**Content**:
- Main title
- Subtitle
- Presenter / Date
**Speaker notes**: [Introduction context]

### Slide 2: [Title]
**Layout**: [type]
**Content**:
- [details]
**Speaker notes**: [talking points]
**Transition**: [connection to next]

[... continue for all slides ...]

## Design Notes
- **Brand requirements**: [if any — logos, fonts, colors the user specified]
- **Constraints**: [any visual preferences or restrictions mentioned during planning]
```

## Handoff

After plan approval, offer next steps:

> "Your deck plan is ready. Next step:
> - Use **/deck-flow:present** to generate the actual PowerPoint
> - Or refine specific slides further"

## Content Constraints

Apply these to every slide in the plan. If a slide violates any of these, restructure it before finalizing.

- **One idea per slide** — If you need "and", split into two slides
- **30 words max per slide** — If content exceeds this, move detail to speaker notes or split the slide
- **Headlines state the takeaway** — "Revenue grew 40%" not "Q3 Revenue Data". The headline IS the point.
- **Vary layout rhythm** — Never use the same layout more than 3 slides in a row. Alternate between high-density (data, bullets) and low-density (single message, image) slides.
- **Prefer visuals over text** — If a point can be a number, chart, image, or comparison instead of a bullet list, use that instead
- **Speaker notes carry the detail** — The slide is a visual aid, not a script. Dense explanation belongs in notes, not on the slide.

### Handling Dense Content

When a narrative point requires complex information:

1. **Split progressively** — Break into 3-4 slides that build on each other
2. **Lead with the insight** — First slide states the conclusion, following slides show the evidence
3. **Use the appendix pattern** — Simple version on the slide, detail in a marked appendix section at the end
