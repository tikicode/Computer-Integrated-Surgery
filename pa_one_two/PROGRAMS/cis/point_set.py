import numpy as np
from .frame import Frame


class PointCloud:
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
    #Find the mean for A and B and then center them
    a_mean = np.mean(A, axis=0)
    b_mean = np.mean(B, axis=0)
    centered_a = A - a_mean
    centered_b = B - b_mean

    #compute Matrix H and use it for Singular Value Decomposition
    H = np.dot(centered_a.T, centered_b)
    u, s, vt = np.linalg.svd(H)

    #prepare these results of SVD, u and v, to find the
    #transformation matrix done on line 71
    u = u.T
    vt = vt.T
    #validate result and account for any potential issues by checking the determinant
    comp_size = vt.shape[0]
    reflection_comp = np.eye(comp_size)
    reflection_comp[comp_size - 1][comp_size - 1] = np.linalg.det(np.dot(vt, u))
    #find the transformation matrix R and the corresponding translation vector
    R = np.dot(vt, np.dot(reflection_comp, u))
    p = (b_mean - np.dot(R, a_mean))
    #return the frame for the point cloud transformation
    return Frame(R, p)
