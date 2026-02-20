# PPTX Import Reference

How to import existing PowerPoint presentations for editing. Read this before running the import process.

## How It Works

The import script (`${CLAUDE_PLUGIN_ROOT}/scripts/pptx-to-js.py`) takes a `.pptx` file and produces a **deck folder** containing:

1. A **PptxGenJS generation script** (`.js`) — one function per slide, runnable with `node`
2. An **assets directory** with extracted images

The generation script is the primary artifact. It reproduces the deck when run from within the deck folder, and can be edited to make changes.

## Running the Script

```bash
# Install dependency (if needed)
pip install python-pptx

# Run the import
python ${CLAUDE_PLUGIN_ROOT}/scripts/pptx-to-js.py <input.pptx>
```

This creates a deck folder automatically. For example, `quarterly-review.pptx` produces:

```
decks/quarterly-review/
  quarterly-review.js     # generation script
  assets/                 # extracted images
```

Run the script from within the deck folder: `cd decks/quarterly-review && node quarterly-review.js`

**Arguments:**
- `<input.pptx>` — path to the source PowerPoint file (required)
- `--deck-dir` / `-d` — override the deck directory (default: `decks/<name>`)

## What Gets Imported

| Element | Fidelity | Notes |
|---------|----------|-------|
| Text content + formatting | ~95% | Font, size, color, bold, italic, alignment, bullets |
| Shapes (rect, rounded rect, line, oval) | ~95% | Position, size, fill, line properties |
| Images | ~100% | Extracted to assets directory, deduplicated by content |
| Tables | ~90% | Cell content, fill colors, bold, font color, borders |
| Speaker notes | ~100% | Plain text extraction |
| Slide backgrounds | ~90% | Solid color backgrounds |
| Charts (basic types) | ~80% | Bar, line, pie, doughnut, area — data and type extracted |
| Text with mixed formatting | ~90% | Per-run font properties preserved in text arrays |

## What Gets Lost or Degraded

| Element | Handling |
|---------|----------|
| Gradient fills | Converted to solid using the primary color; warning comment added |
| Theme colors | Resolved to RGB where possible; may differ from original theme |
| Non-web-safe fonts | Mapped to nearest web-safe font (e.g., Calibri → Arial); warning added |
| Animations and transitions | Silently dropped — PptxGenJS does not support them |
| SmartArt | Attempted as flattened individual shapes; may be incomplete |
| Complex charts (3D, scatter, bubble) | Skipped with warning comment |
| Shape adjustment handles | Default proportions used — custom callout shapes may differ |
| Hyperlinks | Noted in comments but not functional in output |
| Audio and video | Skipped |
| Slide masters and layouts | Flattened — inherited styles resolved to direct values |

## The Generation Script Format

The generated JS follows a strict **one-function-per-slide** structure:

```javascript
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// --- Slide 1: Company Overview ---
function createSlide1(pres) {
  let slide = pres.addSlide();
  slide.background = { color: "1A1A2E" };
  slide.addText("Company Overview", { x: 0.8, y: 1.5, w: 8.4, h: 1, fontSize: 54, fontFace: "Arial", color: "FFFFFF", bold: true });
  slide.addNotes("Welcome everyone. Today I'll walk you through...");
}

// --- Slide 2: Key Metrics ---
function createSlide2(pres) { ... }

// --- Build presentation ---
createSlide1(pres);
createSlide2(pres);
pres.writeFile({ fileName: "company-overview.pptx" });
```

**Why one function per slide:**
- Claude can read and reason about individual slides in isolation
- Modifications are scoped — changing slide 5 cannot accidentally affect slide 12
- Adding slides means adding a new function + inserting its call
- Removing slides means removing a function + its call
- Reordering means changing the order of function calls at the bottom

## Editing the Generation Script

After import, the generation script is the source of truth. Common edit operations:

**Change text on a slide:**
Find the relevant `createSlideN` function and modify the text string in the `addText` call.

**Change colors across the deck:**
Search for hex color values (e.g., `"1A1A2E"`) and replace with the new color.

**Add a new slide:**
Create a new function (e.g., `createSlide3b`) and insert its call at the right position in the build section.

**Remove a slide:**
Delete the function and remove its call from the build section.

**Reorder slides:**
Change the order of `createSlideN(pres)` calls at the bottom of the file.

**Always regenerate and validate** after changes — run with `node` from the deck folder, generate thumbnails, review visually.

## Troubleshooting

### Script fails with "No module named pptx"
```bash
pip install python-pptx
```

### Generated deck looks different from original
Check `// WARNING:` comments in the generated JS file. Common causes:
- Gradient fills converted to solid colors
- Non-web-safe fonts substituted (e.g., Calibri → Arial)
- Theme colors resolved to approximate RGB values
- Slide master styles flattened (formatting that was inherited is now explicit)

### Text overflow or positioning issues
EMU-to-inch conversion is mathematically exact but rounding to 2 decimal places can shift elements by fractions of a pixel. Adjust `x`/`y`/`w`/`h` values manually if needed.

### Images not showing
Ensure you are running `node` from within the deck folder. Image paths in the script are relative to the deck folder (e.g., `assets/slide1_abc123.jpg`).
