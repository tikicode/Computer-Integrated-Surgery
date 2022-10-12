import numpy as np


class Frame:
    def __init__(self, R, p):
        self.R = R
        self.p = p

    def composeFrame(self, otherFrame):
        vec = np.dot(self.R, otherFrame.p)
        vec += self.p
        mat = np.dot(self.R, otherFrame.R)
        return Frame(mat, vec)

    def composeVec(self, v):
        vec = np.dot(self.R, v)
        vec += self.p
        return vec

    def invert(self):
        newR = np.linalg.inv(self.R)
        newP = np.dot(-1 * newR, self.p)
        return Frame(newR, newP)
