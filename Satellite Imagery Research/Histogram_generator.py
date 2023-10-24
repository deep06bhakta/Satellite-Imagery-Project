
import numpy as np
import cv2

# read the image file
img = cv2.imread('/Users/deepbhakta/Downloads/Satellite Imagery Research/Sample Images/satellite2.png')

# convert image to grayscale
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# apply thresholding to make binary image
ret, thresh = cv2.threshold(gray_image, 127, 255, 0)

# find contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# make a copy of the image
output_image = img.copy()

# iterate over the contours and label them
for cnt in contours:
    # check the area of the contour
    area = cv2.contourArea(cnt)
    
    # if the area is greater than 15
    if area > 15:
        # draw the contour
        cv2.drawContours(output_image,[cnt],0,(0,255,0),2)
        
        # label the contour
        if area > 150:
            label = 'DRY'
       # elif area < 100:
       #     label = '0'
        else:
            label = ' '
        cv2.putText(output_image, label, (cnt[0][0][0], cnt[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

# show the output image
cv2.imshow('Output Image',output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()