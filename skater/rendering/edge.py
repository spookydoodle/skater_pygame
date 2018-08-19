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
