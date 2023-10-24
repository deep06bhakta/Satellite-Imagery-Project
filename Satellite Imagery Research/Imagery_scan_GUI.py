##########################################
## Importing all the libraries required ##
##########################################
from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as st
from tkinter import filedialog
from matplotlib import pyplot as plt
import cv2
import numpy as np

#########################################################################################################
## This is the function that takes care of choosing a file to pass on to other funtions to scan images ##
#########################################################################################################

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",

                                          # IF RUNING ON WINDOWS, TAKE OUT THE COMMENTS BELOW (#)
                                          #filetypes = (("all files",
                                          #              "*.*"),
                                          #             ("all files",
                                          #              "*.*"))
                                        )
      
    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
    # Create the root window
    image_input = cv2.imread(filename)

###################################################################################################
## This part of the code segragates the image into two different masks one with plantsno plants  ##
###################################################################################################

# Select region of interest.
#    imcrop = image_input[70:250, 70:250]

# Convert BGR to HSV.
    RGB_HSV = cv2.cvtColor(image_input, cv2.COLOR_BGR2HSV)

# Define range of colors in HSV.
    lower_limit_beige = np.array([0,0,0])
    upper_limit_beige = np.array([25,255,255])

# Define range of colors in HSV
    lower_limit_green = np.array([40,40,40])
    upper_limit_green = np.array([140,255,255])

# Create mask for land
    mask_land = cv2.inRange(RGB_HSV, lower_limit_beige, upper_limit_beige)

# Create mask for plantation
    mask_plants = cv2.inRange(RGB_HSV, lower_limit_green, upper_limit_green)

# Output images with just land and with plants
    output_land = cv2.bitwise_and(image_input, image_input, mask = mask_land)

    output_plants = cv2.bitwise_and(image_input, image_input, mask = mask_plants)
    
    gray = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# Dilate to combine adjacent text contours
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations = 3)

# Find contours and filter using contour properties
    cnts = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        if area > 100 and (w > 20 and w < 35) and (h > 10 and h < 20):
           cv2.rectangle(image_input, (x, y), (x + w, y + h), (36,255,12), 2)

###################################################################################################
## This part of the code make the images them deeply grayscaled and equalized for the histogram ###
###################################################################################################

# Convert the image to grayscale
    gray = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)

# Apply histogram equalization
    hist_equalized = cv2.equalizeHist(gray)

# Show the images
   # cv2.imshow('Grayscale', image_input)
    cv2.imshow('Histogram Equalized', hist_equalized)

# Calculate the histograms for the grayscale and equalized images
    hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
    hist_equalized = cv2.calcHist([hist_equalized], [0], None, [256], [0, 256])

# Show imagees
    cv2.imshow('THRESH', thresh)
    cv2.imshow('ORIGINAL PHOTO', image_input)
    cv2.imshow("LAND WITH NO PLANTATION", output_land)
    cv2.imshow("LAND WITH PLANTATION", output_plants)

# Plot the histograms
    plt.subplot(1, 2, 1)
    plt.plot(hist_gray, color='black')
    plt.xlim([0, 256])      
    plt.subplot(1, 2, 2)
    plt.plot(hist_equalized, color='black')
    plt.xlim([0, 256])
    plt.show()

# Wait until a key pressed.
    cv2.waitKey(0)

####################################################################################################
## This part of the code is the GUI that helps the user select the file that they want to process ##
####################################################################################################

# Setting up an instance of the library to setup a screen
window = Tk()

# Set window title
window.title('File Explorer')
  
# Set window size
window.geometry("700x250")
  
#Set window background color
window.config(background = "grey")
  
# Create a File Explorer label
label_file_explorer = Label(window, 
                            text = "SELECT A PNG IMAGE", 
                            width = 100, 
                            height = 4, 
                            fg = "blue")

button_explore = Button(window,
                        text = "Browse Files", 
                        width = 10, height = 2, 
                        activebackground='#345', 
                        activeforeground='white',
                        command = browseFiles)
  
button_exit = Button(window,
                     text = "Close the program",  
                     activebackground='#345',  
                     activeforeground='white', 
                     command = exit)
  
# Grid method is chosen for placing
# the widgets at respective positions
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(column = 1, row = 1)
button_explore.grid(column = 1, row = 2)
button_exit.grid(column = 1, row = 3)

# Let the window wait for any events
window.mainloop()