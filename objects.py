from math import sin, cos, atan2

class DimensionException(Exception):
    pass

class Vector:
    def __init__(self, *args):
        if args == ():
            self.value = None
        elif type(args[0]) is list and len(args) == 1:
            self.value = args[0]
        elif type(args[0]) is Vector:
            self.value = args[0].value
        elif type(args[0]) is tuple:
            self.value = list(args[0])
        else:
            self.value = list(args)

    def __repr__(self):
        return f'Vector({self.value})'

    def __add__(self, other):
        if type(other) is Vector:
            if len(self.value) != len(other.value):
                raise DimensionException(f"Vector({self.value}) is {len(self.value)}-dimensional, Vector({other.value}) is {len(other)}-dimensional")
            for i in range(len(self)):
                self.value[i] += other.value[i]
            return Vector(self.value)
        else:
            raise TypeError(f"can only concatenate Vector (not '{type(other)}') to Vector")

    def __sub__(self, other):
        if type(other) is Vector:
            if len(self.value) != len(other.value):
                raise DimensionException(
                    f"Vector({self.value}) is {len(self.value)}-dimensional, Vector({other.value}) is {len(other)}-dimensional")
            for i in range(len(self)):
                self.value[i] -= other.value[i]
            return Vector(self.value)
        else:
            raise TypeError(f"can only subtract Vector (not '{type(other)}') from Vector")

    def __mul__(self, other):
        if type(other) is int or type(other) is float:
            for i in range(len(self.value)):
                self.value[i] *= other
            return Vector(self.value)
        else:
            raise TypeError(f"can only multiply int or float (not '{type(other)}') to Vector")

    def __truediv__(self, other):
        if type(other) is int or type(other) is float:
            for i in range(len(self.value)):
                self.value[i] /= other
            return Vector(self.value)
        else:
            raise TypeError(f"can only multiply int or float (not '{type(other)}') to Vector")

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]

    @staticmethod
    def zeros(n):
        return Vector([0 for _ in range(n)])

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]

    @property
    def r(self):
        dist2 = 0
        for x in self.value:
            dist2 += x**2
        return dist2**(1/2)

    @property
    def hat(self):
        return Vector([x/self.r for x in self.value])

    @property
    def theta(self):
        return atan2(self.y, self.x)

    @property
    def int(self):
        return Vector(*[int(i) for i in self.value])

    def set_r_theta(self, r=None, theta=None):
        if r is None and theta is None:
            raise ValueError("'r' and 'theta' cannot be None")
        elif r is None:
            r = self.r
        elif theta is None:
            theta = self.theta

        self.value = [r * cos(theta), r * sin(theta)]
