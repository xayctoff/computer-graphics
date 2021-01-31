import math
import numpy as number

from source.main.constants import BLACK
from source.main.constants import BLUE
from source.main.constants import C
from source.main.constants import GREEN
from source.main.constants import HEIGHT
from source.main.constants import K
from source.main.constants import RED
from source.main.constants import WIDTH
from source.main.model.axis import Axis
from source.main.model.projection import Projection


# Обновление полотна
# @param kind тип проецирования
# @param body объект
# @param canvas непосредственно полотно с объектом
# @return обновлённые координаты объекта
def draw(kind, body, canvas):
    nodes = projection(kind, body.get_nodes())

    # Очищаем полотно перед отображением изменённого объекта
    canvas.get_canvas().delete("all")

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

    # Подвергаем оси проецированию
    axis = projection(kind, axis)

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


# Проецирование объекта
# @param kind тип проецирования
# @param nodes координаты точек объекта
def projection(kind, nodes):
    # При косоугольном проецировании используется пучок прямых неперпендикулярных плоскости экрана
    # При проецировании на ось Z в третьей строке матрице имеем: (-cos 45° sin 45° 0 1)
    if kind.get() is Projection.oblique.value:
        matrix = number.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [-math.cos(K), math.sin(K), 0, 0],
            [0, 0, 0, 1]
        ])

    # При перспективном проецировании пучок прямых проходят через центр проекции
    # В нашем случае это точка C, расположенная в третьей строке матрицы, так как проецируем на ось Z
    else:
        matrix = number.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, C],
            [0, 0, 0, 1]
        ])

    # Обновим объект в зависимости от выбранного типа проецирования
    result = []

    for node in nodes:
        new = number.matmul(node, matrix)
        # Когда осуществляется переход в перспективное проецирование, то изменяется ось h
        # При произведении матрицы проецирования и текущих координат объекта
        # То есть, получаем координату вида (x y 0 1 - z/C)
        # Приведём координаты к виду (x / (1 - z/c) y / (1 - z/c) 0 1)
        # Важно, что при переходе к косоугольному проецированию координаты возвращают вид (x y z 1)
        new = new / (new[3])
        result.append(new)

    # Возвращаем координаты объекта, исходя из текущего аффинного преобразования, в данном случае проецирования
    return number.array(result)


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


# Вращение объекта
# @param body непосредственно объект
# @param vector вектор поворота объекта
# @param axis выбранная ось
def rotate(body, vector, axis):
    # Прибавляем вектор поворота к текущим значениям углов осей объекта
    body.set_angles((body.get_angles() + vector) % 360)

    # Переводим значения углов осей в радианы
    angles = [element * (math.pi / 180) for element in vector]

    # Матрица вращения вокруг оси абсцисс на значение угла angles[0]
    x = number.array([
        [1, 0, 0, 0],
        [0, math.cos(angles[0]), math.sin(angles[0]), 0],
        [0, -math.sin(angles[0]), math.cos(angles[0]), 0],
        [0, 0, 0, 1]
    ])

    # Матрица вращения вокруг оси ординат на значение угла angles[1]
    y = number.array([
        [math.cos(angles[1]), 0, -math.sin(angles[1]), 0],
        [0, 1, 0, 0],
        [math.sin(angles[1]), 0, math.cos(angles[1]), 0],
        [0, 0, 0, 1]
    ])

    # Матрица вращения вокруг оси аппликат на значение угла angles[2]
    z = number.array([
        [math.cos(angles[2]), math.sin(angles[2]), 0, 0],
        [-math.sin(angles[2]), math.cos(angles[2]), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Выбор одной из матриц вращения в зависимости от выбранной оси
    if axis is Axis.x:
        matrix = x
    elif axis is Axis.y:
        matrix = y
    else:
        matrix = z

    # Обновляем координаты объекта, исходя из текущего аффинного преобразования
    # В данном случае — вращение объекта
    update(body, matrix)


# Масштабирование объекта
# @param body непосредственно объект
# @param vector: вектор масштабирования
def scale(body, vector):
    # Прибавляем вектор масштабирования к текущим параметрам размера объекта
    size = body.get_size() + vector
    body.set_size(size)

    # Матрица масштабирования, где диагональ содержит коэффициенты растяжения/сжатия
    matrix = number.array([
        [1 + vector[0], 0, 0, 0],
        [0, 1 + vector[1], 0, 0],
        [0, 0, 1 + vector[2], 0],
        [0, 0, 0, 1]
    ])

    # Обновляем координаты объекта, исходя из текущего аффинного преобразования
    # В данном случае — масштабирование объекта
    update(body, matrix)
