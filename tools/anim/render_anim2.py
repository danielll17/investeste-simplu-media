import sys, subprocess, os
from playwright.sync_api import sync_playwright
FPS=30
mode=sys.argv[1]  # "preview" or "full"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.goto("file://"+os.path.abspath(sys.argv[2])); pg.wait_for_timeout(300)
    durs=pg.evaluate("durs()")
    if mode=="preview":
        for i,(sc,t) in enumerate([(0,2.5),(1,4),(2,4),(3,4),(4,5),(5,4),(6,6),(7,5)]):
            pg.evaluate(f"draw({sc},{t})"); pg.screenshot(path=f"/tmp/pv_{i}.jpg",type="jpeg",quality=80)
    else:
        P=sys.argv[3];os.makedirs(P,exist_ok=True)
        for i,d in enumerate(durs):
            n=int(round(d*FPS)); tmp=f"{P}/s{i}.tmp.mp4"
            ff=subprocess.Popen(["ffmpeg","-y","-loglevel","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-",
                "-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-r",str(FPS),tmp],stdin=subprocess.PIPE)
            for k in range(n):
                pg.evaluate(f"draw({i},{k/FPS})")
                ff.stdin.write(pg.screenshot(type="jpeg",quality=92))
            ff.stdin.close()
            if ff.wait()==0: os.replace(tmp,f"{P}/s{i}.mp4")
            print("scene",i,"done",flush=True)
        print(sum(durs))
    b.close()
