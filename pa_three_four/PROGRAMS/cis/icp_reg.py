import numpy as np
from .frame import Frame
from .icp import find_rigid_body_pose
from .thang import Thang
from .cov_tree import CovTreeNode
from .registration import registration


def ICP(a_read: np.ndarray, b_read: np.ndarray, a_tip: np.ndarray, a_leds: np.ndarray, b_leds: np.ndarray,
        vertices: np.ndarray, indices: np.ndarray, max_iter: int):
    """Method for finding the rigid body pose using ICP
    Parameters
    _________
    a_read : np.ndarray
        The xyz coordinates of A body LED markers in tracker coordinates
    b_read : np.ndarray
        The xyz coordinates of B body LED markers in tracker coordinates
    a_tip : np.ndarray
        The xyz coordinates of the tip in tracker coordinates
    a_leds : np.ndarray
        The xyz coordinates of A body LED markers in body coordinates
    b_leds : np.ndarray
        The xyz coordinates of B body LED markers in body coordinates
    vertices : np.ndarray
        The xyz coordinates of the vertices of the surface mesh
    indices : np.ndarray
        The indices of the vertices of the surface mesh
    max_iter : int
        The maximum number of iterations

    Returns
    _________
    np.ndarray
        The xyz coordinates of the pointer tip with respect to rigid body B
    """
    # build Covariance Tree
    ts = np.array([Thang(vertices[indices[i]]) for i in range(len(indices))])
    cov_tree = CovTreeNode(ts, len(ts))

    # initialize variables
    n_iter = 0
    F_reg = Frame(np.eye(3), np.zeros(3))
    thresh = 10
    d_ks = find_rigid_body_pose(a_read, b_read, a_tip, a_leds, b_leds)
    c_ks = np.array([ts[i].corners[0] for i in range(len(ts))])
    # error statistic
    eps_n = [0]
    e_max = [0]
    sig_n = [0]
    # arrays of threshold points
    A = np.array([])
    B = np.array([])
    term_stack = []

    while n_iter < max_iter:
        s_ks = F_reg.compose_transform(d_ks)
        prev_A = len(A)
        prev_B = len(B)
        # find the closest points
        new_c_ks, A, B = match_points(d_ks, c_ks, s_ks, cov_tree, thresh)
        c_ks = new_c_ks
        # compute registration between d_ks and c_ks below the threshold
        F_reg = registration(A, B)
        eps_n_v, e_max_v, sig_n_v = compute_error_stats(F_reg, d_ks, c_ks)
        eps_n.append(eps_n_v)
        e_max.append(e_max_v)
        sig_n.append(sig_n_v)
        n_iter += 1
        print("Iteration: ", n_iter, "Error: ", eps_n[-1])
        thresh = 3 * eps_n[-1]
        # if the number of points below the threshold drops significantly, increase the threshold
        if (len(A) < 0.8 * prev_A) and (len(B) < 0.8 * prev_B):
            thresh = 15 * eps_n[-1]
        # termination conditions
        if eps_n[-1] < 0.005 and e_max[-1] < 0.01 and sig_n[-1] < 0.001:
            break
        # terminate if the error does not drop significantly
        if n_iter > 1:
            change = eps_n[-1]/eps_n[-2]
            if 0.95 < change < 1:
                term_stack.append(change)
            elif len(term_stack) > 1:
                term_stack.pop()
            if len(term_stack) > 10:
                break
    return F_reg, c_ks, d_ks


def match_points(d_ks: np.ndarray, c_ks: np.ndarray, s_ks: np.ndarray, root: CovTreeNode, threshold: float):
    """Method for finding the closest points on the mesh using the previous closest points
    Parameters
    _________
    d_ks : np.ndarray
        The xyz coordinates of the tip in tracker coordinates
    c_ks : np.ndarray
        The estimated xyz coordinates of the vertices of the surface mesh
    s_ks : np.ndarray
        The xyz coordinates of the tip in body coordinates
    root : CovTreeNode
        The root node of the covariance tree
    threshold : float
        The threshold for the distance between the closest points
    """
    A = []
    B = []
    closest = []
    prev_closest = c_ks
    for i, s in enumerate(s_ks):
        bound = np.linalg.norm(s - prev_closest[i])
        value, bound = root.find_closest_point(s, bound, prev_closest[i])
        closest.append(value)
        # If the distance between the closest points is below the threshold, add them to the arrays
        if bound < threshold:
            A.append(d_ks[i])
            B.append(value)
    return np.array(closest), np.array(A), np.array(B)


def compute_error_stats(F_reg: Frame, d_ks: np.ndarray, c_ks: np.ndarray):
    """Method for computing the error statistics
    Parameters
    _________
    F_reg : Frame
        The rigid body transformation between the tip and the surface mesh
    d_ks : np.ndarray
        The xyz coordinates of the tip in tracker coordinates
    c_ks : np.ndarray
        The estimated xyz coordinates of the vertices of the surface mesh
    """
    E = []
    eps_n = 0
    sig_n = 0
    s_ks = F_reg.compose_transform(d_ks)
    # compute the error between the tip and the surface mesh
    for i in range(len(s_ks)):
        E.append((c_ks[i] - s_ks[i]))
    E = np.array(E)
    dot_E = []
    for i in range(len(E)):
        dot_E.append(np.dot(E[i], E[i]))
    for i in range(len(E)):
        eps_n += dot_E[i] ** 0.5
        sig_n += dot_E[i]
    # compute the error statistics
    eps_n = eps_n / len(E)
    e_max = np.max(dot_E) ** 0.5
    sig_n = sig_n ** 0.5 / len(E)
    return eps_n, e_max, sig_n
