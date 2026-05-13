import os, sys, re
from PyPDF2 import PdfReader, PdfWriter


BOOL_ALIASES = {
  "y": True,
  "yes": True,
  "true": True,
  "n": False,
  "no": False,
  "false": False,
}

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
  pattern = r"(([1-9][0-9]*)-([1-9][0-9]*))|([1-9][0-9]*)"
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



def split(pdf_path="", pages="", merge=""):
  def help():
    return
  
  try:
    _pages = helper_parsePages(pages)
    _merge = BOOL_ALIASES.get(merge.lower(), merge == "--merge" or merge == "-m")


    # Load the PDF
    reader = PdfReader(path)
    num_pages = len(reader.pages)

    # Create output folder if it doesn't exist
    filename = os.path.basename(path)
    outpath = os.path.splitext(filename)[0]  
    os.makedirs(outpath, exist_ok=True)
    
    # Determine pages to process
    pages_to_use = _pages if len(_pages) > 0 else list(range(1, num_pages + 1))

    if _merge:
        # Merge selected pages into one PDF
        writer = PdfWriter()
        for i in pages_to_use:
            writer.add_page(reader.pages[i-1])  # 1-based to 0-based index

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

        npage = len(pages_to_use)
        print(f"Split complete! Wrote {npage} page{'s' if npage > 1 else ''} to: {outpath}")



  except Exception:
    help()

def convert(path="", scale="", paper_size="a4"):
  def help():
    return
  
  try:
    _scale = float(scale)
  except Exception:
    help()

def merge(path="", flatten="", help: bool = False):
  ...


FUNCTIONS = {
  "split": split,
  "convert": convert,
  "merge": merge
}

func_args = {
  "split": "<pages> (--merge | -m)",
  "convert": "<scale> "
}

def mainHelp():
  print(f"Usage:")
  print(f"  python pdf.py <function> <pdf/folder path> <function args>")
  print(f"Functions:")
  for f in FUNCTIONS.keys():
    print(f"  {f}")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    mainHelp()
  else:
    try:
      fn = sys.argv[1]
      path = sys.argv[2]
      args = sys.argv[3:]
      FUNCTIONS[fn](path, *args)
    except Exception:
      mainHelp()