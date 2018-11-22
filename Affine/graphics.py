import numpy as number

from tkinter import *
from defs import *
from model import Object


#   Косоугольное и перспективное проецирование
#   @param kind: тип проецирования
#   @param nodes: координаты точек объекта
def projection(kind, nodes):
    #   При косоугольном проецировании используется пучок прямых неперпендикулярных плоскости экрана
    #   При проецировании на ось Z в третьей строке матрице имеем: (-cos 45° sin 45° 0 1)
    if kind.get() == 0:
        matrix = number.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [-math.cos(K), math.sin(K), 0, 0],
            [0, 0, 0, 1]])

    #   При перспективном проецировании пучок прямых проходят через центр проекции
    #   В нашем случае это точка C, расположенная в третьей строке матрицы, так как проецируем на ось Z
    else:
        matrix = number.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, C],
            [0, 0, 0, 1]
        ])

    #   Обновим объект в зависимости от выбранного типа проецирования
    result = []

    for node in nodes:
        new = number.matmul(node, matrix)
        #   Когда осуществляется переход в перспективное проецирование, то изменяется ось h
        #   При произведении матрицы проецирования и текущих координат объекта
        #   То есть, получаем координату вида (x y 0 1 - z/C)
        #   Приведём координаты к виду (x / (1 - z/c) y / (1 - z/c) 0 1)
        #   Важно, что при переходе к косоугольному проецированию координаты возвращают вид (x y z 1)
        new = new / (new[3])
        result.append(new)

    #   Возвращаем координаты объекта, исходя из текущего афинного преобразования, в данном случае проецирования
    return number.array(result)


#   Обновление экрана
#   @param canvas: полотно, где находится объект
#   @return nodes: обновлённые координаты объекта
def update(kind, canvas):
    nodes = projection(kind, object.nodes)

    #   Очищаем полотно перед отрисовкой изменённого объекта
    canvas.delete("all")

    #   Прорисовываем объект
    for edge in object.edges:
        canvas.create_line(nodes[edge[0]][0] + WIDTH / 2,
                           -nodes[edge[0]][1] + HEIGHT / 2,
                           nodes[edge[1]][0] + WIDTH / 2,
                           -nodes[edge[1]][1] + HEIGHT / 2,
                           fill=BLACK)

    #   Оси координат
    axis = [
        [0, 0, 0, 1],
        [200, 0, 0, 1],
        [0, 200, 0, 1],
        [0, 0, 200, 1]
    ]

    #   Индикатор осей координат (цветовое обозначение)
    indicator = [
        [0, 1, RED],
        [0, 2, BLUE],
        [0, 3, GREEN]
    ]

    #   Подвергаем оси проецированию
    axis = projection(kind, axis)

    #   Прорисовываем оси координат
    for edge in indicator:
        canvas.create_line(axis[edge[0]][0] + WIDTH / 2,
                           -axis[edge[0]][1] + HEIGHT / 2,
                           axis[edge[1]][0] + WIDTH / 2,
                           -axis[edge[1]][1] + HEIGHT / 2,
                           fill=edge[2])

    #   Выводим параметры создаваемого объекта на полотно
    canvas.create_text(WIDTH / 100, HEIGHT / 100, anchor=NW, fill=BLACK,
                       text="Координаты: ({}, {}, {})\n".format(object.coordinates[0], object.coordinates[1],
                                                                object.coordinates[2]) +
                            "Градусы: ({}, {}, {})\n".format(object.angles[0], object.angles[1],
                                                             object.angles[2]) +
                            "Габариты: ({}, {}, {})".format(object.size[0], object.size[1], object.size[2])
                       )
    return nodes


def main():
    root = Tk()
    root.geometry(str(WIDTH + PANEL) + "x" + str(HEIGHT))
    root.title("Афинные преобразования")
    root.resizable(width=False, height=False)

    #   Текущий тип проецирования
    kind = IntVar()
    kind.set(PROJECTION[0])

    #   Генерация полотна
    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg=WHEAT, bd=0, highlightthickness=0)
    canvas.place(x=0, y=0)
    update(kind, canvas)

    #   Перемещение
    label = Label(root, text="Перемещение")
    label.place(x=705, y=5)

    plus = Button(text="+", command=lambda: [object.shift([MOVE, 0, 0, 0]), update(kind, canvas)])
    plus.place(x=705, y=25)
    minus = Button(text="-", command=lambda: [object.shift([-MOVE, 0, 0, 0]), update(kind, canvas)])
    minus.place(x=730, y=25)
    axis = Label(root, text="X")
    axis.place(x=770, y=30)

    plus = Button(text="+", command=lambda: [object.shift([0, MOVE, 0, 0]), update(kind, canvas)])
    plus.place(x=705, y=55)
    minus = Button(text="-", command=lambda: [object.shift([0, -MOVE, 0, 0]), update(kind, canvas)])
    minus.place(x=730, y=55)
    axis = Label(root, text="Y")
    axis.place(x=770, y=60)

    plus = Button(text="+", command=lambda: [object.shift([0, 0, MOVE, 0]), update(kind, canvas)])
    plus.place(x=705, y=85)
    minus = Button(text="-", command=lambda: [object.shift([0, 0, -MOVE, 0]), update(kind, canvas)])
    minus.place(x=730, y=85)
    axis = Label(root, text="Z")
    axis.place(x=770, y=90)

    #   Поворот
    label = Label(root, text="Поворот")
    label.place(x=705, y=115)

    plus = Button(text="+", command=lambda: [object.rotate([TURN, 0., 0., 0.], AXIS[0]), update(kind, canvas)])
    plus.place(x=705, y=135)
    minus = Button(text="-", command=lambda: [object.rotate([-TURN, 0., 0., 0.], AXIS[0]), update(kind, canvas)])
    minus.place(x=730, y=135)
    axis = Label(root, text="X")
    axis.place(x=770, y=140)

    plus = Button(text="+", command=lambda: [object.rotate([0., TURN, 0., 0.], AXIS[1]), update(kind, canvas)])
    plus.place(x=705, y=165)
    minus = Button(text="-", command=lambda: [object.rotate([0., -TURN, 0., 0.], AXIS[1]), update(kind, canvas)])
    minus.place(x=730, y=165)
    axis = Label(root, text="Y")
    axis.place(x=770, y=170)

    plus = Button(text="+", command=lambda: [object.rotate([0., 0., TURN, 0.], AXIS[2]), update(kind, canvas)])
    plus.place(x=705, y=195)
    minus = Button(text="-", command=lambda: [object.rotate([0., 0., -TURN, 0.], AXIS[2]), update(kind, canvas)])
    minus.place(x=730, y=195)
    axis = Label(root, text="Z")
    axis.place(x=770, y=200)

    #   Маcштабирование
    label = Label(root, text="Масштабирование")
    label.place(x=705, y=225)

    plus = Button(text="+", command=lambda: [object.scale([SCALE, SCALE, SCALE, 0]), update(kind, canvas)])
    plus.place(x=705, y=245)
    minus = Button(text="-", command=lambda: [object.scale([-SCALE, -SCALE, -SCALE, 0]), update(kind, canvas)])
    minus.place(x=730, y=245)

    #   Отражение
    label = Label(root, text="Отражение")
    label.place(x=705, y=280)
    x = Button(text="Относительно X", command=lambda: [object.mirror(AXIS[0]),
                                                       update(kind, canvas)])
    x.place(x=705, y=300)
    y = Button(text="Относительно Y", command=lambda: [object.mirror(AXIS[1]),
                                                       update(kind, canvas)])
    y.place(x=705, y=330)
    z = Button(text="Относительно Z", command=lambda: [object.mirror(AXIS[2]),
                                                       update(kind, canvas)])
    z.place(x=705, y=360)

    #   Проецирование
    Radiobutton(text="Косоугольное", variable=kind, value=PROJECTION[0]).place(x=705, y=390)
    Radiobutton(text="Перспективное", variable=kind, value=PROJECTION[1]).place(x=705, y=420)

    Button(text="Проецирование ", command=lambda: update(kind, canvas)).place(x=705, y=460)

    root.mainloop()


if __name__ == "__main__":
    #   Объект, который подвергнется афинным преобразованиям
    object = Object()
    main()
