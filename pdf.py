import os, sys, re, io
from typing import Callable
from math import floor, sqrt

import fitz
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from PIL import Image, ImageFile

# SECTION: DEFS

BOOL_ALIASES = {
  "y": True,
  "yes": True,
  "true": True,
  "n": False,
  "no": False,
  "false": False,
}

INCHES = "in"
MILLIMETERS = "mm"
CENTIMETERS = "cm"

PAGE_SIZES = {
  "a4": (210, 297, MILLIMETERS),
  "short": (8.5, 11, INCHES),
  "folio": (8.5, 13, INCHES)
}

PAGE_SIZE_PX = {}

def size_to_px(dim: tuple, unit:str=INCHES, dpi: int = 300) -> tuple:  
  w, h = dim
  
  if unit != INCHES:  # convert to inches
    
    # if centimeters, convert to millimeters
    if unit == CENTIMETERS:
      w *= 10
      h *= 10
    
    # 25.4mm in inch
    w /= 25.4
    h /= 25.4

  return (floor(w*sqrt(dpi)), floor(h*sqrt(dpi)))

for k, v in PAGE_SIZES.items():
  PAGE_SIZE_PX[k] = size_to_px((v[0], v[1]), v[2])

# SECTION: HELPERS

def helper_parseCmd():
  argv = sys.argv[1:]  # skip script name

  vars = {}
  args = []
  flags = []

  for arg in argv:
    if "=" in arg:
      var, val = arg.split("=", 1)
      var = var.removeprefix("--").removeprefix("-")
      vars[var] = val
    elif arg.startswith("-"):
      flags.append(arg)
    else:
      args.append(arg)

  return args, flags, vars

# scales size to paper size ratio
def helper_ratioSize(from_size: tuple[int, int], to_size: tuple[int, int]) -> tuple[int, int]:

    target_ratio = to_size[0]/to_size[1]    # alpha = tgt_w / tgt_h
    
    scaled_height = floor(max(from_size[1], to_size[1]))
    scaled_width = floor(target_ratio * scaled_height)

    return (scaled_width, scaled_height)

def helper_renamePdf(pdfpath: str, newname: str):
    # Ensure the original file exists
    if not os.path.isfile(pdfpath):
      raise FileNotFoundError(f"File not found: {pdfpath}")
    
    # Get the directory of the original PDF
    folder = os.path.dirname(pdfpath) 
    
    # Build the new full path with .pdf extension
    newpath = os.path.join(folder, f"{newname}.pdf")
    if os.path.isfile(newpath):
      print("WARNING: Renamed file exists!") 
    
    # Rename the file
    os.rename(pdfpath, newpath)

    return newpath  # Optional: return new path


def helper_parsePages(pages: str):
  pattern = r"[1-9][0-9]*(?:-[1-9][0-9]*)?"
  matches = re.findall(pattern, pages)
  result = []
  for match in matches:
    if "-" in match:
      start, end = map(int, match.split("-"))
      for i in range(start, end+1):
        if i not in result: result.append(i)
    else:
      i = int(match)
      if i not in result: result.append(i)
  return result


# scales size by s percent
def helper_scaleSize(from_size: tuple[int, int], percent: float) -> tuple[int, int]:
    return (floor(from_size[0] * percent), floor(from_size[1] * percent))

# get best dimensions based on performance needs
def helper_getBestDimensions(
        imageList: list[Image.Image] | list[ImageFile.ImageFile],
        compfunc: Callable[[Image.Image | ImageFile.ImageFile, tuple[int, int]], bool]
    ) ->tuple[int, int]:
    min_dim = None
    for image in imageList:
        if min_dim is None:
            min_dim = image.size
        if compfunc(image, min_dim):
            min_dim = image.size
    if min_dim is None:
        return (-1, -1)
    return min_dim

def helper_getMinDimensions(imageList: list[Image.Image] | list[ImageFile.ImageFile]):
    return helper_getBestDimensions(imageList, lambda image, best: image.size[0] <= best[0] and image.size[1] <= best[1])

def helper_getMaxDimensions(imageList: list[Image.Image] | list[ImageFile.ImageFile]):
    return helper_getBestDimensions(imageList, lambda image, best: image.size[0] >= best[0] and image.size[1] >= best[1])


# SECTION: Functions

def cmd_split(path, flags, vars):

  # vars
  _pages = helper_parsePages(vars.get("pages", ""))
  
  # flags
  _merge = "--merge" in flags or "-m" in flags

  # Load the PDF
  pdf_path = os.path.splitext(path)[0] + ".pdf"
  reader = PdfReader(pdf_path)
  num_pages = len(reader.pages)

  # Create output folder if it doesn't exist
  filename = os.path.basename(path)
  outpath = os.path.splitext(filename)[0]  
  os.makedirs(outpath, exist_ok=True)
  
  # Determine pages to process
  pages_to_use = _pages if len(_pages) > 0 else list(range(1, num_pages + 1))
  split_pages = 0

  if _merge:
    # Merge selected pages into one PDF
    writer = PdfWriter()
    for i in pages_to_use:
      if 1 < i < num_pages:
        writer.add_page(reader.pages[i-1])  # 1-based to 0-based index
        split_pages += 1

    outfile = os.path.join(outpath, "merged.pdf")
    with open(outfile, "wb") as f:
      writer.write(f)

    print(f"Merged {len(pages_to_use)} page{'s' if len(pages_to_use) > 1 else ''} into: {outfile}")
  else:
    # Split each page into its own PDF
    for i in range(num_pages):
      if (i+1) in pages_to_use:
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        filename = f"{i+1:03d}.pdf"
        outfile = os.path.join(outpath, filename)
        with open(outfile, "wb") as f:
          writer.write(f)
        split_pages += 1

    npage = len(pages_to_use)
    if split_pages > 1:
      print(f"Split complete! Wrote {npage} page{'s' if npage > 1 else ''} to: {outpath}")
    else:
      print(f"Split complete but did not make any page.")


def cmd_convert(path, flags, vars):

  # vars
  _scale = float(vars.get("scale", "1"))
  paper_size = vars.get("page", "a4")
  
  # flags
  _performance = "--fast" in flags or "-f" in flags

  if os.path.isfile(path):  # pdf-to-img

    fmt = "jpg"
    # Create output folder if it doesn't exist
    filename = os.path.basename(path)
    outpath = os.path.splitext(filename)[0]      
    os.makedirs(outpath, exist_ok=True)

    doc = fitz.open(path)

    for i, page in enumerate(doc): # type: ignore
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 144 DPI approx

        out_path = os.path.join(outpath, f"page_{i+1}.{fmt}")

        if fmt == "png":
            pix.save(out_path)
        else:
            pix.save(out_path, jpg_quality=95)

    doc.close()

  elif os.path.isdir(path):  # img-to-pdf
    
    # get image paths
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    imagePaths= sorted([
      os.path.join(path, filename)
      for filename in os.listdir(path)
      if os.path.isfile(os.path.join(path, filename))
      and os.path.splitext(filename)[1].lower() in image_exts
    ])

    # load images from folder using the gathered filenames
    images = []
    for imagePath in imagePaths:
      images.append(Image.open(imagePath))

    if _scale != 1:
      min_dim = (helper_getMinDimensions if _performance else helper_getMaxDimensions)(images)
      scaled_dim = helper_scaleSize(min_dim, _scale)
      images = list(map(lambda image: image.resize(scaled_dim), images))

    if paper_size != "":
    # resize images to minimum/maximum dimensions depending on performance mode flag
      min_dim = (helper_getMinDimensions if _performance else helper_getMaxDimensions)(images)
      scaled_dim = helper_ratioSize(min_dim, PAGE_SIZE_PX[paper_size])
      images = list(map(lambda image: image.resize(scaled_dim), images))
    
    # save to /<folder_name>/<folder_name>.pdf
    
    pdf_path = os.path.splitext(path)[0] + ".pdf"
    
    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

  else:
    raise Exception()

def helper_imgToPdf(img_path):
    img = Image.open(img_path).convert("RGB")
    buffer = io.BytesIO()
    img.save(buffer, format="PDF")
    buffer.seek(0)
    return buffer

def cmd_merge(path, flags, vars):
    _flatten = "--flat" in flags or "-f" in flags

    merger = PdfMerger()

    file_exts = {".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

    files = sorted(
        os.path.join(path, f)
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f))
        and os.path.splitext(f)[1].lower() in file_exts
    )
    delFiles = []

    if _flatten:
      for i in range(len(files)):
        files[i] = cmd_flatten(files[i], [], {})
        delFiles.append(files[i])
      
    temp_buffers = []

    for file_path in files:
      ext = os.path.splitext(file_path)[1].lower()

      if ext == ".pdf":
        merger.append(file_path)
      else:
        pdf_buffer = helper_imgToPdf(file_path)
        temp_buffers.append(pdf_buffer)
        merger.append(pdf_buffer)

    pdf_path = os.path.splitext(path)[0] + ".pdf"

    with open(pdf_path, "wb") as output_file:
      merger.write(output_file)

    merger.close()

    for f in delFiles:
      if os.path.isfile(f):
        os.remove(f)


def cmd_flatten(path, flags, vars):

  """
  Flatten a PDF by rasterizing each page.
  Saves alongside original as *_flattened.pdf
  Returns output path.
  """
  input_dir = os.path.dirname(path)
  filename = os.path.basename(path)

  name, ext = os.path.splitext(filename)

  # assume .pdf if no extension provided
  if ext == "":
    ext = ".pdf"
    path = os.path.join(input_dir, filename + ext)

  output_path = os.path.join(input_dir, f"{name}_flattened.pdf")

  src = fitz.open(path)
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
      stream=pix.tobytes("jpg", jpg_quality=100)
    )

  out.save(output_path)
  src.close()
  out.close()

  print(f"Flattened: {output_path}")
  return output_path


# SECTION: DOCS

def doc_split():
  print(
      "Usage:\n"
      "  python pdf.py split <path-to-pdf>\n"
      "    [--pages=<list>]\n\n"
      "`--pages` format:\n"
      "  Comma-separated page numbers and ranges\n"
      "  Examples:\n"
      "    --pages=1,3,5-10,12\n"
      "    --pages=2-3\n"
      "    --pages=3-7,8-12\n"
      "    --pages=6\n"
  )

def doc_convert():
  print(
      "Usage:\n"
      "  python pdf.py convert <path>\n"
      "    [--scale=<number>]\n"
      "    [--page={a4|short|folio}]\n"
      "    [--fast | -f]\n"
  )
def doc_merge(): ...
def doc_flatten(): ...

FUNCTIONS = {
  "split": cmd_split,
  "convert": cmd_convert,
  "merge": cmd_merge,
  "flatten": cmd_flatten
}

DOCS= {
  "split": doc_split,
  "convert": doc_convert,
  "merge": doc_merge,
  "flatten": doc_flatten
}

def mainHelp():
  print(f"Usage:\n")
  print(f"  python pdf.py <function> <pdf/folder path> <function args>\n")
  print(f"Functions:\n")
  for f in FUNCTIONS.keys():
    print(f"  {f}")

if __name__ == "__main__":
  """
  if len(sys.argv) < 2:
    mainHelp()
  else:
    try:
      args, flags, vars = helper_parseCmd()
      fn = args[0]
      try:
        path = args[1]
        args = args[2:]
        # print(fn, path, args, flags, vars)
        FUNCTIONS[fn](path, flags, vars, *args)
      except Exception:
        DOCS.get(fn, mainHelp)()
    except Exception:
      mainHelp()
  """
  if len(sys.argv) < 2:
    mainHelp()
  else:
    args, flags, vars = helper_parseCmd()
    fn = args[0]
    path = args[1]
    args = args[2:]
    # print(fn, path, args, flags, vars)
    FUNCTIONS[fn](path, flags, vars, *args)
      
