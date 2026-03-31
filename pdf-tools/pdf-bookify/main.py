from PyPDF2 import PdfMerger, PdfReader, PdfWriter # pyright: ignore[reportMissingImports]
from os import getcwd, listdir

def calcPageSort(N: int, index: int = 0):
  """
  Returns a re-sorting of a PDF's pages.
  
  This assumes that the PDF has N pages and that the PDF page-sorting algorithm adds two more blank pages,
  which serve as the cover pages, to the PDF.

  This sorting allows the PDF to be printed with two pages per sheet into a booklet, by printing the first half in the front
  and then the second half into the back.

  `index` specified the index base of the the returned tuple of indices.
  """

  if N % 2 == 1:
    print("Odd pages")
    N += 1

  front = [1, N]
  back = [N+1, N+2]

  assert N % 2 == 0

  print(f"Pages: {((N+2)//4)}")

  i = 1
  while i < ((N+2)//4):
    even = 2*i     # start at 2
    odd = 2*i - 1  # start at 1
    back += [N-odd, even]
    front += [odd+2, N-even]
    i += 1

  join = front + back
  return tuple(i+index-1 for i in join)


def reorganizePages(pdfPath: str, savePath: str):
  # 1. Get the pdf file specified in pdfPath
  # 2. Let N be the number of pages in the pdf. If N == 0, throw an error.
  # 3. If N is odd, add 1 blank page of the smallest sized page in the doc.
  #    This ensures that the resulting PDF has at least 2 pages.
  # 4. Get the page order O specified by calcPageSort(N)
  # 5. Add 2 blank pages of the smallest sized page in the doc.
  #    This ensures that the resulting PDF has at least 4 pages.
  # 4. Reorganize the pages according to the order O.
  # 5. Save the reorganized pdf into savePath.

  # 1. Read PDF
  reader = PdfReader(pdfPath)
  writer = PdfWriter()

  # 2. Get N
  if len(reader.pages) == 0:
    raise ValueError("PDF has no pages.")

  pages = list(reader.pages)
  N = len(pages)

  # Find smallest page size
  min_width = float('inf')
  min_height = float('inf')

  for p in pages:
    w = float(p.mediabox.width)
    h = float(p.mediabox.height)
    min_width = min(min_width, w)
    min_height = min(min_height, h)

  # Helper to create blank page
  def make_blank():
    temp = PdfWriter()
    temp.add_blank_page(width=min_width, height=min_height)
    return temp.pages[0]

  # 3. If N is odd, add 1 blank page
  if N % 2 == 1:
    pages.append(make_blank())
    N += 1

  # 4. Get order BEFORE adding final 2 blanks
  order = calcPageSort(N)

  # 5. Add 2 blank pages (covers)
  pages.append(make_blank())
  pages.append(make_blank())

  total_pages = len(pages)

  # 6. Reorder
  for idx in order:
    if 0 <= idx < total_pages:
      writer.add_page(pages[idx])
    else:
      raise IndexError(f"Page index {idx} out of bounds for total pages {total_pages}")

  # 7. Save
  with open(savePath, "wb") as f:
    writer.write(f)

  # Thanks chat!


if __name__ == "__main__":
  for tgtPath, dstPath in [
    ("Cyberhygiene - Outline.pdf", "cyberhygiene-booklet.pdf")
  ]:
    reorganizePages(tgtPath, dstPath)