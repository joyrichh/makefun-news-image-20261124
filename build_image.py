#!/usr/bin/env python3
"""One-image summary of the world's news for Tuesday 24 November 2026.

The script reads news.json next to it, lays out a navy masthead, six story
cards in two columns and an "also today" band, and saves a 1024 by 1024 PNG
as entry.png. It never touches the network, the clock or random numbers, so
re-running it reproduces the same bytes. Pillow and the system DejaVu faces
are the only build-time needs; the shipped Node program needs nothing but
its standard library.
"""

import json
from datetime import date as parse_date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 1024, 1024
EDGE = 24
SPACE = 16
MASTHEAD_H = 168
CARD_W = (PAGE_W - 2 * EDGE - SPACE) // 2
CARD_H = 204
PALETTE = {
    "navy": "#0E2A47",
    "gold": "#E8B84B",
    "ink": "#111827",
    "grey": "#475569",
    "paper": "#F1F5F9",
    "edge": "#CBD5E1",
    "white": "#FFFFFF",
    "mist": "#BACDE0",
}
DEJAVU = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"
DATA = json.loads((ROOT / "news.json").read_text(encoding="utf-8"))
STORY_DAY = parse_date.fromisoformat(DATA["date"])
DAY_TITLE = f"{STORY_DAY.day} {STORY_DAY.strftime('%B')} {STORY_DAY.year}"
MEASURED = []


def face(filename, size):
    return ImageFont.truetype(str(DEJAVU / filename), size)


def split_lines(canvas, text, font, width):
    rows = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if canvas.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                rows.append(current)
            current = word
    if current:
        rows.append(current)
    return rows


def fit_lines(canvas, text, filename, size, width, max_rows):
    for size in range(size, 13, -1):
        font = face(filename, size)
        rows = split_lines(canvas, text, font, width)
        widths_ok = all(
            canvas.textlength(row, font=font) <= width
            and canvas.textbbox((0, 0), row, font=font)[2] <= width
            for row in rows
        )
        if len(rows) <= max_rows and widths_ok:
            assert " ".join(rows) == text
            return font, rows
    raise ValueError(f"Text does not fit: {text}")


def checked_text(canvas, xy, text, font, colour, box, tag, anchor="la"):
    rect = canvas.textbbox(xy, text, font=font, anchor=anchor)
    x0, y0, x1, y1 = box
    assert x0 <= rect[0] and rect[2] <= x1, (tag, text, rect, box)
    assert y0 <= rect[1] and rect[3] <= y1, (tag, text, rect, box)
    MEASURED.append({
        "label": tag,
        "text": text,
        "bbox": rect,
        "bounds": box,
        "width": canvas.textlength(text, font=font),
        "font_size": font.size,
    })
    canvas.text(xy, text, font=font, fill=colour, anchor=anchor)


def masthead(canvas):
    canvas.rectangle([0, 0, PAGE_W, PAGE_H], fill=PALETTE["white"])
    canvas.rectangle([0, 0, PAGE_W, MASTHEAD_H], fill=PALETTE["navy"])
    canvas.rectangle([0, MASTHEAD_H, PAGE_W, MASTHEAD_H + 4],
                     fill=PALETTE["gold"])
    head_box = (24, 0, 812, MASTHEAD_H)
    checked_text(canvas, (36, 26),
                 f"WORLD NEWS • {DATA['day'].upper()}",
                 face(SANS_BOLD, 21), PALETTE["gold"], head_box, "kicker")
    checked_text(canvas, (36, 56), DAY_TITLE, face(SERIF_BOLD, 58),
                 PALETTE["white"], head_box, "title")
    checked_text(canvas, (36, 126), "The day's biggest stories, in one image",
                 face(SANS, 23), PALETTE["mist"], head_box, "subtitle")
    badge_box = (828, 34, 988, 132)
    canvas.rounded_rectangle(badge_box, radius=12,
                             outline=PALETTE["gold"], width=2)
    checked_text(canvas, (908, 48), STORY_DAY.strftime("%b").upper(),
                 face(SANS_BOLD, 21), PALETTE["gold"], badge_box,
                 "badge month", anchor="mt")
    checked_text(canvas, (908, 74), str(STORY_DAY.day),
                 face(SERIF_BOLD, 40), PALETTE["white"], badge_box,
                 "badge day", anchor="mt")


def story_card(canvas, story, index):
    col, row = index % 2, index // 2
    x = EDGE + col * (CARD_W + SPACE)
    y = 192 + row * (CARD_H + SPACE)
    inner = (x + 20, y + 12, x + CARD_W - 20, y + CARD_H - 10)
    canvas.rounded_rectangle([x, y, x + CARD_W, y + CARD_H], radius=14,
                             fill=PALETTE["white"],
                             outline=PALETTE["edge"], width=1)
    canvas.rounded_rectangle([x, y, x + 8, y + CARD_H], radius=4,
                             fill=story["color"])
    tag_font = face(SANS_BOLD, 17)
    tag_w = canvas.textlength(story["tag"], font=tag_font) + 20
    canvas.rounded_rectangle([x + 22, y + 16, x + 22 + tag_w, y + 44],
                             radius=7, fill=story["color"])
    checked_text(canvas, (x + 32, y + 21), story["tag"], tag_font,
                 PALETTE["white"], inner, f"story {index + 1} tag")
    head_font, head_rows = fit_lines(canvas, story["headline"], SANS_BOLD,
                                     25, CARD_W - 44, 2)
    for n, row_text in enumerate(head_rows):
        checked_text(canvas, (x + 22, y + 56 + n * 30), row_text,
                     head_font, PALETTE["ink"], inner,
                     f"story {index + 1} headline")
    body_font, body_rows = fit_lines(canvas, story["summary"], SANS,
                                     19, CARD_W - 44, 3)
    for n, row_text in enumerate(body_rows):
        checked_text(canvas, (x + 22, y + 122 + n * 25), row_text,
                     body_font, PALETTE["grey"], inner,
                     f"story {index + 1} summary")


def also_band(canvas):
    top = 192 + 3 * CARD_H + 2 * SPACE + 16
    band_box = (EDGE + 22, top + 6, PAGE_W - EDGE - 22, top + 98)
    canvas.rounded_rectangle([EDGE, top, PAGE_W - EDGE, top + 100],
                             radius=14, fill=PALETTE["paper"])
    checked_text(canvas, (EDGE + 22, top + 10), "ALSO TODAY",
                 face(SANS_BOLD, 19), PALETTE["navy"], band_box,
                 "also heading")
    rows = [f"•  {line}" for line in DATA["also_today"]]
    size = next(s for s in range(19, 13, -1) if all(
        canvas.textlength(row, font=face(SANS, s)) <= PAGE_W - 2 * EDGE - 44
        for row in rows
    ))
    for n, row in enumerate(rows):
        checked_text(canvas, (EDGE + 22, top + 33 + n * 20), row,
                     face(SANS, size), PALETTE["ink"], band_box,
                     "also story")


def footer(canvas):
    credit = f"Sources: {' · '.join(DATA['sources'])}  —  {DAY_TITLE}"
    checked_text(canvas, (PAGE_W // 2, 978), credit, face(SANS, 15),
                 PALETTE["grey"], (24, 970, PAGE_W - 24, PAGE_H - 16),
                 "footer", anchor="mt")


def build():
    assert len(DATA["stories"]) == 6
    assert len(DATA["also_today"]) == 3
    assert STORY_DAY.strftime("%A") == DATA["day"]
    MEASURED.clear()
    image = Image.new("RGB", (PAGE_W, PAGE_H), PALETTE["white"])
    canvas = ImageDraw.Draw(image)
    masthead(canvas)
    for index, story in enumerate(DATA["stories"]):
        story_card(canvas, story, index)
    also_band(canvas)
    footer(canvas)
    target = ROOT / "entry.png"
    image.save(target, "PNG", optimize=True)
    assert target.stat().st_size <= 1048576
    print(f"saved {target}: {PAGE_W}x{PAGE_H}, "
          f"{target.stat().st_size:,} bytes; "
          f"{len(MEASURED)} text lines checked")
    return target


if __name__ == "__main__":
    build()
