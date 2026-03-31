# https://stackoverflow.com/questions/66672150/how-to-generate-qr-code-with-python-and-when-scanned-make-it-open-a-url-defined

import qrcode

links = [
  (
    "EvalQR.Cyber.CyberSHEcurity.03.25.26",
    "https://forms.gle/iba18KVpxX3n8acj6"
  )
]

for name, link in links:
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