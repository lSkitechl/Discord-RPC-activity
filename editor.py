from PIL import Image
import os


def prepare_asset(input_path, output_dir="prepared_assets", size=(512, 512), quality=90):
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.basename(input_path)
    name, _ = os.path.splitext(filename)
    output_path = os.path.join(output_dir, f"{name}.png")
    img = Image.open(input_path).convert("RGBA")
    img.thumbnail(size)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    x = (size[0] - img.width) // 2
    y = (size[1] - img.height) // 2
    canvas.paste(img, (x, y))
    canvas.save(output_path, quality=quality)
    return output_path
