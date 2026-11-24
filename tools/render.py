import json, sys, pathlib
from playwright.sync_api import sync_playwright

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:'Inter',sans-serif;background:#0b0b0f;color:#f5f5f7;
 display:flex;flex-direction:column;padding:96px 88px;position:relative;overflow:hidden}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;
 background:radial-gradient(circle,rgba(247,147,26,.28),transparent 65%);top:-300px;right:-350px}
.top{display:flex;justify-content:space-between;font-size:30px;color:#8e8e98;font-weight:500;z-index:1}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;z-index:1}
.num{font-size:150px;font-weight:800;color:#f7931a;line-height:1;margin-bottom:28px}
h1{font-size:104px;font-weight:800;line-height:1.02;letter-spacing:-3px}
h2{font-size:78px;font-weight:800;line-height:1.08;letter-spacing:-2px;margin-bottom:40px}
p{font-size:44px;line-height:1.35;color:#c7c7cf;font-weight:400}
.accent{color:#f7931a}
.cta{margin-top:56px;display:inline-block;background:#f7931a;color:#0b0b0f;font-weight:800;
 font-size:46px;padding:30px 48px;border-radius:24px;align-self:flex-start}
.bottom{display:flex;justify-content:space-between;align-items:center;font-size:28px;color:#6e6e78;z-index:1}
.dots{display:flex;gap:12px}.dot{width:14px;height:14px;border-radius:50%;background:#33333b}
.dot.on{background:#f7931a;width:40px;border-radius:7px}
.disc{font-size:26px;color:#6e6e78;margin-top:40px}
"""

def slide_html(s, i, n, handle, css, swipe_on=True):
    dots = "".join(f'<div class="dot{" on" if k==i else ""}"></div>' for k in range(n))
    if s["type"] == "cover":
        body = f'<h1>{s["title"]}</h1><p style="margin-top:40px">{s["sub"]}</p>'
    elif s["type"] == "text":
        body = f'<h2>{s["title"]}</h2><p>{s["text"]}</p>'
    elif s["type"] == "step":
        body = f'<div class="num">{s["num"]}</div><h2>{s["title"]}</h2><p>{s["text"]}</p>'
    else:
        body = (f'<h2>{s["title"]}</h2><p>{s["text"]}</p>'
                f'<div class="cta">{s["cta"]}</div><div class="disc">{s["disc"]}</div>')
    swipe = "Glisează →" if (i < n-1 and swipe_on) else ""
    return (f'<html><head><style>{css}</style></head><body><div class="glow"></div>'
            f'<div class="top"><span>{handle}</span><span>{i+1}/{n}</span></div>'
            f'<div class="main">{body}</div>'
            f'<div class="bottom"><div class="dots">{dots}</div><span>{swipe}</span></div></body></html>')

TT = CSS.replace('height:1350px','height:1920px').replace('padding:96px 88px','padding:180px 120px 420px 88px')

def main(spec_path, out_dir, fmt="ig"):
    css, h = (TT, 1920) if fmt in ("tt","reel") else (CSS, 1350)
    spec = json.loads(pathlib.Path(spec_path).read_text())
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    slides = spec["slides"]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = b.new_page(viewport={"width":1080,"height":h})
        for i, s in enumerate(slides):
            pg.set_content(slide_html(s, i, len(slides), spec["handle"], css, fmt != "reel"))
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(out/f"slide_{i+1}.png"))
        b.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "ig")
