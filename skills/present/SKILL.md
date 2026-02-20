---
name: present
description: "This skill should be used when the user asks to generate a PowerPoint, create slides from an outline, build a .pptx file, or invoke /deck-flow:present. Use AFTER /deck-flow:craft. Turns a content outline into a designed and generated .pptx file."
---

# Present

Turn a content outline into a designed, visually excellent PowerPoint presentation. This skill handles all slide-level decisions: how many slides each section becomes, which layouts to use, visual design, and generation.

## Prerequisites

- A content outline exists (from **/deck-flow:craft**), OR user provides a clear structured outline
- The **pptx skill** must be available (see "Installing the PPTX Skill" below)

If no outline exists: "Would you like to use **/deck-flow:craft** first to structure your content?"

## Installing the PPTX Skill

The pptx skill is provided by the **document-skills** plugin from the **anthropic-agent-skills** marketplace. If it is not already installed:

1. Install the marketplace plugin registry:
   ```
   claude plugin add anthropic/agent-skills
   ```
2. Install the document-skills plugin (which includes the pptx skill):
   ```
   claude plugin add anthropic/agent-skills:document-skills
   ```

If the pptx skill is not available and cannot be installed, inform the user:
> "The pptx skill is required to generate slides but isn't available in this environment. Install it with:
> 1. `claude plugin add anthropic/agent-skills` (marketplace registry)
> 2. `claude plugin add anthropic/agent-skills:document-skills` (pptx skill)
>
> Alternatively, use the content outline with another presentation tool."

## Process

### 1. Load the Content Outline

Read the content outline document. Extract:
- Total section count and estimated duration
- Each section's key message, content, emphasis level, and speaker notes
- Source references (carry these forward for citation slides or footnotes)
- Design notes (brand requirements, constraints)

### 2. Research Visual Design Excellence

**MANDATORY before any design decisions.** This step prevents generic, template-looking output.

1. Read `${CLAUDE_PLUGIN_ROOT}/references/visual-design-principles.md` — concrete benchmarks, anti-patterns, and a visual checklist drawn from Apple keynotes, TED talks, Airbnb's pitch deck, and peer-reviewed research.
2. Read `${CLAUDE_PLUGIN_ROOT}/references/slide-patterns.md` — layout catalog with usage guidance for choosing the right layout per content type.
3. Search the web for visual inspiration relevant to the specific presentation topic and audience. Look for:
   - Best-in-class decks in the user's industry or presentation type
   - Current design trends (typography, color, layout) for the target context
   - Specific examples of how top presenters handle the content type (e.g., data-heavy, narrative, pitch)
4. Synthesize findings into a concrete design direction before proposing anything.

### 3. Plan Slides From Content Outline

Translate each content section into specific slides. Use the section's emphasis level and the design research to decide:

- **How many slides** each section becomes (high emphasis sections may need 2-4 slides; low emphasis may be a single divider or combined with adjacent content)
- **Which layout** for each slide (refer to the slide-patterns reference for the layout catalog)
- **Content per slide** — enforce: 30 words max, one idea per slide, headlines state the takeaway
- **Layout rhythm** — never the same layout more than 3 slides in a row; alternate between high-density and low-density slides

Present the slide plan to the user for approval:

> "Based on your content outline and visual research, here's how I'd structure the slides:
>
> - Section 1 (Opening) → 1 slide: Title slide
> - Section 2 (Key insight, high emphasis) → 3 slides: Big number, Chart, Single message
> - Section 3 (Context, medium) → 2 slides: Two-column, Bullet list
> - ...
>
> Total: [N] slides. Does this structure work?"

Get approval before proceeding.

### 4. Invoke the PPTX Skill

**MANDATORY**: Before generating any slides, read the pptx skill's SKILL.md completely. Search for a file named `SKILL.md` inside a `pptx` skill directory within the installed plugins.

Read the full file — it contains critical guidance on the html2pptx workflow, color palettes, and validation.

### 5. Design Decisions

Before generating, state your visual design approach informed by the research:

> "I'll create this presentation with:
> - **Color palette**: [chosen palette with hex codes — following 60-30-10 rule]
> - **Typography**: [font choices + size scale — use web-safe fonts only]
> - **Visual style**: [e.g., minimal with generous whitespace, inspired by X]
>
> Does this direction work?"

Get approval before writing any code.

### 6. Generate Slides

Follow the pptx skill's workflow (summarized here, but always defer to the skill's full instructions):

1. Create HTML files for each slide (720pt × 405pt for 16:9)
2. Create JavaScript file using html2pptx.js library
3. Generate the presentation
4. Create thumbnail grid for visual validation

### 7. Visual Validation

Review the thumbnail grid. For each slide check:
- Is 40%+ of the slide whitespace?
- Is color used for meaning, not decoration?
- No cards/boxes used as containers?
- No decorative gradients, shadows, or icon grids?
- Does it feel like a designed slide or a template? (If template — simplify)
- Text cutoff, overflow, or contrast issues?
- Can it be understood in under 3 seconds?

If issues found, fix and regenerate. Repeat until all slides pass.

### 8. Deliver

Provide the final .pptx file with a summary:

> "Your presentation is ready:
> - **File**: [filename.pptx]
> - **Slides**: [N] slides
>
> Any adjustments needed?"

## Slide Content Constraints

Apply these to every slide during the planning step:

- **30 words max per slide** — Move detail to speaker notes or split into additional slides
- **One idea per slide** — If a slide needs "and", split it
- **Headlines state the takeaway** — "Revenue grew 40%" not "Q3 Revenue Data"
- **Prefer visuals over text** — If a point can be a number, chart, or image instead of bullets, use that

## Principles

- **Follow the outline** — The content outline defines what to communicate; the slide plan defines how
- **Validate visually** — Always review thumbnails before delivery
- **Defer to pptx skill** — It has detailed, tested workflows for slide generation
