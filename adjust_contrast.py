from PIL import Image, ImageEnhance

# Load image
image = Image.open("your_image.jpg")

# Adjust brightness (1.0 = original, <1.0 = darker, >1.0 = brighter)
enhancer = ImageEnhance.Brightness(image)
bright_image = enhancer.enhance(1.5)  # 50% brighter
bright_image.save("bright_image.jpg")

# Adjust contrast
enhancer = ImageEnhance.Contrast(image)
contrast_image = enhancer.enhance(1.8)  # stronger contrast
contrast_image.save("contrast_image.jpg")

# Adjust sharpness
enhancer = ImageEnhance.Sharpness(image)
sharp_image = enhancer.enhance(2.0)  # sharper
sharp_image.save("sharp_image.jpg")

print("Adjusted images saved!")
