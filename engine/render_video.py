"""Randeaza un clip animat dintr-un fisier JSON. Folosire: python3 engine/render_video.py spec.json out.mp4 [preview]"""
import json, os, subprocess, sys, tempfile, pathlib
from playwright.sync_api import sync_playwright
FPS = 30
HERE = pathlib.Path(__file__).resolve().parent

def render(spec_path, out, preview=False):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    work = pathlib.Path(tempfile.mkdtemp(prefix="vid_"))
    with sync_playwright() as p:
        kw = {"executable_path": os.environ["CHROME_PATH"]} if os.environ.get("CHROME_PATH") else {}
        b = p.chromium.launch(**kw)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto((HERE / "page.html").as_uri()); pg.wait_for_timeout(300)
        assets = [str(x.relative_to(HERE)) for x in list((HERE / "chars").rglob("*.png")) + list((HERE / "props").glob("*.png"))]
        pg.evaluate("l=>preload(l)", assets)
        pg.evaluate("s=>load(s)", spec)
        durs = pg.evaluate("durs()")
        if preview:
            for i, d in enumerate(durs):
                pg.evaluate(f"draw({i},{d*0.8})")
                pg.screenshot(path=f"{out}_{i}.jpg", type="jpeg", quality=80)
            b.close(); return
        parts = []
        for i, d in enumerate(durs):
            n = int(round(d * FPS)); part = work / f"s{i}.mp4"; tmp = work / f"s{i}.tmp.mp4"
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "mjpeg", "-i", "-",
                                   "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), str(tmp)], stdin=subprocess.PIPE)
            cover_t = spec.get("cover_t", min(durs[0] - 0.3, 3.0))
            for k in range(n):
                # primele cadre ale clipului = coperta (TikTok/Instagram iau primul cadru ca miniatura)
                tt = cover_t if (i == 0 and k < 4) else k / FPS
                pg.evaluate(f"draw({i},{tt})")
                ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
            ff.stdin.close()
            if ff.wait() != 0: raise SystemExit(f"ffmpeg a esuat la scena {i}")
            tmp.rename(part); parts.append(part)
        b.close()
    (work / "list.txt").write_text("".join(f"file '{x}'\n" for x in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(work / "list.txt"), "-c", "copy", str(work / "silent.mp4")], check=True)
    total = sum(durs)
    subprocess.run([sys.executable, str(HERE / "music.py"), f"{total:.2f}", str(work / "m.wav")], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(work / "silent.mp4"), "-i", str(work / "m.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", f"afade=t=out:st={total-1.5:.2f}:d=1.5", "-shortest", str(out)], check=True)
    return total

if __name__ == "__main__":
    r = render(sys.argv[1], sys.argv[2], len(sys.argv) > 3 and sys.argv[3] == "preview")
    print(r)
