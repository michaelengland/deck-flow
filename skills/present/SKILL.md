---
name: present
description: "This skill should be used when the user asks to generate the PowerPoint, build the .pptx file, render slides, or invoke /deckwright:present. Executes a slide design document to produce the final .pptx and .pdf files."
---

# Present

Execute a slide design document to generate the final presentation. This skill takes the complete slide-by-slide spec (with layouts, content, and visual direction) and produces a validated `.pptx` and `.pdf`.

## Prerequisites

- A slide design document exists (from **/deckwright:design**), OR
- User provides a complete slide-by-slide spec with visual direction, OR
- A PptxGenJS generation script exists from a previous import or creation (edit mode)

If no design or generation script exists: "Would you like to use **/deckwright:design** first to plan your slides and visual direction?"

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
- Source references (URLs carried forward from upstream phases)

### 2. Generate Slides

**Before writing any generation code**, read `${CLAUDE_PLUGIN_ROOT}/references/pptx-generation.md` — it contains the complete PptxGenJS API reference, critical pitfalls that cause file corruption, and the full generation workflow.

**Workflow:**
1. Create a JavaScript file that builds the presentation using PptxGenJS (10" × 5.625" for 16:9)
2. Run with `node` to generate the `.pptx`
3. Export to `.pdf` (see the reference for PowerPoint and LibreOffice approaches)
4. Convert to slide images for validation (see "Visual Validation" in the reference)
5. Create a thumbnail grid from the slide images

The reference includes a **Critical Pitfalls** section — follow it exactly before writing any code. Key failure modes covered: hex color formatting, opacity encoding, object reuse, bullet syntax, and gradient limitations.

**Sources in the final output:**

Source references carried from upstream phases should appear as clickable hyperlinks in the `.pptx` (and by extension, the `.pdf`). Use these approaches depending on context:

- **Inline footnote numbers** — Small superscript-style numbers (e.g., "Market grew 40%¹") that link to the source URL via PptxGenJS `hyperlink: { url: "..." }`. Keep them subtle.
- **Sources slide at the end** — A final slide listing all sources as clickable links: `[1] Label — url`. Use this for formal or data-heavy presentations.
- **Speaker notes** — Always include source URLs in the speaker notes for the slides that reference them, even if they also appear inline or on a sources slide.

The goal: every claim in the final deck can be traced back to its source via a clickable link, in both `.pptx` and `.pdf`.

### 3. Visual Validation

Review the thumbnail grid. For each slide check:
- Is 40%+ of the slide whitespace?
- Is color used for meaning, not decoration?
- No cards/boxes used as containers?
- No decorative gradients, shadows, or icon grids?
- Would removing any visual element break the meaning? (If not, remove it)
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
> The generation script is the source of truth — if you need changes, let me know and I'll update the script and regenerate. Edits made directly to the .pptx in PowerPoint will be overwritten on the next run.
>
> Any adjustments needed?"

## Principles

- **Follow the design** — The slide design document is the spec; don't deviate without approval
- **Validate visually** — Always review thumbnails before delivery
- **Fix and regenerate** — If validation fails, fix the code and regenerate rather than declaring "good enough"
