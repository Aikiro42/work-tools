from PIL import Image
import colorsys

WIDTH, HEIGHT = 255, 255

# Create base image
img = Image.new("RGB", (WIDTH, HEIGHT))
pixels = img.load()

for y in range(HEIGHT):
    for x in range(WIDTH):
        # Normalize HSV values to [0, 1] for colorsys
        h = (240+120)/360
        s = x / 255.0
        v = y / 255.0

        r, g, b = colorsys.hsv_to_rgb(h, s, v)

        # Convert to 0–255 RGB
        pixels[x, y] = (
            int(r * 255),
            int(g * 255),
            int(b * 255),
        )

# Upscale 8x (nearest neighbor keeps pixel structure clean)
upscaled = img.resize(
    (WIDTH * 8, HEIGHT * 8),
    resample=Image.NEAREST
)

upscaled.save("hsv_gradient_8x.png")
upscaled.show()