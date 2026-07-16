#!/usr/bin/env python3
"""Normalize competitor-ad JSON or CSV exports using Python's standard library.

Usage:
    python scripts/normalize-ads.py input.json normalized-ads.json
    python scripts/normalize-ads.py input.csv normalized-ads.json

The input should use the canonical fields documented in SKILL.md. Unknown fields are
preserved under source_extra. Warnings are written to stderr; records are never silently
dropped merely because optional data is missing.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


FIELDS: dict[str, Any] = {
    "record_id": None,
    "source": None,
    "source_url": None,
    "retrieved_at": None,
    "advertiser": None,
    "advertiser_id": None,
    "ad_id": None,
    "platform": None,
    "markets": [],
    "languages": [],
    "status": None,
    "first_seen": None,
    "last_seen": None,
    "format": None,
    "headline": None,
    "body": None,
    "cta": None,
    "landing_url": None,
    "media_urls": [],
    "derived_text": None,
    "source_metrics": {},
    "source_notes": None,
}

LIST_FIELDS = {"markets", "languages", "media_urls"}
DATE_FIELDS = {"retrieved_at", "first_seen", "last_seen"}
TRACKING_KEYS = {
    "fbclid",
    "gclid",
    "dclid",
    "msclkid",
    "mc_cid",
    "mc_eid",
}


def warn(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)


def read_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))

    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = payload.get("records", payload.get("ads"))
    else:
        records = None
    if not isinstance(records, list):
        raise ValueError("JSON must be an array or an object containing records/ads array")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every ad record must be a JSON object")
    return records


def clean_scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def clean_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        candidates = value
    elif isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                parsed = json.loads(stripped)
                candidates = parsed if isinstance(parsed, list) else [stripped]
            except json.JSONDecodeError:
                candidates = re.split(r"[|,]", stripped)
        else:
            candidates = re.split(r"[|,]", stripped)
    else:
        candidates = [value]
    return list(dict.fromkeys(str(item).strip() for item in candidates if str(item).strip()))


def canonicalize_url(value: Any) -> str | None:
    value = clean_scalar(value)
    if not isinstance(value, str):
        return value
    try:
        parts = urlsplit(value)
        filtered = [
            (key, val)
            for key, val in parse_qsl(parts.query, keep_blank_values=True)
            if not key.lower().startswith("utm_") and key.lower() not in TRACKING_KEYS
        ]
        host = parts.netloc.lower()
        scheme = parts.scheme.lower()
        path = parts.path.rstrip("/") or "/"
        return urlunsplit((scheme, host, path, urlencode(filtered), ""))
    except ValueError:
        return value


def normalize_date(value: Any, field: str, index: int) -> str | None:
    value = clean_scalar(value)
    if not isinstance(value, str):
        return value
    candidate = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
        if field == "retrieved_at":
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        return parsed.date().isoformat() if len(value) <= 10 else parsed.isoformat()
    except ValueError:
        warn(f"record {index}: kept invalid {field} value {value!r}")
        return value


def normalize_metrics(value: Any, index: int) -> dict[str, Any]:
    if value is None or value == "":
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    warn(f"record {index}: source_metrics was not an object; preserved as raw_value")
    return {"raw_value": value}


def make_fingerprint(record: dict[str, Any]) -> str:
    identity = {
        key: record.get(key)
        for key in (
            "source",
            "advertiser",
            "ad_id",
            "platform",
            "markets",
            "languages",
            "format",
            "headline",
            "body",
            "cta",
            "landing_url",
            "first_seen",
            "last_seen",
        )
    }
    encoded = json.dumps(identity, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def slug(value: Any, fallback: str) -> str:
    text = str(value or fallback).lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return cleaned or fallback


def normalize_record(raw: dict[str, Any], index: int) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for field, default in FIELDS.items():
        value = raw.get(field)
        if field in LIST_FIELDS:
            normalized[field] = clean_list(value)
        elif field in DATE_FIELDS:
            normalized[field] = normalize_date(value, field, index)
        elif field == "source_metrics":
            normalized[field] = normalize_metrics(value, index)
        elif field in {"source_url", "landing_url"}:
            normalized[field] = canonicalize_url(value)
        else:
            normalized[field] = clean_scalar(value)

        if normalized[field] is None and default is not None:
            normalized[field] = default.copy() if hasattr(default, "copy") else default

    normalized["media_urls"] = [
        url for item in normalized["media_urls"] if (url := canonicalize_url(item))
    ]

    extras = {key: value for key, value in raw.items() if key not in FIELDS}
    if extras:
        normalized["source_extra"] = extras

    if not normalized["retrieved_at"]:
        normalized["retrieved_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        warn(f"record {index}: retrieved_at missing; used normalization time")
    if not normalized["source_url"]:
        warn(f"record {index}: source_url missing; record cannot support sourced findings")
    if not normalized["source"]:
        warn(f"record {index}: source missing")
    if not normalized["advertiser"]:
        warn(f"record {index}: advertiser missing")

    fingerprint = make_fingerprint(normalized)
    if not normalized["record_id"]:
        source = slug(normalized["source"], "source")
        advertiser = slug(normalized["advertiser"], "advertiser")
        suffix = slug(normalized["ad_id"], fingerprint[:12])
        normalized["record_id"] = f"{source}:{advertiser}:{suffix}"
    return normalized


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: normalize-ads.py INPUT.(json|csv) OUTPUT.json", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    if not input_path.is_file():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        return 2

    try:
        raw_records = read_records(input_path)
        normalized_records: list[dict[str, Any]] = []
        seen: set[str] = set()
        for index, raw in enumerate(raw_records, start=1):
            record = normalize_record(raw, index)
            fingerprint = make_fingerprint(record)
            if fingerprint in seen:
                warn(f"record {index}: removed exact duplicate {record['record_id']}")
                continue
            seen.add(fingerprint)
            normalized_records.append(record)

        output_path.write_text(
            json.dumps(normalized_records, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(
        f"normalized {len(raw_records)} records to {len(normalized_records)}: {output_path}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
