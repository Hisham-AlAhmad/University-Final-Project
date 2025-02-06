# from PIL import Image 
# from PIL import ImageEnhance 

# # Opens the image file 
# image = Image.open('uploads/raidenCute.jpg') 

# # shows image in image viewer 
# image.show() 
# # Enhance Brightness 
# curr_bri = ImageEnhance.Brightness(image) 
# new_bri = 1.0

# # Brightness enhanced by a factor of 2.5 
# img_brightened = curr_bri.enhance(new_bri) 

# # shows updated image in image viewer 
# img_brightened.show() 

import cv2

# Load the image
image = cv2.imread('uploads/raidenCute.jpg')

# Get the current width and height of the image
height, width = image.shape[:2]

# Calculate the new width and height, ten times larger than the original size
new_width = width * 10
new_height = height * 10

# Resize the image
resized_image = cv2.resize(image, (new_width, new_height))

# Save the enhanced image
cv2.imwrite('enhanced_image.jpg', resized_image)
