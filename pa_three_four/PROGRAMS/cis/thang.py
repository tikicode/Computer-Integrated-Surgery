import numpy as np
from .frame import Frame
from .icp import find_closest_point_triangle as cpt


class Thang:
    """Class used to represent triangles in 3D space

    ...
    Attributes
    ________
    corners : np.ndarray
        A representation of the corners of the triangle, 3x3
    """

    def __init__(self, triangle: np.ndarray):
        """

        Parameters
        _________
        self : Thang
            Thang object
        triangle : np.ndarray
            A representation of the corners of the triangle, 3x3
        """
        self.corners = triangle

    def sort_point(self):
        """Method for sorting the points of the triangle

        Parameters
        _________
        self : Thang
            Thang object

        Returns
        _________
        np.ndarray
            One corner of the triangle
        """
        return self.corners[0]

    def closest_point_to(self, point: np.ndarray):
        """Method for finding the closest point on the triangle to a given point

        Parameters
        _________
        self : Thang
            Thang object
        point : np.ndarray
            The point to find the closest point on the triangle to

        Returns
        _________
        np.ndarray
            The closest point on the triangle to the given point
        """
        return cpt(self.corners[np.array([0, 1, 2])], point)

    def enlarge_bounds(self, frame: Frame, LB: np.ndarray, UB: np.ndarray):
        """Method for finding the bounding box of the triangle

        Parameters
        _________
        self : Thang
            Thang object
        frame : Frame
            The frame to be composed with
        LB : np.ndarray
            The lower bound of the bounding box
        UB : np.ndarray
            The upper bound of the bounding box

        Returns
        _________
        LB : np.ndarray
            The lower bound of the bounding box
        UB : np.ndarray
            The upper bound of the bounding box
        """
        fic = frame.invert().compose_transform(self.corners)
        for i in range(3):
            for j in range(3):
                LB[0][j] = min(LB[0][j], fic[i][j])
                UB[0][j] = max(UB[0][j], fic[i][j])
        return LB, UB

    def bounding_box(self, frame: Frame):
        """Method for finding the bounding box of the triangle

        Parameters
        _________
        self : Thang
            Thang object
        frame : Frame
            The frame to be composed with

        Returns
        _________
        LB : np.ndarray
            The lower bound of the bounding box
        UB : np.ndarray
            The upper bound of the bounding box
        """
        return self.enlarge_bounds(frame, np.array([-np.inf, -np.inf, -np.inf]), np.array([np.inf, np.inf, np.inf]))

    def may_be_in_bounds(self, frame: Frame, LB: np.ndarray, UB: np.ndarray):
        """Method for checking if the triangle is in the bounding box

        Parameters
        _________
        self : Thang
            Thang object
        frame : Frame
            The frame to be composed with
        LB : np.ndarray
            The lower bound of the bounding box
        UB : np.ndarray
            The upper bound of the bounding box

        Returns
        _________
        bool
            True if the triangle is in the bounding box, False otherwise
        """
        fic = frame.invert().compose_transform(self.corners)
        for i in range(3):
            for j in range(3):
                if LB[j] < fic[i][j] < UB[j]:
                    return False
        return True
