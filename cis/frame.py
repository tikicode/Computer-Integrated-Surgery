import numpy as np


class Frame:

    """
    Constructor to create a Frame object which has Rotation R and translation p
    """
    def __init__(self, R, p):
        self.R = R
        self.p = p

    '''Method to perform a composition between two frames
    parameters: two frames
    returns: frame of F1 @ F2
    '''
    def compose_frame(self, other_frame):
        mat = np.dot(self.R, other_frame.R)
        vec = np.dot(self.R, other_frame.p) + other_frame.p
        return Frame(mat, vec)

    '''Method to perform a Frame transformation
    parameters: frame and a vector/pointset
    returns: new vector/pointset after transformation of the original vector/pointset
    '''
    def compose_transform(self, points):
        print(points.shape)
        t_points = np.dot(self.R, points) + self.p
        return t_points

    '''Method to calculate the inverse of a Frame'''
    def invert(self):
        new_r = np.linalg.inv(self.R)
        new_p = np.dot(-1 * new_r, self.p)
        return Frame(new_r, new_r)
