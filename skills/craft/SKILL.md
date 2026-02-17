---
name: craft
description: "Use AFTER /deck-flow:narrative to plan specific slides. Translates narrative into slide-by-slide outline with layout recommendations. Invoke with /deck-flow:craft when user has an approved narrative and wants to plan slides."
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

**For detailed layout guidance**, read `references/slide-patterns.md` in this plugin.

**Common layouts:** Title slide, Section header, Single message, Bullet list, Two-column, Full-bleed image, Image + text, Single chart, Big number, Quote, Timeline, Q&A.

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

## Visual Notes
- **Color palette**: [if specified]
- **Imagery style**: [photos, icons, illustrations]
- **Brand requirements**: [if any]
```

## Handoff

After plan approval, offer next steps:

> "Your deck plan is ready. Next steps:
> - Use **/deck-flow:present** to generate the actual PowerPoint
> - Or use the **pptx skill** directly with this plan
> - Or refine specific slides further"

## Principles

- **One idea per slide** - If you need "and", consider splitting
- **Headlines not titles** - Slide titles should state the takeaway, not the topic
- **Visual hierarchy** - Most important thing should be biggest/boldest
- **Consistent layouts** - Don't switch layouts randomly
- **Speaker notes are essential** - The slide is a visual aid, not a script
