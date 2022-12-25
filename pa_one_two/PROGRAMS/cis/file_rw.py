import pandas as pd
import numpy as np
from pathlib import Path
from .point_set import PointCloud


def get_data_cal_body(fName: Path):
    """Method for collecting calibration object DATA

    Parameters
    _________
    fName : Path
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
    return (PointCloud(np.array(text[["xi", "yi", "zi"]][0:0 + ND])),
            PointCloud(np.array(text[["xi", "yi", "zi"]][ND: ND + NA])),
            PointCloud(np.array(text[["xi", "yi", "zi"]][ND + NA:])))


def get_data_cal_reading(fName: Path):
    """Method for collecting sensor values

    Parameters
    _________
    fName : Path
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
        D.append(PointCloud(np.array(text[["xi", "yi", "zi"]][ind: ND + ind])))
        A.append(PointCloud(np.array(text[["xi", "yi", "zi"]][ND + ind: ND + NA + ind])))
        C.append(PointCloud(np.array(text[["xi", "yi", "zi"]][ND + NA + ind: NC + ND + NA + ind])))
    return D, A, C


def get_data_EM_pivot(fName: Path):
    """Method for collecting EM sensor values

    Parameters
    _________
    fName : Path
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
        G.append(PointCloud(np.array(text[["xi", "yi", "zi"]][ind:0 + NG + ind])))
    return G


def get_data_opt_pivot(fName: Path):
    """Method for collecting optical sensor DATA

    Parameters
    _________
    fName : Path
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
        D.append(PointCloud(np.array(text[["xi", "yi", "zi"]][ind:0 + ND + ind])))
        H.append(PointCloud(np.array(text[["xi", "yi", "zi"]][ind + ND:0 + ND + NH + ind])))
    return D, H


def get_data_CT_fids(fName: Path):
    """Method for collecting CT fiducial coordinates

    Parameters
    _________
    fName : Path
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

    Bi = [PointCloud(np.array(text[["xi", "yi", "zi"]][:]))]
    return Bi


def get_data_EM_fids(fName: Path):
    """Method for collecting DATA in which the probe is in contact with corresponding CT fiducials

    Parameters
    _________
    fName : Path
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
        G.append(PointCloud(np.array(text[["xi", "yi", "zi"]][ind:0 + NG + ind])))
    return G


def get_data_EM_nav(fName: Path):
    """Method for collecting DATA defining test points of the probe tip

    Parameters
    _________
    fName : Path
        The name of the DATA file

    Returns
    _________
    List of PointSet
        Point cloud describing test points of the probe that need to be translated to CT coordinates
    """
    return get_data_EM_fids(fName)


def get_answer_pa2(fName: Path):
    """Method for collecting DATA defining the answer to PA2

    Parameters
    _________
    fName : Path
        The name of the DATA file

    Returns
    _________
    np.ndarray
        The answer to PA2 output2
    """
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"], skiprows=1)
    return np.array(text[["xi", "yi", "zi"]])


def get_answer_pa1(fName: Path):
    """Method for collecting DATA defining the answer to PA1

    Parameters
    _________
    fName : Path
        The name of the DATA file

    Returns
    _________
    np.ndarray
        The answer to PA1/PA2 output1
    """
    text = pd.read_csv(fName, header=None, names=["xi", "yi", "zi"],
                       skiprows=1)
    arr = np.array(text[["xi", "yi", "zi"]][:], dtype=float)
    post_em = arr[0]
    post_opt = arr[1]
    cs = arr[2:]
    return post_em, post_opt, cs
