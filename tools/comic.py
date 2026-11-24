import json, sys, pathlib
from playwright.sync_api import sync_playwright

SKIN = {"mihai": "#f1c7a3", "ana": "#e9b896"}
SHIRT = {"mihai": "#3b82f6", "ana": "#8b5cf6"}
DARK = "#1c1c22"

def face(mood):
    ey, er = -545, 9
    brows = '<path d="M-45,-572 L-18,-575 M18,-575 L45,-572" stroke="#3a2a22" stroke-width="7" stroke-linecap="round"/>'
    mouth = '<path d="M-28,-505 Q0,-482 28,-505" stroke="#3a2a22" stroke-width="7" fill="none" stroke-linecap="round"/>'
    if mood == "excited":
        er = 10
        mouth = '<path d="M-32,-510 Q0,-468 32,-510 Z" fill="#3a2a22"/><path d="M-18,-494 Q0,-484 18,-494" stroke="#e46a6a" stroke-width="8" fill="none"/>'
        brows = '<path d="M-45,-582 L-18,-588 M18,-588 L45,-582" stroke="#3a2a22" stroke-width="7" stroke-linecap="round"/>'
    elif mood == "surprised":
        er = 12
        mouth = '<ellipse cx="0" cy="-498" rx="13" ry="17" fill="#3a2a22"/>'
        brows = '<path d="M-45,-588 L-18,-592 M18,-592 L45,-588" stroke="#3a2a22" stroke-width="7" stroke-linecap="round"/>'
    elif mood == "think":
        ey = -552
        mouth = '<path d="M-18,-502 L20,-506" stroke="#3a2a22" stroke-width="7" stroke-linecap="round"/>'
        brows = '<path d="M-45,-578 L-18,-574 M18,-582 L45,-586" stroke="#3a2a22" stroke-width="7" stroke-linecap="round"/>'
    elif mood == "worried":
        mouth = '<path d="M-24,-498 Q-12,-510 0,-500 Q12,-490 24,-502" stroke="#3a2a22" stroke-width="7" fill="none" stroke-linecap="round"/>'
        brows = '<path d="M-45,-566 L-18,-580 M18,-580 L45,-566" stroke="#3a2a22" stroke-width="7" stroke-linecap="round"/>'
    elif mood == "smirk":
        mouth = '<path d="M-24,-506 Q8,-490 30,-514" stroke="#3a2a22" stroke-width="7" fill="none" stroke-linecap="round"/>'
        brows = '<path d="M-45,-572 L-18,-575 M18,-582 L45,-578" stroke="#3a2a22" stroke-width="7" stroke-linecap="round"/>'
    eyes = f'<circle cx="-30" cy="{ey}" r="{er}" fill="#2a1d18"/><circle cx="30" cy="{ey}" r="{er}" fill="#2a1d18"/>'
    cheeks = '<circle cx="-52" cy="-515" r="13" fill="#f29b8a" opacity=".45"/><circle cx="52" cy="-515" r="13" fill="#f29b8a" opacity=".45"/>'
    return eyes + brows + cheeks + mouth

def arms(who, pose):
    c, s = SHIRT[who], SKIN[who]
    def arm(pts):
        d = " ".join(f"{x},{y}" for x, y in pts)
        hx, hy = pts[-1]
        return (f'<polyline points="{d}" stroke="{c}" stroke-width="36" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<circle cx="{hx}" cy="{hy}" r="20" fill="{s}"/>')
    left = arm([(-78, -400), (-112, -300), (-108, -228)])
    if pose == "phone":
        right = arm([(78, -400), (112, -320), (46, -330)])
        phone = '<rect x="18" y="-410" width="52" height="88" rx="10" fill="#111" stroke="#555" stroke-width="4"/><rect x="25" y="-400" width="38" height="62" rx="4" fill="#f7931a" opacity=".85"/>'
        return left + right + phone
    if pose == "point":
        right = arm([(78, -400), (150, -420), (215, -455)])
        return left + right
    if pose == "hips":
        left = arm([(-78, -400), (-140, -310), (-86, -262)])
        right = arm([(78, -400), (140, -310), (86, -262)])
        return left + right
    if pose == "shrug":
        left = arm([(-78, -400), (-150, -380), (-170, -450)])
        right = arm([(78, -400), (150, -380), (170, -450)])
        return left + right
    right = arm([(78, -400), (112, -300), (108, -228)])
    return left + right

def hair(who, back):
    if who == "mihai":
        if back:
            return ""
        return ('<path d="M-90,-548 Q-100,-650 -20,-648 L-4,-672 L14,-646 L40,-664 L44,-640 '
                'Q100,-630 90,-548 Q78,-608 10,-612 Q-60,-614 -90,-548Z" fill="#2b211c"/>')
    if back:
        return ('<path d="M-102,-560 Q-118,-430 -76,-400 L76,-400 Q118,-430 102,-560 '
                'Q92,-656 0,-656 Q-92,-656 -102,-560Z" fill="#5a3522"/>')
    return ('<path d="M-90,-556 Q-66,-648 4,-642 Q70,-640 90,-556 Q50,-604 -6,-596 Q-50,-604 -90,-556Z" fill="#5a3522"/>'
            '<circle cx="0" cy="-662" r="30" fill="#5a3522"/>')

def person(who, x, y, scale, mood="happy", pose="down", flip=False):
    s, c = SKIN[who], SHIRT[who]
    fx = -1 if flip else 1
    g = [f'<g transform="translate({x},{y}) scale({scale*fx},{scale})">',
         '<ellipse cx="0" cy="4" rx="110" ry="16" fill="#000" opacity=".35"/>',
         f'<rect x="-50" y="-210" width="40" height="205" rx="18" fill="{DARK}"/>',
         f'<rect x="10" y="-210" width="40" height="205" rx="18" fill="{DARK}"/>',
         '<ellipse cx="-34" cy="-6" rx="34" ry="14" fill="#eee"/><ellipse cx="34" cy="-6" rx="34" ry="14" fill="#eee"/>',
         hair(who, True),
         f'<rect x="-88" y="-440" width="176" height="250" rx="48" fill="{c}"/>',
         f'<rect x="-20" y="-468" width="40" height="40" fill="{s}"/>',
         f'<circle cx="0" cy="-540" r="88" fill="{s}"/>',
         hair(who, False), face(mood), arms(who, pose)]
    if who == "mihai":
        g.insert(7, f'<path d="M-40,-440 Q0,-405 40,-440" stroke="#2f6bd0" stroke-width="10" fill="none"/>')
    g.append('</g>')
    return "".join(g)

def tv(x, y):
    return (f'<g transform="translate({x},{y})"><rect x="-120" y="-250" width="240" height="150" rx="10" fill="#111" stroke="#444" stroke-width="6"/>'
            '<rect x="-108" y="-238" width="216" height="126" fill="#1f3b63"/>'
            '<rect x="-12" y="-100" width="24" height="60" fill="#444"/><rect x="-60" y="-44" width="120" height="14" rx="7" fill="#444"/>'
            '<g transform="rotate(-12 80 -250)"><rect x="40" y="-290" width="110" height="56" rx="12" fill="#ef4444"/>'
            '<text x="95" y="-250" font-size="36" font-weight="800" fill="#fff" text-anchor="middle" font-family="Inter">-40%</text></g></g>')

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;font-family:'Inter',sans-serif;background:#0b0b0f;color:#f5f5f7;
 display:flex;flex-direction:column;padding:180px 120px 420px 88px;position:relative;overflow:hidden}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;
 background:radial-gradient(circle,rgba(247,147,26,.22),transparent 65%);top:-300px;right:-350px}
.top{display:flex;justify-content:space-between;font-size:30px;color:#8e8e98;font-weight:500;z-index:1}
.ep{display:inline-block;margin-top:34px;background:#f7931a;color:#0b0b0f;font-weight:800;font-size:28px;
 padding:10px 22px;border-radius:999px;align-self:flex-start;z-index:1}
.narr{margin-top:22px;font-size:36px;color:#a8a8b2;line-height:1.3;z-index:1}
h1{margin-top:30px;font-size:84px;font-weight:800;line-height:1.04;letter-spacing:-2px;z-index:1}
.accent{color:#f7931a}
.talk{flex:1;display:flex;flex-direction:column;justify-content:flex-end;gap:26px;z-index:1;padding-bottom:18px}
.b{position:relative;max-width:640px;background:#f5f5f7;color:#111;font-size:40px;line-height:1.28;
 font-weight:600;padding:26px 32px;border-radius:30px}
.b.l{align-self:flex-start}.b.r{align-self:flex-end;background:#ece6ff}
.b:after{content:"";position:absolute;bottom:-22px;border:14px solid transparent}
.b.l:after{left:70px;border-top:22px solid #f5f5f7;border-left:16px solid #f5f5f7}
.b.r:after{right:70px;border-top:22px solid #ece6ff;border-right:16px solid #ece6ff}
.who{display:block;font-size:26px;font-weight:800;margin-bottom:6px;opacity:.55}
.card{align-self:center;width:500px;background:#16161c;border:3px solid #2c2c35;border-radius:30px;padding:24px 32px}
.card .t{font-size:28px;color:#8e8e98;font-weight:600}.card .v{font-size:46px;font-weight:800;margin-top:6px}
.card .row{display:flex;justify-content:space-between;margin-top:12px;font-size:30px;color:#c7c7cf}
.card .ok{color:#22c55e;font-weight:800}
.opts{font-size:46px;line-height:1.6;font-weight:600;margin-top:20px}
.cta{display:inline-block;background:#f7931a;color:#0b0b0f;font-weight:800;font-size:40px;padding:22px 38px;border-radius:22px;align-self:flex-start;margin-top:26px;z-index:1}
.disc{font-size:24px;color:#6e6e78;margin-top:18px;z-index:1}
svg{z-index:1;display:block;flex-shrink:0}
.bottom{display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#6e6e78;z-index:1;margin-top:20px}
.dots{display:flex;gap:12px}.dot{width:14px;height:14px;border-radius:50%;background:#33333b}
.dot.on{background:#f7931a;width:40px;border-radius:7px}
"""

def scene(s):
    parts = ['<svg width="872" height="560" viewBox="0 0 872 560">',
             '<rect x="0" y="540" width="872" height="20" rx="10" fill="#1a1a21"/>']
    if s.get("tv"):
        parts.append(tv(436, 545))
    m, a = s.get("mihai"), s.get("ana")
    mx, ax = (170, 700) if s.get("tv") else (230, 650)
    if m: parts.append(person("mihai", mx, 545, .8, m[0], m[1]))
    if a: parts.append(person("ana", ax, 545, .8, a[0], a[1], flip=True))
    parts.append('</svg>')
    return "".join(parts)

def slide_html(s, i, n, spec, swipe_on):
    dots = "".join(f'<div class="dot{" on" if k==i else ""}"></div>' for k in range(n))
    h = [f'<div class="top"><span>{spec["handle"]}</span><span>{i+1}/{n}</span></div>',
         f'<div class="ep">{spec["episode"]}</div>']
    if s.get("title"): h.append(f'<h1>{s["title"]}</h1>')
    if s.get("narr"): h.append(f'<div class="narr">{s["narr"]}</div>')
    if s.get("cta"): h.append(f'<div class="cta">{s["cta"]}</div>')
    if s.get("disc"): h.append(f'<div class="disc">{s["disc"]}</div>')
    talk = []
    if s.get("opts"): talk.append(f'<div class="opts">{s["opts"]}</div>')
    if s.get("card"):
        c = s["card"]
        rows = "".join(f'<div class="row"><span>{k}</span><span class="{cls}">{v}</span></div>' for k, v, cls in c["rows"])
        talk.append(f'<div class="card"><div class="t">{c["t"]}</div><div class="v">{c["v"]}</div>{rows}</div>')
    for side, txt in s.get("say", []):
        name = "Mihai" if side == "l" else "Ana"
        talk.append(f'<div class="b {side}"><span class="who">{name}</span>{txt}</div>')
    h.append(f'<div class="talk">{"".join(talk)}</div>')
    h.append(scene(s))
    swipe = "Glisează →" if (i < n-1 and swipe_on) else ""
    h.append(f'<div class="bottom"><div class="dots">{dots}</div><span>{swipe}</span></div>')
    return f'<html><head><style>{CSS}</style></head><body><div class="glow"></div>{"".join(h)}</body></html>'

def main(spec_path, out_dir, fmt="tt"):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    sl = spec["slides"]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for i, s in enumerate(sl):
            pg.set_content(slide_html(s, i, len(sl), spec, fmt != "reel"))
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(out / f"slide_{i+1}.png"))
        b.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "tt")
