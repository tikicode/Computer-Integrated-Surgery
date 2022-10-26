from .pivot_cal import pivot
import numpy as np

from .point_set import PointSet


def distortion(c, c_exp, em_pivot, deg):
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

    F_ijk = F(u, deg)
    coefficient = coefficients(F_ijk, c_exp_scaled)
    correction = correct_distortion(em_pivot, coefficient, min_q, max_q, min_c_exp, max_c_exp, 5)
    pivot_output = pivot(correction)
    return pivot_output, coefficient, min_q, max_q, min_c_exp, max_c_exp


def correct_distortion(data, coefficient, min_q, max_q, min_c_exp, max_c_exp, deg):
    corrected = []
    for i in range(len(data)):
        corrected.append(data[i])
    size = len(corrected[0].points[0])
    for i in range(len(data)):
        u = scaleToBox(data[i].points, min_q, max_q, len(data[i].points))
        F_ijk = F(u, 5)
        corrected[i].points = np.dot(F(scaleToBox(corrected[i].points, min_q, max_q, size), deg), coefficient)
        for j in range(len(corrected[0].points)):
            for k in range(3):
                corrected[i].points[k][j] = corrected[i].points[k][j] * (max_c_exp[k] - min_c_exp[k]) + min_c_exp[k]
    print(corrected, "corrected points")
    return corrected


def F(u, n):
    F_ijk = np.zeros(shape=(len(u[0]), (n + 1) ** 3))
    for h in range(len(u[0])):
        counter = 0
        for i in range(n + 1):
            for j in range(n + 1):
                for k in range(n + 1):
                    F_ijk[h][counter] = bernstein_poly(n, i, u[h][0]) * bernstein_poly(n, j, u[h][1]) * \
                                        bernstein_poly(n, k, u[h][2])
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
