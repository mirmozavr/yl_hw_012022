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
from math import pi
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from matplotlib.patches import Polygon
import mpl_toolkits.mplot3d.art3d as art3d


class Figure:
    @classmethod
    def title(cls):
        return f"This is a {cls.__name__}"

    def perimeter(self):
        return NotImplementedError

    def get_area(self):
        return NotImplementedError

    def get_volume(self):
        return NotImplementedError

    def draw(self):
        return NotImplementedError


class Drawer3D:
    def draw(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        return fig, ax


class Drawer2D:
    def draw(self):
        fig, ax = plt.subplots()
        ax.set_aspect("equal", adjustable="datalim")
        ax.plot()  # Causes an autoscale update.
        plt.grid()
        return fig, ax


class Circle(Drawer2D, Figure):
    def __init__(self, radius: Union[int, float]):
        self.radius = radius

    def perimeter(self):
        return 2 * pi * self.radius

    def get_area(self) -> Union[int, float]:
        return pi * self.radius**2

    def draw(self):
        fig, ax = super().draw()

        circle = plt.Circle(
            (self.radius, self.radius), self.radius, edgecolor="r", facecolor="g"
        )
        ax.add_patch(circle)

        plt.show()


class Square(Drawer2D, Figure):
    def __init__(self, side: Union[int, float]):
        self.side = side

    def perimeter(self):
        return 4 * self.side

    def get_area(self) -> Union[int, float]:
        return self.side**2

    def draw(self):
        fig, ax = super().draw()

        poly = patches.Rectangle(
            (0, 0), self.side, self.side, linewidth=1, edgecolor="r", facecolor="g"
        )
        ax.add_patch(poly)
        plt.show()


class Rectangle(Drawer2D, Figure):
    def __init__(self, side_a: Union[int, float], side_b: Union[int, float]):
        self.width = min(side_a, side_b)
        self.length = max(side_a, side_b)

    def perimeter(self):
        return 2 * (self.width * self.length)

    def get_area(self) -> Union[int, float]:
        return self.width * self.length

    def draw(self):
        fix, ax = super().draw()
        poly = patches.Rectangle(
            (0, 0), self.width, self.length, linewidth=1, edgecolor="r", facecolor="g"
        )
        ax.add_patch(poly)
        plt.show()


class Triangle(Drawer2D, Figure):
    def __init__(
        self,
        coord_a,
        coord_b,
        coord_c,
    ):
        self.coord_a = coord_a
        self.coord_b = coord_b
        self.coord_c = coord_c
        self.side_ab = (
            abs((self.coord_a[0] - self.coord_b[0])) ** 2
            + abs((self.coord_a[1] - self.coord_b[1])) ** 2
        ) ** 0.5
        self.side_bc = (
            abs((self.coord_b[0] - self.coord_c[0])) ** 2
            + abs((self.coord_b[1] - self.coord_c[1])) ** 2
        ) ** 0.5
        self.side_ca = (
            abs((self.coord_c[0] - self.coord_a[0])) ** 2
            + abs((self.coord_c[1] - self.coord_a[1])) ** 2
        ) ** 0.5

    def perimeter(self):
        return self.side_ab + self.side_bc + self.side_ca

    def get_area(self) -> Union[int, float]:
        p = sum((self.side_ab, self.side_bc, self.side_ca)) * 0.5
        return (p * (p - self.side_ab) * (p - self.side_bc) * (p - self.side_ca)) ** 0.5

    def is_isosceles(self) -> bool:
        return any(
            (
                self.side_ab == self.side_bc,
                self.side_ab == self.side_ca,
                self.side_bc == self.side_ca,
            )
        )

    def is_equilateral(self) -> bool:
        return self.side_ab == self.side_bc == self.side_ca

    def draw(self):
        fix, ax = super().draw()
        poly = Polygon(
            [self.coord_a, self.coord_b, self.coord_c], edgecolor="r", facecolor="g"
        )
        poly.set_closed(True)
        ax.add_patch(poly)
        plt.show()


class Trapezoid(Drawer2D, Figure):
    def __init__(
        self,
        base_a: Union[int, float],
        base_b: Union[int, float],
        height: Union[int, float],
    ):
        self.base_a = base_a
        self.base_b = base_b
        self.height = height

    def get_area(self) -> Union[int, float]:
        return (self.base_a + self.base_b) * self.height * 0.5

    def draw(self):
        fix, ax = super().draw()
        poly = Polygon(
            [(0, 0), (self.base_a, 0), (self.base_b, self.height), (0, self.height)],
            edgecolor="r",
            facecolor="g",
        )
        poly.set_closed(True)
        ax.add_patch(poly)
        plt.show()


class Rhombus(Drawer2D, Figure):
    def __init__(self, side: Union[int, float], diagonal: Union[int, float]):
        if diagonal >= 2 * side:
            raise ValueError
        self.side = side
        self.diagonal = diagonal
        self.diagonal2 = (side**2 - (diagonal / 2) ** 2) ** 0.5 * 2
        print(self.side, self.diagonal, self.diagonal2)

    def perimeter(self):
        return 4 * self.side

    def get_area(self) -> Union[int, float]:
        return self.diagonal * (self.side**2 - (self.diagonal / 2) ** 2) ** 0.5

    def draw(self):
        fix, ax = super().draw()
        poly = Polygon(
            [
                (self.diagonal / 2, 0),
                (self.diagonal, self.diagonal2 / 2),
                (self.diagonal / 2, self.diagonal2),
                (0, self.diagonal2 / 2),
            ],
            edgecolor="r",
            facecolor="g",
        )
        poly.set_closed(True)
        ax.add_patch(poly)
        plt.show()


class Sphere(Drawer3D, Figure):
    def __init__(self, radius: Union[int, float]):
        self.radius = radius

    def get_area(self) -> Union[int, float]:
        return 4 * pi * self.radius**2

    def get_volume(self) -> Union[int, float]:
        return 4 / 3 * pi * self.radius**3

    def draw(self):
        fig, ax = super().draw()

        # Make data
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = self.radius * np.outer(np.cos(u), np.sin(v))
        y = self.radius * np.outer(np.sin(u), np.sin(v))
        z = self.radius * np.outer(np.ones(np.size(u)), np.cos(v))

        # Plot the surface
        ax.plot_surface(x, y, z)

        plt.show()


class Parallelepiped:
    ...


class Pyramid:
    ...


class Cylinder(Drawer3D, Figure):
    def __init__(
        self,
        radius: Union[int, float],
        height: Union[int, float],
        is_right: bool = True,
    ):
        self.radius = radius
        self.height = height
        self.is_right = is_right

    def get_area(self):
        if not self.is_right:
            raise NotImplementedError
        return 2 * pi * self.radius * (self.radius + self.height)

    def get_volume(self):
        if not self.is_right:
            raise NotImplementedError
        return pi * self.radius**2 * self.height

    def draw(self):
        def cylinder_mesh(center_x, center_y, radius, height_z):
            z = np.linspace(0, height_z, 50)
            theta = np.linspace(0, 2 * np.pi, 50)
            theta_grid, z_grid = np.meshgrid(theta, z)
            x_grid = radius * np.cos(theta_grid) + center_x
            y_grid = radius * np.sin(theta_grid) + center_y
            return x_grid, y_grid, z_grid

        fig, ax = super().draw()

        x, y, z = cylinder_mesh(self.radius/2, self.radius/2, self.radius, self.height)
        ax.plot_surface(x, y, z, alpha=1, color='b')

        floor = plt.Circle((self.radius/2, self.radius/2), self.radius, color='b')
        ax.add_patch(floor)
        art3d.pathpatch_2d_to_3d(floor, z=0, zdir="z")

        ceiling = plt.Circle((self.radius/2, self.radius/2), self.radius, color='b')
        ax.add_patch(ceiling)
        art3d.pathpatch_2d_to_3d(ceiling, z=self.height, zdir="z")

        plt.show()


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

    def get_volume(self):
        if not (self.is_circular and self.is_right):
            raise NotImplementedError
        return pi * self.radius**2 * self.height
