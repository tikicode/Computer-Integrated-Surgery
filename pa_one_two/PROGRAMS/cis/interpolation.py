import .point_set as ps
import .file_rw as read 
import .prob456 as prob
import .pivot_cal as pivot
import numpy as np



def distortion(cal_body, cal_reading, empivot):


    d_points, a_points, c_points = read.getDataCalBody(cal_body)
    D_points, A_points, C_points = read.getDataCalReading(cal_read)
    c_expected = prob.prob_four(cal_body, cal_reading)
    num_frames = np.shape(c_expected)[0]
    num_points = np.shape(c_expected[0])

    #find min and max q
    minq, maxq = []
    minq[0] = np.min(C_points[0])
    minq[1] = np.min(C_points[1])
    minq[2] = np.min(C_points[2])
    maxq[0] = np.max(C_points[0])
    maxq[1] = np.max(C_points[1])
    maxq[2] = np.max(C_points[2])

    #get u using sensor vals
    u = scaleToBox(C_points, minq, maxq, num_points)
    
    #get Fijk

    #do lstsqs


def scaleToBox(q, qmin, qmax, num):
    u = np.zeros([num, 3])
    for i in range(num):
        for j in range(0,3):
            u[i][j] = (q[i][j] - qmin[j]) / (qmax[j] - qmin[j])
    return u

def bernstein_poly(N, k, u):
    v = 1 - u
    return np.math.factorial(N) / (np.math.factorial(k) * np.math.factorial(N - k)) * u ** (N - k) * v ** k