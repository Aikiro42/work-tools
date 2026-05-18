from PyPDF2 import PdfReader
from pathlib import Path
import pdfplumber, fitz
def pdf_tables_to_html(pdf_path):
    html_output = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                html_output += "<table border='1'>\n"
                for row in table:
                    html_output += "<tr>"
                    for cell in row:
                        html_output += f"<td>{cell or ''}</td>"
                    html_output += "</tr>\n"
                html_output += "</table>\n\n"

    return html_output


debug = True

def get_sex(pdfPath):


  doc = fitz.open("pnpki/Abluyen, Westley Batton.pdf")
  for page_num, page in enumerate(doc):
    images = page.get_images(full=True)
    for _, img in enumerate(images):
      xref = img[0]
      base_image = doc.extract_image(xref)
      image_bytes = base_image["image"]
      rects = page.get_image_rects(xref)

      comp = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x0f\x00\x00\x00\x0f\x08\x02\x00\x00\x00\xb4\xb4\x02\x1d\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95+\x0e\x1b\x00\x00\x00\xcbIDATx\x9c\xa5\x91\xcb\t\x840\x18\x84\xadA\x1b\xb0\x81\x80\xd5$X\x84\xbazQ\x0b\xd0:%\x07\x83\n\xa6\x03\xd7\x0f\\d7\x04E6\x87a\x98L\xe6\x7f$x?9\xc1_\xeem\xdb\xac\xb5\xf3<\x83\xf0+\xb7\xd6\xba\xeb\xba\xb6m\xab\xaa\x02\xe1(~\xf70\x0cY\x96\x19cN\x05\x9e\xe79\xba\xeb\xa6h\xdf\xf7\\/\xcb\xa2\x94\x8a\xa2\x08\x84\xa3P\xe1l\xe9\xe3^\xed\xda4\r$M\xd38\x8e\x85\x10 \x0fP\xea\xbaf\x86\x1f\xf74MeYBH\xc5\x9a$\t\x08Ga\x06\x8a\xf8\xb3\xc9s\xb2\xd1\xdd\xec\xa3\xefq\x1c\x89\x91R\x86a\x08\xc2Q\xd0\xdd\xbe\x8f\xf5\x15\xaf\xc2\xd9\t\xca\xf7\x12=\xfb\xa64\xbd\x82W\xfb>[b\x06\xfe\x12\xbc\xf9\xcb\xdb\xf3\xcc\xbd\x03\x7f\r@\xe8\xf2\x80\x82\xbb\x00\x00\x00\x00IEND\xaeB`\x82'

      for i in range(len(rects)):
        rect = rects[i]
        if debug: print({
          "page": page_num,
          "x0": rect.x0,
          "y0": rect.y0,
          "width": rect.width,
          "height": rect.height,
          "selected": image_bytes == comp
        })

        if image_bytes == comp:  # selected
          if 255 < rect.y0 < 257: # sex
            if 179 < rect.x0 < 181:  # male
              print("Male")
            else: # female
              print("Female")

        with open(f"{i}_{rect.width}x{rect.height}_{rect.y0}-{rect.x0}.png", "wb") as f:
          f.write(image_bytes)
    break
  return False

def parse(dir_path: str):
    
  path = Path(dir_path)
  files = [f.name for f in path.iterdir() if f.is_file()]
  parsed = {}

  for file in files:

    html = pdf_tables_to_html(f"{dir_path}/{file}").split("\n")
    
    province = html[21] \
      .replace("<tr>", "") \
      .replace("Province", "") \
      .replace("Zip Code", "") \
      .replace("</td>", "") \
      .replace("</tr>", "") \
      .split("<td>")[2]
    # print(f"[{province}]", end=" ")

    if province != "Quirino":
      continue

    name = html[5] \
      .replace("</td>","") \
      .replace("<tr>","") \
      .replace("</tr>","") \
      .split("<td>")
    del name[0]
    lastName, firstName, ext, MI = name
    # print(f"{lastName}, {firstName} {MI} {ext}")
    
    email = html[22] \
      .replace("<tr>", "") \
      .replace("<td>", "") \
      .replace("</td>", "") \
      .replace("Email Address", "") \
      .replace("Mobile No.", " ") \
      .replace("</tr>", "") \
      .split(" ")[0]
    # print(email)
    
    # TODO: SEX
    sex = "Female" if get_sex(file) else "Male"

    agency = html[12] \
      .replace("<tr>", "") \
      .replace("<td>", "") \
      .replace("</td>", "") \
      .replace("</tr>", "") \
      .replace("Organization/Agency:", "") \
      .replace(",", " - ")
    # print(agency)

    municipality = html[20] \
      .replace("<tr>", "") \
      .replace("</td>", "") \
      .replace("Barangay:", "") \
      .replace("Municipality / City", " ") \
      .replace("</tr>", "") \
      .split("<td>")[7]
    # print(municipality)

    sep = "\t"

    print(f"{lastName} {firstName} {MI}{f' {ext}' if len(ext) > 0 else ''}{sep}{email}{sep}{sex}{sep}{agency}{sep}{municipality}")

    



# Example usage

# name of applicant
# email address
# sex
# agency
# city/municipality

# action
# date of action
# remarks
# application date

# parsed = parse("pnpki")

print("pnpki/Alvarez, Jhoeanna-Marie Sorilla.pdf")
print(get_sex("pnpki/Alvarez, Jhoeanna-Marie Sorilla.pdf"))
# print("-"*64)
# print("pnpki/Opiano, Dennis Samonte.pdf")
# print(get_sex("pnpki/Opiano, Dennis Samonte.pdf"))