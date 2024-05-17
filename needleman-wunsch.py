from functools import wraps



class NeedlemanWunsch:
    def __init__(self, S: str, T: str, m: float=1, M: float=-1, g: float=-1):
        '''
        S: str, the first sequence
        T: str, the second sequence
        m: float, the match score
        M: float, the mismatch score
        g: float, the gap penalty
        '''
        self.S = S
        self.T = T
        self.m = m
        self.M = M
        self.g = g


    def mem(func):
        cache = {}
        @wraps(func)
        def wrap(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        return wrap


    @mem
    def nwRec(self, i: int, j: int) -> float:
        pass

    def nw(self) -> float:
        return self.nwRec(len(self.S), len(self.T))



# Example usage:
if __name__ == '__main__':
    S = 'AGCT'
    T = 'ACTG'
    nw = NeedlemanWunsch(S, T, m=1, M=-1, g=-1)
    print(nw.nw())
