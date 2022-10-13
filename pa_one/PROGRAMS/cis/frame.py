import numpy as np


class Frame:
    """
    Class used to represent Frames

    ...

    Attributes
    ________
    R : np.ndarray
        A representation of the rotation matrix, 3x3
    p : np.ndarray
        A representation of the translation vector, 3x1
    """

    def __init__(self, R, p):
        """
        Parameters
        _________
        self : Frame
            Frame object
        R : np.ndarray
            Rotation matrix
        p : np.ndarray
            Translation vector
        """
        self.R = R
        self.p = p

    def compose_frame(self, other_frame):
        """Method for computing a frame composition

        Parameters
        _________
        self : Frame
            Frame object
        other_frame : Frame
            The frame to be composed with

        Returns
        _________
        Frame
            The composed frame
        """
        mat = np.dot(self.R, other_frame.R)
        vec = np.dot(self.R, other_frame.p) + self.p
        return Frame(mat, vec)

    def compose_transform(self, points):
        """Method for computing a frame transform

        Parameters
        _________
        self : Frame
            Frame object
        points : np.ndarray
            The points to be transformed

        Returns
        _________
        t_points : np.ndarray
            The transformed points
        """
        t_points = np.dot(self.R, points) + self.p
        return t_points

    def invert(self):
        """Method for computing the inverse of a frame

        Parameters
        _________
        self : Frame
            Frame object

        Returns
        _________
        Frame
            The inverse of the Frame
        """
        new_r = np.linalg.inv(self.R)
        new_p = np.dot(-1 * new_r, self.p)
        return Frame(new_r, new_p)
