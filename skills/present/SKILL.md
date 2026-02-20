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

### 2. Research Visual Design Excellence

**MANDATORY before any design decisions.** This step prevents generic, template-looking output.

1. Read `${CLAUDE_PLUGIN_ROOT}/references/visual-design-principles.md` — it contains concrete benchmarks, anti-patterns, and a per-slide checklist drawn from Apple keynotes, TED talks, Airbnb's pitch deck, and peer-reviewed research.
2. Search the web for visual inspiration relevant to the specific presentation topic and audience. Look for:
   - Best-in-class decks in the user's industry or presentation type
   - Current design trends (typography, color, layout) for the target context
   - Specific examples of how top presenters handle the content type (e.g., data-heavy, narrative, pitch)
3. Synthesize findings into a concrete design direction before proposing anything.

**Key visual benchmarks (from reference):**
- 40%+ whitespace on every slide, 60-80% on hero slides
- 60-30-10 color rule: dominant / secondary / accent
- 1-2 fonts max, headline-to-body ratio of at least 1.5:1 (golden section scale: 16/24/36/54/81pt)
- No cards/boxes as containers — use whitespace and alignment to group
- No decorative gradients, shadows, or icons — flat, clean, intentional
- Asymmetry over symmetry — offset elements, use rule of thirds

### 3. Invoke the PPTX Skill

**MANDATORY**: Before generating any slides, read the pptx skill's SKILL.md completely. Search for a file named `SKILL.md` inside a `pptx` skill directory within the installed plugins.

Read the full file — it contains critical guidance on the html2pptx workflow, color palettes, and validation.

### 4. Design Decisions

Before generating, state your design approach informed by the research:

> "Based on your deck plan and visual research, I'll create this presentation with:
> - **Color palette**: [chosen palette with hex codes — following 60-30-10 rule]
> - **Typography**: [font choices + size scale — use web-safe fonts only]
> - **Visual style**: [e.g., minimal with generous whitespace, inspired by X]
>
> Does this direction work?"

Get approval before writing any code.

### 5. Generate Slides

Follow the pptx skill's workflow (summarized here, but always defer to the skill's full instructions):

1. Create HTML files for each slide (720pt × 405pt for 16:9)
2. Create JavaScript file using html2pptx.js library
3. Generate the presentation
4. Create thumbnail grid for visual validation

### 6. Visual Validation

Review the thumbnail grid. For each slide check:
- Is 40%+ of the slide whitespace?
- Is color used for meaning, not decoration?
- No cards/boxes used as containers?
- No decorative gradients, shadows, or icon grids?
- Does it feel like a designed slide or a template? (If template — simplify)
- Text cutoff, overflow, or contrast issues?
- Can it be understood in under 3 seconds?

If issues found, fix and regenerate. Repeat until all slides pass.

### 7. Deliver

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
