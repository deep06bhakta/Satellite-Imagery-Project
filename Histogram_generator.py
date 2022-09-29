# Import the required packages
import cv2
import numpy as np
from matplotlib import pyplot as plt


# Load the image
img = cv2.imread('C:\\Users\\deepb\\OneDrive\\Desktop\\Satellite Imagery Research\\satellite2.png')

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply histogram equalization
hist_equalized = cv2.equalizeHist(gray)

# Show the images
cv2.imshow('Grayscale', img)
cv2.imshow('Histogram Equalized', hist_equalized)

# Calculate the histograms for the grayscale and equalized images
hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
hist_equalized = cv2.calcHist([hist_equalized], [0], None, [256], [0, 256])

# Plot the histograms
plt.subplot(1, 2, 1)
plt.plot(hist_gray, color='black')
plt.xlim([0, 256])

plt.subplot(1, 2, 2)
plt.plot(hist_equalized, color='black')
plt.xlim([0, 256])
plt.show()

# Wait until a key is pressed
cv2.waitKey(0)

# Destroy all the windows opened before
cv2.destroyAllWindows()