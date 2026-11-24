"""Ruleaza zilnic din GitHub Actions: randeaza si posteaza tot ce e in queue/<azi>/.
Folosire: python3 engine/run_day.py [YYYY-MM-DD] [--no-post]"""
import sys, json, pathlib, datetime, shutil
from zoneinfo import ZoneInfo
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from render_video import render
from post import post

ROOT = pathlib.Path(__file__).resolve().parent.parent
args = [a for a in sys.argv[1:] if not a.startswith("--")]
day = args[0] if args else datetime.datetime.now(ZoneInfo("Europe/Bucharest")).strftime("%Y-%m-%d")
accounts = json.loads((ROOT / "accounts.json").read_text())
qdir = ROOT / "queue" / day
out = ROOT / "out"; out.mkdir(exist_ok=True)
log = []
if not qdir.exists():
    print("Nimic programat pentru", day); sys.exit(0)
for spec_file in sorted(qdir.glob("*.json")):
    spec = json.loads(spec_file.read_text())
    acc_name = spec.get("account", spec_file.stem.split("__")[0])
    acc = accounts[acc_name]
    video = out / f"{day}__{spec_file.stem}.mp4"
    dur = render(spec_file, video)
    res = {"skipped": True} if "--no-post" in sys.argv else post(video, spec, acc)
    log.append({"file": spec_file.name, "account": acc_name, "seconds": dur, "result": res})
    done = ROOT / "done" / day; done.mkdir(parents=True, exist_ok=True)
    if "--no-post" not in sys.argv and not res.get("dry_run"):
        shutil.move(str(spec_file), done / spec_file.name)
(ROOT / "done" / day).mkdir(parents=True, exist_ok=True)
(ROOT / "done" / day / "log.json").write_text(json.dumps(log, ensure_ascii=False, indent=2))
print(json.dumps(log, ensure_ascii=False, indent=2))
