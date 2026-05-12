import os, sys
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(pdfpath: str, outpath: str, pages: list | None = None, join: bool=False, isCert: bool=False):
    # Create output folder if it doesn't exist
    os.makedirs(outpath, exist_ok=True)
    retpaths = []

    # Load the PDF
    reader = PdfReader(pdfpath)
    num_pages = len(reader.pages)

    # Determine pages to process
    pages_to_use = pages if pages is not None else list(range(1, num_pages + 1))

    if join:
        # Merge selected pages into one PDF
        writer = PdfWriter()
        for i in pages_to_use:
            writer.add_page(reader.pages[i-1])  # 1-based to 0-based index

        outfile = os.path.join(outpath, "merged.pdf")
        with open(outfile, "wb") as f:
            writer.write(f)

        retpaths.append(outfile)
        print(f"Merged {len(pages_to_use)} page{'s' if len(pages_to_use) > 1 else ''} into: {outfile}")
    else:
        # Split each page into its own PDF
        for i in range(num_pages):
            if (i+1) in pages_to_use:
                writer = PdfWriter()
                writer.add_page(reader.pages[i])

                filename = f"page_{i+1:03d}.pdf"
                if isCert: filename = f"{i+1}.pdf"
                outfile = os.path.join(outpath, filename)
                with open(outfile, "wb") as f:
                    writer.write(f)

                retpaths.append(outfile)

        npage = len(pages_to_use)
        print(f"Split complete! Wrote {npage} page{'s' if npage > 1 else ''} to: {outpath}")

    return retpaths

def rename_pdf(pdfpath: str, newname: str):
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

All = None

if __name__ == "__main__":
  for pdfname, pages, join, renamelist, isCert in [
      # ("CertGen.AIAwareness.04.22.26", None, False, [], True)
      ("AL.QPO.04.2026", [2], True, [], False)
      # ("AL.QPO.04.01-15.26", [2], True, [], False)
      # ("SALN.Alvarado.EnriqueLuis.11.16.25", [1, 2], True, False),
      # ("SALN.Alvarado.EnriqueLuis.12.31.25", [1, 2], True, False),
      # ("SALN.Alvarado.EnriqueLuis.01.05.26", [1, 2], True, False)
  ]:
    split_pdf(f"{pdfname}.pdf", f"./split/{pdfname}", pages, join, isCert)
    if len(renamelist) <= 0:
      continue
    for i in range(len(renamelist)):
      pdfpath = f"split/{pdfname}/page_{i+1:03d}.pdf"
      if isCert:
        pdfpath = f"split/{pdfname}/{i}.pdf"
      rename_pdf(pdfpath, renamelist[i])