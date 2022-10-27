from .test_generator import random_r_w_t as f
import numpy as np
from pa_one_two.PROGRAMS.cis import point_set as ps
import pytest


def test_reg_no_noise():
    frame = f(0)
    xp = np.zeros((10, 1))
    yp = np.zeros((10, 1))
    zp = np.zeros((10, 1))
    for i in range(10):
        xp[i], yp[i], zp[i] = 10 * i, 10 * i, 10 * i
    A = np.zeros((1000, 3))
    for i in range(10):
        for j in range(10):
            for k in range(10):
                A[i * 100 + j * 10 + k] = np.array([i, j, k])
    print(A.shape)
    B = frame.compose_transform(A)
    calc_frame = ps.registration(A, B)
    assert np.allclose(calc_frame.R, frame.R, atol=1e-3)
    assert np.allclose(calc_frame.p, frame.p, atol=1e-3)
