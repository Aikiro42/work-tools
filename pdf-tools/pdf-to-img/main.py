import fitz
import sys
from pathlib import Path

# Check for input argument
if len(sys.argv) != 2:
    print("Usage: python flatten_pdf.py <path-to-pdf>")
    sys.exit(1)

input_path = Path(sys.argv[1])

if not input_path.exists():
    print(f"Error: File not found: {input_path}")
    sys.exit(1)

output_path = input_path.with_stem(input_path.stem + "_flattened")

src = fitz.open(input_path)
out = fitz.open()

for page in src:
    # Rasterize page (2x scale ≈ 144 DPI)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

    # Create new blank page with same dimensions
    new_page = out.new_page(
        width=page.rect.width,
        height=page.rect.height
    )

    # Insert rasterized image to fill the whole page
    new_page.insert_image(
        page.rect,
        stream=pix.tobytes("png")
    )

# Save flattened PDF
out.save(output_path)

src.close()
out.close()

print(f"Flattened PDF saved to: {output_path}")