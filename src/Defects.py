class Defect:
    def __init__(self, state, x, y, w, h):
        self.state = state
        self.bound_x = x
        self.bound_y = y
        self.bound_w = w
        self.bound_h = h

    def getX(self):
        return self.bound_x

    def getY(self):
        return self.bound_y

    def getW(self):
        return self.bound_w

    def getH(self):
        return self.bound_h

    def getState(self):
        return self.state
