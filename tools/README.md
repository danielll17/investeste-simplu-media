# Unelte @investeste.simplu

Rulează totul din folderul `tools/`. Instalare: `pip install playwright pillow numpy --break-system-packages`, Chrome la /usr/bin/google-chrome, ffmpeg.

- Carusel text: `python3 render.py specs/v15_nvidia.json out_tt tt` (fmt: ig, tt, reel)
- Mihai & Ana: `python3 comic.py specs/v16_ep1.json out_tt tt` (tt sau reel)
- Reel din slide-uri: `python3 reel/make_reel.py out_reel reel.mp4 5`
- Muzică originală: `python3 reel/music.py <secunde> out.wav`
- Clip animat cu oameni-băț: `cd anim && python3 render_anim2.py preview scenes2.html parts` (cadre în /tmp/pv_*.jpg), apoi `full` în loc de `preview`; uni părțile cu ffmpeg concat `-c copy` și adaugă muzica cu `-c:v copy`.

`specs/` conține JSON-urile postărilor vechi, ca exemple de structură.
