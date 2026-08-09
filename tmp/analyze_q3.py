import csv
import math
from collections import defaultdict

import numpy as np
from scipy import stats


def f(row, key):
    value = row[key].strip()
    return float(value) if value else math.nan


def fmt(value, digits=3):
    return "NA" if not math.isfinite(value) else f"{value:.{digits}f}"


def summary(values):
    a = np.asarray([v for v in values if math.isfinite(v)], dtype=float)
    if not len(a):
        return (0,) + (math.nan,) * 6
    return (
        len(a),
        float(np.mean(a)),
        float(np.median(a)),
        float(np.quantile(a, 0.25)),
        float(np.quantile(a, 0.75)),
        float(np.min(a)),
        float(np.max(a)),
    )


def print_group_table(rows, group_key, fields):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[group_key]].append(row)
    for group in sorted(grouped, key=lambda x: int(x) if x.isdigit() else x):
        subset = grouped[group]
        bits = [f"{group_key}={group}", f"n={len(subset)}"]
        for field in fields:
            n, mean, median, q1, q3, lo, hi = summary(f(r, field) for r in subset)
            bits.append(
                f"{field}: valid={n} mean={fmt(mean)} median={fmt(median)} "
                f"IQR=[{fmt(q1)},{fmt(q3)}]"
            )
        print(" | ".join(bits))


def spearman(rows, x_key, y_key):
    pairs = [(f(r, x_key), f(r, y_key)) for r in rows]
    pairs = [(x, y) for x, y in pairs if math.isfinite(x) and math.isfinite(y)]
    x, y = map(np.asarray, zip(*pairs))
    result = stats.spearmanr(x, y)
    return len(x), float(result.statistic), float(result.pvalue)


def standardized_ols(rows, outcome, predictors, transform_y=None):
    data = []
    for row in rows:
        y = f(row, outcome)
        x = [f(row, key) for key in predictors]
        if math.isfinite(y) and all(math.isfinite(v) for v in x):
            data.append((y, *x))
    arr = np.asarray(data, dtype=float)
    y = arr[:, 0]
    if transform_y:
        y = transform_y(y)
    y = (y - y.mean()) / y.std(ddof=0)
    xraw = arr[:, 1:]
    xstd = (xraw - xraw.mean(axis=0)) / xraw.std(axis=0, ddof=0)
    X = np.column_stack([np.ones(len(y)), xstd])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ beta
    df = len(y) - X.shape[1]
    sigma2 = resid @ resid / df
    covariance = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(covariance))
    tvals = beta / se
    pvals = 2 * stats.t.sf(np.abs(tvals), df)
    r2 = 1 - (resid @ resid) / np.sum((y - y.mean()) ** 2)
    return len(y), beta, se, pvals, float(r2)


with open("analysis_dataset.csv", newline="", encoding="utf-8-sig") as handle:
    all_rows = list(csv.DictReader(handle))

occupations = [row for row in all_rows if row["occupation_row_flag"] == "1"]
valid_role = [row for row in occupations if math.isfinite(f(row, "occupation_ai_role_balance"))]

print("OCCUPATION COUNTS")
print("all", len(occupations), "valid role", len(valid_role), "missing role", len(occupations) - len(valid_role))
print("zone counts", {z: sum(r["job_zone"] == z for r in occupations) for z in "12345"})
print("valid role zone counts", {z: sum(r["job_zone"] == z for r in valid_role) for z in "12345"})

print("\nEXPOSURE AND ROLE BY JOB ZONE")
print_group_table(
    occupations,
    "job_zone",
    [
        "median_salary",
        "occupation_ai_exposure_pct",
        "occupation_classification_coverage",
        "occupation_automation_orientation",
        "occupation_augmentation_orientation",
        "occupation_ai_role_balance",
    ],
)

print("\nROLE CLASSIFICATION BY JOB ZONE")
for zone in "12345":
    subset = [r for r in valid_role if r["job_zone"] == zone]
    worker = sum(f(r, "occupation_ai_role_balance") < 0 for r in subset)
    copilot = sum(f(r, "occupation_ai_role_balance") > 0 for r in subset)
    exact = len(subset) - worker - copilot
    strong_worker = sum(f(r, "occupation_ai_role_balance") < -0.1 for r in subset)
    balanced = sum(abs(f(r, "occupation_ai_role_balance")) <= 0.1 for r in subset)
    strong_copilot = sum(f(r, "occupation_ai_role_balance") > 0.1 for r in subset)
    print(
        zone,
        "n", len(subset),
        "worker<0", worker, fmt(worker / len(subset), 3) if subset else "NA",
        "copilot>0", copilot, fmt(copilot / len(subset), 3) if subset else "NA",
        "exact", exact,
        "strong_worker", strong_worker,
        "balanced", balanced,
        "strong_copilot", strong_copilot,
    )

print("\nINTERACTION MODES BY JOB ZONE (valid roles)")
print_group_table(
    valid_role,
    "job_zone",
    [
        "occupation_feedback_loop_share",
        "occupation_directive_share",
        "occupation_task_iteration_share",
        "occupation_validation_share",
        "occupation_learning_share",
    ],
)

print("\nEXPOSURE SHARE BY ZONE")
total_exposure = sum(f(r, "occupation_ai_exposure_pct") for r in occupations)
for zone in "12345":
    zone_total = sum(f(r, "occupation_ai_exposure_pct") for r in occupations if r["job_zone"] == zone)
    print(zone, "sum", fmt(zone_total), "share", fmt(zone_total / total_exposure, 4))

print("\nEXPOSURE-WEIGHTED ROLE BY ZONE")
for zone in "12345":
    subset = [r for r in occupations if r["job_zone"] == zone]
    automation = sum(f(r, "occupation_automation_exposure_pct") for r in subset)
    augmentation = sum(f(r, "occupation_augmentation_exposure_pct") for r in subset)
    classified = automation + augmentation
    worker_exposure = sum(
        f(r, "occupation_classified_exposure_pct")
        for r in subset
        if math.isfinite(f(r, "occupation_ai_role_balance")) and f(r, "occupation_ai_role_balance") < 0
    )
    copilot_exposure = sum(
        f(r, "occupation_classified_exposure_pct")
        for r in subset
        if math.isfinite(f(r, "occupation_ai_role_balance")) and f(r, "occupation_ai_role_balance") > 0
    )
    exact_exposure = classified - worker_exposure - copilot_exposure
    balance = (augmentation - automation) / classified if classified else math.nan
    print(
        zone,
        "classified_exposure", fmt(classified),
        "automation_share", fmt(automation / classified),
        "augmentation_share", fmt(augmentation / classified),
        "balance", fmt(balance),
        "worker_oriented_exposure_share", fmt(worker_exposure / classified),
        "copilot_oriented_exposure_share", fmt(copilot_exposure / classified),
        "exact_exposure_share", fmt(exact_exposure / classified),
    )

print("\nEXPOSURE-WEIGHTED INTERACTION MODES BY ZONE")
mode_exposure_fields = [
    "occupation_feedback_loop_exposure_pct",
    "occupation_directive_exposure_pct",
    "occupation_task_iteration_exposure_pct",
    "occupation_validation_exposure_pct",
    "occupation_learning_exposure_pct",
]
for zone in "12345":
    subset = [r for r in occupations if r["job_zone"] == zone]
    mode_totals = [sum(f(r, key) for r in subset) for key in mode_exposure_fields]
    denominator = sum(mode_totals)
    print(
        zone,
        " ".join(
            f"{key.replace('occupation_', '').replace('_exposure_pct', '')}={fmt(value / denominator)}"
            for key, value in zip(mode_exposure_fields, mode_totals)
        ),
    )

print("\nOVERALL ROLE BY OCCUPATION COUNT AND EXPOSURE")
worker_rows = [r for r in valid_role if f(r, "occupation_ai_role_balance") < 0]
copilot_rows = [r for r in valid_role if f(r, "occupation_ai_role_balance") > 0]
exact_rows = [r for r in valid_role if f(r, "occupation_ai_role_balance") == 0]
classified_total = sum(f(r, "occupation_classified_exposure_pct") for r in valid_role)
for label, subset in [("worker", worker_rows), ("copilot", copilot_rows), ("exact", exact_rows)]:
    exposure = sum(f(r, "occupation_classified_exposure_pct") for r in subset)
    print(label, "occupations", len(subset), "count_share", fmt(len(subset) / len(valid_role)), "exposure_share", fmt(exposure / classified_total))

print("\nJOINT JOB ZONE X SALARY QUARTILE")
quartiles = ["Q1 Lower", "Q2 Lower-middle", "Q3 Upper-middle", "Q4 Higher"]
for zone in "12345":
    for quartile in quartiles:
        subset = [r for r in occupations if r["job_zone"] == zone and r["salary_quartile"] == quartile]
        role_subset = [r for r in subset if math.isfinite(f(r, "occupation_ai_role_balance"))]
        exp = summary(f(r, "occupation_ai_exposure_pct") for r in subset)
        bal = summary(f(r, "occupation_ai_role_balance") for r in role_subset)
        print(
            f"zone={zone} quartile={quartile} n={len(subset)} role_n={len(role_subset)} "
            f"exposure_mean={fmt(exp[1])} exposure_median={fmt(exp[2])} "
            f"balance_mean={fmt(bal[1])} balance_median={fmt(bal[2])}"
        )

print("\nJOINT JOB ZONE X SALARY QUARTILE - EXPOSURE-WEIGHTED ROLE")
for zone in "12345":
    for quartile in quartiles:
        subset = [r for r in occupations if r["job_zone"] == zone and r["salary_quartile"] == quartile]
        auto = sum(f(r, "occupation_automation_exposure_pct") for r in subset)
        aug = sum(f(r, "occupation_augmentation_exposure_pct") for r in subset)
        classified = auto + aug
        balance = (aug - auto) / classified if classified else math.nan
        print(
            f"zone={zone} quartile={quartile} n={len(subset)} "
            f"classified_exposure={fmt(classified)} automation_share={fmt(auto / classified) if classified else 'NA'} "
            f"augmentation_share={fmt(aug / classified) if classified else 'NA'} balance={fmt(balance)}"
        )

print("\nSALARY QUARTILE SUMMARY")
print_group_table(
    occupations,
    "salary_quartile",
    ["median_salary", "occupation_ai_exposure_pct", "occupation_ai_role_balance"],
)

print("\nSPEARMAN CORRELATIONS")
for x, y in [
    ("job_zone", "median_salary"),
    ("job_zone", "occupation_ai_exposure_pct"),
    ("median_salary", "occupation_ai_exposure_pct"),
    ("job_zone", "occupation_ai_role_balance"),
    ("median_salary", "occupation_ai_role_balance"),
    ("median_salary", "occupation_automation_orientation"),
]:
    n, rho, p = spearman(occupations, x, y)
    print(x, "vs", y, "n", n, "rho", fmt(rho), "p", f"{p:.3g}")

print("\nWITHIN-ZONE SALARY CORRELATIONS")
for zone in "12345":
    subset = [r for r in occupations if r["job_zone"] == zone]
    for outcome in ["occupation_ai_exposure_pct", "occupation_ai_role_balance"]:
        n, rho, p = spearman(subset, "median_salary", outcome)
        print("zone", zone, "salary vs", outcome, "n", n, "rho", fmt(rho), "p", f"{p:.3g}")

print("\nKRUSKAL-WALLIS BY ZONE")
for outcome in ["occupation_ai_exposure_pct", "occupation_ai_role_balance"]:
    groups = []
    for zone in "12345":
        values = [f(r, outcome) for r in occupations if r["job_zone"] == zone and math.isfinite(f(r, outcome))]
        groups.append(values)
    result = stats.kruskal(*groups)
    print(outcome, "H", fmt(float(result.statistic)), "p", f"{result.pvalue:.3g}")

print("\nSTANDARDIZED ADDITIVE OLS: zone + salary")
for outcome, transform in [
    ("occupation_ai_exposure_pct", np.log1p),
    ("occupation_ai_role_balance", None),
]:
    n, beta, se, pvals, r2 = standardized_ols(
        occupations, outcome, ["job_zone", "median_salary"], transform_y=transform
    )
    print(
        outcome, "n", n, "beta_zone", fmt(float(beta[1])), "p_zone", f"{pvals[1]:.3g}",
        "beta_salary", fmt(float(beta[2])), "p_salary", f"{pvals[2]:.3g}", "R2", fmt(r2)
    )

print("\nSALARY SENSITIVITY: EXCLUDING 3 HOURLY-RATE ROWS (<1000)")
annual_salary_rows = [r for r in occupations if f(r, "median_salary") >= 1000]
for outcome, transform in [
    ("occupation_ai_exposure_pct", np.log1p),
    ("occupation_ai_role_balance", None),
]:
    n, beta, se, pvals, r2 = standardized_ols(
        annual_salary_rows, outcome, ["job_zone", "median_salary"], transform_y=transform
    )
    print(
        outcome, "n", n, "beta_zone", fmt(float(beta[1])), "p_zone", f"{pvals[1]:.3g}",
        "beta_salary", fmt(float(beta[2])), "p_salary", f"{pvals[2]:.3g}", "R2", fmt(r2)
    )

print("\nTOP/BOTTOM OCCUPATIONS BY ROLE BALANCE (min exposure >= 0.05 pct)")
eligible = [r for r in valid_role if f(r, "occupation_ai_exposure_pct") >= 0.05]
for label, subset in [
    ("worker", sorted(eligible, key=lambda r: f(r, "occupation_ai_role_balance"))[:12]),
    ("copilot", sorted(eligible, key=lambda r: f(r, "occupation_ai_role_balance"), reverse=True)[:12]),
]:
    print(label.upper())
    for r in subset:
        print(
            r["job_name"], "zone", r["job_zone"], "salary", r["median_salary"],
            "quartile", r["salary_quartile"], "exposure", fmt(f(r, "occupation_ai_exposure_pct")),
            "balance", fmt(f(r, "occupation_ai_role_balance")),
            "coverage", fmt(f(r, "occupation_classification_coverage")),
        )

print("\nTOP OCCUPATIONS BY EXPOSURE")
for r in sorted(occupations, key=lambda r: f(r, "occupation_ai_exposure_pct"), reverse=True)[:20]:
    print(
        r["job_name"], "zone", r["job_zone"], "salary", r["median_salary"],
        "quartile", r["salary_quartile"], "exposure", fmt(f(r, "occupation_ai_exposure_pct")),
        "balance", fmt(f(r, "occupation_ai_role_balance")),
        "coverage", fmt(f(r, "occupation_classification_coverage")),
    )
