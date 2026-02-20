# PPTX Generation Reference

How to generate PowerPoint presentations using PptxGenJS. Read this before writing any slide generation code.

## Dependencies

**Required:**
```bash
npm install pptxgenjs
```

**For icons (optional):**
```bash
npm install react-icons react react-dom sharp
```

**For visual validation**, one of:
- **Microsoft PowerPoint** (macOS) — export to PDF via AppleScript
- **LibreOffice** + **Poppler** — `soffice` converts to PDF, `pdftoppm` converts to images

## Quick Start

```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";  // 10" × 5.625"

let slide = pres.addSlide();
slide.addText("Hello World!", { x: 1, y: 1, fontSize: 44, color: "363636" });

pres.writeFile({ fileName: "output.pptx" });
```

## Slide Dimensions

All coordinates are in **inches**.

| Layout | Width | Height | Use |
|--------|-------|--------|-----|
| `LAYOUT_16x9` | 10" | 5.625" | Default — use this |
| `LAYOUT_16x10` | 10" | 6.25" | Widescreen variant |
| `LAYOUT_4x3` | 10" | 7.5" | Legacy |

## Critical Pitfalls

These cause silent file corruption or rendering bugs. Follow them exactly.

1. **NEVER use "#" in hex colors** — `"FF0000"` not `"#FF0000"`. The hash causes file corruption.
2. **NEVER encode opacity in hex strings** — `"00000020"` corrupts the file. Use the `transparency` property instead (0-100 scale).
3. **Use `bullet: true`** for bullet points — NEVER use unicode bullet symbols which create double bullets.
4. **Use `breakLine: true`** between array items for multi-line text within a single text box.
5. **NEVER reuse option objects** — PptxGenJS mutates them in-place (converting values to EMU). Use factory functions that return fresh objects each time.
6. **Gradient fills are NOT supported** — Use a gradient image as a slide/shape background instead.

## Key API

### Text

```javascript
// Simple text
slide.addText("Headline", {
  x: 0.8, y: 0.8, w: 8.4, h: 1,
  fontSize: 54, fontFace: "Arial", color: "1A1A1A",
  bold: true
});

// Multi-line with formatting
slide.addText([
  { text: "First line", options: { fontSize: 28, bold: true, color: "1A1A1A", breakLine: true } },
  { text: "Second line", options: { fontSize: 20, color: "666666" } }
], { x: 0.8, y: 2.5, w: 8.4, h: 2 });

// Bullets
slide.addText([
  { text: "Point one", options: { bullet: true, breakLine: true } },
  { text: "Point two", options: { bullet: true, breakLine: true } },
  { text: "Point three", options: { bullet: true } }
], { x: 0.8, y: 1.5, w: 8.4, h: 3, fontSize: 24, color: "333333" });
```

### Shapes

```javascript
// Rectangle (for backgrounds, dividers, accent bars)
slide.addShape(pres.ShapeType.rect, {
  x: 0, y: 0, w: 10, h: 2,
  fill: { color: "1A1A2E" }
});

// Rounded rectangle
slide.addShape(pres.ShapeType.roundRect, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "F0F0F0" },
  rectRadius: 0.1
});

// Line
slide.addShape(pres.ShapeType.line, {
  x: 0.8, y: 3, w: 8.4, h: 0,
  line: { color: "CCCCCC", width: 1 }
});
```

### Images

```javascript
// From file path
slide.addImage({ path: "photo.jpg", x: 0, y: 0, w: 10, h: 5.625 });

// From base64
slide.addImage({ data: "image/png;base64,...", x: 1, y: 1, w: 4, h: 3 });
```

### Charts

```javascript
// Bar chart
slide.addChart(pres.charts.BAR, [
  { name: "Revenue", labels: ["Q1", "Q2", "Q3", "Q4"], values: [100, 120, 140, 180] }
], {
  x: 0.8, y: 1.5, w: 8.4, h: 3.5,
  showTitle: false,
  showValue: true,
  chartColors: ["4472C4"]
});

// Available chart types: BAR, BAR3D, LINE, PIE, DOUGHNUT, SCATTER, AREA, BUBBLE
```

### Tables

```javascript
let rows = [
  [
    { text: "Metric", options: { bold: true, fill: { color: "1A1A2E" }, color: "FFFFFF" } },
    { text: "Value", options: { bold: true, fill: { color: "1A1A2E" }, color: "FFFFFF" } }
  ],
  [{ text: "Revenue" }, { text: "$2.4M" }],
  [{ text: "Growth" }, { text: "+40%" }]
];

slide.addTable(rows, {
  x: 0.8, y: 1.5, w: 8.4,
  fontSize: 18, color: "333333",
  border: { type: "solid", pt: 0.5, color: "E0E0E0" },
  colW: [4.2, 4.2],
  autoPage: false
});
```

### Slide Backgrounds

```javascript
// Solid color
slide.background = { color: "1A1A2E" };

// Image (full-bleed)
slide.background = { path: "background.jpg" };
```

### Speaker Notes

```javascript
slide.addNotes("Key talking point: Revenue grew 40% driven by enterprise segment.");
```

## Icons via react-icons

Render any icon from react-icons as a PNG for embedding in slides:

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

function renderIconSvg(Icon, color = "000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(Icon, { color: "#" + color, size: String(size) })
  );
}

async function iconToBase64Png(Icon, color, size = 256) {
  const svg = renderIconSvg(Icon, color, size);
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + png.toString("base64");
}

// Usage:
const { FaCheckCircle } = require("react-icons/fa");
const iconData = await iconToBase64Png(FaCheckCircle, "4CAF50", 128);
slide.addImage({ data: iconData, x: 1, y: 1, w: 0.5, h: 0.5 });
```

## Web-Safe Fonts

Only use fonts guaranteed to render correctly:
- Arial, Helvetica
- Times New Roman, Georgia
- Courier New
- Verdana, Tahoma
- Trebuchet MS
- Impact

## PDF Export and Visual Validation

After generating a .pptx, always produce a PDF copy and convert slides to images for visual review.

**All output goes into the deck folder** (`decks/<name>/`):
- Generation script: `<name>.js`
- PowerPoint: `<name>.pptx`
- PDF: `<name>.pdf`
- Slide images: `slides/slide-01.jpg`, `slides/slide-02.jpg`, etc.
- Thumbnail grid: `slides/thumbnails.jpg`

Run generation from within the deck folder: `cd decks/<name> && node <name>.js`

Try these approaches in order based on what's available.

### Option A: PowerPoint on macOS

```bash
rm -rf slides && mkdir -p slides
osascript -e '
  tell application "Microsoft PowerPoint"
    set pptxPath to POSIX file "'"$(pwd)/<name>.pptx"'"
    open pptxPath
    save active presentation in POSIX file "'"$(pwd)/<name>.pdf"'" as save as PDF
    save active presentation in POSIX file "'"$(pwd)/slides/slide"'" as save as PNG
    close active presentation
  end tell'
```

This creates `<name>.pdf` and `slides/slide-01.png`, `slides/slide-02.png`, etc.

Replace `<name>` with the actual deck name (e.g., `quarterly-review`).

### Option B: LibreOffice + Poppler

```bash
rm -rf slides && mkdir -p slides

# Convert .pptx to PDF via LibreOffice
soffice --headless --convert-to pdf <name>.pptx

# Convert PDF pages to JPEG images
pdftoppm -jpeg -r 150 <name>.pdf slides/slide
# Creates slides/slide-01.jpg, slides/slide-02.jpg, etc.
```

### Creating the thumbnail grid

Once slide images exist (from either option), create the grid:

```python
from PIL import Image
import glob, math

images = sorted(glob.glob("slides/slide-*.*"))
cols = 3
rows = math.ceil(len(images) / cols)

thumbs = [Image.open(img) for img in images]
tw, th = thumbs[0].size
grid = Image.new("RGB", (tw * cols, th * rows), "white")

for i, thumb in enumerate(thumbs):
    grid.paste(thumb, ((i % cols) * tw, (i // cols) * th))

grid.save("slides/thumbnails.jpg")
```

### If no conversion tools are available

Deliver the .pptx and ask the user to open it and provide feedback. Skip automated visual validation.

## Workflow Summary

1. Install dependencies (`npm install pptxgenjs`)
2. Create a `.js` file that builds the presentation using the API above
3. Run with `node` to generate the `.pptx`
4. Generate thumbnail grid for visual validation
5. Review, fix, and regenerate until all slides pass
