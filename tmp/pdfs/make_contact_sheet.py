import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

input_dir = Path(sys.argv[1])
output_path = Path(sys.argv[2])
paths = sorted(input_dir.glob("page-*.png"))
thumb_w = 520
label_h = 36
cols = 3
font = ImageFont.load_default(size=20)

thumbs = []
for path in paths:
    image = Image.open(path).convert("RGB")
    height = round(thumb_w * image.height / image.width)
    thumbs.append((path.name, image.resize((thumb_w, height))))

cell_h = max(image.height for _, image in thumbs) + label_h
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * thumb_w, rows * cell_h), "white")
draw = ImageDraw.Draw(sheet)
for index, (name, image) in enumerate(thumbs):
    x = (index % cols) * thumb_w
    y = (index // cols) * cell_h
    draw.text((x + 10, y + 8), name, fill="black", font=font)
    sheet.paste(image, (x, y + label_h))

sheet.save(output_path)
