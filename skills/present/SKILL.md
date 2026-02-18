---
name: present
description: "This skill should be used when the user asks to generate a PowerPoint, create slides from a plan, build a .pptx file, or invoke /deck-flow:present. Use AFTER /deck-flow:craft. Executes a deck plan to produce the actual .pptx file using the pptx skill."
---

# Present

Execute a deck plan to generate the actual PowerPoint presentation.

## Prerequisites

- A deck plan exists (from **/deck-flow:craft**), OR user provides a clear slide-by-slide outline
- The **pptx skill** must be available (see "Installing the PPTX Skill" below)

If no plan exists: "Would you like to use **/deck-flow:craft** first to plan your slides?"

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
> Alternatively, use the deck plan document with another presentation tool."

## Process

### 1. Load the Deck Plan

Read the deck plan document. Extract:
- Total slide count
- Each slide's layout, content, and speaker notes
- Visual requirements (colors, imagery style, brand)
- Source references (carry these forward for citation slides or footnotes)

### 2. Invoke the PPTX Skill

**MANDATORY**: Before generating any slides, read the pptx skill's SKILL.md completely. Search for a file named `SKILL.md` inside a `pptx` skill directory within the installed plugins.

Read the full file — it contains critical guidance on the html2pptx workflow, color palettes, and validation.

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
| Three-column | Three equal sections |
| Full-bleed image | Image covers slide, text overlay |
| Image + text | Image 60-70%, text beside or below |
| Image grid | 2-4 images in grid with optional labels |
| Single chart | Chart centered, headline above |
| Chart + interpretation | Chart 60%, bullets 40% beside it |
| Comparison table | 2-4 columns, 3-5 rows, highlight differences |
| Big number | Oversized number with context label |
| Quote | Centered italic text, attribution below |
| Timeline | Horizontal flow with milestones |
| Steps | Numbered steps, left-to-right or top-to-bottom |
| Summary | 3-5 key takeaways |
| Call to action | One clear next step, contact info |
| Q&A | "Questions?" with optional contact info |

## Principles

- **Follow the plan** — The deck plan is the spec; don't improvise without approval
- **Validate visually** — Always review thumbnails before delivery
- **Defer to pptx skill** — It has detailed, tested workflows for slide generation
