"""Publica un clip pe TikTok + Instagram prin Upload-Post. Fara cheie API (UPLOAD_POST_API_KEY) face doar test (dry run)."""
import os, json, requests

API = "https://api.upload-post.com/api/upload"

def post(video, spec, account):
    key = os.environ.get("UPLOAD_POST_API_KEY")
    cap = spec["caption"]
    tags = " ".join(spec.get("hashtags", [])[:3])
    full = f"{cap}\n\n{tags}".strip()
    ig = full + ("\n\n" + spec["ig_extra"] if spec.get("ig_extra") else "")
    data = [("user", account["user"]), ("title", cap[:90]), ("tiktok_title", full), ("instagram_title", ig),
            ("privacy_level", "PUBLIC_TO_EVERYONE"), ("media_type", "REELS"), ("share_to_feed", "true"), ("async_upload", "true")]
    data += [("platform[]", p) for p in account.get("platforms", ["tiktok", "instagram"])]
    if spec.get("okx"):
        data.append(("brand_content_toggle", "true"))
    if not key:
        print("DRY RUN (lipseste UPLOAD_POST_API_KEY):", json.dumps(dict(data), ensure_ascii=False)[:400])
        return {"dry_run": True}
    with open(video, "rb") as f:
        r = requests.post(API, headers={"Authorization": f"Apikey {key}", "Idempotency-Key": os.path.basename(video)},
                          data=data, files={"video": f}, timeout=300)
    print(r.status_code, r.text[:500])
    r.raise_for_status()
    return r.json()
