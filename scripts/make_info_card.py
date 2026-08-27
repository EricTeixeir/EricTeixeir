"""
Hand-authored terminal-card SVG: identity, bio and contact info typed
out like a shell session (whoami / cat sobre.txt / cat contato.txt).
Each line fades/slides in on a short stagger. Writes info-card.svg.

Edit NAME, TITLE, BIO or CONTACT below to change the content.
"""
import textwrap

NAME = "Eric Teixeira"
TITLE = "Desenvolvedor Full Stack & Infraestrutura"

BIO = [
    "Desenvolvedor com formação em Análise e Desenvolvimento de Sistemas, "
    "experiência prática em desenvolvimento web, backend e infraestrutura. "
    "Atuo construindo sistemas, APIs, integrações e automações, além de "
    "trabalhar com bancos de dados, Docker, Linux e ambientes de produção.",
    "Tenho perfil hands-on e gosto de atuar de ponta a ponta, conectando "
    "desenvolvimento, infraestrutura e operações. Atualmente, estou "
    "direcionando minha carreira para Cybersecurity, aprofundando "
    "conhecimentos em segurança de aplicações, redes, hardening e "
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


def build_rows():
    """Return a flat list of ('prompt'|'name'|'text'|'contact', ...) rows."""
    rows = [("prompt", "whoami"), ("name", NAME, TITLE)]
    rows.append(("prompt", "cat sobre.txt"))
    for i, para in enumerate(BIO):
        for line in textwrap.wrap(para, WRAP_COLS):
            rows.append(("text", line))
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
        f'<svg viewBox="0 0 {WIDTH} {height}" xmlns="http://www.w3.org/2000/svg" '
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
                f'<text x="{PAD_X + 78}" y="{y}" fill="{PROMPT_DIM}" font-size="13">~ $ {cmd}</text>'
                f'</g>'
            )
            y += PARA_GAP
        elif kind == "name":
            _, name, title = row
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{ACCENT}" font-size="16" font-weight="700">{name}</text>'
                f'</g>'
            )
            y += LINE_H
            parts.append(
                f'<g class="line" style="animation-delay: {delay + 0.05:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{VAL_COLOR}" font-size="13">{title}</text>'
                f'</g>'
            )
        elif kind == "text":
            _, line = row
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{VAL_COLOR}" font-size="13">{line}</text>'
                f'</g>'
            )
        elif kind == "contact":
            _, label, value = row
            parts.append(
                f'<g class="line" style="animation-delay: {delay:.2f}s">'
                f'<text x="{PAD_X}" y="{y}" fill="{PROMPT_USER}" font-size="13" font-weight="600">{label}</text>'
                f'<text x="{PAD_X + 90}" y="{y}" fill="{VAL_COLOR}" font-size="13">{value}</text>'
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
