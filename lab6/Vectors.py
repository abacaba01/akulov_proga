import numpy as np


class Vector():

    '''
    Класс векторов
    задается по 3 его кординатам, выдает вектор как 3 его координаты
    умножение на константу - *
    сложжение/вычитание - +/-
    вектороное умножение @
    скалярное умножение Vector.scal
    '''

    def __init__(self, a, b, c):
        self.x = a
        self.y = b
        self.z = c

    def __str__(self):
        return "(" + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k, self.z * k)

    def norm(self):
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __matmul__(self, other):
        return Vector(self.y * other.z - self.z * other.y, - self.x * other.z + self.z * other.x,
                   self.x * other.y - self.y * other.x)

    def scal(self, other):
        return (self.x * other.x + self.y * other.y + self.z * other.z)
