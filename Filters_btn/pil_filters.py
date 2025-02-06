from PIL import Image, ImageOps

# Open the image file
image = Image.open('IMG-20240310-WA0033.png')

# Convert the image to grayscale
gray_image = ImageOps.grayscale(image)

# Adjust the image brightness (e.g., increase by 50%)
brightness_factor = 1.5
brightened_image = ImageOps.colorize(gray_image, '#000000', '#ffffff').point(lambda i: i * brightness_factor)

# Adjust the image contrast (e.g., increase by 20%)
contrast_factor = 1.2
contrasted_image = ImageOps.colorize(gray_image, '#000000', '#ffffff').point(lambda i: i * (contrast_factor - 1) + 128)

# Save the adjusted images
brightened_image.save("brightened_image.jpg")
contrasted_image.save("contrasted_image.jpg")
