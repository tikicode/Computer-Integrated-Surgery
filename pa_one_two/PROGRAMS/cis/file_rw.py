import pandas as pd
import numpy as np
from .point_set import PointSet


def getDataCalBody(fName):
    """Method for collecting calibration object DATA

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    List of PointSet
         Point clouds representing the optical markers on the EM base, optical markers on the calibration object,
         and the EM markers on the calibration object respectively
    """
    headers = pd.read_csv(fName, header=None, names=["Nd", "Na", "Nc", np.nan], nrows=1)
    # number of each
    ND = int(headers["Nd"][0])
    NA = int(headers["Na"][0])
    NC = int(headers["Nc"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)
    return (PointSet(np.array(text[["xi", "yi", "zi"]][0:0 + ND]).T),
            PointSet(np.array(text[["xi", "yi", "zi"]][ND: ND + NA]).T),
            PointSet(np.array(text[["xi", "yi", "zi"]][ND + NA:]).T))


def getDataCalReading(fName):
    """Method for collecting sensor values

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    List of PointSet
        Point clouds representing the optical markers on the EM base, optical markers on the calibration object,
        and the EM markers on the calibration object respectively
    """
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
        D.append(PointSet(np.array(text[["xi", "yi", "zi"]][ind: ND + ind]).T))
        A.append(PointSet(np.array(text[["xi", "yi", "zi"]][ND + ind: ND + NA + ind]).T))
        C.append(PointSet(np.array(text[["xi", "yi", "zi"]][ND + NA + NC + ind:]).T))
    return D, A, C


def getDataEMPivot(fName):
    """Method for collecting EM sensor values

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    List of PointSet
        Point cloud representing the EM sensor DATA for the probe
    """
    headers = pd.read_csv(fName, header=None, names=["Ng", "Nf", np.nan], nrows=1)
    # number of each
    NG = int(headers["Ng"][0])
    NFrame = int(headers["Nf"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

    G = []

    for frame in range(NFrame):
        ind = frame * NG
        G.append(PointSet(np.array(text[["xi", "yi", "zi"]][ind:0 + NG + ind]).T))
    return G


def getDataOptPivot(fName):
    """Method for collecting optical sensor DATA

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    List of PointSet
        Point clouds representing optical markers on the EM base and optical markers on the probe respectively
    """
    headers = pd.read_csv(fName, header=None, names=["Nd", "Nh", "Nf", np.nan], nrows=1)
    # number of each
    ND = int(headers["Nd"][0])
    NH = int(headers["Nh"][0])
    NFrame = int(headers["Nf"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

    D, H = [], []

    for frame in range(NFrame):
        ind = frame * (ND + NH)
        D.append(PointSet(np.array(text[["xi", "yi", "zi"]][ind:0 + ND + ind]).T))
        H.append(PointSet(np.array(text[["xi", "yi", "zi"]][ind + ND:0 + ND + NH + ind]).T))
    return D, H


def getDataCTFids(fName):
    """Method for collecting CT fiducial coordinates

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    PointSet, PointSet
        Point clouds representing coordinates of the CT fiducials
    """
    headers = pd.read_csv(fName, header=None, names=["Nb", np.nan], nrows=1)
    # number of each
    NB = int(headers["Nb"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

    Bi = [PointSet(np.array(text[["xi", "yi", "zi"]][:]).T)]
    return Bi


def getDataEMFids(fName):
    """Method for collecting DATA in which the probe is in contact with corresponding CT fiducials

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    List of PointSet
        Point cloud representing EM markers on the probe and corresponding CT fiducial markers
    """
    headers = pd.read_csv(fName, header=None, names=["Ng", "Nb", np.nan], nrows=1)
    # number of each
    NG = int(headers["Ng"][0])
    NB = int(headers["Nb"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

    G = []

    for frame in range(NB):
        ind = frame * NG
        G.append(PointSet(np.array(text[["xi", "yi", "zi"]][ind:0 + NG + ind]).T))
    return G


def getDataEMNav(fName):
    """Method for collecting DATA defining test points of the probe tip

    Parameters
    _________
    fName : str
        The name of the DATA file

    Returns
    _________
    List of PointSet
        Point cloud describing test points of the probe that need to be translated to CT coordinates
    """
    headers = pd.read_csv(fName, header=None, names=["Ng", "Nf", np.nan], nrows=1)
    # number of each
    NG = int(headers["Ng"][0])
    NFrames = int(headers["Nf"][0])
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)

    G = []

    for frame in range(NFrames):
        ind = frame * NG
        G.append(PointSet(np.array(text[["xi", "yi", "zi"]][ind:0 + NG + ind]).T))
    return G
