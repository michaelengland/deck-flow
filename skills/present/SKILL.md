---
name: present
description: "Use AFTER /deck-flow:craft to generate the actual PowerPoint. Executes the deck plan using the pptx skill. Invoke with /deck-flow:present when user has an approved deck plan and wants to create the .pptx file."
---

# Present

Execute a deck plan to generate the actual PowerPoint presentation.

## Prerequisites

- A deck plan exists (from **/deck-flow:craft**), OR user provides a clear slide-by-slide outline
- The **pptx skill** must be available (it's bundled with Cowork/Claude Code)

If no plan exists: "Would you like to use **/deck-flow:craft** first to plan your slides?"

## Process

### 1. Load the Deck Plan

Read the deck plan document. Extract:
- Total slide count
- Each slide's layout, content, and speaker notes
- Visual requirements (colors, imagery style, brand)

### 2. Invoke the PPTX Skill

**MANDATORY**: Before generating any slides, read the pptx skill's SKILL.md completely.

**How to access the pptx skill:**
- In Cowork: The skill is at `/mnt/.skills/skills/pptx/SKILL.md`
- Read the full file — it contains critical guidance on html2pptx workflow, color palettes, and validation

If the pptx skill is not available, inform the user:
> "The pptx skill is required to generate slides but isn't available in this environment. You can use the deck plan with another tool, or ask to enable the pptx skill."

### 3. Design Decisions

Before generating, state your design approach:

> "Based on your deck plan, I'll create this presentation with:
> - **Color palette**: [chosen palette with hex codes]
> - **Typography**: [font choices — use web-safe fonts only]
> - **Visual style**: [e.g., minimal, bold, corporate]
>
> Does this direction work?"

Get approval before writing any code.

### 4. Generate Slides

Follow the pptx skill's workflow (summarized here, but always defer to the skill's full instructions):

1. Create HTML files for each slide (720pt × 405pt for 16:9)
2. Create JavaScript file using html2pptx.js library
3. Generate the presentation
4. Create thumbnail grid for visual validation

### 5. Visual Validation

Review the thumbnail grid. Check for:
- Text cutoff or overflow
- Positioning issues
- Color contrast problems
- Layout consistency

If issues found, fix and regenerate. Repeat until all slides pass.

### 6. Deliver

Provide the final .pptx file with a summary:

> "Your presentation is ready:
> - **File**: [filename.pptx]
> - **Slides**: [N] slides
>
> Any adjustments needed?"

## Layout Mapping

| Deck Plan Layout | Implementation |
|------------------|----------------|
| Title slide | Full-width centered title, subtitle below |
| Section header | Bold text, colored background block |
| Single message | Large centered text |
| Bullet list | Left-aligned text with spacing |
| Two-column | 50/50 or 40/60 split |
| Full-bleed image | Image covers slide, text overlay |
| Single chart | Chart centered, headline above |
| Big number | Oversized number with context label |
| Quote | Centered italic text, attribution below |

## Principles

- **Follow the plan** — The deck plan is the spec; don't improvise without approval
- **Validate visually** — Always review thumbnails before delivery
- **Defer to pptx skill** — It has detailed, tested workflows for slide generation
