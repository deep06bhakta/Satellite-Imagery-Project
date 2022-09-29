import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2

# open image and convert to numpy array
img = Image.open('C:\\Users\\deepb\\OneDrive\\Desktop\\Satellite Imagery Research\\Sample Images\\test3.png')
arr = np.array(img)


# extract red, green, and blue channels
r = arr[:,:,0]
g = arr[:,:,1]
b = arr[:,:,2]


# calculate NDVI
ndvi = ((b) - (r))/((b) + (r))

# Alternate formula
#ndvi = (g.astype(float)-r.astype(float))/(g.astype(float)+r.astype(float))


# create mask of pixels with NDVI values above 0.3
mask = np.where(ndvi>0.3, 255, 0)

# plot masked image
plt.imshow(mask, cmap='Wistia')
plt.colorbar()
plt.show()

# plot histogram of NDVI values
plt.hist(ndvi.ravel(), bins=256, range=(-1,1))
plt.show()