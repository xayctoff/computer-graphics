from tkinter import *

from source.main.constants import HEIGHT
from source.main.constants import PANEL_WIDTH
from source.main.constants import TITLE
from source.main.constants import WIDTH
from source.main.model.body import Body
from source.main.model.canvas import Canvas


def main():
    body = Body()

    # Инициализация окна
    root = Tk()
    root.geometry(str(WIDTH + PANEL_WIDTH) + "x" + str(HEIGHT))
    root.title(TITLE)
    root.resizable(width=False, height=False)
    root.mainloop()

    # Генерация полотна
    canvas = Canvas(root)

    # Перемещение
    canvas.add_label(root, "Перемещение", 705, 5)

    canvas.add_button("+", "", 705, 25)
    canvas.add_button("-", "", 730, 25)
    canvas.add_label(root, "X", 770, 30)

    canvas.add_button("+", "", 705, 55)
    canvas.add_button("-", "", 730, 55)
    canvas.add_label(root, "Y", 770, 60)

    canvas.add_button("+", "", 705, 85)
    canvas.add_button("+", "", 730, 85)
    canvas.add_label(root, "Z", 770, 90)

    # Поворот
    canvas.add_label(root, "Поворот", 700, 115)

    canvas.add_button("+", "", 705, 135)
    canvas.add_button("-", "", 730, 135)
    canvas.add_label(root, "X", 770, 140)

    canvas.add_button("+", "", 705, 165)
    canvas.add_button("-", "", 730, 165)
    canvas.add_label(root, "Y", 770, 170)

    canvas.add_button("+", "", 705, 195)
    canvas.add_button("-", "", 730, 195)
    canvas.add_label(root, "Z", 770, 200)

    # Масштабирование
    canvas.add_label(root, "Масштабирование", 705, 225)
    canvas.add_button("+", "", 705, 245)
    canvas.add_button("-", "", 730, 245)

    # Отражение
    canvas.add_label(root, "Отражение", 705, 280)
    canvas.add_button("Относительно X", "", 705, 300)
    canvas.add_button("Относительно Y", "", 705, 330)
    canvas.add_button("Относительно Z", "", 705, 360)

    # Проецирование
    canvas.add_radio_buttons("Косоугольное", "", "", 705, 390)
    canvas.add_radio_buttons("Перспективное", "", "", 705, 420)
    canvas.add_button("Проецирование ", "", 705, 460)


if __name__ == "__main__":
    main()