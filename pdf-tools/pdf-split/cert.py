import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(pdfpath: str, outpath: str):
    # Create output folder if it doesn't exist
    os.makedirs(outpath, exist_ok=True)
    retpaths = []

    # Load the PDF
    reader = PdfReader(pdfpath)
    num_pages = len(reader.pages)

    # Split each page into its own PDF
    for i in range(num_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])

        # Output filename with zero-padding
        outfile = os.path.join(outpath, f"page_{i+1:03d}.pdf")
        
        with open(outfile, "wb") as f:
            writer.write(f)

        # retpaths += [outfile]
    print(f"Split complete! Wrote {num_pages} pages to: {outpath}")
    return retpaths

def camelcase(s: str) -> str:
    words = s.split()
    if not words:
        return ""
    
    # First word stays as-is
    first = words[0]
    
    # Capitalize first letter of remaining words, keep rest as-is
    rest = "".join(word[0].upper() + word[1:] if word else "" for word in words[1:])
    
    return first + rest

def what_rename(pdfpath: str, findstring: str, namestring: str) -> str:
    reader = PdfReader(pdfpath)
    # Iterate through all pages
    for page in reader.pages:
        text = page.extract_text() or ""
        if findstring in text:
            if "team" in namestring.lower():
              return f"PSCX-RPC-{namestring}"
            else:
              return f"PSCX-RPC-{camelcase("Team" + namestring)}"
               
    return pdfpath


def rename_pdf(pdfpath: str, newname: str):
    # Ensure the original file exists
    if not os.path.isfile(pdfpath):
        raise FileNotFoundError(f"File not found: {pdfpath}")

    # Get the directory of the original PDF
    folder = os.path.dirname(pdfpath)

    # Build the new full path with .pdf extension
    newpath = os.path.join(folder, f"{newname}.pdf")

    # Rename the file
    os.rename(pdfpath, newpath)

    return newpath  # Optional: return new path


if __name__ == "__main__":
  
  for pdf_path, tgt_path, rename_list in [
      ("CertificateMerged.Cyber.CyberSHEcurity.03.25.26.pdf", "certs/", [])
  ]:
    print("[INFO] Splitting PDF...")
    pages = split_pdf(pdf_path, tgt_path)
    
    if len(rename_list) <= 0:
      print("       No renames necessary.")
      continue
    print("       Renaming...")


    