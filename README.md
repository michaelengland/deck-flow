# deck-flow

Build and edit PowerPoint presentations with AI. A [Claude Code](https://claude.com/claude-code) plugin that generates `.pptx` and `.pdf` files through a guided workflow — separating story, structure, design, and slide generation into distinct phases for better results.

## Why not just "make me a presentation"?

When you ask AI to generate a presentation in one shot, you get generic slides with surface-level content. The AI has to guess your audience, pick a structure, decide on visuals, and write content all at once — and it cuts corners on all of them.

deck-flow fixes this by breaking the problem into phases that build on each other:

1. **Narrative first** — figure out what to say before touching slides. Who's the audience? What should they do afterward? What's the one thing they should remember? This alone transforms the output.
2. **Structure before layout** — organize your key messages, evidence, and emphasis levels into sections. Decide what matters most before deciding how many slides it gets.
3. **Research-driven design** — the design phase reads visual design principles and searches the web for relevant inspiration before proposing colors, fonts, and layouts. No generic templates.
4. **Validated generation** — every slide is checked against a visual quality checklist (whitespace, contrast, anti-patterns) and regenerated until it passes.

Each phase produces a document you review and approve before moving on. You catch problems early — a weak narrative gets fixed at the narrative stage, not after 30 slides have been generated. And because each phase's output is a readable document, you can edit at any level: rethink the story without touching the design, or redesign the visuals without rewriting the content.

Already have a deck? Use **import** to reverse-engineer it into the pipeline and improve it through any phase.

## Requirements

The narrative, craft, and design phases have no dependencies. The present phase (PPTX generation) requires:

- **Node.js** — runs PptxGenJS to generate .pptx files
- **Python** — creates thumbnail grids for visual validation
- **Microsoft PowerPoint** or **LibreOffice** — converts .pptx to images for validation

npm and pip packages are installed automatically during generation and import.

## Installation

Install this plugin in Claude Code:

```bash
claude plugin install michaelengland/deck-flow
```

## Skills

### `/deck-flow:narrative` — Develop your story

Start here. This skill helps you figure out *what to say* before thinking about slides. Through a guided conversation, it explores:

- **Audience** — Who's watching and what do they care about?
- **Purpose** — What should the audience think, feel, or do afterward?
- **Key message** — The one thing they should remember
- **Story framework** — The structure that best fits your content

It recommends from five proven narrative frameworks:

| Framework | Best for |
|-----------|----------|
| Problem → Solution → Impact | Pitches, proposals |
| Situation → Complication → Resolution | Strategic updates, analysis |
| What → So What → Now What | Data presentations, reports |
| Before → After → Bridge | Transformations, case studies |
| Hook → Build → Payoff | Persuasive, storytelling |

**Output:** A narrative document saved to the deck folder.

### `/deck-flow:craft` — Structure your content

Organizes your narrative into logical sections — without locking in slide counts or layouts. For each section it specifies:

- Key message (the takeaway)
- Supporting content and evidence
- Emphasis level (high / medium / low)
- Speaker notes and transitions

**Output:** A content outline saved to the deck folder.

### `/deck-flow:design` — Plan slides and visual direction

Turns your content outline into a complete slide design. This skill:

1. Researches visual design excellence — reads bundled design principles and searches the web for inspiration relevant to your topic
2. Plans how content sections become slides — decides slide count, layouts, and rhythm based on emphasis levels
3. Proposes the visual direction (color palette, typography, style) for approval

**Output:** A slide design document saved to the deck folder.

### `/deck-flow:present` — Generate the presentation

Executes your slide design to produce the final `.pptx` and `.pdf`:

1. Generates slides using PptxGenJS
2. Exports to PDF
3. Validates every slide against a visual checklist (whitespace, contrast, anti-patterns)
4. Fixes and regenerates until all slides pass
5. Delivers both files

### `/deck-flow:import` — Import an existing presentation

Already have a deck you want to improve? This skill takes a `.pptx` file and reverse-engineers it into an editable PptxGenJS generation script:

1. Parses all slides — text, shapes, images, tables, charts, speaker notes
2. Creates a deck folder with a generation script and extracted images
3. Validates the import by regenerating and comparing visually

After import, you can edit the deck directly or enter any phase of the workflow above to make targeted improvements.

**Output:** A deck folder (e.g., `decks/quarterly-review/`) containing the generation script, extracted images, and all subsequent artifacts.

## Deck Folder Structure

Each deck gets its own folder under `decks/`, keeping all artifacts self-contained:

```
decks/quarterly-review/
  quarterly-review.js         # generation script
  quarterly-review.pptx       # output
  quarterly-review.pdf        # PDF export
  narrative.md                # story (from narrative phase)
  content-outline.md          # structure (from craft phase)
  slide-design.md             # visual plan (from design phase)
  assets/                     # extracted/embedded images
  slides/                     # validation images + thumbnails
```

## Typical Workflow

### New Presentation

```
/deck-flow:narrative → /deck-flow:craft → /deck-flow:design → /deck-flow:present
    (story)              (content)           (design)            (slides)
```

Each phase produces a document you can review and revise before moving to the next.

### Editing an Existing Deck

```
/deck-flow:import → choose your starting point → /deck-flow:present
                     ├─ /deck-flow:narrative (rethink the story)
                     ├─ /deck-flow:craft (restructure content)
                     ├─ /deck-flow:design (redesign visuals)
                     └─ direct edits (tell Claude what to change)
```

You don't need to go through all phases. Edit at whatever level makes sense — the generation script carries your changes through to the final output.

## License

MIT
