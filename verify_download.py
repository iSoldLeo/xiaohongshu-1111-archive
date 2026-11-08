"""去重笔记，并核对主页数量、采集记录与本地图片。"""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image


ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "downloads" / "63efba5a000000001001c0e3"
MEDIA = ARCHIVE / "xhs" / "media"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif"}


def main():
    records = []
    for path in sorted((ARCHIVE / "xhs" / "json").glob("creator_contents_*.json")):
        records.extend(json.loads(path.read_text(encoding="utf-8")))
    notes_by_id = {note["note_id"]: note for note in records}
    notes = sorted(notes_by_id.values(), key=lambda note: note["time"], reverse=True)
    profile = json.loads((ARCHIVE / "profile.json").read_text(encoding="utf-8"))

    listed_ids = set(json.loads((ARCHIVE / "note_ids.json").read_text(encoding="utf-8")))

    missing_images = []
    expected_images = 0
    for note in notes:
        urls = [url for url in note["image_list"].split(",") if url]
        if note["type"] != "normal":
            raise ValueError(f"需要核对视频笔记的媒体清单: {note['note_id']}")
        expected_images += len(urls)
        for index in range(1, len(urls) + 1):
            candidates = (MEDIA / note["note_id"]).glob(f"{index:03d}.*")
            if not any(path.suffix.lower() in IMAGE_EXTENSIONS and path.stat().st_size > 0
                       for path in candidates):
                missing_images.append(f"{note['note_id']}/{index:03d}")

    files = sorted(path for path in MEDIA.rglob("*") if path.is_file())
    images = [path for path in files if path.suffix.lower() in IMAGE_EXTENSIONS]
    corrupt_images = []
    for index, path in enumerate(images, start=1):
        try:
            with Image.open(path) as image:
                image.load()
        except Exception as exc:
            corrupt_images.append({"path": str(path.relative_to(ARCHIVE)), "error": str(exc)})
        if index % 1000 == 0:
            print(f"已解码校验 {index}/{len(images)} 张图片", flush=True)

    report = {
        "verified_at": datetime.now(ZoneInfo("Asia/Singapore")).isoformat(),
        "creator_id": "63efba5a000000001001c0e3",
        "creator_name": profile["basicInfo"]["nickname"],
        "profile_posted_count": profile["posted"],
        "raw_record_count": len(records),
        "unique_note_count": len(notes),
        "duplicate_record_count": len(records) - len(notes),
        "listed_unique_note_count": len(listed_ids),
        "missing_note_ids": sorted(listed_ids - notes_by_id.keys()),
        "expected_image_count": expected_images,
        "saved_image_count": len(images),
        "image_formats": dict(Counter(path.suffix.lower() for path in images)),
        "media_bytes": sum(path.stat().st_size for path in files),
        "missing_images": missing_images,
        "corrupt_images": corrupt_images,
        "partial_files": [str(path.relative_to(ARCHIVE)) for path in files if path.suffix == ".part"],
        "zero_byte_files": [str(path.relative_to(ARCHIVE)) for path in files if path.stat().st_size == 0],
    }
    report["complete"] = (
        report["unique_note_count"] == report["profile_posted_count"] == report["listed_unique_note_count"]
        and report["expected_image_count"] == report["saved_image_count"]
        and not any(report[key] for key in (
            "missing_note_ids", "missing_images", "corrupt_images", "partial_files", "zero_byte_files"
        ))
    )
    (ARCHIVE / "notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")
    (ARCHIVE / "download_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
