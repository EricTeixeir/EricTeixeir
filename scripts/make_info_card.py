"""
Hand-authored terminal-card SVG: identity, bio and contact info typed
out like a shell session (whoami / cat sobre.txt / cat contato.txt).
Each line fades/slides in on a short stagger. Writes info-card.svg.

Edit NAME, TITLE, BIO or CONTACT below to change the content.
"""
import re
from xml.sax.saxutils import escape as xml_escape

NAME = "Eric Teixeira"
TITLE = "Desenvolvedor Full Stack & Infraestrutura"

# wrap a word/phrase in **double asterisks** to highlight it in the card
BIO = [
    "Desenvolvedor com formação em **Análise e Desenvolvimento de Sistemas**, "
    "experiência prática em desenvolvimento web, backend e infraestrutura. "
    "Atuo construindo sistemas, **APIs**, integrações e automações, além de "
    "trabalhar com bancos de dados, **Docker**, Linux e ambientes de produção.",
    "Tenho perfil hands-on e gosto de atuar de ponta a ponta, conectando "
    "desenvolvimento, infraestrutura e operações. Atualmente, estou "
    "direcionando minha carreira para **Cybersecurity**, aprofundando "
    "conhecimentos em **segurança de aplicações**, redes, **hardening** e "
    "infraestrutura.",
]

CONTACT = [
    ("github", "github.com/EricTeixeir"),
    ("linkedin", "linkedin.com/in/eric-teixeira-almeida"),
    ("email", "ericteixeiradealmeida@gmail.com"),
]

WIDTH = 620
WRAP_COLS = 72          # ~classic 80-col terminal, minus padding
PAD_X = 20
PAD_TOP = 24
TITLEBAR_H = 28
LINE_H = 21
PARA_GAP = 6            # extra gap after a paragraph, before the next prompt

BG = "#0d1117"
BORDER = "#30363d"
TITLE_BAR = "#161b22"
ACCENT = "#58a6ff"
PROMPT_USER = "#7ee787"
PROMPT_DIM = "#8b949e"
VAL_COLOR = "#c9d1d9"
DIM = "#8b949e"
HL_TEXT = "#f2cc60"   # highlighted keyword text (warm gold)
HL_BG = "#e3b341"     # highlighted keyword chip background (used at low opacity)

CHAR_W = 7.6  # approx monospace glyph advance at font-size 13, used to size highlight chips


def tokenize(text):
    """Split text into (word, highlighted) pairs; **word(s)** mark a highlight."""
    tokens = []
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        highlighted = i % 2 == 1
        for word in part.split():
            tokens.append((word, highlighted))
    return tokens


def wrap_tokens(tokens, width):
    """Word-wrap tokens to `width` visible characters per line."""
    lines, cur, cur_len = [], [], 0
    for word, hl in tokens:
        add_len = len(word) if not cur else len(word) + 1
        if cur and cur_len + add_len > width:
            lines.append(cur)
            cur, cur_len, add_len = [], 0, len(word)
        cur.append((word, hl))
        cur_len += add_len
    if cur:
        lines.append(cur)
    return lines


def line_runs(line_tokens):
    """Merge consecutive same-style tokens into (highlighted, start_char, text) runs."""
    runs, cur_words, cur_hl, cur_start, pos = [], [], None, 0, 0
    for word, hl in line_tokens:
        if cur_words and hl != cur_hl:
            runs.append((cur_hl, cur_start, " ".join(cur_words)))
            cur_words = []
        if not cur_words:
            cur_start = pos
        cur_words.append(word)
        cur_hl = hl
        pos += len(word) + 1
    if cur_words:
        runs.append((cur_hl, cur_start, " ".join(cur_words)))
    return runs


def build_rows():
    """Return a flat list of ('prompt'|'name'|'text'|'contact', ...) rows."""
    rows = [("prompt", "whoami"), ("name", NAME, TITLE)]
    rows.append(("prompt", "cat sobre.txt"))
    for i, para in enumerate(BIO):
        for line_tokens in wrap_tokens(tokenize(para), WRAP_COLS):
            rows.append(("text", line_tokens))
        if i < len(BIO) - 1:
            rows.append(("blank",))
    rows.append(("prompt", "cat contato.txt"))
    for label, value in CONTACT:
        rows.append(("contact", label, value))
    return rows


def render():
    rows = build_rows()

    height = PAD_TOP + TITLEBAR_H
    for row in rows:
        if row[0] == "blank":
            height += 4
        elif row[0] == "name":
            height += LINE_H * 2  # name line + title line
        else:
            height += LINE_H
        if row[0] == "prompt":
            height += PARA_GAP
    height += 20

    parts = [
        f'<svg width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="ui-monospace, SFMono-Regular, Consolas, monospace">',
        f"""
<style>
  .line {{ opacity: 0; transform-box: fill-box; transform-origin: left; animation: fadeSlide 0.35s ease-out forwards; }}
  @keyframes fadeSlide {{
    from {{ opacity: 0; transform: translateX(-8px); }}
    to   {{ opacity: 1; transform: translateX(0); }}
  }}
</style>
""",
        f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{height-1}" rx="6" fill="{BG}" stroke="{BORDER}"/>',
        f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{TITLEBAR_H}" rx="6" fill="{TITLE_BAR}"/>',
        f'<rect x="0.5" y="20" width="{WIDTH-1}" height="9" fill="{TITLE_BAR}"/>',
        f'<line x1="0.5" y1="{TITLEBAR_H + 0.5}" x2="{WIDTH - 0.5}" y2="{TITLEBAR_H + 0.5}" stroke="{BORDER}"/>',
        f'<text x="14" y="18" fill="{DIM}" font-size="11">eric@linux</text>',
    ]
    cx = WIDTH - 20
    parts.append(f'<text x="{cx}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x2715;</text>')
    parts.append(f'<text x="{cx-20}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x25a1;</text>')
    parts.append(f'<text x="{cx-40}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x2212;</text>')
    parts.append(f'<text x="{WIDTH/2}" y="18" fill="{DIM}" font-size="11" text-anchor="middle">~ about</text>')

    y = PAD_TOP + TITLEBAR_H
    delay = 0.08
    for row in rows:
        kind = row[0]
        if kind == "blank":
            y += 4
            continue
        y += LINE_H
        if kind == "prompt":
            _, cmd = row
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{PROMPT_USER}" font-size="13">eric@linux</text>'
                f'<text x="{PAD_X + 78}" y="{y}" fill="{PROMPT_DIM}" font-size="13">~ $ {xml_escape(cmd)}</text>'
                f'</g>'
            )
            y += PARA_GAP
        elif kind == "name":
            _, name, title = row
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{ACCENT}" font-size="16" font-weight="700">{xml_escape(name)}</text>'
                f'</g>'
            )
            y += LINE_H
            parts.append(
                f'<g class="line" style="animation-delay: {delay + 0.05:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{VAL_COLOR}" font-size="13">{xml_escape(title)}</text>'
                f'</g>'
            )
        elif kind == "text":
            _, line_tokens = row
            g_parts = []
            tspans = []
            for hl, start, text in line_runs(line_tokens):
                x = PAD_X + start * CHAR_W
                if hl:
                    chip_w = len(text) * CHAR_W
                    g_parts.append(
                        f'<rect x="{x - 3:.1f}" y="{y - 12}" width="{chip_w + 6:.1f}" height="16" rx="3" '
                        f'fill="{HL_BG}" fill-opacity="0.16"/>'
                    )
                    tspans.append(
                        f'<tspan x="{x:.1f}" fill="{HL_TEXT}" font-weight="700">{xml_escape(text)}</tspan>'
                    )
                else:
                    tspans.append(f'<tspan x="{x:.1f}">{xml_escape(text)}</tspan>')
            g_parts.append(f'<text y="{y}" fill="{VAL_COLOR}" font-size="13">{"".join(tspans)}</text>')
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">' + "".join(g_parts) + '</g>'
            )
        elif kind == "contact":
            _, label, value = row
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{PROMPT_USER}" font-size="13" font-weight="600">{xml_escape(label)}</text>'
                f'<text x="{PAD_X + 90}" y="{y}" fill="{VAL_COLOR}" font-size="13">{xml_escape(value)}</text>'
                f'</g>'
            )
        delay += 0.045

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = render()
    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote info-card.svg ({len(svg)} bytes)")
