---
name: import
description: "This skill should be used when the user wants to import an existing .pptx file into deck-flow, bring in a PowerPoint that was created outside this tool, reverse-engineer a presentation for editing, or invoke /deck-flow:import. Converts a .pptx into a PptxGenJS generation script so it can be edited and regenerated through the deck-flow pipeline."
---

# Import

Import an existing PowerPoint presentation by reverse-engineering it into an editable PptxGenJS generation script. This is the entry point for editing decks that weren't created through deck-flow.

## Process

### 1. Identify the Source File

Ask the user to provide or confirm the path to the `.pptx` they want to edit. If they've already mentioned it, confirm:

> "I'll import `[filename.pptx]` for editing. Is that the right file?"

Do not proceed without a valid file path.

### 2. Read the Import Reference

Read `${CLAUDE_PLUGIN_ROOT}/references/pptx-import.md` for the full import workflow, capabilities, and known limitations.

### 3. Run the Reverse-Engineering Script

1. Ensure python-pptx is installed: `pip install python-pptx`
2. Run the script:
   ```bash
   python ${CLAUDE_PLUGIN_ROOT}/scripts/pptx-to-js.py <input.pptx>
   ```
   This creates a deck folder at `decks/<name>/` containing the generation script and extracted images. For example, `quarterly-review.pptx` produces:
   ```
   decks/quarterly-review/
     quarterly-review.js     # generation script
     assets/                 # extracted images
   ```
3. Check the exit code. If non-zero, read stderr and diagnose the issue.

### 4. Generate Thumbnails from the Original

Before running the generated script, convert the **original** `.pptx` to slide images so you have a baseline for comparison. Use the validation workflow from `${CLAUDE_PLUGIN_ROOT}/references/pptx-generation.md` (PDF Export and Visual Validation section), saving output to `decks/<name>/original/`:

```
decks/<name>/original/
  slides/slide-01.jpg, slide-02.jpg, ...
  slides/thumbnails.jpg
```

### 5. Validate and Fix (Loop)

This step mirrors the present skill's validation loop — regenerate, compare, fix, repeat.

1. Install PptxGenJS if needed: `npm install pptxgenjs`
2. Run the generated script from the deck folder: `cd decks/<name> && node <name>.js`
3. Convert the regenerated `.pptx` to slide images and a thumbnail grid (same validation workflow, output to the deck folder's `slides/` directory as usual)
4. Compare slide-by-slide against the original thumbnails. For each slide, check:
   - Is the text content and positioning correct?
   - Are colors and fonts right?
   - Are images present and correctly placed?
   - Are shapes (backgrounds, dividers, accent bars) reproduced?
   - Is the overall layout and whitespace faithful?
5. **If fixable differences exist** — edit the generation script to correct them and regenerate. Common fixes:
   - Adjust `x`/`y`/`w`/`h` values for positioning
   - Fix font sizes or colors
   - Add missing shapes or backgrounds
   - Correct text content or formatting
6. **Repeat** until the regenerated slides match the original as closely as possible.

### 6. Document Remaining Differences

Once you've fixed everything you can, catalogue what remains. Read the `// WARNING:` comments in the generation script and compare them with any visual differences you can still see.

Present a clear summary to the user:

> "Import complete. Here's the final comparison:
> - **[N] slides match the original** — no visible differences
> - **Remaining differences:**
>   - Slide 3: Gradient background converted to solid `#1A1A2E` (PptxGenJS doesn't support gradients)
>   - Slides 1, 5, 12: Font "Calibri" substituted with "Arial" (web-safe only)
>   - Slide 8: SmartArt diagram simplified to basic shapes
>   - [any other differences]
>
> These are inherent limitations of the import — they cannot be fixed automatically. You can adjust them manually in the generation script if needed."

### 7. Handoff

The generation script is now the source of truth for the deck. Present the user's options:

> "Your presentation is imported. You can now:
> - **Edit directly** — Tell me what to change and I'll modify the generation script
> - Use **/deck-flow:narrative** to rethink the story
> - Use **/deck-flow:craft** to restructure the content
> - Use **/deck-flow:design** to redesign the visual direction
> - Use **/deck-flow:present** to regenerate after any changes"

## Principles

- **Mechanical, not interpretive** — The import produces code, not creative documents. It is a translation, not an analysis.
- **Validate before proceeding** — Always regenerate and compare before declaring the import complete.
- **Surface limitations honestly** — Do not hide what was lost in translation. The user should know about font substitutions, gradient conversions, and skipped elements.
- **The generation script is the source of truth** — After import, all edits flow through the `.js` file.
