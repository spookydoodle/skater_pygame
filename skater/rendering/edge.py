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

    def vertices(self):
        return [self.start, self.end]

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

    def distance_x(self, point):
        """
        Given a `point`, returns a shortest distance in the x axis from `self`

        Depends on the fact that Edges are linear functions.

        TODO: a LinearFunction class

        y = ax + b ->
            y = ax + b ->
            x = (y - b) / a
        """
        # Check if point is already on the edge
        if self.contains(point):
            return 0

        a, b, x_boundaries, y_boundaries = self.get_equation_params()
        
        if not(y_boundaries[0] <= point.y <= y_boundaries[1]):
            # y is outside of the edge boundaries -> `self` will never contain the point
            return inf

        if a == inf:
            # vertical line -> x has to be equal to the line's x
            matching_x = x_boundaries[0]
        
        elif a == 0:
            # horizontal line -> any y will do -> return distance to the nearest point
            # a is a horizontal line ->
            assert(y_boundaries[0] == y_boundaries[1])
            # ... and `point` lies within the `y_boundaries` ->
            assert(point.y == y_boundaries[0])

            # `point` is aligned with the line -> return the nearest edge vertex
            nearest_vertex = min(
                self.vertices(),
                key=lambda v: abs(v.x - point.x))
            matching_x = nearest_vertex.x
        
        else:
            matching_x = (point.y - b) // a
        
        return matching_x - point.x

    def distance_y(self, point):
        if self.contains(point):
            return 0

        a, b, x_boundaries, y_boundaries = self.get_equation_params()
        
        if not(x_boundaries[0] <= point.x <= x_boundaries[1]):
            return inf

        if a == inf:
            assert(x_boundaries[0] == x_boundaries[1])
            assert(point.x == x_boundaries[0])

            distances = [vertex.y - point.y for vertex in self.vertices()]
            nearest_vertex = min(
                self.vertices(),
                key=lambda v: abs(v.y - point.y))
            matching_y = nearest_vertex.y
        
        elif a == 0:
            matching_y = y_boundaries[0]
        
        else:
            matching_y = a * point.x + b
        
        return matching_y - point.y
