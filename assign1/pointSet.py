import numpy as np
import Frame

class PointSet:

    def __init__(self, points):
        this.points = points

    def registration(A, B):
        centeredA = A - np.mean(A.points, axis=1)
        centeredB = B - np.mean(B.points, axis=1)

        H = np.dot(centeredA, centeredB.transpose())

        u, s, vt = np.linalg.svd(H)

        u = u.transpose()
        vt = v.transpose()

        R = np.dot(vt, u)

        # check to make sure not reflection
        # if np.linalg.det( R ) < 0: 
        #     R[:, 3] *= -1

        p = centeredB - numpy.dot(R, centeredA)
        return Frame(R, p)


        # ua, sa, va = np.linalg.svd(centeredA)
        # ub, sb, vb = np.linalg.svd(centeredA)

        # R = np.dot(ub, ua.transpose())

        # C = np.dot(R.transpose(), B)
        # M = np.dot(R.transpose(), A)

        # E = np.linalg.norm(M-C)
        # if E > threshhold: idk what to do from here im very confused


