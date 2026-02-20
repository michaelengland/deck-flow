---
name: import
description: "This skill should be used when the user wants to edit, modify, or improve an existing PowerPoint presentation, import a .pptx for editing, or invoke /deck-flow:import. Reverse-engineers a .pptx into a PptxGenJS generation script that can be edited and regenerated."
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
   python ${CLAUDE_PLUGIN_ROOT}/scripts/pptx-to-js.py <input.pptx> --output generate-deck.js --assets-dir assets
   ```
3. Check the exit code. If non-zero, read stderr and diagnose the issue.

### 4. Validate the Import

1. Install PptxGenJS if needed: `npm install pptxgenjs`
2. Run the generated script: `node generate-deck.js`
3. Verify it produces `output.pptx`
4. Convert to slide images and create a thumbnail grid using the same validation workflow from `${CLAUDE_PLUGIN_ROOT}/references/pptx-generation.md` (PDF Export and Visual Validation section)
5. Show the thumbnail grid to the user and ask:
   > "Here's the imported version of your deck. Does it look correct? Any noticeable differences from the original?"

### 5. Review Warnings

Read through the generated `generate-deck.js` for any `// WARNING:` comments. Summarize these for the user:

> "The import completed with these notes:
> - [list any warnings — font substitutions, gradient conversions, skipped elements]
>
> These are cosmetic differences. Would you like to address any of them before proceeding?"

### 6. Hand Off

The `generate-deck.js` file is now the source of truth for the deck. Present the user's options:

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
