"""Обязательное домашнее задание:
При помощи ООП спроектировать и реализовать геометрический калькулятор
для вычислений, производимых над фигурами. Калькулятор должен поддерживать
вычисления для плоских и объемных фигур.
Плоские фигуры: круг, квадрат, прямоугольник, треугольник, трапеция, ромб.
Объемные фигуры: сфера, куб, параллелепипед, пирамида, цилиндр, конус.
Реализовать как минимум один общий метод вычисления для всех фигур и как минимум
один специфичный для определенных фигур. Например, площадь – общий метод для всех
фигур, медиана – специфичный метод для ряда фигур.
Необходимо: реализовать графический интерфейс для возможностей взаимодействия
пользователя с программой и визуализации фигур (с учетом введенных параметров фигуры).

При реализации использовать все виды методов: статический, метод класса и экземпляра.
"""
import matplotlib.pyplot as plt
from math import pi
from typing import Union

from matplotlib import patches


class Drawer2D:
    def draw(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='datalim')
        ax.plot()  # Causes an autoscale update.
        plt.grid()
        return fig, ax


class Circle(Drawer2D):
    def __init__(self, radius: Union[int, float]):
        self.radius = radius

    def area(self) -> Union[int, float]:
        return pi * self.radius ** 2

    def draw(self):
        fig, ax = super().draw()

        circle = plt.Circle((self.radius, self.radius), self.radius, edgecolor='r', facecolor='g')
        ax.add_patch(circle)

        plt.show()


class Square(Drawer2D):
    def __init__(self, side: Union[int, float]):
        self.side = side

    def area(self) -> Union[int, float]:
        return self.side ** 2

    def draw(self):
        fig, ax = super().draw()

        rect = patches.Rectangle((0, 0), self.side, self.side, linewidth=1, edgecolor='r', facecolor='g')
        ax.add_patch(rect)
        plt.show()


class Rectangle(Drawer2D):
    def __init__(self, side_a: Union[int, float], side_b: Union[int, float]):
        self.width = min(side_a, side_b)
        self.length = max(side_a, side_b)

    def area(self) -> Union[int, float]:
        return self.width * self.length

    def draw(self):
        fix, ax = super().draw()
        rect = patches.Rectangle((0, 0), self.width, self.length, linewidth=1, edgecolor='r', facecolor='g')
        ax.add_patch(rect)
        plt.show()


class Triangle:
    def __init__(
        self,
        side_a: Union[int, float],
        side_b: Union[int, float],
        side_c: Union[int, float],
    ):
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self) -> Union[int, float]:
        p = sum((self.side_a, self.side_b, self.side_c)) * 0.5
        return (p * (p - self.side_a) * (p - self.side_b) * (p - self.side_c)) ** 0.5

    def is_isosceles(self) -> bool:
        return any(
            (
                self.side_a == self.side_b,
                self.side_a == self.side_c,
                self.side_b == self.side_c,
            )
        )

    def is_equilateral(self) -> bool:
        return self.side_a == self.side_b == self.side_c


class Trapezoid:
    def __init__(
        self,
        base_a: Union[int, float],
        base_b: Union[int, float],
        leg_a: Union[int, float],
        leg_b: Union[int, float],
        height: Union[int, float],
    ):
        self.base_a = base_a
        self.base_b = base_b
        self.leg_a = leg_a
        self.leg_b = leg_b
        self.height = height

    def area(self) -> Union[int, float]:
        return (self.base_a + self.base_b) * self.height * 0.5


class Rhombus:
    def __init__(self, side: Union[int, float], diagonal: Union[int, float]):
        self.side = side
        self.diagonal = diagonal

    def area(self) -> Union[int, float]:
        return self.diagonal * (self.side ** 2 - (self.diagonal / 2) ** 2) ** 0.5


class Sphere:
    def __init__(self, radius: Union[int, float]):
        self.radius = radius

    def area(self) -> Union[int, float]:
        return 4 * pi * self.radius ** 2

    def volume(self) -> Union[int, float]:
        return 4 / 3 * pi * self.radius ** 3


class Parallelepiped:
    ...


class Pyramid:
    ...


class Cylinder:
    def __init__(
        self,
        radius: Union[int, float],
        height: Union[int, float],
        is_right: bool = True,
    ):
        self.radius = radius
        self.height = height
        self.is_right = is_right

    def area(self):
        if not self.is_right:
            raise NotImplementedError
        return 2 * pi * self.radius * (self.radius * self.height)

    def volume(self):
        if not self.is_right:
            raise NotImplementedError
        return pi * self.radius ** 2 * self.height


class Cone:
    def __init__(
        self,
        radius: Union[int, float],
        height: Union[int, float],
        is_right: bool = True,
        is_circular: bool = True,
    ):
        self.radius = radius
        self.height = height
        self.is_right = is_right
        self.is_circular = is_circular

    def volume(self):
        if not (self.is_circular and self.is_right):
            raise NotImplementedError
        return pi * self.radius ** 2 * self.height


c = Circle(1)
c.draw()
s = Square(2)
s.draw()
r = Rectangle(5, 2)
r.draw()
