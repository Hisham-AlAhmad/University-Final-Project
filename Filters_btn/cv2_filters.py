import cv2
import numpy as np

# Load the image
img = cv2.imread('IMG-20240310-WA0033.png')

# Convert the image to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Save the grayscale image
cv2.imwrite('black_and_white.jpg', gray_img)

# Create a golden color
golden_color = np.array([255, 215, 0])

# Add the golden color to the image
# golden_img = cv2.addWeighted(img, 0.5, golden_color, 0.5, 0)

# # Save the golden image
# cv2.imwrite('golden_vibes.jpg', golden_img)

# Increase the saturation of the image
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv_img[:, :, 1] = np.clip(hsv_img[:, :, 1] * 1.5, 0, 255)
vivid_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)

# Save the vivid image
cv2.imwrite('vivid.jpg', vivid_img)

# Create a neon color
neon_color = np.array([0, 255, 255])

# Add the neon color to the image
neon_img = cv2.addWeighted(img, 0.5, neon_color, 0.5, 0)

# Save the cyberpunk image
cv2.imwrite('cyberpunk.jpg', neon_img)

# Create a sky blue color
sky_blue_color = np.array([235, 206, 235])

# Add the sky blue color to the image
sky_blue_img = cv2.addWeighted(img, 0.5, sky_blue_color, 0.5, 0)

# Save the sky blue image
cv2.imwrite('sky_blue.jpg', sky_blue_img)

# Create a black ice color
black_ice_color = np.array([0, 191, 255])

# Add the black ice color to the image
black_ice_img = cv2.addWeighted(img, 0.5, black_ice_color, 0.5, 0)

# Save the black ice image
cv2.imwrite('black_ice.jpg', black_ice_img)

# Create a lilt color
lilt_color = np.array([255, 182, 193])

# Add the lilt color to the image
lilt_img = cv2.addWeighted(img, 0.5, lilt_color, 0.5, 0)

# Save the lilt image
cv2.imwrite('lilt.jpg', lilt_img)

# Create an amethyst color
amethyst_color = np.array([153, 51, 255])

# Add the amethyst color to the image
amethyst_img = cv2.addWeighted(img, 0.5, amethyst_color, 0.5, 0)

# Save the amethyst image
cv2.imwrite('amethyst.jpg', amethyst_img)

# Create an autumn color
autumn_color = np.array([255, 165, 0])

# Add the autumn color to the image
autumn_img = cv2.addWeighted(img, 0.5, autumn_color, 0.5, 0)

# Save the autumn image
cv2.imwrite('autumn.jpg', autumn_img)

# Create an ocean blue color
ocean_blue_color = np.array([0, 0, 255])

# Add the ocean blue color to the image
ocean_blue_img = cv2.addWeighted(img, 0.5, ocean_blue_color, 0.5, 0)

# Save the ocean blue image
cv2.imwrite('ocean_blue.jpg', ocean_blue_img)

# Create an orange color
orange_color = np.array([0, 165, 255])

# Add the orange color to the image
orange_img = cv2.addWeighted(img, 0.5, orange_color, 0.5, 0)

# Save the orange image
cv2.imwrite('orange.jpg', orange_img)
