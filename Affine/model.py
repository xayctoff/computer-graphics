import numpy as number

from defs import *


#   Чтение данных из файла
#   @param name: имя файла
#   return array: список с данными (список координат точек или рёбер)
def read_from_file(name):
    array = []
    with open(name) as file:
        for line in file:
            string = [int(i) for i in line.rstrip().split(' ')]
            array.append(string)
    return number.array(array)


#   Класс, определяющий объект, который будет подвержен афинным преобразованиям
class Object:
    #   Конструктор объекта
    #   @param self: непосредственно объект
    def __init__(self):
        #   Считывание из файла списка координат точек объекта и списка рёбер, соединяющих эти точки
        self.nodes = read_from_file('nodes.txt')  # Координаты точек
        self.edges = read_from_file('edges.txt')  # Рёбра

        #   Координаты объекта
        self.coordinates = number.array([0, 0, 0, 1])
        #   Значения углов осей объекта
        self.angles = number.array([0, 0, 0, 0])
        #   Размер объекта
        self.size = number.array([1.0, 1.0, 1.0, 1.0])

        #   Переопределение центра объекта
        self.centring()

    #   Обновление объекта
    #   @param self: непосредственно объект
    #   @param matrix: матрица афинного преобразования
    #   @param nodes: координаты точек объекта
    def update(self, matrix):
        #   По сути, список обновлённых координат объекта
        result = []

        #   Для обновления координат объекта применим произведение матриц
        for node in self.nodes:
            result.append(number.matmul(node, matrix))

        self.nodes = result

    #   Перенос объекта
    #   @param self: непосредственно объект
    #   @param vector: вектор переноса
    def shift(self, vector):
        #   Прибавляем вектор переноса к текущим координатам объекта
        self.coordinates += vector
        #   Матрица переноса, где четвёртая строка содержит координаты перемещения объекта (x y z 1)
        matrix = number.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [vector[0], vector[1], vector[2], 1]
        ])

        #   Обновляем координаты объекта, исходя из текущего афинного преобразования
        #   В данном случае применили перемещение объекта
        self.update(matrix)

    #   Вращение объекта
    #   @param self: непосредственно объект
    #   @param vector: вектор поворота объекта
    #   @param axis: выбранная ось
    def rotate(self, vector, axis):
        #   Прибавляем вектор поворота к текущим значениям углов осей объекта
        self.angles = (self.angles + vector) % 360
        #   Значения углов осей в радианах
        angles = [element * RADIANS for element in vector]

        #   Матрица вращения вокруг оси абсцисс на угол angles[0]
        x = number.array([
            [1, 0, 0, 0],
            [0, math.cos(angles[0]), math.sin(angles[0]), 0],
            [0, -math.sin(angles[0]), math.cos(angles[0]), 0],
            [0, 0, 0, 1]
        ])

        #   Матрица вращения вокруг оси ординат на угол angles[1]
        y = number.array([
            [math.cos(angles[1]), 0, -math.sin(angles[1]), 0],
            [0, 1, 0, 0],
            [math.sin(angles[1]), 0, math.cos(angles[1]), 0],
            [0, 0, 0, 1]
        ])

        #   Матрица вращения вокруг оси аппликат на угол angles[2]
        z = number.array([
            [math.cos(angles[2]), math.sin(angles[2]), 0, 0],
            [-math.sin(angles[2]), math.cos(angles[2]), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        #   Выбор одной из матриц вращения в зависимости от выбранной оси
        matrix = x if axis == 'X' else y if axis == 'Y' else z

        #   Обновляем координаты объекта, исходя из текущего афинного преобразования
        #   В данном случае применили вращение объекта
        self.update(matrix)

    #   Растяжение-сжатие объекта
    #   @param self: непосредственно объект
    #   @param vector: вектор растяжения-сжатия
    def scale(self, vector):
        #   Прибавляем вектор растяжения-сжатия к текущим параметрам размера объекта
        self.size += vector
        #   Матрица растяжения-сжатия, где диагональ матрицы содержит коэффициенты растяжения-сжатия
        matrix = number.array([
            [1 + vector[0], 0, 0, 0],
            [0, 1 + vector[1], 0, 0],
            [0, 0, 1 + vector[2], 0],
            [0, 0, 0, 1]
        ])

        #   Обновляем координаты объекта, исходя из текущего афинного преобразования
        #   В данном случае применили масштабирование объекта
        self.update(matrix)

    #   Отражение объекта
    #   @param self: непосредственно объект
    #   @param axis: ось, относительно которой происходит отражение
    def mirror(self, axis):
        #   Матрица отражения относительно плоскости yz
        x = number.array([
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        #   Матрица отражения относительно плоскости хz
        y = number.array([
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        #   Матрица отражения относительно плоскости ху
        z = number.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ])

        #   Выбор одной из матриц вращения в зависимости от выбранной оси
        matrix = x if axis == 'X' else y if axis == 'Y' else z

        #   Обновляем координаты объекта, исходя из текущего афинного преобразования
        #   В данном случае применяем отражение объекта относительно плоскости
        self.update(matrix)

    #   Переопределение центра объекта с левого нижнего к его фактическому центру
    #   @param self: непосредственно объект
    def centring(self):
        nodes = self.nodes.tolist()
        #   Рассчитаем центр объекта
        axle = lambda axis: (min([node[axis] for node in nodes]) + max([node[axis] for node in nodes])) / 2
        center = [axle(0), axle(1), axle(2), 0]

        self.nodes = self.nodes - center
