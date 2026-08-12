#!/usr/bin/env python3
"""Build the lightweight occupation explorer dataset from the Tableau package."""

from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_WORKBOOK = PROJECT_ROOT.parent / "figures" / "AI_OR_I(2).twbx"
OUTPUT_FILE = PROJECT_ROOT / "public" / "data" / "occupation-profiles.json"
CSV_MEMBER = "Data/programming/analysis_dataset.csv"


def as_float(row: dict[str, str], field: str) -> float | None:
    value = row.get(field, "")
    if value in ("", None):
        return None
    return float(value)


def rounded(value: float | None) -> float | None:
    return None if value is None else round(value, 6)


def main() -> None:
    with zipfile.ZipFile(SOURCE_WORKBOOK) as package:
        with package.open(CSV_MEMBER) as raw:
            reader = csv.DictReader(io.TextIOWrapper(raw, encoding="utf-8-sig", newline=""))
            rows = list(reader)

    by_occupation: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_occupation[row["soc_code"]].append(row)

    occupations = []
    for soc_code, occupation_rows in by_occupation.items():
        first = occupation_rows[0]
        valid_tasks = [
            row for row in occupation_rows if row.get("valid_q2_observation", "").upper() == "TRUE"
        ]
        if not valid_tasks or as_float(first, "occupation_ai_role_balance") is None:
            continue

        tasks = []
        for row in sorted(
            valid_tasks,
            key=lambda item: as_float(item, "task_percentage_job") or 0,
            reverse=True,
        )[:12]:
            tasks.append(
                {
                    "name": row["task_name"],
                    "type": row["task_type"],
                    "cluster": row["task_cluster"],
                    "exposure": rounded(as_float(row, "task_percentage_job")),
                    "automation": rounded(as_float(row, "task_automation_share")),
                    "augmentation": rounded(as_float(row, "task_augmentation_share")),
                    "balance": rounded(as_float(row, "task_ai_role_balance")),
                }
            )

        occupations.append(
            {
                "id": soc_code,
                "name": first["job_name"],
                "family": first["job_family"],
                "exposure": rounded(as_float(first, "occupation_ai_exposure_pct")),
                "automation": rounded(as_float(first, "occupation_automation_orientation")),
                "augmentation": rounded(as_float(first, "occupation_augmentation_orientation")),
                "balance": rounded(as_float(first, "occupation_ai_role_balance")),
                "coverage": rounded(as_float(first, "occupation_classification_coverage")),
                "validTaskCount": int(float(first["occupation_valid_q2_task_count"])),
                "jobZone": int(float(first["job_zone"])) if first.get("job_zone") else None,
                "tasks": tasks,
            }
        )

    occupations.sort(key=lambda item: (-(item["exposure"] or 0), item["name"]))
    payload = {
        "meta": {
            "source": SOURCE_WORKBOOK.name,
            "rowCount": len(rows),
            "occupationCount": len(occupations),
            "definition": "One source row represents one occupation-task pair.",
        },
        "occupations": occupations,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"Wrote {len(occupations)} occupations to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
