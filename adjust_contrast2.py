from PIL import Image

# Load image
image = Image.open("your_image.jpg")

# Resize image
resized = image.resize((400, 400))  # new size (width, height)
resized.save("resized_image.jpg")

# Rotate image
rotated = image.rotate(45, expand=True)  # rotate 45 degrees
rotated.save("rotated_image.jpg")

# Convert to grayscale
grayscale = image.convert("L")
grayscale.save("grayscale_image.jpg")

print("New adjusted images saved!")
