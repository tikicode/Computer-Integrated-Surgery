from .point_set import PointSet as ps
from .file_rw import getDataCalReading
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

    # find min and max q
    min_q, max_q = [], []
    min_q[0] = np.min(c_exp[0])
    min_q[1] = np.min(c_exp[1])
    min_q[2] = np.min(c_exp[2])
    max_q[0] = np.max(c_exp[0])
    max_q[1] = np.max(c_exp[1])
    max_q[2] = np.max(c_exp[2])

    # get u using sensor vals
    num_points = np.shape(c_exp[0])
    u = scaleToBox(c_exp, min_q, max_q, num_points)

    # get F_ijk(u)
    N = 5
    F_ijk = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
        # use bernstein to get F

    p = Fijk.dot(c_exp)
    return p


def scaleToBox(q, qmin, qmax, num):
    u = np.zeros([num, 3])
    for i in range(num):
        u[i][0] = (q[i][0] - qmin[0]) / (qmax[0] - qmin[0])
        u[i][1] = (q[i][1] - qmin[1]) / (qmax[1] - qmin[1])
        u[i][2] = (q[i][2] - qmin[2]) / (qmax[2] - qmin[2])
    return u


def bernstein_poly(N, k, u):
    v = 1 - u
    rp.math.factorial(N) / (np.math.factorial(k) * np.math.factorial(N - k)) * u ** (N - k) * v ** k