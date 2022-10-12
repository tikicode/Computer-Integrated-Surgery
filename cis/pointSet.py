import numpy as np
import frame

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


    def getDataCalBody(fName):
        headers = pd.read_csv(fName, header=None, names=["Nd", "Na", "Nc", np.nan], nrows=1)
        #number of each
        ND = int(text["Nd"][0])
        NA = int(text["Na"][0])
        NC = int(text["Nc"][0])
        text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)
        return (PointSet(np.array(text[["xi", "yi", "zi"]][1:1 + ND])), PointSet(np.array(text[["xi", "yi", "zi"]][1 + ND : 1 + ND + NA])), PointSet(np.array(text[["xi", "yi", "zi"]][1 + ND + NA :])))

    def getDataCalReading(fName):
        headers = pd.read_csv(fName, header=None, names=["Nd", "Na", "Nc", "Nf", np.nan]nrows=1)
        #number of each
        ND = int(text["Nd"][0])
        NA = int(text["Na"][0])
        NC = int(text["Nc"][0])
        NFrame = int(text["Nf"][0])
        text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

        D, A, C = []

        for frame in range(NFrame):
            ind = frame*(ND+NA+NC)
            D.append(PointSet(np.array(text[["xi", "yi", "zi"]][1+ind: 1+ND+ind])))
            A.append(PointSet(np.array(text[["xi", "yi", "zi"]][1+ND+ind: 1+ND+NA+ind])))
            C.append(PointSet(np.array(text[["xi", "yi", "zi"]][1+ND+NA+NC+ind:])))
        return D, A, C

    def getDataEmpivot(fName):
        headers = pd.read_csv(fName, header=None, names=["Ng", "Nf", np.nan]nrows=1)
        #number of each
        NG = int(text["Ng"][0])
        NFrame = int(text["Nf"][0])
        text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

        G = []

        for frame in range(NFrame):
            ind = frame*NG
            G.append(PointSet(np.array(text[["xi", "yi", "zi"]])))
        return G

    