import numpy as np
from .frame import Frame
from .thang import Thang


class CovTreeNode:
    """Class used to represent Covariance Tree Functions

    ...

    Attributes
    ________
    things : np.ndarray
        A representation of a subtree of the surface mesh of an object
    n_things : int
        Number of things in the subtree
    F : Frame
        The frame of the covariance tree node
    UB : np.ndarray
        The upper bound of the covariance tree node
    LB : np.ndarray
        The lower bound of the covariance tree node
    subtrees : CovTreeNode
        The subtrees of the covariance tree node
    have_subtrees : bool
        Whether the covariance tree node has subtrees
    """

    def __init__(self, ts: np.array, n_t: int):
        """
        Parameters
        _________
        self : CovTreeNode
            A node in the covariance tree
        ts : np.ndarray
            The triangles of the covariance tree node
        n_t : int
            The number of triangles in the covariance tree node
        """
        self.things = ts
        self.n_things = n_t
        self.F = self.compute_cov_frame(ts)
        self.UB, self.LB = self.compute_cov_bounds(ts, n_t)
        self.left, self.right, self.have_subtrees = self.construct_subtrees(n_t, 25, 1)

    def compute_cov_bounds(self, ts: np.ndarray, n_t: int):
        """Method for computing the covariance bounds of a node

        Parameters
        _________
        self : CovTreeNode
            A node in the covariance tree
        ts : np.ndarray
            The triangles of the covariance tree node
        n_t : int
            The number of triangles in the covariance tree node

        Returns
        _________
        UB : np.ndarray
            The upper bound of the covariance tree node
        LB : np.ndarray
            The lower bound of the covariance tree node
        """
        UB = self.F.invert().compose_transform(ts[0].sort_point().reshape(1, 3))
        LB = self.F.invert().compose_transform(ts[0].sort_point().reshape(1, 3))
        # compute the minimum and maximum bounds of the triangle points
        for i in range(n_t):
            LB, UB = ts[i].enlarge_bounds(self.F, LB, UB)
        return UB, LB

    def compute_cov_frame(self, ts: np.ndarray):
        """Method for computing the frame transform to the local frame of the node

        Parameters
        _________
        self : CovTreeNode
            A node in the covariance tree
        ts : np.ndarray
            The triangles of the covariance tree node

        Returns
        _________
        Frame
            The covariance frame of the node
        """
        points = np.array([ts[i].sort_point() for i in range(len(ts))])
        n_p = len(points)
        centroid = np.mean(points, axis=0)
        A = np.zeros((3, 3))
        # compute the covariance matrix
        for i in range(n_p):
            A += np.outer(points[i] - centroid, points[i] - centroid)
        u, s, vt = np.linalg.svd(A)

        # prepare these results of SVD, u and v, to find the
        # transformation matrix done on line 71
        u = u.T
        vt = vt.T
        # validate result and account for any potential issues by checking the determinant
        comp_size = vt.shape[0]
        reflection_comp = np.eye(comp_size)
        reflection_comp[comp_size - 1][comp_size - 1] = np.linalg.det(np.dot(vt, u))
        # find the transformation matrix R and the corresponding translation vector
        R = np.dot(vt, np.dot(reflection_comp, vt))
        p = centroid
        # return the frame for the point cloud transformation
        return Frame(R, p)

    def construct_subtrees(self, n_t: int, min_count: int, min_diag: int):
        """Method for constructing the subtrees of a node

        Parameters
        _________
        self : CovTreeNode
            A node in the covariance tree
        n_t : int
            The number of triangles in the covariance tree node
        min_count : int
            The minimum number of triangles in a subtree
        min_diag : int
            The minimum diagonal of a subtree

        Returns
        _________
        left : CovTreeNode
            The left subtree of the covariance tree node
        right : CovTreeNode
            The right subtree of the covariance tree node
        have_subtrees : bool
            Whether the covariance tree node has subtrees
        """
        if n_t <= min_count or np.linalg.norm(self.UB - self.LB) <= min_diag:
            return None, None, False
        left_tree, right_tree = self.split_sort(n_t)
        # check end condition to stop splits if all points are added to one side or the other
        if len(left_tree) == n_t or len(right_tree) == n_t:
            return None, None, False
        left, right = CovTreeNode(left_tree, len(left_tree)), CovTreeNode(right_tree, len(right_tree))
        return left, right, True

    def split_sort(self, n_t: int):
        """Method for dividing the triangles of a node into two subtrees

        Parameters
        _________
        self : CovTreeNode
            A node in the covariance tree
        n_t : int
            The number of triangles in the covariance tree node

        Returns
        _________
        left_tree : np.ndarray
            The triangles in the left subtree
        right_tree : np.ndarray
            The triangles in the right subtree
        """
        left_tree, right_tree = [], []
        ts = self.things
        for i in range(n_t):
            # transform triangle corners into the frame of the node
            if self.F.invert().compose_transform(ts[i].sort_point().reshape(1, 3))[0][0] < 0:
                left_tree.append(ts[i])
            else:
                right_tree.append(ts[i])
        return np.array(left_tree), np.array(right_tree)

    def find_closest_point(self, v: np.ndarray, bound: float, closest: np.ndarray):
        """Method for finding the closest point to a given point

        Parameters
        _________
        self : CovTreeNode
            A node in the covariathnce tree
        v : np.ndarray
            The point to find the closest point to
        bound : float
            The current closest distance
        closest : np.ndarray
            The current closest point

        Returns
        _________
        bound : float
            The closest distance
        closest : np.ndarray
            The closest point
        """
        # convert the point to the frame of the node
        v_local = self.F.invert().compose_transform(v.reshape(1, 3))
        # check if the point is in the bounds of the node
        for i in range(3):
            if v_local[0, i] > self.UB[0, i] + bound or v_local[0, i] < self.LB[0, i] - bound:
                return
        if self.have_subtrees:
            # if the x value is less than -bound, search the left subtree
            if v_local[0, 0] < -bound:
                return self.left.find_closest_point(v, bound, closest)
            elif v_local[0, 0] > bound:
                return self.right.find_closest_point(v, bound, closest)
            # if the x value is greater than bound, search the right subtree
            else:
                left = self.left.find_closest_point(v, bound, closest)
                right = self.right.find_closest_point(v, bound, closest)
                if left is not None and right is None:
                    return left
                elif left is None and right is not None:
                    return right
                elif left is None and right is None:
                    return closest
                else:
                    return min(left, right, key=lambda x: np.linalg.norm(x - v))
        # if the node has no subtrees, search the triangles for the closest point
        else:
            for i in range(self.n_things):
                bound, closest = self.update_closest(self.things[i], v, bound, closest)
            return closest

    def update_closest(self, t: Thang, v: np.ndarray, bound: float, closest: np.ndarray):
        """Method for updating the closest point to a given point

        Parameters
        _________
        self : CovTreeNode
            A node in the covariance tree
        t : Thang
            The triangle to check for the closest point
        v : np.ndarray
            The point to find the closest point to
        bound : float
            The current closest distance
        closest : np.ndarray
            The current closest point

        Returns
        _________
        bound : float
            The distance to the closest point
        closest : np.ndarray
            The closest point
        """
        cp = t.closest_point_to(v)
        dist = np.linalg.norm(cp - v)
        # If this distance is below the bound, set cp as the new closest
        if dist < bound:
            return dist, cp
        return bound, closest

