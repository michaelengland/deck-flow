#!/usr/bin/env python3
"""Reverse-engineer a .pptx file into a PptxGenJS generation script.

Usage:
    python pptx-to-js.py <input.pptx> [--deck-dir decks/<name>]

Produces a JavaScript file that, when run with `node`, reproduces the
presentation using PptxGenJS. Embedded images are extracted to the assets
directory.
"""

import argparse
import hashlib
import math
import os
import re
import sys
from collections import OrderedDict

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EMU_PER_INCH = 914400

WEB_SAFE_FONTS = {
    "Arial", "Helvetica", "Times New Roman", "Georgia",
    "Courier New", "Verdana", "Tahoma", "Trebuchet MS", "Impact",
}

FONT_MAP = {
    # Sans-serif
    "Calibri": "Arial",
    "Segoe UI": "Arial",
    "Helvetica Neue": "Helvetica",
    "Open Sans": "Arial",
    "Lato": "Arial",
    "Roboto": "Arial",
    "Source Sans Pro": "Arial",
    "Noto Sans": "Arial",
    "SF Pro Display": "Helvetica",
    "SF Pro Text": "Helvetica",
    # Serif
    "Cambria": "Georgia",
    "Garamond": "Georgia",
    "Palatino": "Georgia",
    "Palatino Linotype": "Georgia",
    "Book Antiqua": "Georgia",
    # Mono
    "Consolas": "Courier New",
    "Menlo": "Courier New",
    "Monaco": "Courier New",
    "Source Code Pro": "Courier New",
}

ALIGNMENT_MAP = {
    PP_ALIGN.LEFT: "left",
    PP_ALIGN.CENTER: "center",
    PP_ALIGN.RIGHT: "right",
    PP_ALIGN.JUSTIFY: "justify",
}

# PptxGenJS ShapeType names for the shapes we can map
SHAPE_TYPE_MAP = {
    1: "rect",           # MSO_SHAPE.RECTANGLE
    5: "roundRect",      # MSO_SHAPE.ROUNDED_RECTANGLE
    9: "ellipse",        # MSO_SHAPE.OVAL
    20: "line",          # MSO_SHAPE.LINE (not exact, but covers most)
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def emu_to_inches(emu):
    """Convert EMU to inches, rounded to 2 decimal places."""
    if emu is None:
        return 0
    return round(int(emu) / EMU_PER_INCH, 2)


def pt_to_num(pt_val):
    """Convert a python-pptx Pt/Emu value to numeric points."""
    if pt_val is None:
        return None
    if hasattr(pt_val, "pt"):
        return round(pt_val.pt, 1)
    return round(float(pt_val) / 12700, 1)  # EMU to pt


def color_to_hex(color_obj):
    """Extract hex color string (no #) from a python-pptx color object.

    Returns None if the color cannot be resolved.
    """
    if color_obj is None:
        return None
    try:
        if color_obj.type is not None:
            rgb = color_obj.rgb
            if rgb is not None:
                return str(rgb).upper()
        # Try theme color resolution
        if hasattr(color_obj, "theme_color") and color_obj.theme_color is not None:
            # We can't resolve theme colors without the theme XML, so try rgb anyway
            try:
                rgb = color_obj.rgb
                if rgb is not None:
                    return str(rgb).upper()
            except Exception:
                pass
            return None
    except (AttributeError, TypeError):
        return None
    return None


def safe_font(font_name, warnings):
    """Map a font name to a web-safe equivalent.

    Appends a warning if mapping occurs.
    """
    if font_name is None:
        return "Arial"
    if font_name in WEB_SAFE_FONTS:
        return font_name
    mapped = FONT_MAP.get(font_name)
    if mapped:
        warnings.append(f"Font \"{font_name}\" mapped to \"{mapped}\" (web-safe)")
        return mapped
    warnings.append(f"Font \"{font_name}\" not recognized — mapped to \"Arial\"")
    return "Arial"


def slugify(name):
    """Convert a filename to a clean lowercase slug.

    'My Presentation (Final)' -> 'my-presentation-final'
    """
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-")


def js_string(s):
    """Escape a string for safe inclusion in JavaScript source."""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    s = s.replace("\n", "\\n")
    s = s.replace("\r", "")
    s = s.replace("\t", "\\t")
    return f'"{s}"'


def indent(code, level=2):
    """Indent lines of code by the given number of spaces."""
    prefix = " " * level
    return "\n".join(prefix + line if line.strip() else "" for line in code.split("\n"))


# ---------------------------------------------------------------------------
# Image extraction
# ---------------------------------------------------------------------------

def extract_images(prs, assets_dir):
    """Extract embedded images from the presentation.

    Returns a dict mapping python id(shape) -> relative asset path
    (relative to the deck folder, e.g. "assets/slide1_abc123.jpg").
    """
    os.makedirs(assets_dir, exist_ok=True)
    image_map = {}
    seen_hashes = {}

    for slide_idx, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                try:
                    blob = shape.image.blob
                    content_type = shape.image.content_type
                except Exception:
                    continue

                # Deduplicate by content hash
                blob_hash = hashlib.md5(blob).hexdigest()[:12]
                if blob_hash in seen_hashes:
                    image_map[id(shape)] = seen_hashes[blob_hash]
                    continue

                ext = content_type.split("/")[-1].lower()
                if ext == "jpeg":
                    ext = "jpg"
                elif ext not in ("png", "gif", "bmp", "svg+xml"):
                    ext = "png"
                if ext == "svg+xml":
                    ext = "svg"

                filename = f"slide{slide_idx + 1}_{blob_hash}.{ext}"
                filepath = os.path.join(assets_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(blob)

                # Store path relative to deck folder for use in generated JS
                relative_path = os.path.join("assets", filename)
                image_map[id(shape)] = relative_path
                seen_hashes[blob_hash] = relative_path

    return image_map


# ---------------------------------------------------------------------------
# Text processing
# ---------------------------------------------------------------------------

def has_bullet(paragraph):
    """Detect whether a paragraph has bullet formatting."""
    pPr = paragraph._p.find(
        "{http://schemas.openxmlformats.org/drawingml/2006/main}pPr"
    )
    if pPr is None:
        return False
    buNone = pPr.find(
        "{http://schemas.openxmlformats.org/drawingml/2006/main}buNone"
    )
    if buNone is not None:
        return False
    # Check for any bullet element
    for child in pPr:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        if tag.startswith("bu") and tag != "buNone":
            return True
    return False


def process_text_frame(text_frame, warnings):
    """Convert a text frame to PptxGenJS text array entries.

    Returns a list of dicts representing PptxGenJS text array items,
    or a simple string if the text is plain.
    """
    paragraphs = list(text_frame.paragraphs)
    if not paragraphs:
        return []

    entries = []
    for para_idx, para in enumerate(paragraphs):
        is_last_para = para_idx == len(paragraphs) - 1
        is_bullet = has_bullet(para)

        runs = list(para.runs)
        if not runs:
            # Empty paragraph — preserve as line break
            if not is_last_para:
                entries.append({"text": "", "options": {"breakLine": True}})
            continue

        for run_idx, run in enumerate(runs):
            is_last_run_in_para = run_idx == len(runs) - 1
            text = run.text
            if not text and not is_last_run_in_para:
                continue

            opts = {}
            font = run.font

            # Font properties
            if font.name:
                mapped = safe_font(font.name, warnings)
                opts["fontFace"] = mapped
            if font.size:
                opts["fontSize"] = pt_to_num(font.size)
            if font.bold:
                opts["bold"] = True
            if font.italic:
                opts["italic"] = True
            if font.underline:
                opts["underline"] = True

            # Color
            hex_color = color_to_hex(font.color)
            if hex_color:
                opts["color"] = hex_color

            # Bullet (on first run of paragraph only)
            if is_bullet and run_idx == 0:
                opts["bullet"] = True

            # Alignment (on first run of paragraph only)
            if run_idx == 0 and para.alignment and para.alignment in ALIGNMENT_MAP:
                opts["align"] = ALIGNMENT_MAP[para.alignment]

            # Break line after last run of each paragraph (except the very last)
            if is_last_run_in_para and not is_last_para:
                opts["breakLine"] = True

            entries.append({"text": text, "options": opts})

    return entries


# ---------------------------------------------------------------------------
# Shape processing
# ---------------------------------------------------------------------------

def get_fill_props(fill):
    """Extract fill properties from a shape's fill.

    Returns a dict for PptxGenJS fill property, or None.
    """
    try:
        fill_type = fill.type
    except Exception:
        return None

    if fill_type is None:
        return None

    # Solid fill
    from pptx.enum.dml import MSO_THEME_COLOR
    try:
        if fill.type is not None:
            rgb = fill.fore_color.rgb
            if rgb:
                return {"color": str(rgb).upper()}
    except Exception:
        pass

    return None


def get_line_props(line):
    """Extract line properties from a shape's line.

    Returns a dict for PptxGenJS line property, or None.
    """
    try:
        if line.fill.type is None and line.width is None:
            return None
    except Exception:
        return None

    props = {}
    try:
        if line.color and line.color.rgb:
            props["color"] = str(line.color.rgb).upper()
    except Exception:
        pass

    if line.width:
        # Line width in points
        props["width"] = round(line.width.pt, 1)

    return props if props else None


def process_auto_shape(shape, warnings):
    """Convert an auto shape to PptxGenJS code lines."""
    lines = []

    # Determine shape type
    shape_id = None
    try:
        if hasattr(shape, "auto_shape_type") and shape.auto_shape_type is not None:
            shape_id = int(shape.auto_shape_type)
    except Exception:
        pass

    pptx_shape = SHAPE_TYPE_MAP.get(shape_id, "rect")

    x = emu_to_inches(shape.left)
    y = emu_to_inches(shape.top)
    w = emu_to_inches(shape.width)
    h = emu_to_inches(shape.height)

    opts = OrderedDict()
    opts["x"] = x
    opts["y"] = y
    opts["w"] = w
    opts["h"] = h

    # Fill
    try:
        fill_props = get_fill_props(shape.fill)
        if fill_props:
            opts["fill"] = fill_props
    except Exception:
        pass

    # Line
    try:
        line_props = get_line_props(shape.line)
        if line_props:
            opts["line"] = line_props
    except Exception:
        pass

    # Rounded corners
    if pptx_shape == "roundRect":
        opts["rectRadius"] = 0.1  # Default; python-pptx doesn't expose adjustment values easily

    # Rotation
    if shape.rotation and shape.rotation != 0:
        opts["rotate"] = round(shape.rotation, 1)

    # Check if shape has text
    if shape.has_text_frame and shape.text_frame.text.strip():
        text_entries = process_text_frame(shape.text_frame, warnings)
        if text_entries:
            # Text shape — use addText with shape fill
            text_opts = OrderedDict()
            text_opts["x"] = x
            text_opts["y"] = y
            text_opts["w"] = w
            text_opts["h"] = h
            if "fill" in opts:
                text_opts["fill"] = opts["fill"]
            if "line" in opts:
                text_opts["line"] = opts["line"]
            if pptx_shape == "roundRect":
                text_opts["shape"] = "__SHAPE_ROUND_RECT__"
                text_opts["rectRadius"] = 0.1
            if shape.rotation and shape.rotation != 0:
                text_opts["rotate"] = round(shape.rotation, 1)

            # Vertical alignment
            try:
                anchor = shape.text_frame.word_wrap
            except Exception:
                pass
            try:
                from pptx.enum.text import MSO_ANCHOR
                va = shape.text_frame.paragraphs[0]._p.getparent().attrib.get("anchor")
                if va == "ctr":
                    text_opts["valign"] = "middle"
                elif va == "b":
                    text_opts["valign"] = "bottom"
            except Exception:
                pass

            lines.append(format_add_text(text_entries, text_opts))
            return "\n".join(lines)

    # No text — pure shape
    lines.append(f"  slide.addShape(pres.ShapeType.{pptx_shape}, {format_opts(opts)});")
    return "\n".join(lines)


def process_picture(shape, image_map, warnings):
    """Convert a picture shape to PptxGenJS addImage call."""
    path = image_map.get(id(shape))
    if not path:
        return f"  // WARNING: Could not extract image from this shape"

    x = emu_to_inches(shape.left)
    y = emu_to_inches(shape.top)
    w = emu_to_inches(shape.width)
    h = emu_to_inches(shape.height)

    opts = OrderedDict()
    opts["path"] = path
    opts["x"] = x
    opts["y"] = y
    opts["w"] = w
    opts["h"] = h

    if shape.rotation and shape.rotation != 0:
        opts["rotate"] = round(shape.rotation, 1)

    return f"  slide.addImage({format_opts(opts)});"


def process_table(shape, warnings):
    """Convert a table shape to PptxGenJS addTable call."""
    table = shape.table
    lines = []
    lines.append("  let rows = [")

    for row_idx, row in enumerate(table.rows):
        cells = []
        for cell in row.cells:
            cell_opts = OrderedDict()
            cell_opts["text"] = cell.text.strip()

            # Cell fill
            try:
                fill_props = get_fill_props(cell.fill)
                if fill_props:
                    cell_opts["options"] = {"fill": fill_props}
            except Exception:
                pass

            # Bold text in cell
            try:
                for para in cell.text_frame.paragraphs:
                    for run in para.runs:
                        if run.font.bold:
                            if "options" not in cell_opts:
                                cell_opts["options"] = {}
                            cell_opts["options"]["bold"] = True
                            break
                    if "options" in cell_opts and cell_opts["options"].get("bold"):
                        break
            except Exception:
                pass

            # Font color
            try:
                for para in cell.text_frame.paragraphs:
                    for run in para.runs:
                        hex_color = color_to_hex(run.font.color)
                        if hex_color:
                            if "options" not in cell_opts:
                                cell_opts["options"] = {}
                            cell_opts["options"]["color"] = hex_color
                            break
                    break
            except Exception:
                pass

            cells.append(cell_opts)

        # Format the row
        row_str = "    ["
        cell_strs = []
        for c in cells:
            if "options" in c:
                cell_strs.append(
                    f'{{ text: {js_string(c["text"])}, options: {format_opts(c["options"])} }}'
                )
            else:
                cell_strs.append(f'{{ text: {js_string(c["text"])} }}')
        row_str += ", ".join(cell_strs) + "]"
        if row_idx < len(table.rows) - 1:
            row_str += ","
        lines.append(row_str)

    lines.append("  ];")

    x = emu_to_inches(shape.left)
    y = emu_to_inches(shape.top)
    w = emu_to_inches(shape.width)

    table_opts = OrderedDict()
    table_opts["x"] = x
    table_opts["y"] = y
    table_opts["w"] = w
    table_opts["fontSize"] = 14
    table_opts["border"] = {"type": "solid", "pt": 0.5, "color": "E0E0E0"}
    table_opts["autoPage"] = False

    # Column widths
    col_count = len(table.columns)
    if col_count > 0:
        col_widths = [round(emu_to_inches(col.width), 2) for col in table.columns]
        table_opts["colW"] = col_widths

    lines.append(f"  slide.addTable(rows, {format_opts(table_opts)});")
    return "\n".join(lines)


def process_chart(shape, warnings):
    """Convert a chart shape to PptxGenJS addChart call.

    Only handles basic chart types. Returns a warning comment for complex charts.
    """
    try:
        chart = shape.chart
    except Exception:
        return "  // WARNING: Could not read chart data from this shape"

    x = emu_to_inches(shape.left)
    y = emu_to_inches(shape.top)
    w = emu_to_inches(shape.width)
    h = emu_to_inches(shape.height)

    # Try to extract chart data
    try:
        chart_type_name = str(chart.chart_type).split("(")[0].strip()
    except Exception:
        chart_type_name = "UNKNOWN"

    # Map chart types
    pptx_to_pptxgen = {
        "COLUMN_CLUSTERED": "BAR",
        "COLUMN_STACKED": "BAR",
        "BAR_CLUSTERED": "BAR",
        "BAR_STACKED": "BAR",
        "LINE": "LINE",
        "LINE_MARKERS": "LINE",
        "PIE": "PIE",
        "DOUGHNUT": "DOUGHNUT",
        "AREA": "AREA",
        "XY_SCATTER": "SCATTER",
    }

    js_chart_type = None
    for key, val in pptx_to_pptxgen.items():
        if key in chart_type_name.upper():
            js_chart_type = val
            break

    if not js_chart_type:
        warnings.append(f"Chart type \"{chart_type_name}\" not supported — skipped")
        return f"  // WARNING: Chart type \"{chart_type_name}\" not supported by PptxGenJS — skipped"

    # Extract series data
    lines = []
    try:
        series_data = []
        for series in chart.series:
            name = series.name if hasattr(series, "name") else "Series"
            values = list(series.values)

            # Try to get category labels
            labels = []
            try:
                for cat in chart.plots[0].categories:
                    labels.append(str(cat))
            except Exception:
                labels = [f"Cat{i+1}" for i in range(len(values))]

            series_data.append({"name": name, "labels": labels, "values": values})

        lines.append("  slide.addChart(pres.charts." + js_chart_type + ", [")
        for s_idx, s in enumerate(series_data):
            comma = "," if s_idx < len(series_data) - 1 else ""
            labels_str = ", ".join(js_string(l) for l in s["labels"])
            values_str = ", ".join(str(v) for v in s["values"])
            lines.append(
                f'    {{ name: {js_string(s["name"])}, labels: [{labels_str}], values: [{values_str}] }}{comma}'
            )
        lines.append("  ], {")
        lines.append(f"    x: {x}, y: {y}, w: {w}, h: {h},")
        lines.append("    showTitle: false,")
        lines.append("    showValue: true")
        lines.append("  });")
    except Exception as e:
        warnings.append(f"Could not extract chart data: {e}")
        return f"  // WARNING: Could not extract data from chart — {e}"

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_opts(opts):
    """Format a dict as a JavaScript object literal."""
    if not opts:
        return "{}"

    parts = []
    for key, val in (opts.items() if isinstance(opts, OrderedDict) else sorted(opts.items())):
        parts.append(f"{key}: {format_js_value(val)}")
    return "{ " + ", ".join(parts) + " }"


def format_js_value(val):
    """Format a Python value as a JavaScript literal."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return "true" if val else "false"
    if isinstance(val, (int, float)):
        # Clean up .0 floats
        if isinstance(val, float) and val == int(val):
            return str(int(val))
        return str(val)
    if isinstance(val, str):
        if val.startswith("__") and val.endswith("__"):
            # Special marker for JS references
            ref = val.strip("_")
            if ref == "SHAPE_ROUND_RECT":
                return "pres.ShapeType.roundRect"
            return val
        return js_string(val)
    if isinstance(val, list):
        items = ", ".join(format_js_value(v) for v in val)
        return f"[{items}]"
    if isinstance(val, dict):
        return format_opts(val)
    return str(val)


def format_add_text(entries, container_opts):
    """Format a PptxGenJS addText call with text array and container options."""
    if len(entries) == 1 and not entries[0].get("options"):
        # Simple string text
        return f"  slide.addText({js_string(entries[0]['text'])}, {format_opts(container_opts)});"

    lines = []
    lines.append("  slide.addText([")
    for i, entry in enumerate(entries):
        comma = "," if i < len(entries) - 1 else ""
        opts = entry.get("options", {})
        if opts:
            lines.append(
                f"    {{ text: {js_string(entry['text'])}, options: {format_opts(opts)} }}{comma}"
            )
        else:
            lines.append(f"    {{ text: {js_string(entry['text'])} }}{comma}")
    lines.append(f"  ], {format_opts(container_opts)});")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Slide processing
# ---------------------------------------------------------------------------

def get_slide_title(slide):
    """Extract a title or first significant text from a slide."""
    # Try placeholders first
    for shape in slide.placeholders:
        try:
            if shape.placeholder_format.type == PP_PLACEHOLDER.TITLE:
                return shape.text.strip()[:60]
        except Exception:
            pass
        try:
            if shape.placeholder_format.type == PP_PLACEHOLDER.CENTER_TITLE:
                return shape.text.strip()[:60]
        except Exception:
            pass

    # Fall back to first text shape with content
    for shape in slide.shapes:
        if shape.has_text_frame and shape.text_frame.text.strip():
            return shape.text_frame.text.strip()[:60]

    return "Untitled"


def process_slide(slide, slide_idx, image_map, warnings):
    """Generate the function body for a single slide.

    Returns a list of JS code lines (without the function wrapper).
    """
    lines = []

    # Background
    try:
        bg = slide.background
        bg_fill = bg.fill
        if bg_fill.type is not None:
            try:
                rgb = bg_fill.fore_color.rgb
                if rgb:
                    hex_color = str(rgb).upper()
                    lines.append(f'  slide.background = {{ color: "{hex_color}" }};')
            except Exception:
                pass
    except Exception:
        pass

    # Process shapes in order (z-index)
    for shape in slide.shapes:
        shape_type = shape.shape_type

        try:
            if shape_type == MSO_SHAPE_TYPE.PICTURE:
                lines.append(process_picture(shape, image_map, warnings))

            elif shape_type == MSO_SHAPE_TYPE.TABLE:
                lines.append(process_table(shape, warnings))

            elif shape_type == MSO_SHAPE_TYPE.CHART:
                lines.append(process_chart(shape, warnings))

            elif shape_type == MSO_SHAPE_TYPE.GROUP:
                # Attempt to process group members individually
                lines.append("  // Group shape — processing members individually")
                try:
                    for group_shape in shape.shapes:
                        if group_shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                            lines.append(process_picture(group_shape, image_map, warnings))
                        elif hasattr(group_shape, "has_text_frame"):
                            lines.append(process_auto_shape(group_shape, warnings))
                except Exception:
                    warnings.append("Could not fully process a group shape")
                    lines.append("  // WARNING: Could not fully extract group shape contents")

            elif hasattr(shape, "has_text_frame"):
                # Auto shapes, text boxes, placeholders
                lines.append(process_auto_shape(shape, warnings))

            else:
                lines.append(f"  // Skipped unsupported shape type: {shape_type}")

        except Exception as e:
            lines.append(f"  // WARNING: Error processing shape — {e}")

    # Speaker notes
    try:
        if slide.has_notes_slide:
            notes_text = slide.notes_slide.notes_text_frame.text.strip()
            if notes_text:
                lines.append(f"  slide.addNotes({js_string(notes_text)});")
    except Exception:
        pass

    return lines


# ---------------------------------------------------------------------------
# JS assembly
# ---------------------------------------------------------------------------

def generate_js(prs, image_map, output_path, pptx_filename, warnings):
    """Assemble the full JavaScript file."""
    slide_count = len(prs.slides)
    lines = []

    # Header
    lines.append('const pptxgen = require("pptxgenjs");')
    lines.append("")
    lines.append("let pres = new pptxgen();")
    lines.append('pres.layout = "LAYOUT_16x9";')
    lines.append("")

    # Warnings summary
    if warnings:
        lines.append("// === Import Warnings ===")
        for w in warnings:
            lines.append(f"// WARNING: {w}")
        lines.append("")

    # One function per slide
    titles = []
    for slide_idx, slide in enumerate(prs.slides):
        num = slide_idx + 1
        title = get_slide_title(slide)
        titles.append(title)

        lines.append(f"// --- Slide {num}: {title} ---")
        lines.append(f"function createSlide{num}(pres) {{")
        lines.append("  let slide = pres.addSlide();")

        slide_lines = process_slide(slide, slide_idx, image_map, warnings)
        lines.extend(slide_lines)

        lines.append("}")
        lines.append("")

    # Build section
    lines.append("// --- Build presentation ---")
    for i in range(slide_count):
        lines.append(f"createSlide{i + 1}(pres);")
    lines.append("")
    lines.append(f'pres.writeFile({{ fileName: {js_string(pptx_filename)} }});')

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Reverse-engineer a .pptx into a PptxGenJS generation script."
    )
    parser.add_argument("input", help="Path to the .pptx file")
    parser.add_argument(
        "--deck-dir", "-d",
        default=None,
        help="Deck output directory (default: decks/<name>)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not args.input.lower().endswith(".pptx"):
        print(f"Error: Expected a .pptx file, got: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Derive paths from input filename
    base_name = slugify(os.path.splitext(os.path.basename(args.input))[0])
    deck_dir = args.deck_dir or os.path.join("decks", base_name)
    js_path = os.path.join(deck_dir, base_name + ".js")
    assets_dir = os.path.join(deck_dir, "assets")
    pptx_filename = base_name + ".pptx"

    os.makedirs(deck_dir, exist_ok=True)

    print(f"Reading: {args.input}")
    print(f"Deck folder: {deck_dir}/")
    prs = Presentation(args.input)
    print(f"Found {len(prs.slides)} slides")

    warnings = []

    # Extract images
    image_map = extract_images(prs, assets_dir)
    if image_map:
        print(f"Extracted {len(image_map)} images to {assets_dir}/")

    # Generate JS (uses relative paths — run from within the deck folder)
    js_code = generate_js(prs, image_map, js_path, pptx_filename, warnings)

    # Write output
    with open(js_path, "w") as f:
        f.write(js_code)
    print(f"Generated: {js_path}")

    # Print warnings summary
    if warnings:
        # Deduplicate
        unique_warnings = list(dict.fromkeys(warnings))
        print(f"\n{len(unique_warnings)} warning(s):")
        for w in unique_warnings:
            print(f"  - {w}")

    print(f"\nDone. Run with: cd {deck_dir} && node {base_name}.js")


if __name__ == "__main__":
    main()
