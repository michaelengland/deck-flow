---
name: present
description: "This skill should be used when the user asks to generate the PowerPoint, build the .pptx file, render slides, or invoke /deck-flow:present. Use AFTER /deck-flow:design. Executes a slide design document to produce the final .pptx file."
---

# Present

Execute a slide design document to generate the final PowerPoint file. This skill takes the complete slide-by-slide spec (with layouts, content, and visual direction) and produces a validated .pptx.

## Prerequisites

- A slide design document exists (from **/deck-flow:design**), OR
- User provides a complete slide-by-slide spec with visual direction, OR
- A PptxGenJS generation script exists from a previous import or creation (edit mode)

If no design or generation script exists: "Would you like to use **/deck-flow:design** first to plan your slides and visual direction?"

## Process

### Edit Mode Check

Before starting, check: does a deck folder in `decks/` contain a PptxGenJS generation script (a `.js` file containing `require("pptxgenjs")`)?

- **If no**: This is a new presentation. Follow the standard process below.
- **If yes**: This is an edit. Read the existing generation script and modify only the affected slide functions based on user instructions or upstream design documents. Do not rewrite unchanged slides. Specifically:
  1. Read the generation script to understand the current slide functions
  2. Identify which slides need changes (from user request or updated design doc)
  3. Modify only those `createSlideN` functions — preserve everything else verbatim
  4. If adding slides, create new functions and insert their calls at the right position
  5. If removing slides, delete the function and its call
  6. After modifications, continue to step 3 (Visual Validation) as usual

### 1. Load the Slide Design

Read the slide design document. Extract:
- Visual direction (color palette, typography, visual style)
- Each slide's layout, content, and speaker notes
- Source references (for citation slides or footnotes)

### 2. Generate Slides

**Before writing any generation code**, read `${CLAUDE_PLUGIN_ROOT}/references/pptx-generation.md` — it contains the complete PptxGenJS API reference, critical pitfalls that cause file corruption, and the full generation workflow.

**Workflow:**
1. Create a JavaScript file that builds the presentation using PptxGenJS (10" × 5.625" for 16:9)
2. Run with `node` to generate the `.pptx`
3. Convert to slide images for validation (see "Visual Validation" in the reference for multiple approaches depending on whether PowerPoint or LibreOffice is available)
4. Create a thumbnail grid from the slide images

**Critical reminders (from reference):**
- NEVER use "#" in hex colors — causes file corruption
- NEVER reuse option objects — PptxGenJS mutates them in-place
- Use `bullet: true` for bullets, NEVER unicode symbols
- Use `breakLine: true` between text array items for multi-line text
- Only use web-safe fonts: Arial, Helvetica, Verdana, Georgia, Times New Roman, Courier New

### 3. Visual Validation

Review the thumbnail grid. For each slide check:
- Is 40%+ of the slide whitespace?
- Is color used for meaning, not decoration?
- No cards/boxes used as containers?
- No decorative gradients, shadows, or icon grids?
- Does it feel like a designed slide or a template? (If template — simplify)
- Text cutoff, overflow, or contrast issues?
- Can it be understood in under 3 seconds?

If issues found, fix and regenerate. Repeat until all slides pass.

### 4. Deliver

Provide the final .pptx file with a summary:

> "Your presentation is ready:
> - **PowerPoint**: [filename.pptx]
> - **PDF**: [filename.pdf]
> - **Slides**: [N] slides
>
> Any adjustments needed?"

## Principles

- **Follow the design** — The slide design document is the spec; don't deviate without approval
- **Validate visually** — Always review thumbnails before delivery
- **Fix and regenerate** — If validation fails, fix the code and regenerate rather than declaring "good enough"
