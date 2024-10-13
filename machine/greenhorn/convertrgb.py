from PIL import Image

# Load the PNG image
image_path = "./outputpdfimg-000.png"  # change this
image = Image.open(image_path)

# Print original image mode and size
print(f"Original image mode: {image.mode}")  # Should be 'P'
print(f"Image size: {image.size}")

# Convert to RGB mode if necessary
if image.mode != "RGB":
    image = image.convert("RGB")
    rgb_image_path = "output_rgb.png"  # choose path
    image.save(rgb_image_path)
    print(f"Converted image saved at {rgb_image_path} with mode {image.mode}")

# Print new image mode to confirm
new_image = Image.open(rgb_image_path)
print(f"New image mode: {new_image.mode}")  # Should be 'RGB'
