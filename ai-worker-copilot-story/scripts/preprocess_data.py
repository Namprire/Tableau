from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import median


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent
DATA = ROOT / "analysis_dataset.csv"
OUT = PROJECT / "src" / "lib" / "data"


def number(row: dict[str, str], key: str) -> float | None:
    value = row.get(key, "").strip()
    if not value:
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def rounded(value: float | None, digits: int = 6) -> float | None:
    return round(value, digits) if value is not None else None


def role_totals(rows: list[dict[str, str]]) -> tuple[float, float, float]:
    automation = sum(number(row, "occupation_automation_exposure_pct") or 0 for row in rows)
    augmentation = sum(number(row, "occupation_augmentation_exposure_pct") or 0 for row in rows)
    return automation, augmentation, automation + augmentation


def write_json(name: str, value: object) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / name).open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, separators=(",", ":"))


with DATA.open(newline="", encoding="utf-8-sig") as handle:
    rows = list(csv.DictReader(handle))

occupation_rows = [row for row in rows if row["occupation_row_flag"] == "1"]
rows_by_job: dict[str, list[dict[str, str]]] = defaultdict(list)
for row in rows:
    rows_by_job[row["job_name"]].append(row)

total_exposure = sum(number(row, "occupation_ai_exposure_pct") or 0 for row in occupation_rows)
total_classified = sum(number(row, "occupation_classified_exposure_pct") or 0 for row in occupation_rows)

zone_output = []
zone_one_median = median(
    number(row, "occupation_ai_exposure_pct") or 0
    for row in occupation_rows
    if row["job_zone"] == "1"
)
for zone in range(1, 6):
    subset = [row for row in occupation_rows if row["job_zone"] == str(zone)]
    valid = [row for row in subset if number(row, "occupation_ai_role_balance") is not None]
    exposures = [number(row, "occupation_ai_exposure_pct") or 0 for row in subset]
    automation, augmentation, classified = role_totals(subset)
    zone_output.append(
        {
            "zone": zone,
            "count": len(subset),
            "validCount": len(valid),
            "exposureShare": rounded(sum(exposures) / total_exposure),
            "medianExposure": rounded(median(exposures)),
            "medianMultiple": rounded(median(exposures) / zone_one_median, 3),
            "workerShare": rounded(automation / classified if classified else None),
            "copilotShare": rounded(augmentation / classified if classified else None),
        }
    )

family_groups: dict[str, list[dict[str, str]]] = defaultdict(list)
for row in occupation_rows:
    family_groups[row["job_family"]].append(row)

family_output = []
for family, subset in family_groups.items():
    exposure = sum(number(row, "occupation_ai_exposure_pct") or 0 for row in subset)
    automation, augmentation, classified = role_totals(subset)
    family_output.append(
        {
            "family": family,
            "count": len(subset),
            "exposureShare": rounded(exposure / total_exposure),
            "workerShare": rounded(automation / classified if classified else None),
            "copilotShare": rounded(augmentation / classified if classified else None),
        }
    )
family_output.sort(key=lambda item: item["exposureShare"] or 0, reverse=True)

quartile_order = ["Q1 Lower", "Q2 Lower-middle", "Q3 Upper-middle", "Q4 Higher"]
salary_output = []
for quartile in quartile_order:
    subset = [row for row in occupation_rows if row["salary_quartile"] == quartile]
    automation, augmentation, classified = role_totals(subset)
    salary_output.append(
        {
            "quartile": quartile,
            "count": len(subset),
            "exposureShare": rounded(classified / total_classified),
            "workerShare": rounded(automation / classified if classified else None),
            "copilotShare": rounded(augmentation / classified if classified else None),
        }
    )

q4_rows = [row for row in occupation_rows if row["salary_quartile"] == "Q4 Higher"]
q4_automation, q4_augmentation, q4_total = role_totals(q4_rows)
q4_zone_output = []
for zone in range(1, 6):
    subset = [row for row in q4_rows if row["job_zone"] == str(zone)]
    automation, augmentation, classified = role_totals(subset)
    q4_zone_output.append(
        {
            "zone": zone,
            "count": len(subset),
            "exposureShare": rounded(classified / q4_total if q4_total else None),
            "workerShare": rounded(automation / classified if classified else None),
            "copilotShare": rounded(augmentation / classified if classified else None),
        }
    )

occupation_output = []
for row in occupation_rows:
    task_rows = [task for task in rows_by_job[row["job_name"]] if task["valid_q2_observation"] == "TRUE"]
    worker_tasks = [task for task in task_rows if (number(task, "task_ai_role_balance") or 0) < -0.1]
    copilot_tasks = [task for task in task_rows if (number(task, "task_ai_role_balance") or 0) > 0.1]
    worker_tasks.sort(key=lambda task: number(task, "q2_classified_exposure_pct") or 0, reverse=True)
    copilot_tasks.sort(key=lambda task: number(task, "q2_classified_exposure_pct") or 0, reverse=True)

    def task_summary(task: dict[str, str] | None) -> dict[str, object] | None:
        if task is None:
            return None
        return {
            "name": task["task_name"],
            "balance": rounded(number(task, "task_ai_role_balance"), 3),
            "classifiedExposure": rounded(number(task, "q2_classified_exposure_pct"), 4),
        }

    occupation_output.append(
        {
            "name": row["job_name"],
            "family": row["job_family"],
            "zone": int(row["job_zone"]),
            "salary": rounded(number(row, "median_salary"), 2),
            "salaryQuartile": row["salary_quartile"],
            "exposure": rounded(number(row, "occupation_ai_exposure_pct"), 4),
            "roleBalance": rounded(number(row, "occupation_ai_role_balance"), 4),
            "workerShare": rounded(number(row, "occupation_automation_orientation"), 4),
            "copilotShare": rounded(number(row, "occupation_augmentation_orientation"), 4),
            "coverage": rounded(number(row, "occupation_classification_coverage"), 4),
            "workerTask": task_summary(worker_tasks[0] if worker_tasks else None),
            "copilotTask": task_summary(copilot_tasks[0] if copilot_tasks else None),
        }
    )
occupation_output.sort(key=lambda item: item["name"])

valid_occupations = [row for row in occupation_rows if number(row, "occupation_ai_role_balance") is not None]
meta = {
    "taskRows": len(rows),
    "occupations": len(occupation_rows),
    "classifiedOccupations": len(valid_occupations),
    "zones45ExposureShare": rounded(sum(item["exposureShare"] or 0 for item in zone_output if item["zone"] >= 4)),
    "q4ExposureShare": next(item["exposureShare"] for item in salary_output if item["quartile"] == "Q4 Higher"),
    "q4CopilotShare": next(item["copilotShare"] for item in salary_output if item["quartile"] == "Q4 Higher"),
}

write_json("meta.json", meta)
write_json("job-zones.json", zone_output)
write_json("job-families.json", family_output)
write_json("salary-context.json", {"quartiles": salary_output, "q4Zones": q4_zone_output})
write_json("occupations.json", occupation_output)

print(
    f"Wrote {len(occupation_output)} occupations, {len(family_output)} families, "
    f"{len(zone_output)} job zones and {len(salary_output)} salary groups."
)
