import numpy as np
from .point_set import PointSet
from .point_set import registration


def pivot(ps_data):
    """Method for performing a pivot calibration

    Parameters
    _________
    ps_data : PointSet
        The point cloud of calibration data

    Returns
    _________
    np.linalg.lstsq
        The least squares solution to the calibration problem
    """
    local_probe = ps_data[0].points
    gj = local_probe - np.mean(local_probe, axis=1, keepdims=True)

    num_frames = len(ps_data)

    lstsq_r = np.zeros((3 * num_frames, 6))
    lstsq_p = np.zeros((3 * num_frames, 1))

    for i in range(num_frames):
        frame_k = registration(ps_data[i], PointSet(gj))
        cur_r, cur_p = frame_k.R, frame_k.p
        ti = 3 * i
        lstsq_r[ti:ti + 3, 0:3] = cur_r
        lstsq_p[ti:ti + 3] = -1 * cur_p
        lstsq_r[ti][3] = -1
        lstsq_r[ti + 1][4] = -1
        lstsq_r[ti + 2][5] = -1

    return np.linalg.lstsq(lstsq_r, lstsq_p, rcond=None)
