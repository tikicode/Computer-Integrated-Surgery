import numpy as np
import cis.frame as fr
import cis.point_set as ps
import cis.pivot_cal as pc
import cis.io as io


def prob_four(cal_body, cal_reading):
    # do something to read the files
    # calbod = open(calbody, "r")
    # calread = open(calReading, "r")
    # read file method

    cal_bod = io.getDataCalBody(cal_body)
    cal_read = io.getDataCalReading(cal_reading)
    d_points = cal_bod[0]
    a_points = cal_bod[1]
    c_points = cal_bod[2]
    D_points = cal_read[0]
    A_points = cal_read[1]
    cExp = []
    for frame in range(len(D_points)):
        FD = ps.registration(d_points, D_points[frame])
        FA = ps.registration(a_points, A_points[frame])
        Ci = FA.compose_vec(c_points)
        Ci = (FD.invert()).compose_frame(Ci)
        cExp.append(Ci)

    return cExp


def prob_five(filename):
    em_data = io.getDataEMPivot(filename)
    pivot_em = pc.pivot(em_data, 0)
    return pivot_em[0][0:3]


def prob_six(filename, cal_body, cal_reading):
    opt = io.getDataOptPivot(filename)
    cal_bod = io.getDataCalBody(cal_body)
    cal_read = io.getDataCalReading(cal_reading)
    d_points = cal_bod[0]
    D_points = cal_read[0]
    FD = fr.Frame()
    for frame in range(len(D_points)):
        FD = ps.registration(d_points, D_points[frame])
    opt_to_em = FD.compose_vec(opt)
    pivot_opt_to_em = pc.pivot(opt_to_em, 1)
    return pivot_opt_to_em[0][0:3]
