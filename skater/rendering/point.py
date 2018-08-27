class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(x:{}, y:{})".format(self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    def __add__(self, other):
        x, y = (other.x, other.y) if isinstance(other, Point) else other
        return Point(self.x + x, self.y + y)

    def within(self, x_boundaries, y_boundaries):
        return self.x >= x_boundaries[0] and self.x <= x_boundaries[1] \
            and self.y >= y_boundaries[0] and self.y <= y_boundaries[1]