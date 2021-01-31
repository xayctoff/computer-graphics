from tkinter import *

from source.main.constants import HEIGHT
from source.main.constants import WHEAT
from source.main.constants import WIDTH


class MetaCanvas(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            instance = super().__call__(*args, **kwargs)
            self._instances[self] = instance
        return self._instances[self]


class BaseCanvas(metaclass=MetaCanvas):

    def __init__(self, root):
        self._canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg=WHEAT, bd=0, highlightthickness=0)
        self._canvas.place(x=0, y=0)

        self._labels = []
        self._buttons = []
        self._radio_buttons = []

    def add_label(self, root, text, abscissa, ordinate):
        label = Label(root, text=text)
        label.place(x=abscissa, y=ordinate)
        self._labels.append(label)

    def add_button(self, text, command, abscissa, ordinate):
        button = Button(text=text, command=command)
        button.place(x=abscissa, y=ordinate)
        self._buttons.append(button)

    def add_radio_buttons(self, text, variable, value, abscissa, ordinate):
        radio_button = Radiobutton(text=text, variable=variable, value=value)
        radio_button.place(x=abscissa, y=ordinate)
        self._radio_buttons.append(radio_button)

    def get_canvas(self):
        return self._canvas
