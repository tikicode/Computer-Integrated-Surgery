import numpy as np
class Frame:

    '''Constructor to create a Frame object which has Rotation R and translation p'''
    def __init__(self, R, p):
        self.R = R
        self.p = p

    '''Method to perform a composition between two frames
    parameters: two frames
    returns: frame of F1 @ F2
    '''
    def composeFrame(self, otherFrame):
        vec = np.dot(self.R, otherFrame.p)
        vec += self.p
        mat = np.dot(self.R, otherFrame.R)
        return Frame(mat, vec)

    '''Method to perform a Frame transformation
    parameters: frame and a vector/pointset
    returns: new vector/pointset after transformation of the original vector/pointset
    '''
    def composeVec(self, v):
        vec = np.dot(self.R,v)
        vec+=self.p
        return vec
    
    '''Method to calculate the inverse of a Frame'''
    def invert(self):
        newR = np.linalg.inv(self.R)
        newP = np.dot(-1*newR, self.p)
        return Frame(newR, newP)
