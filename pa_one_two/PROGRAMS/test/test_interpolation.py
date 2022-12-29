import numpy as np
import pytest
from pa_one_two.PROGRAMS.cis.interpolation import bernstein, min_max, scale_to_box, unscale, bernstein_c_ij, \
    correct_distortion


def test_bernstein():
    print(bernstein(5, 3, 1))
    assert np.allclose(bernstein(5, 3, 1), 0)
    assert np.allclose(bernstein(5, 3, 0.5), 0.3125)
    assert np.allclose(bernstein(5, 4, 0.5), 0.15625)


def test_min_max():
    q = np.array([[1, 4, 7], [2, 5, 8], [3, 6, 9]])
    q_min, q_max = min_max(q)
    assert np.equal(q_min, np.array([1, 4, 7])).all()
    assert np.equal(q_max, np.array([3, 6, 9])).all()


def test_scale_to_box():
    q = np.array([[0, 0, 0], [2, 2, 2], [4, 4, 4]])
    q_min, q_max = min_max(q)
    box_frame = scale_to_box(q, q_min, q_max)
    assert np.equal(box_frame, np.array([[0, 0, 0], [.5, .5, .5], [1, 1, 1]])).all()
