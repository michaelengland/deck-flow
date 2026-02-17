# deck-flow

A Claude Code plugin that guides you through building presentations in three phases: **narrative**, **craft**, and **present**. Instead of jumping straight into slides, deck-flow helps you develop your story first, plan your deck structure second, and generate the PowerPoint last.

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

### `/deck-flow:craft` — Plan your slides

Once your narrative is solid, this skill translates it into a concrete slide-by-slide plan. For each slide it specifies:

- Layout type (title, bullet list, two-column, big number, quote, etc.)
- Content and headline
- Speaker notes
- Transition to the next slide

It includes guidance on slide count based on presentation length and validates the plan incrementally in batches.

**Output:** A detailed deck plan saved to `docs/plans/`.

### `/deck-flow:present` — Generate the PowerPoint

Takes your deck plan and produces the actual `.pptx` file. This skill:

1. Loads your deck plan
2. Proposes design decisions (color palette, typography, visual style) for approval
3. Generates slides using the pptx skill
4. Validates the output visually via thumbnail grid
5. Delivers the final file

**Requires:** The pptx skill (bundled with Cowork/Claude Code).

## Typical Workflow

```
/deck-flow:narrative  →  /deck-flow:craft  →  /deck-flow:present
    (story)                 (structure)            (slides)
```

Each phase produces a document you can review and revise before moving to the next.

## License

MIT
