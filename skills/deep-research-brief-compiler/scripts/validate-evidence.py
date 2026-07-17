#!/usr/bin/env python3
"""Validate a research evidence ledger and inline citations in a decision brief.

Usage:
    python scripts/validate-evidence.py evidence-ledger.json decision-brief.md

Uses only Python's standard library. Exits non-zero for structural, citation, or confidence
errors. Warnings identify unused sources and weak claim support.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


SOURCE_ID = re.compile(r"^S\d{2,}$")
CLAIM_ID = re.compile(r"^C\d{2,}$")
INLINE_CITATION = re.compile(r"\[(S\d{2,})\]")
DIMENSION_RANGES = {
    "authority": (0, 3),
    "directness": (0, 2),
    "corroboration": (0, 2),
    "timeliness_scope_fit": (0, 2),
    "consistency": (0, 1),
}


def require_list(value: Any, field: str, errors: list[str]) -> list[Any]:
    if not isinstance(value, list):
        errors.append(f"{field} must be an array")
        return []
    return value


def validate_unique_ids(
    records: list[Any],
    field: str,
    pattern: re.Pattern[str],
    errors: list[str],
) -> set[str]:
    ids: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"{field}[{index}] must be an object")
            continue
        expected_field = "source_id" if field == "sources" else "claim_id"
        value = record.get(expected_field)
        if not isinstance(value, str) or not pattern.fullmatch(value):
            errors.append(f"{field}[{index}].{expected_field} has invalid format")
            continue
        if value in ids:
            errors.append(f"duplicate {expected_field}: {value}")
        ids.add(value)
    return ids


def expected_label(total: int) -> str:
    if total >= 8:
        return "high"
    if total >= 5:
        return "medium"
    if total >= 2:
        return "low"
    return "unsupported"


def validate_confidence(claim: dict[str, Any], errors: list[str]) -> None:
    claim_id = claim.get("claim_id", "<unknown>")
    confidence = claim.get("confidence")
    if not isinstance(confidence, dict):
        errors.append(f"{claim_id}: confidence must be an object")
        return

    subtotal = 0
    for field, (minimum, maximum) in DIMENSION_RANGES.items():
        value = confidence.get(field)
        if not isinstance(value, int) or not minimum <= value <= maximum:
            errors.append(f"{claim_id}: confidence.{field} must be {minimum}–{maximum}")
            continue
        subtotal += value

    penalties = confidence.get("penalties")
    if not isinstance(penalties, int) or penalties < 0:
        errors.append(f"{claim_id}: confidence.penalties must be a non-negative integer")
        penalties = 0

    calculated = max(0, subtotal - penalties)
    total = confidence.get("total")
    if total != calculated:
        errors.append(f"{claim_id}: confidence.total is {total!r}; expected {calculated}")

    label = confidence.get("label")
    if label not in {"high", "medium", "low", "unsupported", "disputed"}:
        errors.append(f"{claim_id}: invalid confidence.label {label!r}")
    elif label != "disputed" and label != expected_label(calculated):
        errors.append(
            f"{claim_id}: confidence.label is {label!r}; expected {expected_label(calculated)!r}"
        )

    if not isinstance(confidence.get("rationale"), str) or not confidence["rationale"].strip():
        errors.append(f"{claim_id}: confidence.rationale is required")


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: validate-evidence.py EVIDENCE.json BRIEF.md", file=sys.stderr)
        return 2

    ledger_path = Path(sys.argv[1])
    brief_path = Path(sys.argv[2])
    errors: list[str] = []
    warnings: list[str] = []

    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        brief = brief_path.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if not isinstance(ledger, dict):
        print("error: evidence ledger must be a JSON object", file=sys.stderr)
        return 2

    sources = require_list(ledger.get("sources"), "sources", errors)
    claims = require_list(ledger.get("claims"), "claims", errors)
    source_ids = validate_unique_ids(sources, "sources", SOURCE_ID, errors)
    validate_unique_ids(claims, "claims", CLAIM_ID, errors)

    claim_source_ids: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("claim_id", "<unknown>")
        statement = claim.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            errors.append(f"{claim_id}: statement is required")

        supporting = require_list(
            claim.get("supporting_source_ids"),
            f"{claim_id}.supporting_source_ids",
            errors,
        )
        contradicting = require_list(
            claim.get("contradicting_source_ids"),
            f"{claim_id}.contradicting_source_ids",
            errors,
        )
        for source_id in supporting + contradicting:
            if source_id not in source_ids:
                errors.append(f"{claim_id}: unknown source ID {source_id!r}")
            elif isinstance(source_id, str):
                claim_source_ids.add(source_id)

        if not supporting and claim.get("claim_type") != "assumption":
            warnings.append(f"{claim_id}: non-assumption claim has no supporting source")
        validate_confidence(claim, errors)

    cited_ids = set(INLINE_CITATION.findall(brief))
    for source_id in sorted(cited_ids - source_ids):
        errors.append(f"brief cites unknown source ID {source_id}")
    for source_id in sorted(claim_source_ids - cited_ids):
        errors.append(f"claim evidence source {source_id} is not cited in the brief")
    for source_id in sorted(source_ids - claim_source_ids - cited_ids):
        warnings.append(f"source {source_id} is unused")

    if not cited_ids:
        errors.append("brief contains no inline source citations")

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)

    if errors:
        return 1
    print(
        f"OK: {len(sources)} sources, {len(claims)} claims, {len(cited_ids)} cited sources"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
