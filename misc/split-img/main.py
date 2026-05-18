from PIL import Image
import os
import sys

def split_image(image_path, cols=17, rows=10, output_dir="tiles"):
    img = Image.open(image_path)
    width, height = img.size

    # base tile size
    base_w = 28+5
    base_h = 28+5

    # cumulative positions
    x_positions = [0]
    for w in range(cols):
        x_positions.append(5*w + x_positions[-1] + base_w)

    y_positions = [0]
    for h in range(rows):
        y_positions.append(y_positions[-1] + base_h)

    os.makedirs(output_dir, exist_ok=True)

    count = 0
    for r in range(rows):
        for c in range(cols):
            left = x_positions[c]
            upper = y_positions[r]
            right = x_positions[c + 1]
            lower = y_positions[r + 1]

            tile = img.crop((left, upper, right, lower))

            filename = f"tile_r{r:02d}_c{c:02d}.png"
            tile.save(os.path.join(output_dir, filename))
            count += 1

    print(f"Saved {count} tiles to '{output_dir}'")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split.py input_image [output_dir]")
        sys.exit(1)

    image_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "tiles"

    split_image(image_path, cols=17, rows=10, output_dir=output_dir)