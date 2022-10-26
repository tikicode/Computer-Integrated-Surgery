from .point_set import PointSet as ps
from .file_rw import getDataCalReading, getDataEMPivot
from .file_rw import getDataCalBody
from .pa2probs import prob_one
from .pivot_cal import pivot
import numpy as np


def distortion(cal_body, cal_reading, empivot):
    c = getDataCalReading(cal_reading)
    c_exp = prob_one(cal_body, cal_reading)

    num_frames = len(c_exp)
    num_points = len(c_exp[0].points)

    c_new = c[0].points
    c_exp_new = c_exp[0].points

    for i in range(1, num_frames):
        c_new = np.concatenate((c_new, c[i].points), axis=0)
        c_exp_new = np.concatenate((c_exp_new, c_exp[i].points), axis=0)

    min_q, max_q = [], []
    min_c_exp, max_c_exp = [], []
    for i in range(3):
        min_q.append(min(c_new[i]))
        max_q.append(max(c_new[i]))
        min_c_exp.append(min(c_exp_new[i]))
        max_c_exp.append(max(c_exp_new[i]))

    # get u using sensor vals
    u = scaleToBox(c_new, min_q, max_q, num_points)
    c_exp_scaled = scaleToBox(c_exp_new, min_c_exp, max_c_exp, num_points)

    F_ijk = F(u, 5)
    coefficient = coefficients(F_ijk, c_exp_scaled)
    correction = correct_distortion(empivot, coefficient, min_q, max_q, min_c_exp, max_c_exp)
    pivot_em_dist = pivot(correction)
    return pivot_em_dist


def correct_distortion(file_name, coefficient, min_q, max_q, min_c_exp, max_c_exp):
    em_pivot = getDataEMPivot(file_name)
    corrected = []
    for i in range(len(em_pivot)):
        u = scaleToBox(em_pivot[i].points, min_q, max_q, len(em_pivot[i].points))
        F_ijk = F(u, 5)
        corrected.append(F_ijk @ coefficient)
        for j in range(len(corrected[i])):
            for k in range(3):
                corrected[i].points[j][k] = corrected[i].points[j][k] * (max_c_exp[k] - min_c_exp[k]) + min_c_exp[k]
    return corrected


def F(u, n):
    F_ijk = np.zeros(len(u[0]), (n + 1) ** 3)
    for h in range(len(u[0])):
        counter = 0
        for i in range(n + 1):
            for j in range(n + 1):
                for k in range(n + 1):
                    F_ijk[h][counter] = bernstein_poly(n, i, u[0]) * bernstein_poly(n, j, u[1]) * \
                                        bernstein_poly(n, k, u[2])
                    counter += 1
    return F_ijk


def scaleToBox(q, q_min, q_max, num):
    u = np.zeros(shape=(num, 3))
    for i in range(num):
        u[i][0] = (q[0][i] - q_min[0]) / (q_max[0] - q_min[0])
        u[i][1] = (q[1][i] - q_min[1]) / (q_max[1] - q_min[1])
        u[i][2] = (q[2][i] - q_min[2]) / (q_max[2] - q_min[2])
    return u


def bernstein_poly(N, k, u):
    v = 1 - u
    return np.math.factorial(N) / (np.math.factorial(k) * np.math.factorial(N - k)) * (u ** k) * (v ** (N - k))


def coefficients(F_ijk, c_exp_new):
    return np.linalg.lstsq(F_ijk, c_exp_new, rcond=None)[0]
