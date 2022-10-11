import numpy
class Frame:

    def __init__(self, R, p):
        self.R = R
        self.p = p

    def composeFrame(self, otherFrame):
        vec = numpy.dot(self.R, otherFrame.p)
        vec += self.p
        mat = numpy.dot(self.R, otheFrame.R)
        return Frame(mat, vec)

    def composeVec(self, v):
        vec = numpy.dot(self.R,v)
        vec+=self.p
        return vec
    
    def invert(self):
        newR = numpy.linalg.inv(self.R)
        newP = numpy.dot(-1*newR, self.p)
        return Frame(newR, newP)
