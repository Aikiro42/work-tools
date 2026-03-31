from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from os import getcwd, listdir

def merge(folder:str, fileName:str=""):
  # directives: []
  merger = PdfMerger()

  if fileName == "":
    fileName = folder
  files = sorted(listdir(f"./{folder}"))
  for pdf in files:
    merger.append(f"./{folder}/{pdf}")
  
  with open(f"./{fileName}.pdf", "wb") as output_file:
    merger.write(output_file)
  
  merger.close()

def rotate_pdf(path: str, angle: int = 90, output: str | None = None):
    reader = PdfReader(path)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(angle)  # positive = clockwise
        writer.add_page(page)

    if output is None:
        output = path  # overwrite original

    with open(output, "wb") as f:
        writer.write(f)

if __name__ == "__main__":

  for folder, rotate, filename in [
    # ('dtr', ['DTRAS.Alvarado.EnriqueLuis.03.04.26.pdf'])
    ('dtr', [], "DTR.Alvarado.EnriqueLuis.03.01-15.26")
  ]:
    for rot in rotate:
       rotate_pdf(f"{folder}/{rot}")
    merge(folder, filename)