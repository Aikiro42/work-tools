# https://stackoverflow.com/questions/66672150/how-to-generate-qr-code-with-python-and-when-scanned-make-it-open-a-url-defined

import qrcode, sys

link = ""
if len(sys.argv) > 1:
  link = sys.argv[1]
else:
  link = input("Enter link: ")


name = "qr_out"
if len(sys.argv) > 2:
  name = sys.argv[2]

qr = qrcode.QRCode(
  version=2,  # automatic size
  error_correction=qrcode.constants.ERROR_CORRECT_L,
  box_size=4,
  border=0,
)

qr.add_data(link)
qr.make(fit=True)

img = qr.make_image(
  back_color="transparent"  # ← transparent background
).convert("RGBA")

img.save(f"{name}.png")
print(f"File saved to {name}.png")