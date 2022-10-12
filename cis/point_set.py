import numpy as np
import pandas as pd
import frame as fr


class PointSet:

    def __init__(self, points):
        self.points = points

    '''
    Non-Iterative registration algorithm from Arun, Huang, and Blostein
    parameters: two point sets
    return: frame for the transformation
    '''


def registration(A, B):
    centeredA = A - np.mean(A.points, axis=1)
    centeredB = B - np.mean(B.points, axis=1)

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


'''Methods to read each type of file'''


def getDataCalBody(fName):
    headers = pd.read_csv(fName, header=None, names=["Nd", "Na", "Nc", np.nan], nrows=1)
    # number of each
    ND = int(headers["Nd"][0])
    NA = int(headers["Na"][0])
    NC = int(headers["Nc"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)
    return (PointSet(np.array(text[["xi", "yi", "zi"]][1:1 + ND])),
            PointSet(np.array(text[["xi", "yi", "zi"]][1 + ND: 1 + ND + NA])),
            PointSet(np.array(text[["xi", "yi", "zi"]][1 + ND + NA:])))


def getDataCalReading(fName):
    headers = pd.read_csv(fName, header=None, names=["Nd", "Na", "Nc", "Nf", np.nan], nrows=1)
    # number of each
    ND = int(headers["Nd"][0])
    NA = int(headers["Na"][0])
    NC = int(headers["Nc"][0])
    NFrame = int(headers["Nf"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

    D, A, C = [], [], []

    for frame in range(NFrame):
        ind = frame * (ND + NA + NC)
        D.append(PointSet(np.array(text[["xi", "yi", "zi"]][1 + ind: 1 + ND + ind])))
        A.append(PointSet(np.array(text[["xi", "yi", "zi"]][1 + ND + ind: 1 + ND + NA + ind])))
        C.append(PointSet(np.array(text[["xi", "yi", "zi"]][1 + ND + NA + NC + ind:])))
    return D, A, C


def getDataEMPivot(fName):
    headers = pd.read_csv(fName, header=None, names=["Ng", "Nf", np.nan], nrows=1)
    # number of each
    NG = int(headers["Ng"][0])
    NFrame = int(headers["Nf"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

    G = []

    for frame in range(NFrame):
        ind = frame * NG
        G.append(PointSet(np.array(text[["xi", "yi", "zi"]][1 + ind:1 + NG + ind])))
    return G


def getDataOptPivot(fName):
    headers = pd.read_csv(fName, header=None, names=["Nd", "Nh", "Nf", np.nan], nrows=1)
    # number of each
    ND = int(headers["Nd"][0])
    NH = int(headers["Nh"][0])
    NFrame = int(headers["Nf"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

    D, H = [], []

    for frame in range(NFrame):
        ind = frame * (ND + NH)
        D.append(PointSet(np.array(text[["xi", "yi", "zi"]][1 + ind:1 + ND + ind])))
        H.append(PointSet(np.array(text[["xi", "yi", "zi"]][1 + ind + ND:1 + ND + NH + ind])))
    return D, H
