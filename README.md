# deck-flow

A Claude Code plugin that guides you through building presentations in three phases: **narrative**, **craft**, and **present**. Instead of jumping straight into slides, deck-flow helps you develop your story first, structure your content second, and design + generate the PowerPoint last.

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

Once your narrative is solid, this skill organizes it into logical sections — without locking in specific slide counts or layouts. For each section it specifies:

- Key message (the takeaway)
- Supporting content and evidence
- Emphasis level (high / medium / low)
- Speaker notes and transitions

Slide-level decisions (how many slides per section, which layouts) are deliberately deferred to the present phase, where visual design research informs those choices.

**Output:** A content outline saved to `docs/plans/`.

### `/deck-flow:present` — Design and generate the PowerPoint

Takes your content outline and produces the actual `.pptx` file. This skill:

1. Loads your content outline
2. Researches visual design excellence — reads bundled design principles (benchmarks from Apple keynotes, TED, Airbnb's pitch deck) and searches the web for inspiration relevant to your topic
3. Plans slides from the outline — decides how many slides each section needs and which layouts to use, based on emphasis levels and design research
4. Proposes the slide plan and visual design (color palette, typography, visual style) for approval
5. Generates slides using PptxGenJS (bundled workflow — no external plugins required)
6. Validates every slide against a concrete checklist (3-second rule, whitespace %, word count, etc.)
7. Delivers the final file

## Typical Workflow

```
/deck-flow:narrative  →  /deck-flow:craft  →  /deck-flow:present
    (story)               (content)             (design + slides)
```

Each phase produces a document you can review and revise before moving to the next.

## License

MIT
