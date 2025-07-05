# Gui

`gui.py` is a Python script for the Numworks calculator. It provides
a simple way to create a Graphical UI.

- normal version: [src/gui.py](src/gui.py)
- minified version: [minified/gui.py](src/gui.py)


## Overview

This module allows placing simple GUI elements on stacked rows, each row being centered horizontally.

![A GUI with some buttons, a range and a textbox.](/about/example.png)


### Label

Shows some text


### Button

A toggleable button. Only one can be enabled at the same time on a row.


### Slider (aka. a range if you prefer)

Used to select a number between a minimum and a maximum.


### TextBox

A field allowing typing text.



## How to use?

See the `example()` function in [gui.py](/src/gui.py).


## Notes

There is a lot of room for improvement, but I don't need this module anymore
and have far too many other things to do. It's usable in this state, but really
rigid.


## Dependencies

To run it on your computer, you need this modules:
- [ion-numworks](https://pypi.org/project/ion-numworks/)
- [kandinsky](https://pypi.org/project/kandinsky/)