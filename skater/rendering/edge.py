from math import inf

class Edge:
    """
    A 1 point wide line connectng two vertices.
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return "Edge: {}, {}".format(self.start, self.end)

    def __eq__(self, other):
        return isinstance(other, Edge) and (self.start, self.end) == (other.start, other.end)

    def get_equation_params(self):
        """
        Extracts the linear equation parameters: f = ax + b, x = <x_0, x_1>, y = <y_0, y_1>

        A line segment is a linear function with boundaries. The function may be used
        to compute if a point lies on the line
        """
        # order points by their position on the x axis
        left, right = sorted(
            [self.start, self.end],
            key = lambda p: p.x)

        # slope
        if (right.x == left.x):
            # infinite slope case
            a = inf
        else:
            a = (right.y - left.y) / (right.x - left.x)

        # offset
        b = left.y - a * left.x

        # boundaries (sorted)
        x_boundaries = (left.x, right.x)  # left and right are already sorted by x
        y_boundaries = (min(left.y, right.y), max(left.y, right.y))  # put the smaller value first, bigger second

        return a, b, x_boundaries, y_boundaries

    def contains(self, point):
        """
        Checks if a point lies on the line
        """
        a, b, x_boundaries, y_boundaries = self.get_equation_params()

        if point.within(x_boundaries, y_boundaries):
            # calculate the linear function value at point.x: y = ax + b
            fun_value = a * point.x + b
            difference = point.y - fun_value

            # allow some margin (we may be dealing with floating point values)
            return abs(difference) <= 0.5
        else:
            return False

    def matching_x(self, y):
        """
        Given a fixed `y`, returns an `x` value that would make a point lie on the edge

        Depends on the fact that Edges are linear functions.

        TODO: a LinearFunction class

        y = ax + b ->
            y = ax + b ->
            x = (y - b) / a
        """
        a, b, x_boundaries, y_boundaries = self.get_equation_params()
        
        if not(y_boundaries[0] <= y <= y_boundaries[1]):
            # y is outside of the edge boundaries -> `self` will never contain the point
            return inf
        elif a == inf:
            # horizontal line -> x has to be equal to the line's x
            return x_boundaries[0]
        else:
            return (y - b) // a

    def matching_y(self, x):
        """
        Given a fixed `x`, returns a `y` value that would make a point lie on the edge

        Depends on the fact that Edges are linear functions.

        TODO: a LinearFunction class

        y = ax + b
        """
        a, b, x_boundaries, y_boundaries = self.get_equation_params()
        
        if not(x_boundaries[0] <= x <= x_boundaries[1]):
            return inf
        elif a == inf:
            # a is a horizontal line -> any y will do
            return x
        else:
            return a * x + b

    def distance_x(self, point):
        return self.matching_x(point.y) - point.x

    def distance_y(self, point):
        return self.matching_y(point.x) - point.y