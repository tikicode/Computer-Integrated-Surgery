import numpy as np
from frame import Frame


class PointSet:
    """
    Class used to represent point clouds

    ...

    Attributes
    ________
    points : np.ndarray
        Points in the point cloud separated as columns
    """

    def __init__(self, points):
        """
        Parameters
        _________
        self : PointSet
            PointSet object
        points : np.ndarray
            Points in the point cloud separated as columns
        """
        self.points = points

    '''
    Non-Iterative registration algorithm from Arun, Huang, and Blostein
    parameters: two point sets
    return: frame for the transformation
    '''


def registration(A, B):
    """Method for computing a point cloud registration

    Parameters
    _________
    A : PointSet
        One point cloud
    B : PointSet
        The point cloud to be mapped to

    Returns
    _________
    Frame
        The point cloud transformation for the two point cloud inputs
    """
    a_mean = np.mean(A.points, axis=1, keepdims=True)
    b_mean = np.mean(B.points, axis=1, keepdims=True)
    centered_a = A.points - a_mean
    centered_b = B.points - b_mean

    H = np.dot(centered_a, centered_b.transpose())
    u, s, vt = np.linalg.svd(H)

    u = u.transpose()
    vt = vt.transpose()

    comp_size = vt.shape[0]
    reflection_comp = np.eye(comp_size)
    reflection_comp[comp_size - 1][comp_size - 1] = np.linalg.det(np.dot(vt, u))

    R = np.dot(vt, np.dot(reflection_comp, u))
    p = b_mean - np.dot(R, a_mean)

    return Frame(R, p)
