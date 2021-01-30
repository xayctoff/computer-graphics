import numpy as number


#   Чтение данных из файла
#   @param name имя файла
#   @return список с выгруженными данными
def read_from_file(name):
    array = []

    with open(name) as file:
        for line in file:
            string = [int(i) for i in line.rstrip().split(' ')]
            array.append(string)

    return number.array(array)
