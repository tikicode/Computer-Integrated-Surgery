import pytest
import numpy as np
from pa_three_four.PROGRAMS.cis import cov_tree as ct
from pa_three_four.PROGRAMS.cis.thang import Thang


def test_compute_cov_bounds():
    # Create a cube using vertices
    mesh_vertices = np.array([[-1, -1, -1], [-1, -1, 1], [-1, 1, 1], [1, 1, 1], [1, -1, 1], [1, -1, -1], [1, 1, -1],
                              [-1, 1, -1]])
    # find indices of triangles forming pyramid to side of origin
    indices = np.array([[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5]])
    # Create a covariance tree from the cube
    ts = np.array([Thang(mesh_vertices[indices[i]]) for i in range(len(indices))])
    tester = ct.CovTreeNode(ts, len(ts))
    # Frame of the covariance tree node is at center of pyramid
    UB = tester.UB
    LB = tester.LB
    # The upper and lower bounds should be the corners of a box with a corner at the origin and a corner at (2,2,2)
    assert np.allclose(UB, [[2, 2, 2]], atol=1e-3)
    assert np.allclose(LB, [[0, 0, 0]], atol=1e-3)


def test_compute_cov_frame():
    # Create a cube using vertices
    mesh_vertices = np.array([[-1, -1, -1], [-1, -1, 1], [-1, 1, 1], [1, 1, 1], [1, -1, 1], [1, -1, -1], [1, 1, -1]])
    indices = np.array([[0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 5]])
    # Create a covariance tree from the mesh
    ts = np.array([Thang(mesh_vertices[indices[i]]) for i in range(4)])
    tester = ct.CovTreeNode(ts, len(ts))
    # Frame of the covariance tree node is at center of pyramid
    R = tester.F.R
    p = tester.F.p
    assert np.allclose(R, [[1, 0, 0], [0, 1, 0], [0, 0, 1]], atol=1e-3)
    assert np.allclose(p, [[-1, -1, -1]], atol=1e-3)


def test_find_closest_point():
    # Create a pyramid using vertices (no bottom)
    mesh_vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [.5, .5, 1]])
    indices = np.array([[0, 1, 4], [0, 2, 4], [2, 3, 4], [1, 3, 4]])
    # Choose a point above the pyramid
    ts = np.array([Thang(mesh_vertices[indices[i]]) for i in range(len(indices))])
    tester = ct.CovTreeNode(ts, len(ts))

    c_min = tester.find_closest_point(np.array([[.5, .5, 1.5]]), 10, np.array([[0, 0, 0]]))
    # The closest point should be the top of the pyramid
    assert np.allclose(c_min, np.array([[.5, .5, 1]]), atol=1e-3)


def test_update_closest():
    # Create a pyramid using vertices (no bottom)
    mesh_vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [.5, .5, 1]])
    indices = np.array([[0, 1, 4], [0, 2, 4], [2, 3, 4], [1, 3, 4]])
    # Choose a point above the pyramid
    ts = np.array([Thang(mesh_vertices[indices[i]]) for i in range(len(indices))])
    tester = ct
    bound, closest = tester.update_closest(ts[0], np.array([[.5, .5, 1.5]]), 10, np.array([[0, 0, 0]]))
    # The closest point should be the top of the pyramid and the bound should be 0.5
    print(bound, closest)
    assert np.allclose(closest, np.array([[.5, .5, 1]]), atol=1e-3)
    assert np.allclose(bound, 0.5, atol=1e-3)

