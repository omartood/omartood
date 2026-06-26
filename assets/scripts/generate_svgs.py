#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates the animated SVG assets used by the GitHub profile README.

Why a generator? The hero banner is a fully-meshed neural network (40 edges +
14 nodes + drifting particles). Hand-authoring that is error-prone; generating
it keeps coordinates consistent and the output easy to re-tune.

All animation is pure SVG + CSS (no JavaScript) so it renders on GitHub, where
SVGs referenced as <img> keep their internal <style> blocks.

Run:  python assets/scripts/generate_svgs.py
Out:  svg/hero.svg, svg/pipeline.svg, svg/keywords.svg, svg/footer.svg
"""

import os

# --- palette ----------------------------------------------------------------
PURPLE = "#8B5CF6"
CYAN = "#06B6D4"
EMERALD = "#10B981"
WHITE = "#FFFFFF"
BG = "#0D1117"
MUTED = "#8B949E"
FAINT = "#C9D1D9"

FONT = "'Segoe UI', Roboto, 'Helvetica Neue', system-ui, -apple-system, sans-serif"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "svg"))


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", os.path.relpath(path, os.path.join(HERE, "..", "..")))


# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
def hero():
    W, H = 1200, 420

    # layers: (x, [y...], colour)
    layers = [
        (120, [120, 210, 300], CYAN),
        (330, [80, 165, 250, 335], PURPLE),
        (870, [80, 165, 250, 335], PURPLE),
        (1080, [120, 210, 300], EMERALD),
    ]
    nodes = [[(x, y, c) for y in ys] for (x, ys, c) in layers]

    # edges: full mesh between consecutive layers
    edges = []
    for i in range(len(nodes) - 1):
        for (x1, y1, _) in nodes[i]:
            for (x2, y2, _) in nodes[i + 1]:
                edges.append((x1, y1, x2, y2))

    edge_svg = []
    for idx, (x1, y1, x2, y2) in enumerate(edges):
        delay = round(-(idx % 12) * 0.22, 2)
        edge_svg.append(
            '<line class="edge" x1="%d" y1="%d" x2="%d" y2="%d" '
            'style="animation-delay:%ss"/>' % (x1, y1, x2, y2, delay)
        )

    node_svg = []
    for li, layer in enumerate(nodes):
        for ni, (x, y, c) in enumerate(layer):
            delay = round(-((li * 4 + ni) % 8) * 0.3, 2)
            node_svg.append(
                '<g class="node" style="animation-delay:%ss">'
                '<circle cx="%d" cy="%d" r="13" fill="%s" opacity="0.18"/>'
                '<circle cx="%d" cy="%d" r="5.5" fill="%s" filter="url(#glow)"/>'
                '<circle cx="%d" cy="%d" r="2.4" fill="%s"/>'
                "</g>" % (delay, x, y, c, x, y, c, x, y, WHITE)
            )

    # drifting particles
    particle_svg = []
    px = [90, 230, 410, 560, 640, 740, 900, 1010, 1130, 180, 480, 820]
    for i, x in enumerate(px):
        dur = round(7 + (i % 5) * 1.6, 1)
        delay = round(-(i * 1.3), 1)
        r = 1.5 + (i % 3) * 0.7
        col = [CYAN, PURPLE, EMERALD][i % 3]
        particle_svg.append(
            '<circle class="particle" cx="%d" cy="430" r="%.1f" fill="%s" '
            'style="animation-duration:%ss;animation-delay:%ss"/>'
            % (x, r, col, dur, delay)
        )

    style = """
    <style>
      .edge {
        stroke: url(#edgeGrad);
        stroke-width: 1.1;
        stroke-dasharray: 5 9;
        opacity: 0.55;
        animation: flow 2.6s linear infinite;
      }
      @keyframes flow { to { stroke-dashoffset: -28; } }
      .node { animation: pulse 3.2s ease-in-out infinite; transform-origin: center; }
      @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
      }
      .particle {
        opacity: 0;
        animation-name: drift;
        animation-timing-function: linear;
        animation-iteration-count: infinite;
      }
      @keyframes drift {
        0%   { transform: translateY(0) scale(1);   opacity: 0; }
        12%  { opacity: 0.9; }
        88%  { opacity: 0.9; }
        100% { transform: translateY(-440px) scale(0.4); opacity: 0; }
      }
      .title { font-family: %FONT%; }
    </style>
    """.replace("%FONT%", FONT)

    defs = """
    <defs>
      <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="%P%">
          <animate attributeName="stop-color" values="%P%;%C%;%P%" dur="6s" repeatCount="indefinite"/>
        </stop>
        <stop offset="55%" stop-color="%C%">
          <animate attributeName="stop-color" values="%C%;%E%;%C%" dur="6s" repeatCount="indefinite"/>
        </stop>
        <stop offset="100%" stop-color="%E%">
          <animate attributeName="stop-color" values="%E%;%P%;%E%" dur="6s" repeatCount="indefinite"/>
        </stop>
      </linearGradient>
      <linearGradient id="edgeGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="%C%"/>
        <stop offset="50%" stop-color="%P%"/>
        <stop offset="100%" stop-color="%E%"/>
      </linearGradient>
      <radialGradient id="vignette" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="%BG%" stop-opacity="0.95"/>
        <stop offset="55%" stop-color="%BG%" stop-opacity="0.78"/>
        <stop offset="100%" stop-color="%BG%" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="blobP" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="%P%" stop-opacity="0.30"/>
        <stop offset="100%" stop-color="%P%" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="blobC" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="%C%" stop-opacity="0.28"/>
        <stop offset="100%" stop-color="%C%" stop-opacity="0"/>
      </radialGradient>
      <filter id="glow" x="-120%" y="-120%" width="340%" height="340%">
        <feGaussianBlur stdDeviation="3.2" result="b"/>
        <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
      <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation="6" result="b"/>
        <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
    </defs>
    """
    for k, v in {"%P%": PURPLE, "%C%": CYAN, "%E%": EMERALD, "%BG%": BG}.items():
        defs = defs.replace(k, v)

    text = """
    <g class="title" text-anchor="middle">
      <text x="600" y="172" font-size="72" font-weight="800" letter-spacing="3"
            fill="url(#titleGrad)" filter="url(#softGlow)">OMAR TOOD</text>
      <text x="600" y="212" font-size="22" font-weight="600" letter-spacing="3"
            fill="%C%">MSc in Artificial Intelligence</text>
      <text x="600" y="246" font-size="16" font-weight="500" letter-spacing="4"
            fill="%MUTED%">AI RESEARCHER &#160;&#183;&#160; LLM ENGINEER &#160;&#183;&#160; SOFTWARE ENGINEER</text>
      <text x="600" y="296" font-size="16" letter-spacing="1" fill="%FAINT%">Building intelligent systems with Transformers, Large Language Models,</text>
      <text x="600" y="320" font-size="16" letter-spacing="1" fill="%FAINT%">Agentic AI, and Somali NLP.</text>
    </g>
    """.replace("%C%", CYAN).replace("%MUTED%", MUTED).replace("%FAINT%", FAINT)

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="100%%" role="img" aria-label="Omar Tood — AI Researcher">' % (W, H)
        + style
        + defs
        + '<rect width="%d" height="%d" fill="%s" rx="14"/>' % (W, H, BG)
        + '<ellipse cx="230" cy="120" rx="420" ry="320" fill="url(#blobP)"/>'
        + '<ellipse cx="980" cy="320" rx="420" ry="320" fill="url(#blobC)"/>'
        + '<g>' + "".join(edge_svg) + "</g>"
        + '<g>' + "".join(node_svg) + "</g>"
        + '<g>' + "".join(particle_svg) + "</g>"
        + '<ellipse cx="600" cy="220" rx="560" ry="200" fill="url(#vignette)"/>'
        + text
        + "</svg>"
    )
    write("hero.svg", svg)


# ---------------------------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------------------------
def pipeline():
    W, H = 520, 560
    stages = ["Dataset", "Embedding", "Self-Attention", "Reasoning", "Output"]
    ys = [60, 160, 260, 360, 460]
    bw, bh, cx = 300, 58, 260

    style = """
    <style>
      .pf { font-family: %FONT%; }
      .stage { animation: lift 5s ease-in-out infinite; transform-origin: center; }
      @keyframes lift { 0%,100%{opacity:.78} 50%{opacity:1} }
      .glowbox { stroke-dasharray: 720; animation: trace 5s linear infinite; }
      @keyframes trace { to { stroke-dashoffset: -720; } }
      .tok { animation: travel 5s ease-in-out infinite; }
      @keyframes travel {
        0%   { transform: translateY(0);   opacity: 0; }
        8%   { opacity: 1; }
        92%  { opacity: 1; }
        100% { transform: translateY(400px); opacity: 0; }
      }
    </style>
    """.replace("%FONT%", FONT)

    defs = """
    <defs>
      <linearGradient id="pg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="%P%"/><stop offset="100%" stop-color="%C%"/>
      </linearGradient>
      <filter id="pglow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="3"/>
      </filter>
    </defs>
    """.replace("%P%", PURPLE).replace("%C%", CYAN)

    boxes = []
    for i, (s, y) in enumerate(zip(stages, ys)):
        bx = cx - bw / 2
        delay = round(i * 1.0, 1)
        boxes.append(
            '<g class="stage" style="animation-delay:%ss">'
            '<rect x="%.0f" y="%d" width="%d" height="%d" rx="12" '
            'fill="#11161D" stroke="#222a35" stroke-width="1"/>'
            '<rect class="glowbox" x="%.0f" y="%d" width="%d" height="%d" rx="12" '
            'fill="none" stroke="url(#pg)" stroke-width="1.6" '
            'style="animation-delay:%ss"/>'
            '<text class="pf" x="%d" y="%d" text-anchor="middle" '
            'font-size="19" font-weight="600" fill="%s">%s</text>'
            "</g>"
            % (delay, bx, y, bw, bh, bx, y, bw, bh, round(-i * 1.0, 1),
               cx, y + 36, WHITE, s)
        )

    connectors = []
    for i in range(len(ys) - 1):
        y1 = ys[i] + bh
        y2 = ys[i + 1]
        connectors.append(
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#2b3340" stroke-width="2"/>'
            % (cx, y1, cx, y2)
        )
        # arrow
        connectors.append(
            '<path d="M%d %d l-5 -7 h10 z" fill="#2b3340"/>' % (cx, y2)
        )

    # travelling token down the whole column
    tokens = []
    for k in range(2):
        tokens.append(
            '<circle class="tok" cx="%d" cy="%d" r="4.5" fill="%s" '
            'filter="url(#pglow)" style="animation-delay:%ss"/>'
            % (cx, ys[0] + bh, CYAN, round(k * 2.5, 1))
        )

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" '
        'role="img" aria-label="AI pipeline">' % (W, H)
        + style + defs
        + '<rect width="%d" height="%d" fill="%s" rx="14"/>' % (W, H, BG)
        + "".join(connectors) + "".join(tokens) + "".join(boxes)
        + "</svg>"
    )
    write("pipeline.svg", svg)


# ---------------------------------------------------------------------------
# KEYWORDS (rotating)
# ---------------------------------------------------------------------------
def keywords():
    W, H = 760, 70
    words = [
        "Large Language Models", "Transformer Architectures",
        "Retrieval-Augmented Generation", "AI Agents", "Deep Learning",
        "Somali NLP", "Machine Learning Research", "Open Source",
    ]
    n = len(words)
    per = 2.6
    total = round(n * per, 2)
    cols = [CYAN, PURPLE, EMERALD]

    # build per-word keyframes so exactly one is visible at a time
    css = [".kw{font-family:%s;opacity:0;}" % FONT]
    css.append(
        "@keyframes kwfade{0%%{opacity:0;transform:translateY(6px);}"
        "4%%{opacity:1;transform:translateY(0);}"
        "%.1f%%{opacity:1;transform:translateY(0);}"
        "%.1f%%{opacity:0;transform:translateY(-6px);}"
        "100%%{opacity:0;}}" % (100.0 / n - 4, 100.0 / n)
    )
    css.append(".dot{animation:blink 1.3s ease-in-out infinite;}")
    css.append("@keyframes blink{0%,100%{opacity:.3}50%{opacity:1}}")

    texts = []
    for i, w in enumerate(words):
        delay = round(i * per, 2)
        texts.append(
            '<text class="kw" x="56" y="44" font-size="26" font-weight="700" '
            'fill="%s" style="animation:kwfade %ss ease-in-out infinite;'
            'animation-delay:%ss;transform-origin:left;">%s</text>'
            % (cols[i % 3], total, delay, w)
        )

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" '
        'role="img" aria-label="Focus areas">' % (W, H)
        + "<style>" + "".join(css) + "</style>"
        + '<rect width="%d" height="%d" fill="%s" rx="10"/>' % (W, H, BG)
        + '<circle class="dot" cx="30" cy="36" r="7" fill="%s"/>' % EMERALD
        + "".join(texts)
        + "</svg>"
    )
    write("keywords.svg", svg)


# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------
def footer():
    W, H = 1000, 130
    style = """
    <style>
      .ft { font-family: %FONT%; }
      .shine { animation: sweep 5s linear infinite; }
      @keyframes sweep { 0%{transform:translateX(-260px)} 100%{transform:translateX(1260px)} }
      .ln { stroke-dasharray: 6 8; animation: flow2 3s linear infinite; }
      @keyframes flow2 { to { stroke-dashoffset: -28; } }
    </style>
    """.replace("%FONT%", FONT)

    defs = """
    <defs>
      <linearGradient id="fg" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="%P%"/>
        <stop offset="50%" stop-color="%C%"/>
        <stop offset="100%" stop-color="%E%"/>
      </linearGradient>
      <linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="%W%" stop-opacity="0"/>
        <stop offset="50%" stop-color="%W%" stop-opacity="0.85"/>
        <stop offset="100%" stop-color="%W%" stop-opacity="0"/>
      </linearGradient>
      <clipPath id="txtClip">
        <text x="500" y="64" text-anchor="middle" font-size="34" font-weight="800"
              font-family="%FONT%">Training models. Building intelligence. Shaping the future.</text>
      </clipPath>
    </defs>
    """
    for k, v in {"%P%": PURPLE, "%C%": CYAN, "%E%": EMERALD, "%W%": WHITE, "%FONT%": FONT}.items():
        defs = defs.replace(k, v)

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" '
        'role="img" aria-label="footer">' % (W, H)
        + style + defs
        + '<rect width="%d" height="%d" fill="%s" rx="12"/>' % (W, H, BG)
        + '<text class="ft" x="500" y="64" text-anchor="middle" font-size="34" '
          'font-weight="800" fill="url(#fg)">Training models. Building intelligence. Shaping the future.</text>'
        + '<g clip-path="url(#txtClip)">'
          '<rect class="shine" x="-260" y="20" width="180" height="70" fill="url(#shineGrad)"/>'
          "</g>"
        + '<line class="ln" x1="320" y1="92" x2="680" y2="92" stroke="url(#fg)" stroke-width="2"/>'
        + '<circle cx="320" cy="92" r="3.5" fill="%s"/>' % PURPLE
        + '<circle cx="680" cy="92" r="3.5" fill="%s"/>' % EMERALD
        + "</svg>"
    )
    write("footer.svg", svg)


# ---------------------------------------------------------------------------
# ATTENTION (self-attention arcs over a Somali sentence)
# ---------------------------------------------------------------------------
def attention():
    # "I am learning AI and Somali NLP"
    tokens = ["Aniga", "waxaan", "baranayaa", "AI", "iyo", "Somali", "NLP"]
    translation = "“I am learning AI and Somali NLP”"

    fs = 18
    charw = 9.3
    padx = 18
    gap = 14
    margin = 64
    pill_h = 46

    widths = [max(52, int(len(t) * charw) + 2 * padx) for t in tokens]
    total = sum(widths) + gap * (len(tokens) - 1)
    W = total + 2 * margin
    H = 300
    pill_y = 214          # arcs anchor at the top edge of each pill
    text_y = pill_y + 30

    xs, centers = [], []
    cx = margin
    for w in widths:
        xs.append(cx)
        centers.append(cx + w / 2)
        cx += w + gap

    style = (
        "<style>"
        ".at{font-family:" + FONT + ";}"
        ".arc{stroke:url(#attArc);fill:none;stroke-dasharray:5 7;"
        "animation:aflow 1.2s linear infinite;}"
        "@keyframes aflow{to{stroke-dashoffset:-24;}}"
        ".qg{opacity:0;animation:qslot %ss ease-in-out infinite;}"
        "@keyframes qslot{0%%{opacity:0}1.5%%{opacity:1}%s%%{opacity:1}"
        "%s%%{opacity:0}100%%{opacity:0}}"
        ".pill{animation:ppulse 3.4s ease-in-out infinite;transform-origin:center;}"
        "@keyframes ppulse{0%%,100%%{opacity:.82}50%%{opacity:1}}"
        "</style>"
    ) % (
        round(len(tokens) * 2.0, 1),
        round(100.0 / len(tokens) - 1.2, 1),
        round(100.0 / len(tokens), 1),
    )

    defs = (
        "<defs>"
        '<linearGradient id="attArc" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="' + CYAN + '"/>'
        '<stop offset="100%" stop-color="' + PURPLE + '"/></linearGradient>'
        '<filter id="aglow" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="2.4"/></filter>'
        "</defs>"
    )

    # static token pills (drawn first, behind the arcs)
    pills = []
    for i, t in enumerate(tokens):
        delay = round(-(i % 4) * 0.4, 1)
        pills.append(
            '<g class="pill" style="animation-delay:%ss">'
            '<rect x="%.0f" y="%d" width="%d" height="%d" rx="12" '
            'fill="#11161D" stroke="#222a35" stroke-width="1"/>'
            '<text class="at" x="%.0f" y="%d" text-anchor="middle" '
            'font-size="%d" font-weight="600" fill="%s">%s</text>'
            '<circle cx="%.0f" cy="%d" r="2.6" fill="%s"/>'
            "</g>"
            % (delay, xs[i], pill_y, widths[i], pill_h,
               centers[i], pill_y + 30, fs, WHITE, t,
               centers[i], pill_y, CYAN)
        )

    # one query-group per token: ring on the active token + arcs to every key
    groups = []
    for qi in range(len(tokens)):
        qx = centers[qi]
        parts = [
            '<g class="qg" style="animation-delay:%ss">' % round(qi * 2.0, 1)
        ]
        # arcs from this query to all other tokens
        for ki in range(len(tokens)):
            if ki == qi:
                continue
            kx = centers[ki]
            dist = abs(qx - kx)
            peak = max(16, pill_y - 30 - dist * 0.26)
            midx = (qx + kx) / 2
            sw = 1.0 + ((qi * 5 + ki * 3) % 4) * 0.7   # pseudo attention weight
            op = round(0.45 + ((qi + ki) % 3) * 0.18, 2)
            fdelay = round(-((ki) % 5) * 0.24, 2)
            parts.append(
                '<path class="arc" d="M%.1f %d Q%.1f %.1f %.1f %d" '
                'stroke-width="%.1f" opacity="%.2f" '
                'style="animation-delay:%ss"/>'
                % (qx, pill_y, midx, peak, kx, pill_y, sw, op, fdelay)
            )
        # highlight ring on the active query token
        parts.append(
            '<rect x="%.0f" y="%d" width="%d" height="%d" rx="12" fill="none" '
            'stroke="%s" stroke-width="2" filter="url(#aglow)"/>'
            % (xs[qi], pill_y, widths[qi], pill_h, EMERALD)
        )
        parts.append("</g>")
        groups.append("".join(parts))

    caption = (
        '<text class="at" x="%d" y="%d" text-anchor="middle" font-size="14" '
        'font-style="italic" fill="%s">%s</text>'
        % (W / 2, text_y + pill_h + 6, MUTED, translation)
    )

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" '
        'role="img" aria-label="Self-attention over a Somali sentence">' % (W, H)
        + style + defs
        + '<rect width="%d" height="%d" fill="%s" rx="14"/>' % (W, H, BG)
        + "".join(pills)
        + "".join(groups)
        + caption
        + "</svg>"
    )
    write("attention.svg", svg)


if __name__ == "__main__":
    hero()
    keywords()
    attention()
    footer()
    print("done ->", OUT)
