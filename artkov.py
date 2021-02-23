from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import ImageTk, Image
import numpy as np

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


print(hexToRgb("#000000"))
print(hexToRgb("#ffffff"))


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
            print(dot.fill)
            print(dot.center)
            print(dot.radius)
            print(dot.id)

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
last_piece = user-created canvas
while(True):
    create 9 blank canvases
    fill each one with last_piece makeNext() method
    store all the dots for the canvas the user picks (or if programmatically, pick one randomly and sleep(500))
    update last_piece
    create 9 new canvases
'''




root = Tk(className="Artkov")
root.geometry("1000x700")
root.attributes("-fullscreen", True)

top = Frame(root, bg='pink')
center = Frame(root, bg='white', padx=3, pady=3)

center_options = Frame(center)
canvas = InitialCanvas(center, bg="white", height=700, width=900)

top_label = Label(top, text='Hi there. Let\'s make some art!')

radius_label = Label(center_options, text='Radius:')
radius_slider = Scale(center_options, from_=1, to=100,
                      orient=HORIZONTAL, command=canvas.setDotSize)
radius_slider.set(30)
color_button = Button(
    center_options, text="Choose new color", command=canvas.pickColor)

go_button = Button(
    center_options, text="Make some random art!", command=canvas.getDots)

top.grid(row=0, column=0)
center.grid(row=1, column=0)

canvas.grid(row=0, column=0)
center_options.grid(row=0, column=1)
top_label.grid(row=0, column=0)

radius_label.pack()
radius_slider.pack()
color_button.pack()
go_button.pack()

root.mainloop()
