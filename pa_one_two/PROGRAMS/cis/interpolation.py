import numpy as np


def remove_distortion(point_set, coefficient, deg, q_min, q_max, q_exp_min, q_exp_max):
    """Method to remove distortion from the point set

    Parameters
    _________
    point_set : np.ndarray
        The point set to remove distortion from
    coefficient : np.ndarray
        The bernstein coefficients for the distortion calibration
    deg : int
        The degree of the bernstein polynomial
    q_min : np.ndarray
        The minimum values for the distorted data
    q_max : np.ndarray
        The maximum values for the distorted data
    q_exp_min : np.ndarray
        The minimum values for the expected data
    q_exp_max : np.ndarray
        The maximum values for the expected data

    Returns
    _________
    corrected : np.ndarray
        The combined frames of the corrected point set
    """
    all_data = np.zeros(shape=(len(point_set) * point_set[0].points.shape[0], 3))
    # combine all frames
    for i in range(len(point_set)):
        index = point_set[0].points.shape[0] * i
        all_data[index:index + point_set[0].points.shape[0]] = point_set[i].points
    # scale to box for the bernstein polynomial
    u = scale_to_box(all_data, q_min, q_max)
    corrected = np.zeros(all_data.shape)
    # loop through the N, k, and u values for the bernstein polynomials and calculate the corrected values
    for i in range(len(u)):
        for j in range(deg + 1):
            for k in range(deg + 1):
                for l in range(deg + 1):
                    corrected[i] += np.dot(coefficient[j * (deg + 1) ** 2 + k * (deg + 1) + l],
                                           bernstein(deg, j, u[i][0]) * bernstein(deg, k, u[i][1]) *
                                           bernstein(deg, l, u[i][2]))
    # scale the corrected values back to the original scale
    corrected = unscale(corrected, q_exp_min, q_exp_max)
    return corrected


def bernstein_c_ij(c, c_exp, deg):
    """Method to calculate the bernstein coefficients for the distortion calibration

    Parameters
    _________
    c : np.ndarray
        The distorted data
    c_exp : np.ndarray
        The expected data
    deg : int
        The degree of the bernstein polynomial

    Returns
    _________
    coefficient : np.ndarray
        The bernstein coefficients for the distortion calibration
    """
    # scale the expected and distorted data to lie between 0 and 1
    q_min, q_max = min_max(c)
    u = scale_to_box(c, q_min, q_max)
    q_exp_min, q_exp_max = min_max(c_exp)
    u_exp = scale_to_box(c_exp, q_exp_min, q_exp_max)

    # calculate the bernstein coefficients using least squares between boxed data and each coefficient
    F_ijk = np.zeros(shape=(len(u), (deg + 1) ** 3))
    for mat_i in range(len(u)):
        mat_jk = 0
        for i in range(deg + 1):
            for j in range(deg + 1):
                for k in range(deg + 1):
                    F_ijk[mat_i][mat_jk] = bernstein(deg, i, u_exp[mat_i][0]) * bernstein(deg, j, u_exp[mat_i][1]) * \
                                           bernstein(deg, k, u_exp[mat_i][2])
                    mat_jk += 1
    return np.linalg.lstsq(F_ijk, u, rcond=None)[0], q_min, q_max, q_exp_min, q_exp_max


def min_max(q):
    """Method to calculate the minimum and maximum values for the data

    Parameters
    _________
    q : np.ndarray
        The data to calculate the minimum and maximum values for

    Returns
    _________
    q_min : np.ndarray
        The minimum values for the data
    q_max : np.ndarray
        The maximum values for the data
    """
    q_max = np.amax(q, axis=0)
    q_min = np.amin(q, axis=0)
    return q_min, q_max


def scale_to_box(q, q_min, q_max):
    """Method to scale the data to lie between 0 and 1

    Parameters
    _________
    q : np.ndarray
        The data to scale
    q_min : np.ndarray
        The minimum values for the data
    q_max : np.ndarray
        The maximum values for the data

    Returns
    _________
    q_scaled : np.ndarray
        The scaled data between 0 and 1
    """
    box_frame = (q - q_min) / (q_max - q_min)
    return box_frame


def unscale(q, q_min, q_max):
    """Method to scale the data back to the original scale

        Parameters
        _________
        q : np.ndarray
            The data to scale
        q_min : np.ndarray
            The minimum values for the data
        q_max : np.ndarray
            The maximum values for the data

        Returns
        _________
        q_scaled : np.ndarray
            The data scales back to the original scale
        """
    scale_up = q * (q_max - q_min) + q_min
    return scale_up


def bernstein(N, k, u):
    """Method to calculate the bernstein polynomial

    Parameters
    _________
    N : int
        The degree of the bernstein polynomial
    k : int
        The index of the bernstein polynomial
    u : float
        Binomial coefficient of the bernstein polynomial

    Returns
    _________
    bernstein : float
        The bernstein coefficient for one index

    """
    v = 1 - u
    return np.math.factorial(N) / (np.math.factorial(k) * np.math.factorial(N - k)) * (u ** k) * (v ** (N - k))
