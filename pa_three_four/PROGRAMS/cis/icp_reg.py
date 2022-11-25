import numpy as np
from .frame import Frame
from .icp import find_rigid_body_pose
from .thang import Thang
from .cov_tree import CovTreeNode
from .registration import registration
import time


def ICP(a_read, b_read, a_tip, a_leds, b_leds, vertices, indices, max_iter):
    # Build Covariance Tree
    ts = np.array([Thang(vertices[indices[i]]) for i in range(len(indices))])
    cov_tree = CovTreeNode(ts, len(ts))

    # Initialize variables
    n_iter = 0
    F_reg = Frame(np.eye(3), np.zeros(3))
    thresh = 100
    d_ks = find_rigid_body_pose(a_read, b_read, a_tip, a_leds, b_leds)
    c_ks = np.array([ts[i].corners[0] for i in range(len(ts))])
    # Error Statistic
    eps_n = [0]
    A = np.array([])
    B = np.array([])
    term_stack = []

    while n_iter < max_iter:
        s_ks = F_reg.compose_transform(d_ks)
        prev_A = len(A)
        prev_B = len(B)
        new_c_ks, A, B = match_points(d_ks, ts, s_ks, cov_tree, thresh)
        c_ks = new_c_ks
        F_reg = registration(A, B)
        eps_n.append(compute_error_stats(F_reg, A, B))
        n_iter += 1
        print("Iteration: ", n_iter, "Error: ", eps_n[-1])
        thresh = 3 * eps_n[-1]
        if (len(A) < 0.5 * prev_A) and (len(B) < 0.5 * prev_B):
            thresh = 15 * eps_n[-1]
        if eps_n[-1] < 0.005:
            break
        if n_iter > 1:
            change = eps_n[-1]/eps_n[-2]
            if 0.95 < change < 1:
                term_stack.append(change)
            elif len(term_stack) > 1:
                term_stack.pop()
            if len(term_stack) > 5:
                break
    return F_reg, c_ks, d_ks


def match_points(d_ks, ts, s_ks, root, threshold):
    A = []
    B = []
    closest = []
    prev_closest = ts[0].corners[0]
    for i, s in enumerate(s_ks):
        bound = np.linalg.norm(s - prev_closest)
        st_s = time.time()
        value = root.find_closest_point(s, bound, prev_closest)
        et_s = time.time()
        print("Search Time: ", i, et_s - st_s)
        closest.append(value)
        if np.linalg.norm(value - s) < threshold:
            A.append(d_ks[i])
            B.append(value)
        prev_closest = closest[-1]
    return np.array(closest), np.array(A), np.array(B)


def compute_error_stats(F_reg: Frame, A: np.ndarray, B: np.ndarray):
    E = []
    eps_n = 0
    A_new = F_reg.compose_transform(A)
    for i in range(len(A)):
        E.append((B[i] - A_new[i]))
    E = np.array(E)
    for i in range(len(E)):
        eps_n += np.dot(E[i], E[i]) ** 0.5
    eps_n = eps_n / len(E)
    return eps_n
