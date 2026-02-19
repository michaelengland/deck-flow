# Visual Design Principles Reference

Concrete, research-backed design principles for building visually exceptional presentations. Load this before making any design decisions in the present phase.

## The Core Problem

Most generated presentations look generic because they treat slides as documents — dense, uniform, and text-heavy. Exceptional decks treat slides as billboards: one idea, maximum impact, minimum clutter.

## Benchmarks From the Best

### Text Density

| Source | Words Per Slide | Approach |
|--------|----------------|----------|
| Apple keynotes (Steve Jobs era) | 3-7 words | "3-Second Rule" — audience should grasp the slide in 3 seconds |
| TED official guidelines | 1 idea per slide | "Your slides are not your notes" |
| Guy Kawasaki (10/20/30 rule) | ~30 words max | 30pt minimum font enforces brevity |
| Airbnb original pitch deck | 15-25 words | One claim per slide, large type |
| Sequoia pitch deck template | 10-30 words | Headline + 3-4 short bullets max |

**Rule of thumb**: If a slide has more than 30 words, split it.

### Typography

**Size ratios matter more than absolute sizes.**

| Element | Recommended Size | Purpose |
|---------|-----------------|---------|
| Hero/impact number | 100-200pt | Single-stat slides, attention anchors |
| Slide headline | 44-60pt | Primary message — readable from back of room |
| Body text | 24-32pt | Supporting detail (use sparingly) |
| Captions/labels | 16-20pt | Chart labels, footnotes |

**Key ratios:**
- Hero-to-body ratio: at least 3:1 (e.g., 120pt hero / 28pt body = 4.3:1)
- Headline-to-body ratio: at least 1.5:1
- Use the golden section scale: 16, 24, 36, 54, 81pt (each ~1.5x the previous)

**Font count**: 1-2 fonts maximum. One sans-serif for headings, optionally one serif or mono for contrast. Never three.

### Color

**The 60-30-10 rule:**
- 60% — dominant/background color (usually white, off-white, or dark)
- 30% — secondary color (text, containers)
- 10% — accent color (highlights, CTAs, key data)

**What the best decks do:**
- 2-3 colors total, applied consistently
- Apple: white background, black text, one blue/green/product accent
- Stripe: white/off-white backgrounds, purple accent, grey body text
- Linear: dark backgrounds, white text, purple/blue accent
- One accent color used only for emphasis — never for decoration

**What generic decks do wrong:**
- 5+ colors with no hierarchy
- Every bullet point or card a different color
- Gradients on everything
- Color used for decoration instead of meaning

### Whitespace

The single biggest differentiator between exceptional and generic decks.

**Quantified guidance:**
- Minimum 40% of every slide should be empty space
- Hero slides (single message, big number): 60-80% whitespace
- Content slides (bullets, charts): 40-50% whitespace
- Generous padding: at least 60-80px from all slide edges
- Line spacing: 1.4-1.6x for body text, 1.2x for headlines

**Apple's approach**: Slides are often 70-80% empty. A single word, number, or product image with nothing else. The emptiness IS the design.

### Imagery

| Approach | When to Use | Example |
|----------|-------------|---------|
| Full-bleed photography | Emotional impact, context setting | Apple product reveals |
| Single centered product/screenshot | Feature demos, product slides | Linear changelog |
| No imagery — just type | Key messages, statistics, transitions | Most TED talks |
| Simple flat icons | Process flows, feature lists (sparingly) | Sequoia template |

**What to avoid:**
- Stock photography (especially people-in-office, handshake, lightbulb)
- Clip art or illustrative icons on every slide
- Images as decoration rather than communication
- Small images surrounded by text

### Layout Variation

Exceptional decks vary their visual rhythm deliberately:

**Pattern**: Alternate between high-density and low-density slides.
- After a data-heavy slide, follow with a single-message breather
- After 2-3 content slides, insert a full-bleed image or section divider
- Never use the same layout more than 3 slides in a row

**Asymmetry over symmetry:**
- Don't center everything — offset text to left/right with image on the other side
- Use the rule of thirds: place key elements at intersection points
- Leave one quadrant intentionally empty

## Anti-Patterns: What Makes Decks Look Generic

### The "Template" Look

These specific traits make a deck instantly look AI-generated or template-based:

1. **Cards/boxes on every slide** — Rounded-rectangle containers around every group of text. Real designers use whitespace and alignment to group content, not boxes.

2. **Uniform layouts** — Every content slide has the same structure (title + 3 columns, title + bullets). Exceptional decks vary layout intentionally.

3. **Too many elements per slide** — Title + subtitle + 3 icons + 3 headings + 3 descriptions + a footer. Reduce to 1-2 elements.

4. **Decorative gradients and shadows** — Subtle drop shadows on every card, gradient backgrounds. Clean, flat design reads as more professional.

5. **Icon overload** — A grid of icons with labels underneath. Icons should be functional (wayfinding, emphasis), not decorative filler.

6. **Bullet point lists on every slide** — Bullets are a last resort. Prefer: one statement, one number, one image, or a simple comparison.

7. **Logos and footers on every slide** — Brand bar on every slide is corporate-template energy. Use branding on title and closing slides only.

8. **Centered everything** — Center-aligned text on every slide creates visual monotony. Mix alignment strategies.

### The Fix for Each

| Anti-Pattern | Fix |
|-------------|-----|
| Cards/boxes everywhere | Remove containers. Use whitespace + alignment to group. |
| Uniform layouts | Deliberately alternate: message → data → image → message |
| Too many elements | Cut to 1-2 elements. Ask "what can I remove?" |
| Decorative gradients | Flat colors. If using gradients, one subtle one max. |
| Icon overload | Remove icons. Use size/weight/color for hierarchy instead. |
| Bullet lists | Convert to: single statement, comparison, big number, or visual |
| Logo on every slide | Logo on title + closing only. |
| Center everything | Left-align body text. Vary headline placement. |

## Handling Complex Information

When a slide genuinely needs to convey dense information:

1. **Build it progressively** — Split into 3-4 slides that build on each other rather than one dense slide
2. **Annotate, don't list** — Instead of a bullet list explaining a chart, annotate directly on the chart
3. **Headline carries the insight** — The slide title should state the conclusion ("Revenue grew 40%"), not describe the content ("Q3 Revenue Data")
4. **Use the appendix pattern** — Put the simple version on the slide, reference detailed data in an appendix or handout

## Quick Checklist Before Generating Any Slide

For every slide, verify:

- [ ] Can it be understood in under 3 seconds?
- [ ] Is there only ONE main idea?
- [ ] Is 40%+ of the slide whitespace?
- [ ] Are there 30 or fewer words?
- [ ] Does the headline state a takeaway (not a topic)?
- [ ] Is color used for meaning, not decoration?
- [ ] Would removing any element break the meaning? (If not, remove it)

## Sources

- Steve Jobs' 3-Second Slide Rule — Forbes/Carmine Gallo
- Guy Kawasaki 10/20/30 Rule — guykawasaki.com
- TED Official Slide Guidelines — ted.com
- "Ten Simple Rules for Effective Presentation Slides" — PLoS Computational Biology (peer-reviewed)
- David JP Phillips "How to Avoid Death by PowerPoint" — TEDx Stockholm
- Airbnb Pitch Deck Teardown — Slidebean
- Sequoia Capital Pitch Deck Template — via Winning Presentations
- Typography scale (Golden Section) — Made in Keynote / Medium
- BrightCarbon Font Size Recommendations — brightcarbon.com
- 60-30-10 Color Rule — Pitchworx
- "Why AI Presentations Look AI-Generated" — LLeMental
- Information Density in Slide Decks — Andrew Quagliata
