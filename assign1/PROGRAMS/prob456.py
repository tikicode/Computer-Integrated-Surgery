import numpy as np
import Frame
import PointSet


def probFour(calbody, calReading):
    # do something to read the files
    # calbod = open(calbody, "r")
    # calread = open(calReading, "r")
    # read file method


    dPoints = calbody d points
    aPoints = calbody a points
    cPoints = calbody c points
    Frames = calReading frame
    cExp = []
    for frame in Frames :
        DPoints = calReading at given frame index d points
        APoints = calReading at given frame index a points
        FD = registration(dPoints, DPoints)
        FA = registration(aPoints, APoints)
        Ci = FA.composeVec(cPoints)
        Ci = (FD.invert()).composeFrame(Ci)
        cExp.append(Ci)

    return cExp




        
