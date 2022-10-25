import .point_set as ps
import .file_rw as read 
import .pa2probs as prob
import .pivot_cal as pivot
import numpy as np



def distortion(cal_body, cal_reading, empivot):


    
    c_exp = prob.prob_one(cal_body, cal_reading)

    #find min and max q
    minq, maxq = []
    minq[0] = np.min(c_exp[0])
    minq[1] = np.min(c_exp[1])
    minq[2] = np.min(c_exp[2])
    maxq[0] = np.max(c_exp[0])
    maxq[1] = np.max(c_exp[1])
    maxq[2] = np.max(c_exp[2])

    #get u using sensor vals
    num_points = np.shape(c_exp[0])
    u = scaleToBox(c_exp, minq, maxq, num_points)
    
    #get Fijk(u)
    N=5
    Fijk = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                #use bernstein to get F

    p = Fijk.dot(c_exp)
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