#!/usr/bin/env python3
"""Upload the Muallimi soniy lesson audio to Cloudflare R2, and check it.

    uv run --with boto3 python scripts/tajweed/upload_r2.py --dry-run
    uv run --with boto3 python scripts/tajweed/upload_r2.py
    python3 scripts/tajweed/upload_r2.py --verify      # public URLs only, no keys

Source: data/tajweed/downloads/NNN_<Slug>.mp3 (gitignored), as listed in
data/tajweed/muallimi.json. Each file goes to `tajweed/muallimi-soniy/NNN.mp3` with
audio/mpeg, a year-long immutable cache and its sha256 as object metadata, so a
re-run skips every file that is already there unchanged.

Credentials come from the environment (see .env.example) and are never printed.
--verify needs only TAJWEED_AUDIO_BASE_URL: it HEADs every public URL and checks
status, size and Range support. Light: one file in memory at a time.
"""

import argparse
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOWNLOADS = os.path.join(ROOT, "data", "tajweed", "downloads")
MANIFEST = os.path.join(ROOT, "data", "tajweed", "muallimi.json")
PREFIX = "tajweed/muallimi-soniy/"
CACHE = "public, max-age=31536000, immutable"


def _lessons() -> list:
    with open(MANIFEST, encoding="utf-8") as fp:
        return json.load(fp)["lessons"]


def _local(n: int) -> str:
    for name in os.listdir(DOWNLOADS):
        if re.match(r"^%03d_.+\.mp3$" % n, name):
            return os.path.join(DOWNLOADS, name)
    raise FileNotFoundError("no download for lesson %d" % n)


def _env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        sys.exit("%s is not set (see .env.example)" % name)
    return value


def upload(dry_run: bool) -> int:
    import hashlib

    import boto3
    from botocore.exceptions import ClientError

    s3 = boto3.client(
        "s3",
        endpoint_url="https://%s.r2.cloudflarestorage.com" % _env("R2_ACCOUNT_ID"),
        aws_access_key_id=_env("R2_ACCESS_KEY_ID"),
        aws_secret_access_key=_env("R2_SECRET_ACCESS_KEY"),
        region_name="auto",
    )
    bucket = _env("R2_BUCKET")
    sent = skipped = 0
    for lesson in _lessons():
        key = PREFIX + lesson["file"]
        try:
            head = s3.head_object(Bucket=bucket, Key=key)
            if head.get("Metadata", {}).get("sha256") == lesson["sha256"]:
                skipped += 1
                continue
        except ClientError as err:
            if err.response.get("Error", {}).get("Code") not in ("404", "NoSuchKey", "NotFound"):
                raise
        with open(_local(lesson["n"]), "rb") as fp:
            data = fp.read()
        if hashlib.sha256(data).hexdigest() != lesson["sha256"]:
            sys.exit("%s differs from muallimi.json; re-run scripts/tajweed/muallimi.py" % key)
        print(("would upload" if dry_run else "upload"), key, "%.1f MB" % (len(data) / 1e6))
        if not dry_run:
            s3.put_object(
                Bucket=bucket,
                Key=key,
                Body=data,
                ContentType="audio/mpeg",
                CacheControl=CACHE,
                Metadata={"sha256": lesson["sha256"]},
            )
        sent += 1
    print("%d %s, %d already there" % (sent, "to upload" if dry_run else "uploaded", skipped))
    return 0


def verify() -> int:
    base = _env("TAJWEED_AUDIO_BASE_URL").rstrip("/") + "/"
    bad = 0
    for lesson in _lessons():
        url = base + lesson["file"]
        req = urllib.request.Request(url, method="HEAD", headers={"Range": "bytes=0-1"})
        try:
            with urllib.request.urlopen(req, timeout=20) as res:
                status = res.status
                total = (res.headers.get("Content-Range") or "").rpartition("/")[2]
                ok = status == 206 and total == str(lesson["bytes"])
        except OSError as err:
            status, total, ok = err, "", False
        if not ok:
            bad += 1
            print("BAD", url, status, total, "expected", lesson["bytes"])
    print("%d/%d ok" % (len(_lessons()) - bad, len(_lessons())))
    return 1 if bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="list what would be uploaded")
    ap.add_argument("--verify", action="store_true", help="check every public URL")
    args = ap.parse_args()
    return verify() if args.verify else upload(args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
