import numpy as np

from .interpolation import distortion, correct_distortion, remove_distortion, bernstein_c_ij
from .point_set import PointCloud
from .point_set import registration
from .pivot_cal import pivot
from .file_rw import getDataOptPivot, getDataEMFids, getDataCTFids
from .file_rw import getDataEMPivot
from .file_rw import getDataCalBody
from .file_rw import getDataCalReading
from .frame import compose_transform


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


def prob_three(cal_body, cal_reading, em_pivot):
    D, A, C = getDataCalReading(cal_reading)
    c_exp = prob_one(cal_body, cal_reading)
    coefficients, q_min, q_max, q_exp_min, q_exp_max = bernstein_c_ij(C, c_exp, 5)
    em_pivot_undistorted = remove_distortion(em_pivot, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max)
    p_tip_em, base_em = pivot(em_pivot_undistorted)
    return coefficients, p_tip_em, base_em, em_pivot_undistorted


def prob_four(cal_body, cal_reading, em_fids, em_pivot, q_min, q_max, q_exp_min, q_exp_max):
    em_fids = getDataEMFids(em_fids)
    coefficients, p_tip_em, base_em, em_pivot_undistorted = prob_three(cal_body, cal_reading, em_pivot)
    em_fids_undistorted = remove_distortion(em_fids, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max)
    g0 = np.mean(em_pivot_undistorted, axis=1)[0]
    g_j = em_pivot_undistorted[0] - g0
    b_j = []
    for i in range(len(em_fids_undistorted)):
        F_G = registration(g_j, em_fids_undistorted[i])
        b_j.append(compose_transform(F_G, p_tip_em))
    b_j = np.array(b_j)
    return b_j, em_fids_undistorted


def prob_five(ct_fids, b_j):
    ct_fids = getDataCTFids(ct_fids)
    F_reg = registration(b_j, ct_fids)
    return F_reg


def prob_six(em_nav, em_fids_undistorted, p_tip_em, F_reg, coefficients, q_min, q_max, q_exp_min, q_exp_max):
    em_nav = getDataEMPivot(em_nav)
    em_nav_undistorted = remove_distortion(em_nav, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max)
    g0 = np.mean(em_nav_undistorted, axis=1)[0]
    g_j = em_nav_undistorted[0] - g0
    b_nav = []
    for i in range(len(em_fids_undistorted)):
        F_G = registration(g_j, em_fids_undistorted[i])
        b_nav.append(compose_transform(F_reg, compose_transform(F_G, p_tip_em))
    b_nav = np.array(b_nav)
    return b_nav

