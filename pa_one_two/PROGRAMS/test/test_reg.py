from .test_generator import random_r_w_t as f
import numpy as np
import pytest
import pa_one.PROGRAMS.cis.point_set as ps


def test_reg_no_noise():
    frame = f(0)
    xp = np.zeros((10, 1))
    yp = np.zeros((10, 1))
    zp = np.zeros((10, 1))
    for i in range(10):
        xp[i], yp[i], zp[i] = 10 * i, 10 * i, 10 * i
    A = np.vstack(np.meshgrid(xp, yp, zp)).reshape(3, -1)
    B = frame.compose_transform(A)
    calc_frame = ps.registration(ps.PointSet(A), ps.PointSet(B))
    assert np.allclose(calc_frame.R, frame.R, atol=1e-3)
    assert np.allclose(calc_frame.p, frame.p, atol=1e-3)
