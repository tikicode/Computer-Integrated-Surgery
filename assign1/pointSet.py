import numpy as np


class PointSet:

    def __init__(self, points):
        this.points = points

    def registration(A, B):
        centeredA = A - A.mean(axis=0)
        centeredB = B - B.mean(axis=0)

        ua, sa, va = np.linalg.svd(centeredA)
        ub, sb, vb = np.linalg.svd(centeredA)

        R = np.dot(ub, ua.transpose())

        C = np.dot(R.transpose(), B)
        M = np.dot(R.transpose(), A)

        
