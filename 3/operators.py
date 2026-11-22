from dataclasses import dataclass
from functools import total_ordering
from math import hypot


@dataclass
class ComplexNumber:
    real: float
    imaginary: float

    def __add__(self, other):
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return ComplexNumber(self.real + other.real, self.imaginary + other.imaginary)

    def __sub__(self, other):
        if not isinstance(other, ComplexNumber):
            return NotImplemented
        return ComplexNumber(self.real - other.real, self.imaginary - other.imaginary)


@dataclass
class Person:
    name: str
    age: int
    gender: str

    def __gt__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age


@dataclass
class Vector:
    x: float
    y: float
    z: float

    def __mul__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z


@dataclass(order=True)
class Circle:
    radius: float


@total_ordering
@dataclass(eq=False)
class Point:
    x: float
    y: float

    def distance(self):
        return hypot(self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.distance() == other.distance()

    def __lt__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.distance() < other.distance()


class Matrix:
    def __init__(self, rows):
        self.rows = tuple(tuple(row) for row in rows)
        if not self.rows or not self.rows[0]:
            raise ValueError("A matrix needs at least one row and column")
        if any(len(row) != len(self.rows[0]) for row in self.rows):
            raise ValueError("Matrix rows must have equal lengths")

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if len(self.rows[0]) != len(other.rows):
            raise ValueError("Left column count must equal right row count")

        columns = list(zip(*other.rows))
        return Matrix([
            [sum(a * b for a, b in zip(row, column)) for column in columns]
            for row in self.rows
        ])
