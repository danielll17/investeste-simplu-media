# Postare automată

În fiecare zi la 16:45 (ora României), GitHub Actions rulează `engine/run_day.py`. Scriptul ia fișierele din `queue/<data de azi>/`, desenează clipurile animate și le publică pe TikTok și Instagram prin Upload-Post. Fișierele publicate se mută în `done/<data>/`, împreună cu un `log.json`.

## Ce trebuie setat o singură dată
1. Cont pe upload-post.com, cu un profil numit `investeste-simplu` la care conectezi TikTok și Instagram.
2. Cheia API de la Upload-Post se pune în GitHub: Settings > Secrets and variables > Actions > New repository secret, cu numele `UPLOAD_POST_API_KEY`.
3. Pentru fiecare cont nou: o intrare în `accounts.json` (numele profilului din Upload-Post).

Fără cheie, scriptul doar desenează clipul și scrie în jurnal ce ar fi postat (test).

## Un clip = un fișier JSON
`queue/2026-11-25/investeste-simplu.json` (contul se ia din câmpul `account`; pentru mai multe clipuri în aceeași zi pe același cont: `investeste-simplu__2.json`).

```json
{
  "account": "investeste-simplu",
  "okx": true,
  "caption": "Textul descrierii",
  "ig_extra": "Rând în plus doar pe Instagram (disclaimer)",
  "hashtags": ["#bani", "#economii", "#educatiefinanciara"],
  "scenes": [ ... ]
}
```

Textul dintre `*stele*` iese portocaliu. Rândurile lungi se împart singure.

## Tipuri de scene
| type | câmpuri | ce face |
|---|---|---|
| `hook` | title, title2, pose, prop | titlu mare + personaj; prop `bills` = bancnote care zboară |
| `text` | title, lines[], pose, prop | titlu + 1-3 rânduri + personaj |
| `counter` | title, sub, calc, add, prop, items[], stamp[], good | adună bani la un total care continuă între scene; prop `cup`, `pkg`, `subs` (cu items: [["Netflix","40"]]) |
| `flow` | title, boxes[], highlight, stamp, jar | schemă cu căsuțe și săgeți; `stamp` = ștampilă roșie la final; `jar` = moneda cade în borcan |
| `grow` | title, sub, from, to, steps, step_label, down, note | cifră care crește sau scade (down) + borcan |
| `cta` | lines[], cta, disc[] | finalul cu link-ul din bio și disclaimer |
| `question` | title, title2, options[4], footer | întrebarea A/B/C/D |

Opțional pe orice scenă: `d` (durata în secunde).

**Poze personaj:** stand, happy, sad, wow, think, idea, shrug, arms_up, phone, point, wave, lotus, wallet.
**Obiecte (prop):** cup, tv, house, car, chart_up, chart_down, jar, jar_empty, money, pkg, phone, calendar.

## Test local
`CHROME_PATH=/usr/bin/google-chrome python3 engine/run_day.py 2026-11-25 --no-post`
sau doar cadre de previzualizare: `python3 engine/render_video.py queue/.../x.json /tmp/p preview`
