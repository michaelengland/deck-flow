---
name: narrative
description: "This skill should be used when the user asks to brainstorm a presentation, develop a story for slides, plan a talk, or invoke /deck-flow:narrative. Use BEFORE creating any slides. Explores audience, purpose, and story arc through sequential questioning. Produces a validated narrative document."
---

# Narrative

Develop the story and message before thinking about slides. This skill converts rough presentation ideas into validated narrative documents through collaborative dialogue.

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

Throughout the narrative process, track all source materials the user provides or references. These are critical for the downstream craft and present phases.

For every claim, data point, or key argument in the narrative, note the source:
- Documents, reports, or files the user shared
- URLs, articles, or external references mentioned
- Internal data, metrics, or research cited
- Quotes or attributions

Include these in the narrative document so they carry forward into slide creation.

### 6. Document the Narrative

Save the validated narrative to `decks/<name>/narrative.md` (create the deck folder if it doesn't exist).

**Document format:**

```markdown
# [Presentation Title] - Narrative

> **Next step:** Use **/deck-flow:craft** to structure this narrative into a content outline.

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
- [Source 1]: [description — e.g., "Q3 Revenue Report, pg 12"]
- [Source 2]: [description — e.g., "Customer survey results, June 2025"]
- [Source 3]: [description]

## Notes
[Any constraints, open questions, or considerations for downstream phases]
```

## Handoff

After narrative approval, offer next steps:

> "Your narrative is ready. Next step:
> - Use **/deck-flow:craft** to structure this into a content outline
> - Or refine this narrative further"

## Principles

- **One question at a time** - Don't overwhelm
- **Multiple-choice when possible** - Reduces cognitive load
- **Ruthless focus** - Cut anything that doesn't serve the key message (YAGNI for presentations)
- **Validate incrementally** - Check understanding after each section
- **Stay flexible** - Revisit earlier decisions if new information emerges
- **Cite sources** - Every claim should trace back to a source; this ensures credibility and makes downstream slide creation easier
