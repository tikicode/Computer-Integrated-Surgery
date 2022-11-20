import numpy as np
import pytest
from pa_three_four.PROGRAMS.cis import icp


def test_find_closest_point():
    # Create a pyramid using vertices (no bottom)
    mesh_vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [.5, .5, 1]])
    indices = np.array([[0, 1, 4], [0, 2, 4], [2, 3, 4], [1, 3, 4]])
    # Choose a point above the pyramid
    s_k = np.array([[.5, .5, 1.5]])
    c_min = icp.find_closest_point(mesh_vertices, indices, s_k)
    # The closest point should be the top of the pyramid
    assert np.allclose(c_min, np.array([[.5, .5, 1]]), atol=1e-3)


def test_find_closest_point_triangle():
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    s_k = np.array([[0, 0, 1]])
    c = icp.find_closest_point_triangle(vertices, s_k)
    assert np.allclose(c, np.array([[0, 0, 0]]), atol=1e-3)


def test_project_on_segment():
    c = np.array([.5, -.5, 0])
    p = np.array([0, 0, 0])
    q = np.array([1, 0, 0])
    c = icp.project_on_segment(c, p, q)
    assert np.allclose(c, np.array([[0.5, 0, 0]]), atol=1e-3)


def test_find_euclidian_distance():
    p = np.array([[0, 0, 0]])
    q = np.array([[1, 1, 1]])
    d = icp.find_euclidian_distance(p, q)
    assert np.allclose(d, np.sqrt(3), atol=1e-3)
