import numpy as np
import cis.frame as fr


class PointSet:

    def __init__(self, points):
        self.points = points

    '''
    Non-Iterative registration algorithm from Arun, Huang, and Blostein
    parameters: two point sets
    return: frame for the transformation
    '''


def registration(A, B):
    centeredA = A.points - np.mean(A.points, axis=1, keepdims=True)
    centeredB = B.points - np.mean(B.points, axis=1, keepdims=True)
    H = np.dot(centeredA, centeredB.transpose())

    u, s, vt = np.linalg.svd(H)

    u = u.transpose()
    vt = vt.transpose()

    R = np.dot(vt, u)

    # check to make sure not reflection
    if np.linalg.det(R) < 0:
        R[:, 3] *= -1

    p = centeredB - np.dot(R, centeredA)
    return fr.Frame(R, p)

