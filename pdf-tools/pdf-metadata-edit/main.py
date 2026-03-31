
from PyPDF2 import PdfFileReader, PdfFileWriter

if __name__ == "__main__":
  reader = PdfFileReader("source.pdf")
  writer = PdfFileWriter()

  writer.appendPagesFromReader(reader)
  metadata = reader.getDocumentInfo()
  writer.addMetadata(metadata)

  # Write your custom metadata here:
  writer.addMetadata({"/Some": "Example"})

  with open("result.pdf", "wb") as fp:
      writer.write(fp)