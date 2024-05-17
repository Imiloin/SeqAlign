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
        if i == 0 and j == 0:
            return 0
        elif i == 0:
            return j * self.g
        elif j == 0:
            return i * self.g
        else:
            match = self.m if self.S[i-1] == self.T[j-1] else self.M
            return max(
                self.nwRec(i-1, j-1) + match,
                self.nwRec(i-1, j) + self.g,
                self.nwRec(i, j-1) + self.g
            )

    def nw(self) -> float:
        return self.nwRec(len(self.S), len(self.T))

    def alignment_matrix(self) -> 'list[list[float]]':
        matrix = [[0 for _ in range(len(self.T)+1)] for _ in range(len(self.S)+1)]
        for i in range(len(self.S)+1):
            matrix[i][0] = i * self.g
        for j in range(len(self.T)+1):
            matrix[0][j] = j * self.g
        for i in range(1, len(self.S)+1):
            for j in range(1, len(self.T)+1):
                match = self.m if self.S[i-1] == self.T[j-1] else self.M
                matrix[i][j] = max(
                    matrix[i-1][j-1] + match,
                    matrix[i-1][j] + self.g,
                    matrix[i][j-1] + self.g
                )
        return matrix



# Example usage:
if __name__ == '__main__':
    S = 'AGGGCT'
    T = 'AGGCA'
    nw = NeedlemanWunsch(S, T, m=2, M=-2, g=-3)
    print(nw.nw())
    print(nw.alignment_matrix())
