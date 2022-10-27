import numpy as np


def remove_distortion(point_set, coefficient, deg, q_min, q_max, q_exp_min, q_exp_max):
    all_data = np.zeros(shape=(len(point_set) * point_set[0].points.shape[0], 3))
    for i in range(len(point_set)):
        index = point_set[0].points.shape[0] * i
        all_data[index:index + point_set[0].points.shape[0]] = point_set[i].points
    u = scale_to_box(all_data, q_min, q_max)
    corrected = np.zeros(all_data.shape)
    for i in range(len(u)):
        for j in range(deg + 1):
            for k in range(deg + 1):
                for l in range(deg + 1):
                    corrected[i] += np.dot(coefficient[j * (deg + 1) ** 2 + k * (deg + 1) + l],
                                           bernstein(deg, j, u[i][0]) * bernstein(deg, k, u[i][1]) * bernstein(deg, l, u[i][2]))
    corrected = unscale(corrected, q_exp_min, q_exp_max)
    return corrected


def bernstein_c_ij(c, c_exp, deg):
    q_min, q_max = min_max(c)
    u = scale_to_box(c, q_min, q_max)
    q_exp_min, q_exp_max = min_max(c_exp)
    u_exp = scale_to_box(c_exp, q_exp_min, q_exp_max)

    F_ijk = np.zeros(shape=(len(u), (deg + 1) ** 3))
    for mat_i in range(len(u)):
        mat_jk = 0
        for i in range(deg + 1):
            for j in range(deg + 1):
                for k in range(deg + 1):
                    F_ijk[mat_i][mat_jk] = bernstein(deg, i, u_exp[mat_i][0]) * bernstein(deg, j, u_exp[mat_i][1]) * \
                                           bernstein(deg, k, u_exp[mat_i][2])
                    mat_jk += 1
    return np.linalg.lstsq(F_ijk, u, rcond=None)[0], q_min, q_max, q_exp_min, q_exp_max


def min_max(q):
    q_max = np.amax(q, axis=0)
    q_min = np.amin(q, axis=0)
    return q_min, q_max


def scale_to_box(q, q_min, q_max):
    box_frame = (q - q_min) / (q_max - q_min)
    return box_frame


def unscale(q, q_min, q_max):
    scale_up = q * (q_max - q_min) + q_min
    return scale_up


def bernstein(N, k, u):
    v = 1 - u
    return np.math.factorial(N) / (np.math.factorial(k) * np.math.factorial(N - k)) * (u ** k) * (v ** (N - k))
