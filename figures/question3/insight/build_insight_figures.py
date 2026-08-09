from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = ROOT / "analysis_dataset.csv"
OUTPUT_DIR = Path(__file__).resolve().parent

BG = "#F7F5F0"
INK = "#162335"
MUTED = "#667080"
GRID = "#D7D5CE"
LIGHT = "#C7D1D9"
EXPOSURE = "#355C7D"
AUTOMATION = "#D4674C"
AUGMENTATION = "#2B7A78"
GOLD = "#C89B3C"
WHITE = "#FFFFFF"

mpl.rcParams.update(
    {
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 15,
        "axes.titleweight": 600,
        "axes.labelsize": 11,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "text.color": INK,
        "axes.edgecolor": GRID,
        "axes.linewidth": 0.8,
        "grid.color": GRID,
        "grid.linewidth": 0.7,
        "svg.fonttype": "none",
    }
)


def n(row: dict[str, str], key: str) -> float:
    value = row[key].strip()
    return float(value) if value else math.nan


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row["occupation_row_flag"] == "1"]


def title(fig: plt.Figure, headline: str, subhead: str) -> None:
    fig.suptitle(headline, x=0.055, y=0.975, ha="left", va="top", fontsize=22, fontweight=600, color=INK)
    fig.text(0.055, 0.918, subhead, ha="left", va="top", fontsize=11, color=MUTED)


def clean(ax: plt.Axes, grid_axis: str | None = None) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, zorder=0)


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUTPUT_DIR / f"{stem}.png", dpi=220, bbox_inches="tight", pad_inches=0.25)
    fig.savefig(OUTPUT_DIR / f"{stem}.svg", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def role_totals(subset: list[dict[str, str]]) -> tuple[float, float, float]:
    auto = sum(n(row, "occupation_automation_exposure_pct") for row in subset)
    aug = sum(n(row, "occupation_augmentation_exposure_pct") for row in subset)
    return auto, aug, auto + aug


def exposure_by_zone(rows: list[dict[str, str]]) -> None:
    zones = [5, 4, 3, 2, 1]
    total = sum(n(row, "occupation_ai_exposure_pct") for row in rows)
    zone_rows = {zone: [row for row in rows if int(row["job_zone"]) == zone] for zone in zones}
    shares = {zone: sum(n(row, "occupation_ai_exposure_pct") for row in zone_rows[zone]) / total for zone in zones}
    medians = {zone: float(np.median([n(row, "occupation_ai_exposure_pct") for row in zone_rows[zone]])) for zone in zones}
    baseline = medians[1]
    multiples = {zone: medians[zone] / baseline for zone in zones}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 7.2), gridspec_kw={"width_ratios": [1.15, 0.85]})
    fig.subplots_adjust(left=0.15, right=0.95, top=0.80, bottom=0.15, wspace=0.34)
    title(
        fig,
        "AI exposure is a high-skill story: Zones 4–5 account for 77%",
        "Zone 4 dominates total observed exposure, while the typical Zone 5 occupation is slightly more exposed.",
    )

    y = np.arange(len(zones))
    values = np.asarray([shares[zone] for zone in zones])
    colors = [EXPOSURE if zone in (4, 5) else LIGHT for zone in zones]
    ax1.barh(y, values, color=colors, height=0.58, zorder=3)
    ax1.set_yticks(y, [f"Job Zone {zone}" for zone in zones])
    ax1.set_xlim(0, 0.61)
    ax1.set_xticks([0, 0.2, 0.4, 0.6], ["0%", "20%", "40%", "60%"])
    ax1.set_title("Share of all occupation exposure", loc="left", pad=14)
    ax1.set_xlabel("Share of summed exposure", labelpad=12)
    for yi, zone in enumerate(zones):
        ax1.text(values[yi] + 0.014, yi, f"{values[yi]:.1%}", va="center", ha="left", fontsize=12, fontweight=600, color=INK)
    clean(ax1, "x")

    mult_values = np.asarray([multiples[zone] for zone in zones])
    ax2.hlines(y, 0, mult_values, color=GRID, lw=5, zorder=1)
    ax2.scatter(mult_values, y, s=125, color=[GOLD if zone in (4, 5) else EXPOSURE for zone in zones], zorder=3)
    ax2.set_yticks(y, [f"Job Zone {zone}" for zone in zones])
    ax2.set_xlim(0, 11.7)
    ax2.set_xticks([0, 2, 4, 6, 8, 10], ["0×", "2×", "4×", "6×", "8×", "10×"])
    ax2.set_title("Typical occupation vs. Job Zone 1", loc="left", pad=14)
    ax2.set_xlabel("Median exposure multiple", labelpad=12)
    for yi, zone in enumerate(zones):
        ax2.text(mult_values[yi] + 0.28, yi, f"{mult_values[yi]:.1f}×", va="center", ha="left", fontsize=12, fontweight=600)
    clean(ax2, "x")

    fig.text(
        0.055,
        0.045,
        "Core insight: higher-complexity work is both more typically exposed and responsible for most observed AI use; Zone 4 leads because of computing occupations.",
        fontsize=9.8,
        color=MUTED,
    )
    save(fig, "insight-1-exposure-concentration")


def role_by_family(rows: list[dict[str, str]]) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["job_family"]].append(row)
    total_exposure = sum(n(row, "occupation_ai_exposure_pct") for row in rows)

    selected = [
        "Computer and Mathematical",
        "Education, Training, and Library",
        "Arts, Design, Entertainment, Sports, and Media",
        "Office and Administrative Support",
        "Life, Physical, and Social Science",
        "Business and Financial Operations",
        "Healthcare Practitioners and Technical",
        "Production",
    ]
    labels = {
        "Computer and Mathematical": "Computer & mathematical",
        "Education, Training, and Library": "Education & training",
        "Arts, Design, Entertainment, Sports, and Media": "Arts, media & entertainment",
        "Office and Administrative Support": "Office & administrative",
        "Life, Physical, and Social Science": "Life, physical & social science",
        "Business and Financial Operations": "Business & finance",
        "Healthcare Practitioners and Technical": "Healthcare professionals",
        "Production": "Production",
    }
    metrics = []
    for family in selected:
        subset = grouped[family]
        exposure = sum(n(row, "occupation_ai_exposure_pct") for row in subset)
        auto, aug, classified = role_totals(subset)
        metrics.append(
            {
                "family": family,
                "exposure_share": exposure / total_exposure,
                "auto_share": auto / classified,
                "aug_share": aug / classified,
            }
        )

    fig, ax = plt.subplots(figsize=(12.2, 7.5))
    fig.subplots_adjust(left=0.27, right=0.95, top=0.80, bottom=0.16)
    title(
        fig,
        "The worker side is concentrated in computing; the copilot side is broader",
        "Bar length shows each job family’s share of all AI exposure; color divides that exposure into worker and copilot interaction.",
    )

    y = np.arange(len(metrics))
    total_width = np.asarray([m["exposure_share"] for m in metrics])
    auto_width = np.asarray([m["exposure_share"] * m["auto_share"] for m in metrics])
    aug_width = np.asarray([m["exposure_share"] * m["aug_share"] for m in metrics])
    ax.barh(y, auto_width, color=AUTOMATION, height=0.62, zorder=3)
    ax.barh(y, aug_width, left=auto_width, color=AUGMENTATION, height=0.62, zorder=3)
    ax.set_yticks(y, [labels[m["family"]] for m in metrics])
    ax.set_xlim(0, 0.46)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4], ["0%", "10%", "20%", "30%", "40%"])
    ax.set_xlabel("Share of all occupation AI exposure", labelpad=12)
    ax.invert_yaxis()
    clean(ax, "x")

    for yi, metric in enumerate(metrics):
        total = metric["exposure_share"]
        ax.text(total + 0.010, yi, f"{total:.1%} exposure · {metric['aug_share']:.0%} copilot", va="center", fontsize=10.5, color=INK)
        if yi == 0:
            ax.text(auto_width[yi] / 2, yi, f"{metric['auto_share']:.0%}\nworker", ha="center", va="center", color=WHITE, fontsize=10, fontweight=600)
            ax.text(auto_width[yi] + aug_width[yi] / 2, yi, f"{metric['aug_share']:.0%}\ncopilot", ha="center", va="center", color=WHITE, fontsize=10, fontweight=600)

    legend = fig.legend(
        handles=[Patch(facecolor=AUTOMATION, label="AI as worker"), Patch(facecolor=AUGMENTATION, label="AI as copilot")],
        loc="upper left",
        bbox_to_anchor=(0.055, 0.86),
        frameon=False,
        ncol=2,
    )
    for text in legend.get_texts():
        text.set_color(MUTED)

    fig.text(
        0.055,
        0.045,
        "These eight families represent about 85% of exposure. Production is worker-oriented, but contributes only 2%; healthcare is 74% copilot-oriented.",
        fontsize=9.8,
        color=MUTED,
    )
    save(fig, "insight-2-worker-copilot-job-families")


def salary_context(rows: list[dict[str, str]]) -> None:
    quartiles = ["Q1 Lower", "Q2 Lower-middle", "Q3 Upper-middle", "Q4 Higher"]
    qlabels = ["Q1 Lower", "Q2 Lower-middle", "Q3 Upper-middle", "Q4 Higher"]
    total_classified = sum(n(row, "occupation_classified_exposure_pct") for row in rows)
    quartile_metrics = []
    for quartile in quartiles:
        subset = [row for row in rows if row["salary_quartile"] == quartile]
        auto, aug, classified = role_totals(subset)
        quartile_metrics.append(
            {
                "quartile": quartile,
                "share": classified / total_classified,
                "auto": auto / classified,
                "aug": aug / classified,
            }
        )

    q4_rows = [row for row in rows if row["salary_quartile"] == "Q4 Higher"]
    q4_auto, q4_aug, q4_total = role_totals(q4_rows)
    zone_metrics = []
    for zone in [5, 4]:
        subset = [row for row in q4_rows if int(row["job_zone"]) == zone]
        auto, aug, classified = role_totals(subset)
        zone_metrics.append(
            {
                "zone": zone,
                "n": len(subset),
                "share": classified / q4_total,
                "auto": auto / classified,
                "aug": aug / classified,
            }
        )

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 7.4), gridspec_kw={"width_ratios": [1.02, 0.98]})
    fig.subplots_adjust(left=0.15, right=0.95, top=0.76, bottom=0.17, wspace=0.34)
    title(
        fig,
        "High salary does not automatically mean copilot—Job Zone changes the answer",
        "The highest salary quartile contains almost half of classified exposure, but Zone 4 computing makes it nearly balanced overall.",
    )

    y1 = np.arange(len(quartile_metrics))
    totals1 = np.asarray([m["share"] for m in quartile_metrics])
    auto1 = totals1 * np.asarray([m["auto"] for m in quartile_metrics])
    aug1 = totals1 * np.asarray([m["aug"] for m in quartile_metrics])
    ax1.barh(y1, auto1, color=AUTOMATION, height=0.62, zorder=3)
    ax1.barh(y1, aug1, left=auto1, color=AUGMENTATION, height=0.62, zorder=3)
    ax1.set_yticks(y1, qlabels)
    ax1.set_xlim(0, 0.67)
    ax1.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], ["0%", "10%", "20%", "30%", "40%", "50%", "60%"])
    ax1.set_title("All Job Zones combined", loc="left", pad=15)
    ax1.set_xlabel("Share of classified exposure", labelpad=12)
    ax1.invert_yaxis()
    clean(ax1, "x")
    for yi, metric in enumerate(quartile_metrics):
        ax1.text(metric["share"] + 0.012, yi, f"{metric['share']:.0%} exposure · {metric['aug']:.0%} copilot", va="center", fontsize=10.3)

    y2 = np.arange(len(zone_metrics))
    totals2 = np.asarray([m["share"] for m in zone_metrics])
    auto2 = totals2 * np.asarray([m["auto"] for m in zone_metrics])
    aug2 = totals2 * np.asarray([m["aug"] for m in zone_metrics])
    ax2.barh(y2, auto2, color=AUTOMATION, height=0.62, zorder=3)
    ax2.barh(y2, aug2, left=auto2, color=AUGMENTATION, height=0.62, zorder=3)
    ax2.set_yticks(y2, [f"Job Zone {m['zone']}  (n={m['n']})" for m in zone_metrics])
    ax2.set_xlim(0, 0.88)
    ax2.set_xticks([0, 0.2, 0.4, 0.6, 0.8], ["0%", "20%", "40%", "60%", "80%"])
    ax2.set_title("Inside the highest salary quartile", loc="left", pad=15)
    ax2.set_xlabel("Share of Q4 classified exposure", labelpad=12)
    ax2.invert_yaxis()
    clean(ax2, "x")
    for yi, metric in enumerate(zone_metrics):
        ax2.text(metric["share"] + 0.012, yi, f"{metric['share']:.0%} of Q4 · {metric['aug']:.0%} copilot", va="center", fontsize=10.3)

    legend = fig.legend(
        handles=[Patch(facecolor=AUTOMATION, label="AI as worker"), Patch(facecolor=AUGMENTATION, label="AI as copilot")],
        loc="upper left",
        bbox_to_anchor=(0.055, 0.885),
        frameon=False,
        ncol=2,
    )
    for text in legend.get_texts():
        text.set_color(MUTED)

    fig.text(
        0.055,
        0.045,
        "Core insight: Q4 is not the most copilot-oriented salary group. About 80% of its classified exposure comes from nearly balanced Zone 4 occupations; Zones 1–3 contribute less than 1% combined.",
        fontsize=9.8,
        color=MUTED,
    )
    save(fig, "insight-3-salary-needs-job-zone-context")


def preview() -> None:
    paths = [
        OUTPUT_DIR / "insight-1-exposure-concentration.png",
        OUTPUT_DIR / "insight-2-worker-copilot-job-families.png",
        OUTPUT_DIR / "insight-3-salary-needs-job-zone-context.png",
    ]
    images = [Image.open(path).convert("RGB") for path in paths]
    width = 1400
    resized = []
    for image in images:
        height = round(width * image.height / image.width)
        resized.append(image.resize((width, height), Image.Resampling.LANCZOS))
    margin = 30
    total_height = sum(image.height for image in resized) + margin * (len(resized) + 1)
    sheet = Image.new("RGB", (width + margin * 2, total_height), BG)
    y = margin
    for image in resized:
        sheet.paste(image, (margin, y))
        y += image.height + margin
    sheet.save(OUTPUT_DIR / "question3-insight-figures-preview.png", quality=95)


def main() -> None:
    rows = load_rows()
    exposure_by_zone(rows)
    role_by_family(rows)
    salary_context(rows)
    preview()
    print(f"Created insight figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
