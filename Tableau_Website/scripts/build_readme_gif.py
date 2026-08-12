"""Build the animated README tour from the captured website screenshots."""

from pathlib import Path

from PIL import Image


MEDIA_DIR = Path(__file__).resolve().parents[1] / "docs" / "media"
FRAME_NAMES = [
    "hero",
    "quiz",
    "evidence",
    "workday",
    "handoff",
    "handoff-result",
    "comparison",
    "explorer",
]


def main() -> None:
    frames = []
    for name in FRAME_NAMES:
        with Image.open(MEDIA_DIR / f"{name}.png") as image:
            resized = image.convert("RGB").resize((960, 667), Image.Resampling.LANCZOS)
            frames.append(resized.quantize(colors=192, method=Image.Quantize.MEDIANCUT))

    frames[0].save(
        MEDIA_DIR / "website-tour.gif",
        save_all=True,
        append_images=frames[1:],
        duration=1400,
        loop=0,
        optimize=True,
        disposal=2,
    )


if __name__ == "__main__":
    main()
