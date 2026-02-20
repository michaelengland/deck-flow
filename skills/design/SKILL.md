---
name: design
description: "This skill should be used when the user asks to design slides, plan slide layouts, choose a visual direction for a presentation, or invoke /deck-flow:design. Use AFTER /deck-flow:craft. Researches visual design, plans how content sections become slides, and proposes the visual direction."
---

# Design

Turn a content outline into a complete slide design — deciding how many slides each section becomes, which layouts to use, and what the visual direction should be. Outputs a saved slide design document that the present phase executes.

## Prerequisites

- A content outline exists (from **/deck-flow:craft**), OR
- User provides a clear structured outline, OR
- A PptxGenJS generation script exists from a previous import or creation (edit mode)

If no outline or generation script exists: "Would you like to use **/deck-flow:craft** first to structure your content?"

## Process

### Edit Mode Check

Before starting, check: does a deck folder in `decks/` contain a PptxGenJS generation script (a `.js` file containing `require("pptxgenjs")`)?

- **If no**: Follow the standard process below.
- **If yes**: This is an edit. Read the generation script to understand the current deck, then:
  1. Extract the current visual direction — collect all hex colors used (with frequency), fonts, size scales, and layout patterns across slides
  2. Summarize the current design back to the user:
     > "Here's the current visual direction I see:
     > - **Colors**: [extracted palette]
     > - **Typography**: [fonts and sizes in use]
     > - **Layouts**: [summary of patterns]
     >
     > What would you like to change?"
  3. Based on user input, produce or update a slide design document — explicitly note which slides are "keep as-is" vs. "modify" vs. "rebuild"
  4. Continue to step 5 (Document the Slide Design) to save the updated design

### 1. Load the Content Outline

Read the content outline document. Extract:
- Total section count and estimated duration
- Each section's key message, content, emphasis level, and speaker notes
- Source references
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

### 4. Visual Direction

Propose the visual design approach informed by the research:

> "I'll design this presentation with:
> - **Color palette**: [chosen palette with hex codes — following 60-30-10 rule]
> - **Typography**: [font choices + size scale — web-safe fonts only]
> - **Visual style**: [e.g., minimal with generous whitespace, inspired by X]
>
> Does this direction work?"

Get approval before documenting.

### 5. Document the Slide Design

Save the validated design to `decks/<name>/slide-design.md` (use the existing deck folder, or create one if it doesn't exist).

**Document format:**

```markdown
# [Presentation Title] - Slide Design

> **Next step:** Use **/deck-flow:present** to generate the .pptx file.

## Visual Direction
- **Color palette**: [hex codes — 60% dominant / 30% secondary / 10% accent]
- **Typography**: [font choices + size scale]
- **Visual style**: [description + inspiration sources]

## Slide Plan

### Slide 1: [Title — states the takeaway]
**Layout**: [layout type]
**Content**:
- [Headline or key point — 30 words max]
- [Supporting details]
**Speaker notes**: [talking points]

### Slide 2: [Title]
**Layout**: [type]
**Content**:
- [details]
**Speaker notes**: [talking points]

[... continue for all slides ...]

## Source References
- [Carried forward from content outline]
```

## Handoff

After design approval, offer next steps:

> "Your slide design is ready. Next step:
> - Use **/deck-flow:present** to generate the actual .pptx file
> - Or refine the design further"

## Slide Content Constraints

Apply these to every slide during the planning step:

- **30 words max per slide** — Move detail to speaker notes or split into additional slides
- **One idea per slide** — If a slide needs "and", split it
- **Headlines state the takeaway** — "Revenue grew 40%" not "Q3 Revenue Data"
- **Prefer visuals over text** — If a point can be a number, chart, or image instead of bullets, use that

## Principles

- **Research first** — Never propose a design direction without reading the references and searching the web
- **Emphasis drives structure** — High-emphasis sections get more slides and visual weight; low-emphasis sections stay brief
- **Validate incrementally** — Get approval on slide plan before visual direction, get approval on visual direction before documenting
