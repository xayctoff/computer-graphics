import tkinter as tk

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


class Canvas(metaclass=MetaCanvas):

    def __init__(self, root):
        canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=WHEAT, bd=0, highlightthickness=0)
        canvas.place(x=0, y=0)

        self._labels = []
        self._buttons = []
        self._radio_buttons = []

    def add_label(self, root, text, x, y):
        label = Label(root, text)
        label.place(x, y)
        self._labels.append(label)

    def add_button(self, text, command, x, y):
        button = Button(text, command)
        button.place(x, y)
        self._buttons.append(button)

    def add_radio_buttons(self, text, variable, value, x, y):
        radio_button = RadioButton(text, variable, value)
        radio_button.place(x, y)
        self._radio_buttons.append(radio_button)
