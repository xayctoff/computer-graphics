import numpy as number

from source.main.util.reader import read_from_file


class Body:
    def __init__(self):
        #   Считывание из файла списка координат точек объекта и списка рёбер, соединяющих эти точки
        self.nodes = read_from_file('nodes.txt')
        self.edges = read_from_file('edges.txt')

        #   Координаты объекта
        self.coordinates = number.array([0, 0, 0, 1])
        #   Значения углов осей объекта
        self.angles = number.array([0, 0, 0, 0])
        #   Размер объекта
        self.size = number.array([1.0, 1.0, 1.0, 1.0])
