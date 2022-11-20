import pytest
from pa_three_four.PROGRAMS.cis.thang import Thang
from pa_three_four.PROGRAMS.cis.frame import Frame
import numpy as np


def test_sort_point():
    a_thang = Thang(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]]))
    assert np.allclose(a_thang.sort_point(), np.array([0, 0, 0]), atol=1e-3)


def test_closest_point_to():
    a_thang = Thang(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]]))
    assert np.allclose(a_thang.closest_point_to(np.array([[1, 0, 1]])), np.array([1, 0, 0]), atol=1e-3)


def test_enlarge_bounds():
    a_thang = Thang(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]]))
    f = Frame(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), np.array([0, 0, 0]))
    LB, UB = a_thang.enlarge_bounds(f, np.array([[0.25, 0.25, 0]]), np.array([[0.5, 0.5, 0]]))
    print(LB, UB)
    assert np.allclose(LB, np.array([0, 0, 0]), atol=1e-3)
    assert np.allclose(UB, np.array([1, 1, 0]), atol=1e-3)


def test_bounding_box():
    a_thang = Thang(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]]))
    f = Frame(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), np.array([0, 0, 0]))
    LB, UB = a_thang.bounding_box(f)
    assert np.allclose(LB, np.array([0, 0, 0]), atol=1e-3)
    assert np.allclose(UB, np.array([1, 1, 0]), atol=1e-3)


def test_may_be_in_bounds():
    a_thang = Thang(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]]))
    f = Frame(np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), np.array([0, 0, 0]))
    a_thang.may_be_in_bounds(f, np.array([[.5, 0, 0]]), np.array([[1.5, 0, 0]]))
