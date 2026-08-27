# https://stackoverflow.com/questions/66672150/how-to-generate-qr-code-with-python-and-when-scanned-make-it-open-a-url-defined

import qrcode, sys, cv2

cmdflags = [
  "--scan", "-s"
]

flags = []
args = []
for cmdarg in sys.argv[1:]:
  # hardcoded flags
  if cmdarg in cmdflags:
    flags += [cmdarg]
  else:
    args += [cmdarg]

if len(args) > 0:
  link = args[0]
else:
  print("Usage: python qr.py [--scan | -s] <link/path>")
  quit()

if ("--scan" in flags) or ("-s" in flags):
  # scan qr from string path
  image_path = link
  image = cv2.imread(image_path)

  if image is None:
      raise FileNotFoundError(f"Could not read image: {image_path}")

  detector = cv2.QRCodeDetector()
  data, points, _ = detector.detectAndDecode(image)

  if not data:
      raise ValueError("No QR code found in the image.")
  
  print(data)
  
else:
  # generate qr from link
  name = "qr_out"
  if len(sys.argv) > 2:
    name = sys.argv[2]

  qr = qrcode.QRCode(
    version=2,  # automatic size
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=4,
    border=4,
  )

  qr.add_data(link)
  qr.make(fit=True)

  img = qr.make_image(
    back_color="white"  # ← transparent background
  ).convert("RGB")

  img.save(f"{name}.png")
  print(f"File saved to {name}.png")