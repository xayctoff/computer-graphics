import numpy as number


#   Чтение данных из файла
#   @param path путь к файлу
#   @return список с выгруженными данными
def read_from_file(path):
    array = []

    with open(path) as file:
        for line in file:
            string = [int(i) for i in line.rstrip().split(' ')]
            array.append(string)

    return number.array(array)
