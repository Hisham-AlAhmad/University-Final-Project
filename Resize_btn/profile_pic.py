from flask import Flask, render_template, request, send_from_directory, Blueprint, jsonify
from PIL import Image, ImageFilter, ImageEnhance
from werkzeug.utils import secure_filename
import os


def enhancing_image(image):
    # Sharpen the image
    image = image.filter(ImageFilter.SHARPEN)  # sharpen by x1
    # Detailing the image
    image = image.filter(ImageFilter.DETAIL)  # detail by x1
    # Smooth the image
    image = image.filter(ImageFilter.SMOOTH)  # smooth by x1
    # Adjust contrast and brightness
    contrast_factor = 1.3  # Increase contrast by 30%
    brightness_factor = 1.5  # Increase brightness by 50%
    saturation_factor = 1.2  # Increase saturation by 20%
    # Create an ImageEnhance object for the image and enhance it
    enhancer = ImageEnhance.Contrast(image)
    enhancer.enhance(contrast_factor)
    enhancer = ImageEnhance.Brightness(image)
    enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation_factor)  # This one is for saturation
    return image


# Open the image file
img = Image.open('alhaj1.png')
img = enhancing_image(img)
# Calculate the new dimensions while maintaining the aspect ratio
width, height = img.size
new_width = 360

new_height = int(new_width * height / width)
# Resize the image

img = img.resize((new_width, new_height))
# Add black padding to the image
new_img = Image.new('RGB', (360, 360), color='black')

new_img.paste(img, (0, (360 - new_height) // 2))
# Save the resized image
new_img.save('alhaj_ppt.png')
