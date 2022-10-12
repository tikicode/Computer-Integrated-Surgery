import scipy.linalg as la
import numpy as np
import frame 
import pointSet

def pivot(ps_data, n):
    local_probe = ps_data[0][n].points
    gj = local_probe - np.mean(local_probe, axis = 1, keepdims = True)

    num_frames = len(ps_data[0])

    svd_r = np.zeros((3 * num_frames, 6))
    svd_p = np.zeros((3 * num_frames, 1))

    for i in range(num_frames):
        frame_k = pointSet.registration(ps_data[0][i], gj) 
        cur_r, cur_p = frame_k.R, frame_k.p
        ti = 3*i
        svd_r(ti : ti + 2, 0 : 2) = cur_r
        svd_p[ti + 2] = -1 * cur_p
        svd_r[ti][3] = -1
        svd_r[ti + 1][4] = -1
        svd_r[ti + 2][5] = -1

    return la.lstsq(svd_r, svd_p)




