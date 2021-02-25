from tkinter import *
from tkinter import filedialog, colorchooser
from PIL import ImageTk, Image
import numpy as np
from math import floor
from random import choices

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

# of dots / size / color is equally likely to lead to any other.
Initially, make it basically completely random, meaning that every

But, based on the user's choices, change the transition matrices over time (basically learn the user's preferences).
"""

MIN_NUM_DOTS = 1
MAX_NUM_DOTS = 20
MIN_DOT_SIZE = 2
MAX_DOT_SIZE = 50
INIT_DOT_SIZE = 40
INIT_CANVAS_SIZE = 800
GRID_CANVAS_SIZE = 200
CANVAS_SCALING_FACTOR = GRID_CANVAS_SIZE / INIT_CANVAS_SIZE

DROPOFF = 0.75
# closer to 1 => new choices farther away from previous choice.
# closer to 0 => new choices closer to previous choice.

DECREASE_REPEATS_PARAM = 0.4
# closer to 1 => repeats are the most likely choice
# closer to 0 => repeats will never occur

size_tmatrix = [[] for _ in range(MAX_DOT_SIZE + 1)]
for i in range(len(size_tmatrix)):
    row = size_tmatrix[i]
    for j in range(len(size_tmatrix)):
        if j < MIN_DOT_SIZE:
            row.append(0)
        elif j == i:
            row.append(DECREASE_REPEATS_PARAM)
        else:
            row.append(DROPOFF ** abs(j - i))


def rgbToHex(rgb):
    r, b, g = [int(max(0, min(255, x))) for x in rgb]
    return "#{0:02x}{1:02x}{2:02x}".format(r, b, g)


def hexToRgb(hexcode):
    hexcode = hexcode[1:]
    return tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))


class Dot():
    def __init__(self, canvas, center, radius, fill, **kwargs):
        self.canvas = canvas
        self.radius = int(radius)
        self.center = center
        self.fill = fill
        canvas.dots.append(self)

        x, y = center
        r = self.radius
        coords = x + r, y + r, x - r, y - r
        self.id = canvas.create_oval(
            coords, fill=self.fill, width=0, **kwargs)


class MyCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.dots = []

    def copy_canvas(self, last_canvas):
        if self == last_canvas:
            return
        self.delete("all")
        self.dots = []
        for dot in last_canvas.dots:
            Dot(self, dot.center, dot.radius, dot.fill)

    def makeNext(self, last_canvas):
        inspiration_dots = last_canvas.dots
        self.delete("all")
        self.dots = []
        for dot in inspiration_dots:
            # calculate if dot should die / duplicate
            # if dot dies:
            #     continue
            # else if duplicates:
            #     create a new dot (add to the end of the list)

            possible_sizes = [i for i in range(MIN_DOT_SIZE, MAX_DOT_SIZE + 1)]
            probabilities = [size_tmatrix[dot.radius][i]
                             for i in possible_sizes]
            new_size = choices(possible_sizes, weights=probabilities)[0]

            # choose a new color using transition matrix

            Dot(self, dot.center, new_size, dot.fill)


def flattenDistrib(distrib):
    s = sum(distrib)
    scale = 1 / s
    return [i * scale for i in distrib]


class InitialCanvas(MyCanvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Button-1>", self.handleClick)
        self.dotFill = "#000000"
        self.dotSize = INIT_DOT_SIZE

    def handleClick(self, e):
        center = [e.x, e.y]
        Dot(self, center, self.dotSize, self.dotFill)

    def pickColor(self):
        color_code = colorchooser.askcolor(title="Choose color")
        self.dotFill = color_code[1]

    def setDotSize(self, val):
        self.dotSize = int(val)


def artstart(center, canvas):
    def handleGridClick(last_canvas, canvases):
        def func(*args):
            canvases[4].copy_canvas(last_canvas)
            for i, canvas in enumerate(canvases):
                if i != 4:
                    canvas.makeNext(canvases[4])
        return func

    dots = canvas.dots
    canvas.destroy()
    canvases = [None] * 9
    for i in range(9):
        row = floor(i / 9 * 3)
        col = i % 3
        canvases[i] = MyCanvas(center, bg="white", height=200, width=200)
        canvases[i].grid(row=row, column=col)
    middle_canvas = canvases[4]
    for dot in dots:
        scaled_radius = dot.radius * CANVAS_SCALING_FACTOR
        scaled_center = [coord * CANVAS_SCALING_FACTOR for coord in dot.center]
        Dot(middle_canvas, scaled_center, scaled_radius, dot.fill)

    for i in range(9):
        if i != 4:
            canvases[i].makeNext(middle_canvas)

    for canvas in canvases:
        canvas.bind("<Button-1>", handleGridClick(canvas, canvases))


# create root window
root = Tk(className="Artkov")
root.geometry("1000x700")
root.attributes("-fullscreen", True)

# create frames
top_frame = Frame(root, bg='pink')
center_frame = Frame(root, bg='white', padx=3, pady=3)
bottom_frame = Frame(root, bg='pink')

# create frames within center
center_options = Frame(center_frame)
init_canvas = InitialCanvas(
    center_frame, bg="white", height=INIT_CANVAS_SIZE, width=INIT_CANVAS_SIZE)

# create items within top / center_options
top_label = Label(top_frame, text='Hi there. Let\'s make some art!')
exit_button = Button(bottom_frame, text="Exit", command=root.quit)

radius_label = Label(center_options, text='Radius:')
radius_slider = Scale(center_options, from_=MIN_DOT_SIZE / CANVAS_SCALING_FACTOR, to=MAX_DOT_SIZE / CANVAS_SCALING_FACTOR,
                      orient=HORIZONTAL, command=init_canvas.setDotSize)
radius_slider.set(INIT_DOT_SIZE)
color_button = Button(
    center_options, text="Choose new color", command=init_canvas.pickColor)

go_button = Button(
    center_options, text="Make some random art!", command=lambda: artstart(center_frame, init_canvas))

# place frames, sub-frames, and items
top_frame.pack()
center_frame.pack()
bottom_frame.pack()

init_canvas.grid(row=0, column=0)
center_options.grid(row=0, column=1)
top_label.grid(row=0, column=0)

radius_label.pack()
radius_slider.pack()
color_button.pack()
go_button.pack()
exit_button.pack()

root.mainloop()
