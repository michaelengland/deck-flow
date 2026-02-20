# deck-flow

A Claude Code plugin that guides you through building presentations in four phases: **narrative**, **craft**, **design**, and **present**. Instead of jumping straight into slides, deck-flow separates what to say, how to structure it, how it should look, and how to build it.

## Installation

Add this plugin to Claude Code:

```bash
claude plugin add michaelengland/deck-flow
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

**Output:** A validated narrative document saved to `docs/plans/`.

### `/deck-flow:craft` — Structure your content

Organizes your narrative into logical sections — without locking in slide counts or layouts. For each section it specifies:

- Key message (the takeaway)
- Supporting content and evidence
- Emphasis level (high / medium / low)
- Speaker notes and transitions

**Output:** A content outline saved to `docs/plans/`.

### `/deck-flow:design` — Plan slides and visual direction

Turns your content outline into a complete slide design. This skill:

1. Researches visual design excellence — reads bundled design principles and searches the web for inspiration relevant to your topic
2. Plans how content sections become slides — decides slide count, layouts, and rhythm based on emphasis levels
3. Proposes the visual direction (color palette, typography, style) for approval

**Output:** A slide design document saved to `docs/plans/`.

### `/deck-flow:present` — Generate the PowerPoint

Executes your slide design to produce the actual `.pptx` file:

1. Generates slides using PptxGenJS
2. Validates every slide against a visual checklist (whitespace, contrast, anti-patterns)
3. Fixes and regenerates until all slides pass
4. Delivers the final file

## Typical Workflow

```
/deck-flow:narrative → /deck-flow:craft → /deck-flow:design → /deck-flow:present
    (story)              (content)           (design)            (slides)
```

Each phase produces a document you can review and revise before moving to the next.

## License

MIT
