import numpy as np
import Frame
import PointSet


def probFour(calbody, calReading):
    # do something to read the files
    # calbod = open(calbody, "r")
    # calread = open(calReading, "r")
    # read file method

    calbod = ps.getDataCalBody(calbody)
    calread = ps.getDataCalReading(calReading)
    dPoints = calbod[0]
    aPoints = calbod[1]
    cPoints = calbod[2]
    DPoints = calread[0]
    APoints = calread[1]
    CPoints = calread[2]
    cExp = []
    for frame in range(len(DPoints)) :
        FD = registration(dPoints, DPoints[frame])
        FA = registration(aPoints, APoints[frame])
        Ci = FA.composeVec(cPoints)
        Ci = (FD.invert()).composeFrame(Ci)
        cExp.append(Ci)

    return cExp