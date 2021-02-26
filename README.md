# Artkov: An interactive GUI that uses markov chains to create dot art.

## How to Run

To run this program, you need a python 3 environment with [tkinter](https://docs.python.org/3/library/tkinter.html), [pillow](https://pillow.readthedocs.io/en/stable/), and [numpy](https://numpy.org/).
In my environment, tkinter and pillow were already there; this may be different for you.

When you run the program, you will be presented with a canvas. If you click on this canvas, a dot will be created with its center where you clicked. By default, the dot will be black and its size will be based on your screen, but you can change both of these with the slider and the button on the right of the screen. Also, if you'd like to exit the program, you can press the "Exit" button.

Once you have made dots to your heart's content, you can press the button that says "Make some random art!" Nine canvases will appear, with the middle canvas being a scaled down version of the art you made. The other eight canvases will be based on the artwork you made, but each dot may have different sizes and colors than those in the piece you made. These parameters are changing via a markov chain (more details later).

If you click on any canvas, including the middle one, the canvas you click on will go to the middle and eight new art pieces will be made from the one you clicked on. You can also press the "Auto-select" button to have the computer make a random choice.

A markov chain requires a transition matrix to base its probabilistic choices on. This may come from a dataset (i.e. a markov chain to predict the weather would likely use lots of past weather data), but could also update its matrix with present results (your markov chain could run an operation once a day to add today's weather conditions to its matrix).

My transition matrices don't do either of those. The question my system asks is: given that my dot's radius is 100 pixels, what should it be next? I tried to think of a way to answer this question that would result in interesting visual changes to the art. I decided to have a constant value in between 0 and 1, that I called "Dropoff," and the probability of the next value would be proportional to the Dropoff raised to the distance from the last value. For example, if the last dot had a radius of 100, then transition_matrix[100][98] would be Dropoff^2. Essentially, this meant that the next value is likely to be close to the last one. There is also another parameter that will decrease the probability of the last value repeating itself.

The program is suppose to open a full screen window, but every once in a while it isn't full screen. This should work fine, but if you want the best experience, then you might want to close the window and run the program again.

## How is this meaningful to me?

This project was inspired heavily by the book _The Dot_, by Peter H. Reynolds. This book was meaningful to me as a child, and so I wanted to create a system that was in some way related to the book. This evolved into a system that allows you to easily create interesting dot art, and modify your own creation.

## How did this challenge me?

While Python is a relatively comfortable language for me, I had never used the tkinter package before. It definitely felt like a challenge to not only learn the various methods of the package, but create something within the project guidelines. I am happy with my choice of technologies, because I've spent some time building web applications, but much less time making things that resemble native apps.

## Is this creative?

I think that this system is _somewhat_ creative. From our formal, albeit simple, definition, I feel like it is more novel than it is creative. The art that the system creates definitely feels personally creative, and I'm often excited and surprised in the random directions the generation goes. I feel less qualified to say whether the system creates valuable art in the domain, as frankly, I don't know very much about visual art!

## Examples

All examples were created from a starting canvas (that I made) with four black dots of the same size.
