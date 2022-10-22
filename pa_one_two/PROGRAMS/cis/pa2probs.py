from .point_set import PointSet
from .point_set import registration
from .pivot_cal import pivot
from .file_rw import getDataOptPivot
from .file_rw import getDataEMPivot
from .file_rw import getDataCalBody
from .file_rw import getDataCalReading


def prob_one(cal_body, cal_reading):
    """Method solving problem one

    Parameters
    _________
    cal_body : str
        File location for calbody.txt
    cal_reading : str
        File location for calreadings.txt

    Returns
    _________
    c_exp : np.ndarray
        The expected values for the distortion calibration DATA
    """
    d_points, a_points, c_points = getDataCalBody(cal_body)
    D_points, A_points, C_points = getDataCalReading(cal_reading)
    c_exp = []
    for frame in range(len(D_points)):
        FD = registration(d_points, D_points[frame])
        FA = registration(a_points, A_points[frame])
        NF = FD.invert().compose_frame(FA)
        Ci = PointSet(NF.compose_transform(c_points.points))
        c_exp.append(Ci)

    return c_exp
