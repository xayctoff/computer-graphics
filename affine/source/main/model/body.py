import numpy as number
import os

from source.main.util.reader import read_from_file


# Объект, подлежащий изменению через аффинные преобразования
class Body:
    def __init__(self):
        #   Считывание из файла списка координат точек объекта и списка рёбер, соединяющих данные точки
        self._nodes = read_from_file(os.path.relpath("../source/resources/nodes.txt", os.path.dirname(__file__)))
        self._edges = read_from_file(os.path.relpath("../source/resources/edges.txt", os.path.dirname(__file__)))

        #   Координаты объекта
        self._coordinates = number.array([0, 0, 0, 1])
        #   Значения углов осей объекта
        self._angles = number.array([0, 0, 0, 0])
        #   Размер объекта
        self._size = number.array([1.0, 1.0, 1.0, 1.0])

    def get_nodes(self):
        return self._nodes

    def set_nodes(self, nodes):
        self._nodes = nodes

    def get_edges(self):
        return self._edges

    def set_edges(self, edges):
        self._edges = edges

    def get_coordinates(self):
        return self._coordinates

    def set_coordinates(self, coordinates):
        self._coordinates = coordinates

    def get_angles(self):
        return self._angles

    def set_angles(self, angles):
        self._angles = angles

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size
