"""
Hand-authored terminal-card SVG: identity typed out like a shell
session (whoami), then a "cat sobre.json" with real JSON syntax
coloring (keys / strings / punctuation) instead of prose. Each line
fades/slides in on a short stagger. Writes info-card.svg.

Edit NAME, TITLE, INFO or CONTACT below to change the content.
"""
from xml.sax.saxutils import escape as xml_escape

HOST = "kali"  # nod to Kali Linux, matches the Cybersecurity direction below
NAME = "Eric Teixeira"
TITLE = "Full Stack Developer | Security-focused"

# ordered key -> value (str) or key -> list[str] for a JSON array
INFO = [
    ("formacao", "Análise e Desenvolvimento de Sistemas"),
    ("atuacao", [
        "desenvolvimento full stack",
        "APIs REST",
        "integrações",
        "automação",
        "infraestrutura",
        "observabilidade",
    ]),
    ("perfil", "hands-on, ponta a ponta"),
    ("especialidade", "Full Stack + Infraestrutura"),
    ("direcionamento", "Cybersecurity"),
    ("foco_atual", [
        "segurança de aplicações",
        "redes",
        "hardening",
        "segurança de infraestrutura",
    ]),
    ("stack", ["Node.js", "React", "PostgreSQL", "Docker", "Linux", "Nginx", "Grafana", "Zabbix"]),
]

CONTACT = [
    ("github", "github.com/EricTeixeir"),
    ("linkedin", "linkedin.com/in/eric-teixeira-almeida"),
    ("email", "ericteixeiradealmeida@gmail.com"),
]

WIDTH = 620
PAD_X = 20
PAD_TOP = 24
TITLEBAR_H = 28
LINE_H = 21
PARA_GAP = 6           # extra gap after a prompt line, before its output
INDENT_W = 18           # px per JSON indent level

BG = "#0d1117"
BORDER = "#30363d"
TITLE_BAR = "#161b22"
ACCENT = "#58a6ff"
PROMPT_USER = "#7ee787"
PROMPT_DIM = "#8b949e"
VAL_COLOR = "#c9d1d9"
DIM = "#8b949e"
JSON_KEY = "#79c0ff"    # JSON object keys
JSON_STR = "#f2cc60"    # JSON string values (also used for array items)
JSON_PUNCT = "#8b949e"  # braces, brackets, commas, colons


BLANK = (-1, [])  # spacer row between top-level fields, matches the source formatting


def q(s):
    return f'"{s}"'


def build_json_lines():
    """Return [(indent, [(text, color), ...]), ...] for the sobre.json body."""
    lines = [(0, [("{", JSON_PUNCT)])]

    def kv(indent, key, value, comma):
        segs = [(q(key), JSON_KEY), (": ", JSON_PUNCT), (q(value), JSON_STR)]
        if comma:
            segs.append((",", JSON_PUNCT))
        lines.append((indent, segs))

    for key, value in INFO:
        if isinstance(value, list):
            lines.append((1, [(q(key), JSON_KEY), (": [", JSON_PUNCT)]))
            for j, item in enumerate(value):
                comma = j < len(value) - 1
                lines.append((2, [(q(item), JSON_STR), ((",", JSON_PUNCT) if comma else ("", JSON_PUNCT))]))
            lines.append((1, [("],", JSON_PUNCT)]))
        else:
            kv(1, key, value, comma=True)
        lines.append(BLANK)

    lines.append((1, [(q("contato"), JSON_KEY), (": {", JSON_PUNCT)]))
    for j, (key, value) in enumerate(CONTACT):
        kv(2, key, value, comma=(j < len(CONTACT) - 1))
    lines.append((1, [("}", JSON_PUNCT)]))

    lines.append((0, [("}", JSON_PUNCT)]))
    return lines


BLANK_H = 10  # spacer row height, shorter than a full line

def build_rows():
    """Return a flat list of ('prompt'|'name'|'json'|'blank', ...) rows."""
    rows = [("prompt", "whoami"), ("name", NAME, TITLE)]
    rows.append(("prompt", "cat sobre.json"))
    for indent, segments in build_json_lines():
        rows.append(("blank",) if indent == -1 else ("json", indent, segments))
    return rows


def render():
    rows = build_rows()

    height = PAD_TOP + TITLEBAR_H
    for row in rows:
        if row[0] == "blank":
            height += BLANK_H
        elif row[0] == "name":
            height += LINE_H * 2
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
        f'<text x="14" y="18" fill="{DIM}" font-size="11">eric@{HOST}</text>',
    ]
    cx = WIDTH - 20
    parts.append(f'<text x="{cx}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x2715;</text>')
    parts.append(f'<text x="{cx-20}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x25a1;</text>')
    parts.append(f'<text x="{cx-40}" y="18" fill="{DIM}" font-size="12" text-anchor="middle">&#x2212;</text>')
    parts.append(f'<text x="{WIDTH/2}" y="18" fill="{DIM}" font-size="11" text-anchor="middle">~ sobre.json</text>')

    y = PAD_TOP + TITLEBAR_H
    delay = 0.08
    for row in rows:
        kind = row[0]
        if kind == "blank":
            y += BLANK_H
            continue
        y += LINE_H
        if kind == "prompt":
            _, cmd = row
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{PROMPT_USER}" font-size="13">eric@{HOST}</text>'
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
        elif kind == "json":
            _, indent, segments = row
            x = PAD_X + indent * INDENT_W
            tspans = "".join(
                f'<tspan fill="{color}">{xml_escape(text)}</tspan>' for text, color in segments if text
            )
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">'
                f'<text x="{x}" y="{y}" font-size="13">{tspans}</text>'
                f'</g>'
            )
        delay += 0.035

    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = render()
    with open("info-card.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote info-card.svg ({len(svg)} bytes)")
