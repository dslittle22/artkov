from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import ImageTk, Image
import numpy as np
from math import floor

"""
Author: Danny Little

UI FLOW:

Start with a white canvas and a dot, with:
- random center
- random color
- random size (between a min and max size)


(possibly allow user to place, size, and color their own dot)

Have a "start" button.
When they click start, have a 3x3 grid with that image in the middle, and 8 newly generated art pieces based on that one.

Use markov things for
- Changing the number of dots
- Changing the size of each dot
- Changing the color of each dot

We'd probably want to take the average across the whole piece of size, color, and position, and use that for the next piece.

#of dots / size / color is equally likely to lead to any other.
Initially, make it basically completely random, meaning that every

But, based on the user's choices, change the transition matrices over time (basically learn the user's preferences).
"""


def rgbToHex(rgb):
    r, b, g = [int(max(0, min(255, x))) for x in rgb]
    return "#{0:02x}{1:02x}{2:02x}".format(r, b, g)


def hexToRgb(hexcode):
    hexcode = hexcode[1:]
    return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))


class Dot():
    def __init__(self, canvas, center, **kwargs):
        self.canvas = canvas
        self.radius = canvas.dotSize
        self.center = center
        self.fill = canvas.dotColor

        x, y = center
        r = self.radius
        coords = x + r, y + r, x - r, y - r
        self.id = canvas.create_oval(
            coords, fill=self.fill, width=0, **kwargs)


class InitialCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.handleClick)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        self.dotColor = "#000000"
        self.dotSize = 30
        self.dots = []

    def handleClick(self, e):
        center = [e.x, e.y]
        canvas.dots.append(Dot(self, center))

    def resize(self, newW, newH):
        wscale = float(newW)/self.width
        hscale = float(newH)/self.height
        self.config(width=newW, height=newH)
        self.scale("all", 0, 0, wscale, hscale)

    def pickColor(self):
        color_code = colorchooser.askcolor(title="Choose color")
        self.dotColor = color_code[1]

    def setDotSize(self, val):
        self.dotSize = int(val)

    def getDots(self):
        for dot in self.dots:
            print(f'fill color: {dot.fill}')
            print(f'center: {dot.center}')
            print(f'radius: {dot.radius}')
            print(f'id: {dot.id}')
            print(f'coords: {dot.canvas.coords(dot.id)}')

    def makeNext():
        """
        for each dot:
            if dot disappears:
                do not include dot
            else if dot duplicates:
                create a new dot (add to the end of the list)

            choose a new color using transition matrix
            choose a new radius using transition matrix
            choose a new center using transition matrix
        return list of new dots
        """


'''
Routine for creating new pieces:
last_canvas = user-created canvas
delete last canvas
canvases = 9 new blank canvases
while(True):
    fill each one with last_canvas makeNext() method
    wait for user to pick a canvas, and store dots (or if programmatically, pick one randomly and sleep(500))
    update last_canvas
    clear all canvases
'''


def artstart(center, canvas):
    dots = canvas.dots
    canvas.destroy()
    canvases = {}
    for i in range(9):
        row = floor(i / 9 * 3)
        col = i % 3
        canvases[i] = Canvas(center, bg="white", height=200, width=200)
        canvases[i].grid(row=row, column=col)
    middle_canvas = canvases[4]
    for dot in dots:
        """
        self.canvas = canvas
        self.radius = canvas.dotSize
        self.center = center
        self.fill = canvas.dotColor

        x, y = center
        r = self.radius
        coords = x + r, y + r, x - r, y - r
        self.id = canvas.create_oval(
        """
        scaling_factor = 200 / 800
        r = dot.radius * scaling_factor
        x, y = [coord * scaling_factor for coord in dot.center]
        coords = x + r, y + r, x - r, y - r
        middle_canvas.create_oval(coords, fill=dot.fill, width=0)


# create root window
root = Tk(className="Artkov")
root.geometry("1000x700")
root.attributes("-fullscreen", True)

# create frames
top = Frame(root, bg='pink')
center = Frame(root, bg='white', padx=3, pady=3)
bottom = Frame(root, bg='pink')

# create frames within center
center_options = Frame(center)
canvas = InitialCanvas(center, bg="white", height=800, width=800)

# create items within top / center_options
top_label = Label(top, text='Hi there. Let\'s make some art!')
exit_button = Button(bottom, text="Exit", command=root.quit)

radius_label = Label(center_options, text='Radius:')
radius_slider = Scale(center_options, from_=1, to=100,
                      orient=HORIZONTAL, command=canvas.setDotSize)
radius_slider.set(30)
color_button = Button(
    center_options, text="Choose new color", command=canvas.pickColor)

go_button = Button(
    center_options, text="Make some random art!", command=lambda: artstart(center, canvas))

# place frames, sub-frames, and items
top.pack()
center.pack()
bottom.pack()

canvas.grid(row=0, column=0)
center_options.grid(row=0, column=1)
top_label.grid(row=0, column=0)

radius_label.pack()
radius_slider.pack()
color_button.pack()
go_button.pack()
exit_button.pack()

root.mainloop()
