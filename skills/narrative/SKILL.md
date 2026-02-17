---
name: narrative
description: "Use BEFORE creating any presentation. Explores audience, purpose, and story arc through sequential questioning. Produces a validated narrative document. Invoke with /deck-flow:narrative or when user wants to brainstorm a presentation."
---

# Narrative

Develop the story and message before thinking about slides. This skill converts rough presentation ideas into validated narrative documents through collaborative dialogue.

## Process

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
4. **Constraints**: Time limit? Slide count? Existing template or brand guidelines?
5. **Content**: What evidence, data, or examples support the message?

Stop questioning when you have enough clarity to propose a narrative arc.

### 3. Explore Story Frameworks

Present 2-3 narrative frameworks that fit the content. Lead with your recommendation.

**For detailed framework guidance**, read `references/narrative-frameworks.md` in this plugin.

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

### 5. Document the Narrative

Save the validated narrative to: `docs/plans/YYYY-MM-DD-<topic>-narrative.md`

**Document format:**

```markdown
# [Presentation Title] - Narrative

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

## Notes
[Any constraints, open questions, or considerations for slide design]
```

## Handoff

After narrative approval, offer next steps:

> "Your narrative is ready. Next steps:
> - Use **/deck-flow:craft** to plan specific slides and layouts
> - Or refine this narrative further"

## Principles

- **One question at a time** - Don't overwhelm
- **Multiple-choice when possible** - Reduces cognitive load
- **Ruthless focus** - Cut anything that doesn't serve the key message (YAGNI for presentations)
- **Validate incrementally** - Check understanding after each section
- **Stay flexible** - Revisit earlier decisions if new information emerges
