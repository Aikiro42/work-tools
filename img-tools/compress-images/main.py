from PIL import Image
from io import BytesIO
import os

def listDir(relativePath: str) -> list[str]:
    """
    Return a list of file and directory names in the given relative path.

    Args:
        relativePath (str): Path relative to the current working directory

    Returns:
        list[str]: Names of files and directories
    """
    try:
        return os.listdir(relativePath)
    except FileNotFoundError:
        return []
    except NotADirectoryError:
        return []

def compressImage(file, scale=1.0):
    """
    Compress and optionally resize an image.

    Args:
        file: bytes, file-like object, or open file handle
        scale (float): resize factor (e.g. 0.5 = 50%)

    Returns:
        BytesIO: compressed image file-like object
    """

    # Load image
    if isinstance(file, (bytes, bytearray)):
        img = Image.open(BytesIO(file))
    else:
        img = Image.open(file)

    # Resize if needed
    if scale != 1.0:
        new_size = (
            int(img.width * scale),
            int(img.height * scale)
        )
        img = img.resize(new_size, Image.LANCZOS)

    # Prepare output buffer
    output = BytesIO()

    # Preserve format when possible
    format = img.format or "JPEG"

    # Convert unsupported modes
    if format == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Save with compression
    img.save(
        output,
        format=format,
        optimize=True,
        quality=85  # adjust for more/less compression
    )

    output.seek(0)
    return output


if __name__ == "__main__":
    inFolder = "./input"
    outFolder = "./output"
    for img in listDir(inFolder):
        with open(f"{inFolder}/{img}", "rb") as f:
            compressed = compressImage(f, scale=0.5)

        with open(f"{outFolder}/{img}", "wb") as out:
            out.write(compressed.read())
