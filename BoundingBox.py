import numpy


class BoundingBox:
    def __init__(self, points):
        self.points = points

    def getMinpoint(self):
        """ Returns current min point from the bounding box """

        return numpy.amin(self.points, 0)

    def getMaxpoint(self):
        """ Returns current max point from the bounding box """

        return numpy.amax(self.points, 0)

    def moveToCenter(self):
        """ Moves center of bounding box to origin (0, 0, 0) """

        center = self.calculateCenter()
        self.points = self.points - center

    def calculate_center_coordinate(self, axis):
        """ Calculates vector to 0 for specific axis """

        min_point = self.getMinpoint()
        max_point = self.getMaxpoint()

        local_center_point = (max_point[axis] - min_point[axis]) / 2

        return min_point[axis] + local_center_point

    def scaleToBoundingBox(self):
        """ Scales all points from -1 to 1 || Scalingfactor"""

        max_point = self.getMaxpoint()
        max_x = max_point[0]
        max_y = max_point[1]
        divisor = max(max_x, max_y)  # should try to consider negative numbers later maybe
        self.points = self.points / divisor

    def calculateCenter(self):
        """ Builds the vector to the center """

        return numpy.array(
            [
                self.calculate_center_coordinate(0),# center of x axis
                self.calculate_center_coordinate(1),# center of y axis
                self.calculate_center_coordinate(2),# center of z axis
            ]
        )

    def move_up(self):
        """ For Shadow"""
        max_point = self.getMaxpoint()
        min_point = self.getMinpoint()
        max_y = max_point[1]
        min_y = min_point[1]
        delta_y = (max_y - min_y) / 2
        for p in self.points:
            p[1] = p[1] + delta_y
