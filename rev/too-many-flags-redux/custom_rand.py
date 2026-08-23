from secrets import randbelow

class SemiPRand:
    def __init__(self, seed=None):
        if(isinstance(seed, int)):
            self.curr = seed
        else:
            self.curr = randbelow(50000)
        self.mod = 18541 * 77351

    def next(self, max=None):
        self.curr = (self.curr**2) % self.mod
        if(isinstance(max, int)):
            return self.curr % max
        else:
            return self.curr
