

class CovTreeNode:
    def __init__(self, F, UB, LB, have_subtrees, n_things, subtrees, things):
        self.F = F
        self.UB = UB
        self.LB = LB
        self.have_subtrees = have_subtrees
        self.n_things = n_things
        self.subtrees = subtrees
        self.things = things

    def CovTreeNode(self, Ts, nT):
        self.things = Ts
        self.n_things = nT
        self.F = compute_cov_frame(Ts, nT)
        [self.UB, self.LB] = compute_cov_bounds(Ts, nT, self.F)
        construct_subtrees(self)

    def compute_cov_bounds(F, Ts, nT):
        
