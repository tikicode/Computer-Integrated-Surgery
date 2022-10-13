import numpy as np
import cis.frame as fr
import cis.point_set as ps
import cis.pivot_cal as pc
import cis.io as io


def prob_four(cal_body, cal_reading):
    # do something to read the files
    # cal_bod = open(cal_body, "r")
    # cal_read = open(calReading, "r")
    # read file method

    d_points, a_points, c_points = io.getDataCalBody(cal_body)
    D_points, A_points, C_points = io.getDataCalReading(cal_reading)
    c_exp = []
    for frame in range(len(D_points)):
        FD = ps.registration(d_points, D_points[frame])
        FA = ps.registration(a_points, A_points[frame])
        NF = FA.compose_frame(FD.invert())
        Ci = ps.PointSet(NF.compose_transform(c_points.points))
        c_exp.append(Ci)

    return c_exp


def prob_five(em_pivot):
    em_data = io.getDataEMPivot(em_pivot)
    pivot_em = pc.pivot(em_data, 0)
    return pivot_em[0][0:3]


def prob_six(opt_pivot, cal_body, cal_reading):
    opt_D, opt_H = io.getDataOptPivot(opt_pivot)
    d_points, a_points, c_points = io.getDataCalBody(cal_body)
    D_points, A_points, C_points = io.getDataCalReading(cal_reading)
    FD = fr.Frame()
    for frame in range(len(D_points)):
        FD = ps.registration(d_points, D_points[frame])
    opt_to_em = FD.compose_vec(opt)
    pivot_opt_to_em = pc.pivot(opt_to_em, 1)
    return pivot_opt_to_em[0][0:3]
