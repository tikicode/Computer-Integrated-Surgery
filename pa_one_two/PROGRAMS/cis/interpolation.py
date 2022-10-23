import .point_set as ps
import .file_rw as read 
import .prob456 as prob
import .pivot_cal as pivot
import numpy as np



def distortion(cal_body, cal_reading, empivot):


    #d_points, a_points, c_points = read.getDataCalBody(cal_body)
    D_points, A_points, C_points = read.getDataCalReading(cal_read)
    

    #find min and max q
    minq, maxq = []
    minq[0] = np.min(C_points[0])
    minq[1] = np.min(C_points[1])
    minq[2] = np.min(C_points[2])
    maxq[0] = np.max(C_points[0])
    maxq[1] = np.max(C_points[1])
    maxq[2] = np.max(C_points[2])

    #get u using sensor vals
    num_points = np.shape(C_points[0])
    u = scaleToBox(C_points, minq, maxq, num_points)
    
    #get Fijk(u)
    N=5
    Fijk = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                #use bernstein to get F

    p = Fijk.dot(C_points)
    return p

    


def scaleToBox(q, qmin, qmax, num):
    u = np.zeros([num, 3])
    for i in range(num):
        u[i][0] = (q[i][0] - qmin[0]) / (qmax[0] - qmin[0])
        u[i][1] = (q[i][1] - qmin[1]) / (qmax[1] - qmin[1])
        u[i][2] = (q[i][2] - qmin[2]) / (qmax[2] - qmin[2])
    return u

def bernstein_poly(N, k, u):
    v = 1 - u
    return np.math.factorial(N) / (np.math.factorial(k) * np.math.factorial(N - k)) * u ** (N - k) * v ** k