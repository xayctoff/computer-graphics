import numpy as number

from source.main.constants import BLACK
from source.main.constants import BLUE
from source.main.constants import GREEN
from source.main.constants import HEIGHT
from source.main.constants import RED
from source.main.constants import WIDTH


# Обновление полотна
# @param kind тип проецирования
# @param body объект
# @param canvas непосредственно полотно с объектом
# @return обновлённые координаты объекта
def draw(kind, body, canvas):
    # Очищаем полотно перед отображением изменённого объекта
    canvas.get_canvas().delete("all")

    nodes = body.get_nodes()

    # Прорисовываем объект
    for edge in body.get_edges():
        canvas.get_canvas().create_line(nodes[edge[0]][0] + WIDTH / 2,
                                        -nodes[edge[0]][1] + HEIGHT / 2,
                                        nodes[edge[1]][0] + WIDTH / 2,
                                        -nodes[edge[1]][1] + HEIGHT / 2,
                                        fill=BLACK)

    # Матрица осей координат объекта
    axis = [
        [0, 0, 0, 1],
        [200, 0, 0, 1],
        [0, 200, 0, 1],
        [0, 0, 200, 1]
    ]

    # Индикатор осей координат (цветовое обозначение)
    indicator = [
        [0, 1, RED],
        [0, 2, BLUE],
        [0, 3, GREEN]
    ]

    # Прорисовываем оси координат
    for edge in indicator:
        canvas.get_canvas().create_line(axis[edge[0]][0] + WIDTH / 2,
                                        -axis[edge[0]][1] + HEIGHT / 2,
                                        axis[edge[1]][0] + WIDTH / 2,
                                        -axis[edge[1]][1] + HEIGHT / 2,
                                        fill=edge[2])

    # Выводим параметры создаваемого объекта на полотно
    canvas.get_canvas().create_text(WIDTH / 100, HEIGHT / 100, anchor="nw", fill=BLACK,
                                    text="Координаты: ({}, {}, {})\n".format(body.get_coordinates()[0],
                                                                             body.get_coordinates()[1],
                                                                             body.get_coordinates()[2]) +
                                         "Градусы: ({}, {}, {})\n".format(body.get_angles()[0],
                                                                          body.get_angles()[1],
                                                                          body.get_angles()[2]) +
                                         "Габариты: ({}, {}, {})".format(body.get_size()[0],
                                                                         body.get_size()[1],
                                                                         body.get_size()[2])
                                    )
    return nodes


# Обновление объекта
# @param body непосредственно объект
# @param matrix матрица аффинного преобразования
# @param nodes координаты точек объекта
def update(body, matrix):
    # Список обновлённых координат объекта
    result = []

    # Для обновления координат объекта применим произведение матриц
    for node in body.get_nodes():
        result.append(number.matmul(node, matrix))

    body.set_nodes(result)


# Перенос объекта
# @param body непосредственно объект
# @param vector вектор переноса
def shift(body, vector):
    # Прибавляем вектор переноса к текущим координатам объекта
    coordinates = body.get_coordinates() + vector
    body.set_coordinates(coordinates)

    # Матрица переноса, где четвёртая строка содержит координаты перемещения объекта (x y z 1)
    matrix = number.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [vector[0], vector[1], vector[2], 1]
    ])

    # Обновляем координаты объекта, исходя из текущего аффинного преобразования
    # В данном случае — перемещение объекта
    update(body, matrix)
