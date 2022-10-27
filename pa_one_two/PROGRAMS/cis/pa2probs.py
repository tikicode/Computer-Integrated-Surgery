import numpy as np

from .interpolation import remove_distortion, bernstein_c_ij
from .point_set import PointCloud
from .point_set import registration
from .pivot_cal import pivot
from .file_rw import getDataEMFids, getDataCTFids
from .file_rw import getDataEMPivot
from .file_rw import getDataCalBody
from .file_rw import getDataCalReading
from .frame import Frame


def prob_three(cal_reading, em_pivot, c_exp):
    D, A, C = getDataCalReading(cal_reading)
    em_pivot = getDataEMPivot(em_pivot)
    pts_em = em_pivot[0].points.shape[0]
    c = np.zeros(shape=(len(C) * C[0].points.shape[0], 3))
    for i in range(len(C)):
        index = C[0].points.shape[0] * i
        c[index:index + C[0].points.shape[0]] = C[i].points

    coefficients, q_min, q_max, q_exp_min, q_exp_max = bernstein_c_ij(c, c_exp, 5)
    em_pivot_undistorted_reg = remove_distortion(em_pivot, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max)
    em_pivot_undistorted = em_pivot_undistorted_reg.reshape((len(em_pivot), len(em_pivot[0].points), 3))
    em_pivot_undistorted_ps = []
    for i in range(em_pivot_undistorted.shape[0]):
        index = pts_em * i
        frame = np.array(em_pivot_undistorted_reg[index:index + pts_em])
        em_pivot_undistorted_ps.append(PointCloud(frame))
    p_tip_em, base_em = pivot(em_pivot_undistorted_ps)
    return coefficients, p_tip_em, base_em, em_pivot_undistorted, q_min, q_max, q_exp_min, q_exp_max


def prob_four(em_fids, q_min, q_max, q_exp_min, q_exp_max, coefficients, p_tip_em, em_pivot_undistorted):
    em_fids = getDataEMFids(em_fids)
    em_fids_undistorted = remove_distortion(em_fids, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max).\
        reshape((len(em_fids), len(em_fids[0].points), 3))
    g0 = np.mean(em_pivot_undistorted, axis=1)[0]
    g_j = (em_pivot_undistorted[0] - g0)
    b_j = []
    for i in range(em_fids_undistorted.shape[0]):
        F_G = registration(g_j, em_fids_undistorted[i])
        b_j.append(F_G.compose_transform(np.array([p_tip_em])))
    b_j = np.array(b_j).reshape(len(em_fids), 3)
    return b_j


def prob_five(ct_fids, b_j):
    ct_fids = getDataCTFids(ct_fids)
    F_reg = registration(b_j, ct_fids[0].points)
    return F_reg


def prob_six(em_nav, em_pivot_undistorted, p_tip_em, F_reg, coefficients, q_min, q_max, q_exp_min, q_exp_max):
    em_nav = getDataEMPivot(em_nav)
    em_nav_undistorted = remove_distortion(em_nav, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max)\
        .reshape((len(em_nav), len(em_nav[0].points), 3))
    g0 = np.mean(em_pivot_undistorted, axis=1)[0]
    g_j = em_pivot_undistorted[0] - g0
    b_nav = []
    for i in range(em_nav_undistorted.shape[0]):
        F_G = registration(g_j, em_nav_undistorted[i])
        b_nav.append(F_reg.compose_transform(F_G.compose_transform(np.array([p_tip_em]))))
    b_nav = np.array(b_nav)
    return b_nav.reshape(len(em_nav), 3)
