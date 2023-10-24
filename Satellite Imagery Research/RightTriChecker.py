import math
from tkinter import *

class RightTriangle:
    def __init__(self, a, b, c='0'):
        try:
            self.a = float(a)
            self.b = float(b)
            if c == '0':
                self.c = math.sqrt(self.a ** 2 + self.b ** 2)
            else:
                self.c = float(c)
        except:
            raise ValueError('Error: both sides and the hypotenuse must be nonnegative')
        if self.a <= 0 or self.b <= 0 or self.c <= 0:
            raise ValueError('Error: both sides and the hypotenuse must be nonnegative')
        if math.fabs(self.a ** 2 + self.b ** 2 - self.c ** 2) > 0.01:
            raise ValueError('Error: sides do not form a valid right triangle')


    def __eq__(self, other):
        return (self.c - other.c) <= 0.01

    def __str__(self):
        return f'Right Triangle with side a = {self.a:.1f}, side b = {self.b:.1f}, and hypotenuse = {self.c:.1f}'

root = Tk()
root.title("Right Triangle Calculator")
root.geometry("400x200")

# Create the labels
aLabel = Label(root, text="Enter side a:")
bLabel = Label(root, text="Enter side b:")
cLabel = Label(root, text="Enter side c:")

# Create the text fields
aEntry = Entry(root)
bEntry = Entry(root)
cEntry = Entry(root)

# Create the submit button
submitButton = Button(root, text="Submit", command=lambda:submit())

# Create the output label
outputLabel = Label(root, text="")

# Create the submit function
def submit():
    try:
        a = aEntry.get()
        b = bEntry.get()
        righttri = RightTriangle(a, b)
        outputLabel.config(text=str(righttri))
    except ValueError as value_error:
        outputLabel.config(text=value_error)
    
    try:
        a = aEntry.get()
        b = bEntry.get()
        c = cEntry.get()
        righttri = RightTriangle(a, b, c)
        outputLabel.config(text=str(righttri))
    except ValueError as value_error:
        outputLabel.config(text=value_error)

# Place the labels, text fields, and button on the window
aLabel.pack()
aEntry.pack()
bLabel.pack()
bEntry.pack()
cLabel.pack()
cEntry.pack()
submitButton.pack()
outputLabel.pack()

# Start the GUI
root.mainloop()