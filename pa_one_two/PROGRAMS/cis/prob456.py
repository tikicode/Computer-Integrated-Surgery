from .point_set import PointCloud
from .point_set import registration
from .pivot_cal import pivot
from .file_rw import get_data_opt_pivot
from .file_rw import get_data_EM_pivot
from .file_rw import get_data_cal_body
from .file_rw import get_data_cal_reading


def prob_four(cal_body, cal_reading):
    """Method solving problem 4

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
    #get the points from the input files
    d_points, a_points, c_points = get_data_cal_body(cal_body)
    D_points, A_points, C_points = get_data_cal_reading(cal_reading)
    c_exp = []
    
    #iterate through each of the frames and compute Ci to append to C_exp
    for frame in range(len(D_points)):
        FD = registration(d_points.points, D_points[frame].points)
        FA = registration(a_points.points, A_points[frame].points)
        NF = FD.invert().compose_frame(FA)
        Ci = PointCloud(NF.compose_transform(c_points.points))
        c_exp.append(Ci)
    return c_exp


def prob_five(em_pivot):
    """Method solving problem 5

    Parameters
    _________
    em_pivot : str
        File location for empivot.txt

    Returns
    _________
    np.ndarray
        The position of the EM probe relative to the EM tracker base
    """
    em_data = get_data_EM_pivot(em_pivot)
    tip_in_tool, _ = pivot(em_data)
    return tip_in_tool


def prob_six(opt_pivot, cal_body):
    """Method solving problem 6

    Parameters
    _________
    opt_pivot : str
        File location for optpivot.txt
    cal_body : str
        File location for calbody.txt

    Returns
    _________
    np.ndarray
        The solution to problem 6, position of the optical tracker beacon in EM tracker coordinates for each
        observation frame of optical tracker DATA
    """
    opt_D, opt_H = get_data_opt_pivot(opt_pivot)
    d_points, a_points, c_points = get_data_cal_body(cal_body)
    FD = registration(opt_D[0].points, d_points.points)
    for i in range(len(opt_H)):
        opt_H[i] = PointCloud(FD.compose_transform(opt_H[i].points))
    tip_in_tool, _ = pivot(opt_H)
    return tip_in_tool
