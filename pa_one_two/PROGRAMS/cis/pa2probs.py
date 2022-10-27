import numpy as np

from .interpolation import distortion, correct_distortion, remove_distortion, bernstein_c_ij
from .point_set import PointCloud
from .point_set import registration
from .pivot_cal import pivot
from .file_rw import getDataOptPivot, getDataEMFids, getDataCTFids
from .file_rw import getDataEMPivot
from .file_rw import getDataCalBody
from .file_rw import getDataCalReading


def prob_one(cal_body, cal_reading):
    """Method solving problem one

    Parameters
    _________
    cal_body : str
        File location for calbody.txt
    cal_reading : str
        File location for calreadings.txt

    Returns
    _________
    c_exp : np.ndarray
        The expected values for the distortion calibration DATA
    """
    d_points, a_points, c_points = getDataCalBody(cal_body)
    D_points, A_points, C_points = getDataCalReading(cal_reading)
    c_exp = []
    for frame in range(len(D_points)):
        FD = registration(d_points, D_points[frame])
        FA = registration(a_points, A_points[frame])
        NF = FD.invert().compose_frame(FA)
        Ci = PointCloud(NF.compose_transform(c_points.points))
        c_exp.append(Ci)

    return c_exp


def prob_four(cal_body, cal_reading, em_fids):
    em_fids = getDataEMFids(em_fids)
    em_pivot = getDataEMPivot(em_pivot)
    D, A, C = getDataCalReading(cal_reading)
    c_exp = prob_one(cal_body, cal_reading)
    coefficients = bernstein_c_ij(C, c_exp, 5)

    G_j = G_new[0].points - np.mean(G[0].points, axis=1, keepdims=True)
    B_j = []
    for frame in G_new:
        FG = registration(PointCloud(G_j), frame)
        B_j.append(FG.compose_transform(pivot_output))
    B_j = np.array(B_j)
    return PointCloud(B_j)


def prob_five(ct_fids, B_j):
    ct_fids = getDataCTFids(ct_fids)
    print(ct_fids)
    print(B_j)
    print(B_j.points)
    F_reg = registration(ct_fids, B_j)
    return F_reg


def prob_six(cal_body, cal_reading, em_pivot, ct_fids):

