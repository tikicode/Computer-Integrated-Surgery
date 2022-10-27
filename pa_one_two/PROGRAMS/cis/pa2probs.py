import numpy as np

from .interpolation import remove_distortion, bernstein_c_ij
from .point_set import PointCloud
from .point_set import registration
from .pivot_cal import pivot
from .file_rw import getDataEMFids, getDataCTFids
from .file_rw import getDataEMPivot
from .file_rw import getDataCalReading


def prob_three(cal_reading, em_pivot, c_exp):
    """Method solving problem 3

    Parameters
    _________
    cal_reading : str
        File location for calreadings.txt
    em_pivot : str
        File location for empivot.txt
    c_exp : np.ndarray
        The expected values for the corrected distortion calibration data

    Returns
    _________
    coefficients: np.ndarray
        The coefficients for the distortion calibration
    p_tip_em: np.ndarray
        The position of the EM probe tip relative to the EM tracker base
    em_pivot_undistorted: np.ndarray
        The undistorted em_pivot data
    q_min: np.ndarray
        The minimum values for the distorted data
    q_max: np.ndarray
        The maximum values for the distorted data
    q_exp_min: np.ndarray
        The minimum values for the expected data
    q_exp_max: np.ndarray
        The maximum values for the expected data
    """
    D, A, C = getDataCalReading(cal_reading)
    em_pivot = getDataEMPivot(em_pivot)
    pts_em = em_pivot[0].points.shape[0]
    c = np.zeros(shape=(len(C) * C[0].points.shape[0], 3))
    for i in range(len(C)):
        index = C[0].points.shape[0] * i
        c[index:index + C[0].points.shape[0]] = C[i].points

    # compute bernstein coefficients
    coefficients, q_min, q_max, q_exp_min, q_exp_max = bernstein_c_ij(c, c_exp, 5)
    em_pivot_undistorted_reg = remove_distortion(em_pivot, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max)
    em_pivot_undistorted = em_pivot_undistorted_reg.reshape((len(em_pivot), len(em_pivot[0].points), 3))
    em_pivot_undistorted_ps = []

    # solve for the pivot calibration of the undistorted em data
    for i in range(em_pivot_undistorted.shape[0]):
        index = pts_em * i
        frame = np.array(em_pivot_undistorted_reg[index:index + pts_em])
        em_pivot_undistorted_ps.append(PointCloud(frame))
    p_tip_em, base_em = pivot(em_pivot_undistorted_ps)
    return coefficients, p_tip_em, base_em, em_pivot_undistorted, q_min, q_max, q_exp_min, q_exp_max


def prob_four(em_fids, q_min, q_max, q_exp_min, q_exp_max, coefficients, p_tip_em, em_pivot_undistorted):
    """
    Method solving problem 4

    Parameters
    _________
    em_fids: nd.ndarray
        The EM fiducial data
    q_min: np.ndarray
        The minimum values for the distorted data
    q_max: np.ndarray
        The maximum values for the distorted data
    q_exp_min: np.ndarray
        The minimum values for the expected data
    q_exp_max: np.ndarray
        The maximum values for the expected dat
    coefficients: np.ndarray
        The coefficients for the distortion calibration
    p_tip_em: np.ndarray
        The position of the EM probe tip relative to the EM tracker base
    em_pivot_undistorted: np.ndarray
        The undistorted em_pivot data

    Returns
    _________
    coefficients: np.ndarray
        The coefficients for the distortion calibration
    p_tip_em: np.ndarray
        The position of the EM probe tip relative to the EM tracker base
    em_pivot_undistorted: np.ndarray
        The undistorted em_pivot data
    q_min: np.ndarray
        The minimum values for the distorted data
    q_max: np.ndarray
        The maximum values for the distorted data
    q_exp_min: np.ndarray
        The minimum values for the expected data
    q_exp_max: np.ndarray
        The maximum values for the expected data
    """
    em_fids = getDataEMFids(em_fids)
    em_fids_undistorted = remove_distortion(em_fids, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max).\
        reshape((len(em_fids), len(em_fids[0].points), 3))
    g0 = np.mean(em_pivot_undistorted, axis=1)[0]
    g_j = (em_pivot_undistorted[0] - g0)
    b_j = []
    # compute registration between residuals of the objsered data and the em tip
    for i in range(em_fids_undistorted.shape[0]):
        F_G = registration(g_j, em_fids_undistorted[i])
        b_j.append(F_G.compose_transform(np.array([p_tip_em])))
    b_j = np.array(b_j).reshape(len(em_fids), 3)
    return b_j


def prob_five(ct_fids, b_j):
    """
    Method solving problem 5

    Parameters
     _________
    ct_fids: nd.ndarray
        The CT fiducial data
    b_j: np.ndarray
        The located em fiducial data

    Returns
         _________
    F_reg: Frame
        The registration between the em fiducial points and the ct fiducial points
    """
    ct_fids = getDataCTFids(ct_fids)
    # compute registration between the em fiducial points and the ct fiducial points
    F_reg = registration(b_j, ct_fids[0].points)
    return F_reg


def prob_six(em_nav, em_pivot_undistorted, p_tip_em, F_reg, coefficients, q_min, q_max, q_exp_min, q_exp_max):
    """ Method solving problem 6

    Parameters
    _________
    em_nav: nd.ndarray
        The EM navigation data
    em_pivot_undistorted: np.ndarray
        The undistorted em_pivot data
    p_tip_em: np.ndarray
        The position of the EM probe tip relative to the EM tracker base
    F_reg: Frame
        The registration between the em fiducial points and the ct fiducial points
    coefficients: np.ndarray
        The coefficients for the distortion calibration
    q_min: np.ndarray
        The minimum values for the distorted data
    q_max: np.ndarray
        The maximum values for the distorted data
    q_exp_min: np.ndarray
        The minimum values for the expected data
    q_exp_max: np.ndarray
        The maximum values for the expected data

    Returns
    _________
    b_nav: np.ndarray
        The located em navigation data
    """
    em_nav = getDataEMPivot(em_nav)
    em_nav_undistorted = remove_distortion(em_nav, coefficients, 5, q_min, q_max, q_exp_min, q_exp_max)\
        .reshape((len(em_nav), len(em_nav[0].points), 3))
    g0 = np.mean(em_pivot_undistorted, axis=1)[0]
    g_j = em_pivot_undistorted[0] - g0
    b_nav = []
    for i in range(em_nav_undistorted.shape[0]):
        # compute registration between residuals and the em nav points
        F_G = registration(g_j, em_nav_undistorted[i])
        # find pointer coordinates with respect to the CT image
        b_nav.append(F_reg.compose_transform(F_G.compose_transform(np.array([p_tip_em]))))
    b_nav = np.array(b_nav)
    return b_nav.reshape(len(em_nav), 3)
