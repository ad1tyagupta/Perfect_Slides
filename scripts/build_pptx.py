#!/usr/bin/env python3
"""
Build an editable .pptx from a deck.json spec.

Every element becomes a native PowerPoint shape, text box, table or chart.
Nothing is a screenshot. The recipient can edit any of it, and chart data
stays live inside the file.

Usage:
    python build_pptx.py deck.json out.pptx

Requires:
    pip install python-pptx
"""

import json
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.util import Emu, Pt
except ImportError:
    print("Needs python-pptx.\n"
          "  pip install python-pptx\n"
          "or install everything at once:\n"
          "  pip install -r requirements.txt")
    sys.exit(2)

# --- Geometry -------------------------------------------------------------
# Decks are authored on a 1920x1080 stage. PowerPoint 16:9 is 13.333 x 7.5in.
# 1920 px maps to 12192000 EMU, so one stage pixel is exactly 6350 EMU.
EMU_PER_PX = 6350
STAGE_W, STAGE_H = 1920, 1080


def px(v):
    """Stage pixels to EMU."""
    return Emu(int(v * EMU_PER_PX))


def pt(v):
    """Stage pixels to points. 1920px wide slide is 960pt wide, so half."""
    return Pt(v * 0.5)


def rgb(hex_str):
    h = hex_str.lstrip('#')
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# --- Defaults -------------------------------------------------------------
THEME_FALLBACK = {
    "colors": {
        "bg": "#0E2635", "ink": "#EAF4F8", "accent": "#00A8D8",
        "muted": "#8FB2C0", "panel": "#173B4F", "on_accent": "#062130",
    },
    # body_safe / display_safe are what PowerPoint uses when the real font is
    # missing on the viewer's machine. Always name something widely installed.
    "fonts": {
        "display": "Georgia", "display_safe": "Georgia",
        "body": "Calibri", "body_safe": "Calibri",
    },
}


class DeckBuilder:
    def __init__(self, spec):
        self.spec = spec
        self.theme = self._merge_theme(spec.get("theme", {}))
        self.c = self.theme["colors"]
        self.f = self.theme["fonts"]

        self.prs = Presentation()
        self.prs.slide_width = px(STAGE_W)
        self.prs.slide_height = px(STAGE_H)
        self.blank = self.prs.slide_layouts[6]

    @staticmethod
    def _merge_theme(theme):
        merged = {k: dict(v) for k, v in THEME_FALLBACK.items()}
        for key in ("colors", "fonts"):
            merged[key].update(theme.get(key, {}))
        # If no safe font was named, fall back to the real one.
        merged["fonts"].setdefault("display_safe", merged["fonts"]["display"])
        merged["fonts"].setdefault("body_safe", merged["fonts"]["body"])
        return merged

    # --- Primitives -------------------------------------------------------
    def _bg(self, slide, colour=None):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = rgb(colour or self.c["bg"])

    def _text(self, slide, x, y, w, h, text, *, size=28, bold=False,
              colour=None, font=None, align="left", italic=False,
              line_spacing=1.2, anchor="top", shrink=True):
        box = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                              "bottom": MSO_ANCHOR.BOTTOM}[anchor]
        if shrink:
            # Last-resort guard. Layout should already fit; this stops a long
            # translation from silently overflowing the box.
            tf.auto_size = None

        for i, line in enumerate(str(text).split("\n")):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER,
                              "right": PP_ALIGN.RIGHT}[align]
            para.line_spacing = line_spacing
            run = para.add_run()
            run.text = line
            run.font.size = pt(size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.name = font or self.f["body_safe"]
            run.font.color.rgb = rgb(colour or self.c["ink"])
        return box

    def _rect(self, slide, x, y, w, h, colour, *, radius=False, line=None):
        shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
        shp = slide.shapes.add_shape(shape_type, px(x), px(y), px(w), px(h))
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(colour)
        if line:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(1)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
        if shp.has_text_frame:
            shp.text_frame.clear()
        return shp

    def _accent_rule(self, slide, x, y, w=6, h=60):
        self._rect(slide, x, y, w, h, self.c["accent"])

    def _headline(self, slide, text, *, y=92, kicker=None):
        if kicker:
            self._text(slide, 92, y - 42, 1200, 40, kicker.upper(),
                       size=20, bold=True, colour=self.c["accent"])
        self._text(slide, 92, y, 1620, 180, text,
                   size=58, bold=True, font=self.f["display_safe"],
                   line_spacing=1.05)

    def _source(self, slide, text):
        if not text:
            return
        self._text(slide, 92, 990, 1500, 40, text,
                   size=17, colour=self.c["muted"])

    def _notes(self, slide, text):
        if text:
            slide.notes_slide.notes_text_frame.text = text

    # --- Layouts ----------------------------------------------------------
    def layout_title(self, slide, s):
        self._bg(slide)
        self._text(slide, 110, 300, 1400, 60, s.get("kicker", "").upper(),
                   size=26, bold=True, colour=self.c["accent"])
        self._text(slide, 110, 370, 1500, 320, s["headline"],
                   size=112, bold=True, font=self.f["display_safe"], line_spacing=1.0)
        if s.get("subhead"):
            self._text(slide, 110, 720, 1200, 140, s["subhead"],
                       size=30, colour=self.c["muted"], line_spacing=1.4)
        meta = " · ".join(filter(None, [
            self.spec["meta"].get("author"), self.spec["meta"].get("date")
        ]))
        if meta:
            self._text(slide, 110, 940, 1400, 50, meta, size=22, colour=self.c["ink"])

    def layout_section(self, slide, s):
        self._bg(slide, self.c["accent"])
        self._text(slide, 110, 420, 1700, 240, s["headline"],
                   size=96, bold=True, font=self.f["display_safe"],
                   colour=self.c.get("on_accent", "#FFFFFF"), line_spacing=1.05)
        if s.get("subhead"):
            self._text(slide, 110, 690, 1300, 100, s["subhead"], size=28,
                       colour=self.c.get("on_accent", "#FFFFFF"))

    def layout_statement(self, slide, s):
        self._bg(slide)
        has_sub = bool(s.get("subhead"))
        top = 330 if has_sub else 380

        if s.get("kicker"):
            self._text(slide, 160, top - 70, 1400, 50, s["kicker"].upper(),
                       size=24, bold=True, colour=self.c["accent"])

        self._accent_rule(slide, 110, top + 20, 8, 200)
        self._text(slide, 160, top, 1600, 300, s["headline"],
                   size=76, bold=True, font=self.f["display_safe"],
                   line_spacing=1.15, anchor="middle")

        if has_sub:
            self._text(slide, 160, top + 320, 1300, 180, s["subhead"],
                       size=30, colour=self.c["muted"], line_spacing=1.45)

        self._source(slide, s.get("source"))

    def layout_stats(self, slide, s):
        self._bg(slide)
        self._headline(slide, s["headline"], kicker=s.get("kicker"))
        items = s["body"]["items"][:3]
        col_w = (STAGE_W - 184 - 60 * (len(items) - 1)) / len(items)

        for i, item in enumerate(items):
            x = 92 + i * (col_w + 60)
            self._accent_rule(slide, x, 400, 5, 200)
            self._text(slide, x + 28, 380, col_w - 28, 150, item["value"],
                       size=110, bold=True, font=self.f["display_safe"])
            self._text(slide, x + 28, 540, col_w - 28, 140, item["label"],
                       size=24, colour=self.c["muted"], line_spacing=1.35)
        self._source(slide, s.get("source"))

    def layout_bullets(self, slide, s):
        self._bg(slide)
        self._headline(slide, s["headline"], kicker=s.get("kicker"))
        y = 340
        for point in s["body"]["points"]:
            self._rect(slide, 96, y + 16, 14, 14, self.c["accent"], radius=True)
            self._text(slide, 136, y, 1500, 80, point, size=30, line_spacing=1.3)
            y += 92
        self._source(slide, s.get("source"))

    def layout_quote(self, slide, s):
        self._bg(slide)
        self._text(slide, 140, 320, 1640, 320, f'"{s["body"]["quote"]}"',
                   size=64, italic=True, font=self.f["display_safe"], line_spacing=1.25)
        attribution = s["body"].get("attribution")
        if attribution:
            self._text(slide, 140, 700, 1200, 60, attribution,
                       size=26, colour=self.c["accent"], bold=True)

    def layout_cards(self, slide, s):
        self._bg(slide)
        self._headline(slide, s["headline"], kicker=s.get("kicker"))
        cards = s["body"]["cards"][:6]
        cols = 3 if len(cards) > 2 else len(cards)
        rows = -(-len(cards) // cols)
        cw = (STAGE_W - 184 - 30 * (cols - 1)) / cols
        ch = (620 - 30 * (rows - 1)) / rows

        for i, card in enumerate(cards):
            x = 92 + (i % cols) * (cw + 30)
            y = 340 + (i // cols) * (ch + 30)
            self._rect(slide, x, y, cw, ch, self.c["panel"],
                       radius=True, line=self.c["accent"])
            self._text(slide, x + 32, y + 30, cw - 64, 90, card["title"],
                       size=32, bold=True, font=self.f["display_safe"])
            if card.get("detail"):
                self._text(slide, x + 32, y + 128, cw - 64, ch - 160, card["detail"],
                           size=22, colour=self.c["muted"], line_spacing=1.35)
        self._source(slide, s.get("source"))

    def layout_timeline(self, slide, s):
        self._bg(slide)
        self._headline(slide, s["headline"], kicker=s.get("kicker"))
        events = s["body"]["events"]
        self._rect(slide, 120, 620, STAGE_W - 240, 4, self.c["muted"])
        step = (STAGE_W - 240) / max(len(events) - 1, 1)

        for i, ev in enumerate(events):
            x = 120 + i * step
            last = i == len(events) - 1
            self._rect(slide, x - 13, 609, 26, 26,
                       self.c["accent"] if last else self.c["bg"],
                       radius=True, line=self.c["accent"])
            self._text(slide, x - 130, 500, 260, 50, ev["when"],
                       size=22, bold=True, colour=self.c["accent"], align="center")
            self._text(slide, x - 130, 670, 260, 160, ev["what"],
                       size=26, align="center", line_spacing=1.25)
        self._source(slide, s.get("source"))

    def layout_table(self, slide, s):
        self._bg(slide)
        self._headline(slide, s["headline"], kicker=s.get("kicker"))
        headers = s["body"]["headers"]
        rows = s["body"]["rows"]

        shape = slide.shapes.add_table(
            len(rows) + 1, len(headers), px(92), px(340),
            px(STAGE_W - 184), px(min(600, 70 * (len(rows) + 1)))
        )
        table = shape.table

        for j, head in enumerate(headers):
            cell = table.cell(0, j)
            cell.text = str(head)
            para = cell.text_frame.paragraphs[0]
            para.runs[0].font.size = pt(24)
            para.runs[0].font.bold = True
            para.runs[0].font.color.rgb = rgb(self.c["accent"])
            para.runs[0].font.name = self.f["body_safe"]
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(self.c["bg"])

        for i, row in enumerate(rows, start=1):
            for j, val in enumerate(row):
                cell = table.cell(i, j)
                cell.text = str(val)
                para = cell.text_frame.paragraphs[0]
                para.runs[0].font.size = pt(22)
                para.runs[0].font.color.rgb = rgb(self.c["ink"])
                para.runs[0].font.name = self.f["body_safe"]
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb(self.c["panel"])
        self._source(slide, s.get("source"))

    def layout_chart(self, slide, s):
        """Native PowerPoint chart. The data stays editable inside the file."""
        self._bg(slide)
        self._headline(slide, s["headline"], kicker=s.get("kicker"))

        body = s["body"]
        kind = body.get("chart", "bar")
        chart_type = {
            "bar": XL_CHART_TYPE.COLUMN_CLUSTERED,
            "hbar": XL_CHART_TYPE.BAR_CLUSTERED,
            "line": XL_CHART_TYPE.LINE_MARKERS,
            "pie": XL_CHART_TYPE.PIE,
            "donut": XL_CHART_TYPE.DOUGHNUT,
            "area": XL_CHART_TYPE.AREA,
        }.get(kind, XL_CHART_TYPE.COLUMN_CLUSTERED)

        data = CategoryChartData()
        data.categories = body["categories"]
        for series in body["series"]:
            data.add_series(series["name"], series["values"])

        gf = slide.shapes.add_chart(
            chart_type, px(140), px(330), px(STAGE_W - 280), px(600), data
        )
        chart = gf.chart
        chart.has_title = False

        # One series needs no legend. The headline already says what it is.
        multi = len(body["series"]) > 1
        chart.has_legend = multi
        if multi:
            chart.legend.position = XL_LEGEND_POSITION.BOTTOM
            chart.legend.include_in_layout = False
            chart.legend.font.size = pt(20)
            chart.legend.font.color.rgb = rgb(self.c["muted"])

        palette = [self.c["accent"], self.c["muted"], self.c["panel"]]
        for i, plot_series in enumerate(chart.series):
            plot_series.format.fill.solid()
            plot_series.format.fill.fore_color.rgb = rgb(palette[i % len(palette)])

        if kind not in ("pie", "donut"):
            for axis in (chart.category_axis, chart.value_axis):
                axis.tick_labels.font.size = pt(20)
                axis.tick_labels.font.color.rgb = rgb(self.c["muted"])
                axis.tick_labels.font.name = self.f["body_safe"]
            chart.value_axis.has_major_gridlines = True

        self._source(slide, s.get("source"))

    def layout_image(self, slide, s):
        self._bg(slide)
        path = Path(s["body"]["path"])
        if not path.exists():
            self._text(slide, 92, 500, 1700, 100,
                       f"[missing image: {path}]", size=30, colour=self.c["muted"])
            return

        if s["body"].get("full_bleed"):
            slide.shapes.add_picture(str(path), 0, 0, px(STAGE_W), px(STAGE_H))
            if s.get("headline"):
                self._rect(slide, 0, 760, STAGE_W, 320, self.c["bg"])
                self._text(slide, 110, 820, 1500, 200, s["headline"],
                           size=64, bold=True, font=self.f["display_safe"])
        else:
            self._headline(slide, s.get("headline", ""), kicker=s.get("kicker"))
            slide.shapes.add_picture(str(path), px(960), px(330), height=px(600))
            if s.get("subhead"):
                self._text(slide, 92, 380, 800, 400, s["subhead"],
                           size=28, colour=self.c["muted"], line_spacing=1.45)
        self._source(slide, s.get("source"))

    # --- Drive ------------------------------------------------------------
    LAYOUTS = {
        "title": layout_title, "section": layout_section, "statement": layout_statement,
        "stats": layout_stats, "bullets": layout_bullets, "quote": layout_quote,
        "cards": layout_cards, "timeline": layout_timeline, "table": layout_table,
        "chart": layout_chart, "image": layout_image,
    }

    def build(self, out_path):
        for i, s in enumerate(self.spec["slides"], start=1):
            name = s.get("layout", "bullets")
            fn = self.LAYOUTS.get(name)
            if fn is None:
                print(f"  ! slide {i}: unknown layout '{name}', using bullets")
                fn = self.LAYOUTS["bullets"]

            slide = self.prs.slides.add_slide(self.blank)
            fn(self, slide, s)
            self._notes(slide, s.get("notes"))
            print(f"  {i:>2}. {name:<10} {s.get('headline', '')[:56]}")

        self.prs.save(out_path)
        return out_path


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    spec_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    print(f"Building {len(spec['slides'])} slides")
    builder = DeckBuilder(spec)
    builder.build(out_path)

    size_kb = out_path.stat().st_size / 1024
    print(f"\nWrote {out_path}  ({size_kb:.0f} KB)")

    # Say plainly which font the file actually uses, so nobody is surprised
    # when the deck opens on a client machine.
    f = builder.f
    swaps = [(f["display"], f["display_safe"]), (f["body"], f["body_safe"])]
    swapped = [(want, got) for want, got in swaps if want != got]
    if swapped:
        for want, got in swapped:
            print(f"Font: design calls for {want}, .pptx uses {got}.")
        print("Mention this at delivery. Installing the design font is the only "
              "way the .pptx matches the HTML.")


if __name__ == "__main__":
    main()
