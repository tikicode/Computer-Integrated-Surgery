from scipy.stats import special_ortho_group as so
import numpy as np
import pa_three_four.PROGRAMS.cis.frame as fr


def random_r_w_t(n):
    rng = np.random.RandomState(n)
    rot = so.rvs(3)
    rot = np.dot(rot, rot.T)
    trans = rng.rand(1, 3)
    frame = fr.Frame(rot, trans)
    return frame
