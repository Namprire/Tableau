from __future__ import annotations

import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "analysis_dataset.csv"
OUTPUT_DIR = Path(__file__).resolve().parent

BG = "#F7F5F0"
INK = "#162335"
MUTED = "#667080"
GRID = "#D7D5CE"
EXPOSURE = "#355C7D"
EXPOSURE_LIGHT = "#A7B8C8"
AUTOMATION = "#D4674C"
AUGMENTATION = "#2B7A78"
NEUTRAL = "#ECE8DF"
WHITE = "#FFFFFF"
GOLD = "#C89B3C"

mpl.rcParams.update(
    {
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.titlesize": 20,
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


def number(row: dict[str, str], key: str) -> float:
    value = row[key].strip()
    return float(value) if value else math.nan


def load_occupations() -> list[dict[str, str]]:
    with DATA_PATH.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row["occupation_row_flag"] == "1"]


def add_title(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.suptitle(title, x=0.065, y=0.975, ha="left", va="top", fontsize=22, fontweight=600, color=INK)
    fig.text(0.065, 0.925, subtitle, ha="left", va="top", fontsize=11, color=MUTED)


def clean_axes(ax: plt.Axes, *, grid_axis: str | None = None) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid_axis:
        ax.grid(axis=grid_axis, zorder=0)
    ax.tick_params(length=0)


def save_figure(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUTPUT_DIR / f"{stem}.png", dpi=220, bbox_inches="tight", pad_inches=0.25)
    fig.savefig(OUTPUT_DIR / f"{stem}.svg", bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)


def figure_1_exposure(rows: list[dict[str, str]]) -> None:
    zones = [1, 2, 3, 4, 5]
    by_zone = {
        zone: np.asarray(
            [number(row, "occupation_ai_exposure_pct") for row in rows if int(row["job_zone"]) == zone],
            dtype=float,
        )
        for zone in zones
    }
    total = sum(number(row, "occupation_ai_exposure_pct") for row in rows)
    shares = {zone: by_zone[zone].sum() / total for zone in zones}

    fig, ax = plt.subplots(figsize=(11.8, 7.2))
    fig.subplots_adjust(left=0.16, right=0.89, top=0.82, bottom=0.17)
    add_title(
        fig,
        "AI exposure rises with job complexity—and concentrates in Zone 4",
        "Each dot is one occupation. Boxes show the interquartile range and median; the x-axis is logarithmic.",
    )

    rng = np.random.default_rng(42)
    for zone in zones:
        values = by_zone[zone]
        y = np.full(len(values), zone, dtype=float) + rng.uniform(-0.19, 0.19, len(values))
        ax.scatter(
            values,
            y,
            s=22,
            color=GOLD if zone == 4 else EXPOSURE_LIGHT,
            alpha=0.62 if zone == 4 else 0.48,
            edgecolors="none",
            zorder=2,
        )
        q1, median, q3 = np.quantile(values, [0.25, 0.5, 0.75])
        ax.plot([q1, q3], [zone, zone], color=INK, lw=7, solid_capstyle="round", zorder=4)
        ax.scatter([median], [zone], s=78, color=WHITE, edgecolor=INK, linewidth=1.8, zorder=5)
        ax.text(
            q3 * 1.20,
            zone,
            f"median {median:.3f}%",
            va="center",
            ha="left",
            fontsize=10,
            color=INK,
            fontweight=500,
            zorder=6,
        )

    ax.set_xscale("log")
    ax.set_xlim(0.00045, 12)
    ax.set_ylim(0.45, 5.55)
    ax.set_yticks(zones, [f"Job Zone {zone}" for zone in zones])
    ax.set_xticks([0.001, 0.01, 0.1, 1, 10], ["0.001%", "0.01%", "0.1%", "1%", "10%"])
    ax.set_xlabel("Occupation AI exposure (% of observed AI conversations)", labelpad=14)
    clean_axes(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)
    ax.invert_yaxis()

    ax.text(
        1.02,
        0.98,
        "SHARE OF SUMMED\nEXPOSURE",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        color=MUTED,
        fontweight=500,
    )
    for zone in zones:
        y_axes = 1 - ((zone - 0.45) / 5.10)
        ax.text(
            1.02,
            y_axes,
            f"{shares[zone]:.1%}",
            transform=ax.transAxes,
            ha="left",
            va="center",
            fontsize=13,
            color=GOLD if zone == 4 else INK,
            fontweight=600 if zone == 4 else 500,
        )

    fig.text(
        0.065,
        0.055,
        "Reading: typical exposure increases through Zone 5, while a few highly exposed computing occupations make Zone 4 dominant overall.",
        fontsize=10,
        color=MUTED,
    )
    save_figure(fig, "figure-1-exposure-by-job-zone")


def aggregate_role(rows: list[dict[str, str]], subset_filter=None) -> tuple[float, float, float]:
    subset = rows if subset_filter is None else [row for row in rows if subset_filter(row)]
    auto = sum(number(row, "occupation_automation_exposure_pct") for row in subset)
    aug = sum(number(row, "occupation_augmentation_exposure_pct") for row in subset)
    return auto, aug, auto + aug


def figure_2_role(rows: list[dict[str, str]]) -> None:
    zones = [1, 2, 3, 4, 5]
    role = {}
    for zone in zones:
        auto, aug, total = aggregate_role(rows, lambda row, z=zone: int(row["job_zone"]) == z)
        role[zone] = (auto / total, aug / total)

    fig, ax = plt.subplots(figsize=(11.8, 7.1))
    fig.subplots_adjust(left=0.17, right=0.94, top=0.79, bottom=0.15)
    add_title(
        fig,
        "AI acts more like a copilot in every Job Zone",
        "Exposure-weighted shares of valid interactions; distance from the center shows the strength of the orientation.",
    )

    y = np.arange(len(zones))
    automation = np.asarray([role[z][0] for z in zones])
    augmentation = np.asarray([role[z][1] for z in zones])
    ax.barh(y, -automation, color=AUTOMATION, height=0.62, zorder=3)
    ax.barh(y, augmentation, color=AUGMENTATION, height=0.62, zorder=3)
    ax.axvline(0, color=INK, lw=1.2, zorder=4)

    for index, zone in enumerate(zones):
        auto, aug = role[zone]
        ax.text(-auto + 0.025, index, f"{auto:.1%}", va="center", ha="left", color=WHITE, fontweight=600)
        ax.text(aug - 0.025, index, f"{aug:.1%}", va="center", ha="right", color=WHITE, fontweight=600)
        if zone == 4:
            ax.annotate(
                "Near-even boundary",
                xy=(0.535, index),
                xytext=(0.78, index - 0.48),
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.0),
                fontsize=10,
                color=MUTED,
                ha="right",
            )
        if zone == 5:
            ax.annotate(
                "Strongest copilot pattern",
                xy=(0.683, index),
                xytext=(0.78, index - 0.55),
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.0),
                fontsize=10,
                color=MUTED,
                ha="right",
            )

    ax.set_xlim(-0.82, 0.82)
    ax.set_yticks(y, [f"Job Zone {z}" for z in zones])
    ax.set_xticks([-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75], ["75%", "50%", "25%", "0", "25%", "50%", "75%"])
    ax.set_xlabel("Share of classified AI interaction", labelpad=13)
    clean_axes(ax, grid_axis="x")
    ax.spines["left"].set_visible(False)
    ax.invert_yaxis()
    legend = fig.legend(
        handles=[
            Patch(facecolor=AUTOMATION, label="AI as worker: directive + feedback loop"),
            Patch(facecolor=AUGMENTATION, label="AI as copilot: iteration + validation + learning"),
        ],
        loc="upper left",
        bbox_to_anchor=(0.06, 0.865),
        ncol=2,
        frameon=False,
        fontsize=10,
    )
    for text in legend.get_texts():
        text.set_color(MUTED)

    fig.text(
        0.065,
        0.035,
        "Zone 5 is 68.3% copilot-oriented. Zone 4 is only 53.5% copilot-oriented because feedback-loop and directive use are unusually prominent.",
        fontsize=10,
        color=MUTED,
    )
    save_figure(fig, "figure-2-worker-vs-copilot-by-job-zone")


def figure_3_joint_matrix(rows: list[dict[str, str]]) -> None:
    quartiles = ["Q1 Lower", "Q2 Lower-middle", "Q3 Upper-middle", "Q4 Higher"]
    short_quartiles = ["Q1\nLower", "Q2\nLower-middle", "Q3\nUpper-middle", "Q4\nHigher"]
    zones = [1, 2, 3, 4, 5]
    grouped: dict[tuple[int, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["job_zone"]), row["salary_quartile"])].append(row)

    cells = []
    for zone in zones:
        for qi, quartile in enumerate(quartiles):
            subset = grouped[(zone, quartile)]
            auto = sum(number(row, "occupation_automation_exposure_pct") for row in subset)
            aug = sum(number(row, "occupation_augmentation_exposure_pct") for row in subset)
            total = auto + aug
            cells.append(
                {
                    "zone": zone,
                    "qi": qi,
                    "n": len(subset),
                    "exposure": total,
                    "aug_share": aug / total if total else math.nan,
                }
            )

    fig, ax = plt.subplots(figsize=(11.8, 7.8))
    fig.subplots_adjust(left=0.14, right=0.92, top=0.81, bottom=0.24)
    add_title(
        fig,
        "Salary changes the pattern—but Job Zone defines the context",
        "Circle color shows augmentation share; circle area shows classified exposure. Labels show augmentation share and occupation count.",
    )

    cmap = LinearSegmentedColormap.from_list("role", [AUTOMATION, NEUTRAL, AUGMENTATION])
    norm = Normalize(vmin=0.30, vmax=0.72)
    exposures = np.asarray([cell["exposure"] for cell in cells])
    max_exposure = exposures.max()

    for cell in cells:
        x = cell["qi"]
        y = cell["zone"]
        if cell["n"] == 0:
            ax.text(x, y, "—", ha="center", va="center", color=GRID, fontsize=20)
            continue
        size = 380 + 2250 * math.sqrt(cell["exposure"] / max_exposure)
        sparse = cell["n"] < 10
        ax.scatter(
            [x],
            [y],
            s=size,
            c=[cmap(norm(cell["aug_share"]))],
            edgecolor=INK if not sparse else MUTED,
            linewidth=1.3,
            alpha=0.98 if not sparse else 0.52,
            zorder=3,
        )
        label_color = INK if 0.43 <= cell["aug_share"] <= 0.60 else WHITE
        ax.text(
            x,
            y + 0.035,
            f"{cell['aug_share']:.0%}",
            ha="center",
            va="center",
            fontsize=11,
            fontweight=600,
            color=label_color,
            zorder=4,
        )
        ax.text(
            x,
            y - 0.20,
            f"n={cell['n']}",
            ha="center",
            va="center",
            fontsize=8.5,
            color=label_color,
            zorder=4,
        )

    ax.set_xlim(-0.65, 3.65)
    ax.set_ylim(0.4, 5.6)
    ax.set_xticks(range(4), short_quartiles)
    ax.set_yticks(zones, [f"Job Zone {z}" for z in zones])
    ax.set_xlabel("Salary quartile", labelpad=13)
    ax.set_ylabel("")
    ax.tick_params(axis="x", pad=8)
    ax.grid(axis="both", color=GRID, linewidth=0.8, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.annotate(
        "Largest exposure cell\n50.8% copilot / 49.2% worker",
        xy=(3, 4),
        xytext=(2.35, 3.43),
        arrowprops=dict(arrowstyle="-", color=INK, lw=1.1),
        ha="center",
        va="center",
        fontsize=10,
        color=INK,
        bbox=dict(boxstyle="round,pad=0.35", facecolor=BG, edgecolor=GRID),
        zorder=6,
    )
    ax.annotate(
        "High-salary Zone 5\nremains strongly copilot-oriented",
        xy=(3, 5),
        xytext=(2.15, 5.48),
        arrowprops=dict(arrowstyle="-", color=INK, lw=1.1),
        ha="center",
        va="center",
        fontsize=10,
        color=INK,
        bbox=dict(boxstyle="round,pad=0.35", facecolor=BG, edgecolor=GRID),
        zorder=6,
    )

    cax = fig.add_axes([0.20, 0.105, 0.36, 0.024])
    mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, orientation="horizontal")
    cax.set_xticks([0.30, 0.50, 0.70], ["Worker", "Balanced", "Copilot"])
    cax.tick_params(length=0, labelsize=9, colors=MUTED)
    cax.set_title("Interaction role", fontsize=9, color=MUTED, pad=7)

    size_ax = fig.add_axes([0.64, 0.075, 0.28, 0.09])
    size_ax.set_xlim(0, 1)
    size_ax.set_ylim(0, 1)
    size_ax.axis("off")
    for x, exposure in [(0.18, 1), (0.48, 10), (0.80, 35)]:
        size = 380 + 2250 * math.sqrt(exposure / max_exposure)
        size_ax.scatter([x], [0.48], s=size * 0.25, facecolor="none", edgecolor=MUTED, linewidth=1)
        size_ax.text(x, 0.05, f"{exposure:g}%", ha="center", va="bottom", fontsize=8.5, color=MUTED)
    size_ax.text(0.50, 0.97, "Classified exposure", ha="center", va="top", fontsize=9, color=MUTED)

    fig.text(
        0.065,
        0.035,
        "Faded circles have fewer than 10 occupations and should not drive the conclusion.",
        fontsize=9.5,
        color=MUTED,
    )
    save_figure(fig, "figure-3-job-zone-salary-matrix")


def figure_4_occupations(rows: list[dict[str, str]]) -> None:
    valid = [row for row in rows if math.isfinite(number(row, "occupation_ai_role_balance"))]
    x = np.asarray([number(row, "occupation_ai_role_balance") for row in valid])
    y = np.asarray([number(row, "occupation_ai_exposure_pct") for row in valid])
    colors = [AUTOMATION if value < 0 else AUGMENTATION for value in x]

    fig, ax = plt.subplots(figsize=(11.8, 7.8))
    fig.subplots_adjust(left=0.13, right=0.95, top=0.81, bottom=0.16)
    add_title(
        fig,
        "The worker–copilot boundary is occupation-specific",
        "High-exposure software roles lean worker; research, instruction, and analysis occupations lean copilot.",
    )

    ax.scatter(x, y, s=30, c=colors, alpha=0.32, edgecolors="none", zorder=2)
    ax.axvline(0, color=INK, lw=1.2, zorder=1)
    ax.set_yscale("log")
    ax.set_xlim(-1.02, 1.02)
    ax.set_ylim(0.00055, 12)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1], ["−1.0", "−0.5", "Balanced", "+0.5", "+1.0"])
    ax.set_yticks([0.001, 0.01, 0.1, 1, 10], ["0.001%", "0.01%", "0.1%", "1%", "10%"])
    ax.set_xlabel("AI role balance  ← worker-oriented     copilot-oriented →", labelpad=13)
    ax.set_ylabel("Occupation AI exposure", labelpad=12)
    clean_axes(ax, grid_axis="y")

    labels = {
        "Software Developers, Systems Software": (18, 24, "Systems software developers"),
        "Computer Programmers": (-110, -20, "Computer programmers"),
        "Network and Computer Systems Administrators": (-120, -30, "Network & systems admins"),
        "Interpreters and Translators": (-120, -5, "Interpreters & translators"),
        "Web Developers": (18, 10, "Web developers"),
        "Tutors": (18, 14, "Tutors"),
        "Instructional Designers and Technologists": (20, -30, "Instructional designers"),
        "Computer and Information Research Scientists": (20, 12, "Computer research scientists"),
        "Statisticians": (18, -28, "Statisticians"),
    }
    row_by_name = {row["job_name"]: row for row in valid}
    for name, (dx, dy, display) in labels.items():
        row = row_by_name[name]
        balance = number(row, "occupation_ai_role_balance")
        exposure = number(row, "occupation_ai_exposure_pct")
        color = AUTOMATION if balance < 0 else AUGMENTATION
        ax.scatter([balance], [exposure], s=72, color=color, edgecolor=WHITE, linewidth=1.3, zorder=5)
        ax.annotate(
            display,
            xy=(balance, exposure),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=9.3,
            color=INK,
            ha="left" if dx > 0 else "right",
            va="center",
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8),
            zorder=6,
        )

    ax.text(-0.98, 8.2, "AI AS WORKER", ha="left", va="top", fontsize=10, color=AUTOMATION, fontweight=600)
    ax.text(0.98, 8.2, "AI AS COPILOT", ha="right", va="top", fontsize=10, color=AUGMENTATION, fontweight=600)
    fig.text(
        0.065,
        0.045,
        "Role balance = augmentation share − automation share. Values near zero are genuinely mixed rather than strongly classified.",
        fontsize=9.5,
        color=MUTED,
    )
    save_figure(fig, "figure-4-occupation-worker-copilot-landscape")


def make_contact_sheet() -> None:
    paths = [
        OUTPUT_DIR / "figure-1-exposure-by-job-zone.png",
        OUTPUT_DIR / "figure-2-worker-vs-copilot-by-job-zone.png",
        OUTPUT_DIR / "figure-3-job-zone-salary-matrix.png",
        OUTPUT_DIR / "figure-4-occupation-worker-copilot-landscape.png",
    ]
    images = [Image.open(path).convert("RGB") for path in paths]
    tile_width = 1100
    resized = []
    for image in images:
        height = round(tile_width * image.height / image.width)
        resized.append(image.resize((tile_width, height), Image.Resampling.LANCZOS))
    row_height = max(image.height for image in resized)
    margin = 28
    sheet = Image.new("RGB", (tile_width * 2 + margin * 3, row_height * 2 + margin * 3), BG)
    positions = [
        (margin, margin),
        (tile_width + margin * 2, margin),
        (margin, row_height + margin * 2),
        (tile_width + margin * 2, row_height + margin * 2),
    ]
    for image, position in zip(resized, positions):
        sheet.paste(image, position)
    sheet.save(OUTPUT_DIR / "question-3-figure-set-preview.png", quality=95)


def main() -> None:
    rows = load_occupations()
    figure_1_exposure(rows)
    figure_2_role(rows)
    figure_3_joint_matrix(rows)
    figure_4_occupations(rows)
    make_contact_sheet()
    print(f"Created figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
