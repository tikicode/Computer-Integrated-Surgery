import numpy as np
from pa_three_four.PROGRAMS.cis import icp


def test_find_closest_point():
    mesh_vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
