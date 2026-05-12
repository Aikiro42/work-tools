from pathlib import Path
from os import listdir
import fitz
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


def rotate_pdf(path: str, angle: int = 90):
    """Rotate PDF in-place."""
    reader = PdfReader(path)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(angle)
        writer.add_page(page)

    with open(path, "wb") as f:
        writer.write(f)


def flatten_pdf(input_path: str) -> str:
    """
    Flatten a PDF by rasterizing each page.
    Saves alongside original as *_flattened.pdf
    Returns output path.
    """
    input_path = Path(input_path)
    output_path = input_path.with_stem(input_path.stem + "_flattened")

    src = fitz.open(input_path)
    out = fitz.open()

    for page in src:
        # Rasterize page (~144 DPI)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        # Create blank page with same dimensions
        new_page = out.new_page(
            width=page.rect.width,
            height=page.rect.height
        )

        # Insert rasterized image
        new_page.insert_image(
            page.rect,
            stream=pix.tobytes("jpg",jpg_quality=100)
        )

    out.save(output_path)
    src.close()
    out.close()

    print(f"Flattened: {output_path}")
    return str(output_path)


def merge(folder: str, file_name: str = ""):
    """
    Flatten all PDFs in folder, then merge flattened copies.
    """
    if file_name == "":
        file_name = folder

    folder_path = Path(folder)

    # Only original PDFs, skip already-flattened files
    pdfs = sorted(
        p for p in folder_path.iterdir()
        if p.suffix.lower() == ".pdf"
        and not p.stem.endswith("_flattened")
    )

    merger = PdfMerger()

    for pdf in pdfs:
        flattened = flatten_pdf(pdf)
        merger.append(flattened)

    output = f"{file_name}.pdf"
    with open(output, "wb") as f:
        merger.write(f)

    merger.close()
    print(f"\nMerged output: {output}")


if __name__ == "__main__":

    for folder, rotate, filename in [
        ("pef", [], "PEF.Alvarado.1s2026"),
        # ("TO.Alvarado.EnriqueLuis.04.01-30.26", [], None),
        # ("TO.Attachment.04.28-30.26", [], "TO.Attachment.04.28-30.26"),
    ]:
        if filename is None:
            filename = folder

        # Rotate specified files first
        for rot in rotate:
            rotate_pdf(f"{folder}/{rot}")

        # Flatten + merge
        merge(folder, filename)