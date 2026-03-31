from math import floor, sqrt

INCHES = "in"
MILLIMETERS = "mm"
CENTIMETERS = "cm"

PAGE_SIZES = {
  "a4": (210, 297, MILLIMETERS),
  "short": (8.5, 11, INCHES),
  "folio": (8.5, 13, INCHES)
}

PAGE_SIZE_PX = {}

def size_to_px(dim: tuple, unit:str=INCHES, dpi: int = 300) -> tuple:  
  w, h = dim
  
  if unit != INCHES:  # convert to inches
    
    # if centimeters, convert to millimeters
    if unit == CENTIMETERS:
      w *= 10
      h *= 10
    
    # 25.4mm in inch
    w /= 25.4
    h /= 25.4

  return (floor(w*sqrt(dpi)), floor(h*sqrt(dpi)))

for k, v in PAGE_SIZES.items():
  PAGE_SIZE_PX[k] = size_to_px((v[0], v[1]), v[2])
