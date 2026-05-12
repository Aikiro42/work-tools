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
    ('dtr2', [], 'DTRMerged.Alvarado.EnriqueLuis.04.01-30.26')
    # ('TO.Alvarado.EnriqueLuis.04.01-30.26', [], None)
    # ('TO.Attachment.04.28-30.26',[], "TO.Attachment.04.28-30.26")
  ]:
    if filename is None:
       filename = folder
    for rot in rotate:
       rotate_pdf(f"{folder}/{rot}")
    merge(folder, filename)