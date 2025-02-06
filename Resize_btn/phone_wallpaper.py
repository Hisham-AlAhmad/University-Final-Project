import cv2
import numpy as np

# Open the original image
img = cv2.imread('IMG-20240310-WA0033.png')

# Calculate the new dimensions while maintaining the aspect ratio
height, width, _ = img.shape
new_width = 360
new_height = int(new_width * height / width)

# Create a new black image
new_img = np.zeros((1080, 2400, 3), dtype=np.uint8)
new_img.fill(0)

# Resize the image
resized_img = cv2.resize(img, (new_width, new_height))

# Calculate the vertical position of the pasted image
y = (2400 - new_height) // 2

# Paste the resized image onto the new black image
new_img[y:y+new_height, :] = resized_img

# Save the resized image
cv2.imwrite('resized_image.jpg', new_img)