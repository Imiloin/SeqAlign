class SmithWaterman:
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

    def alignment_matrix(self) -> 'list[list[float]]':
        matrix = [[0 for _ in range(len(self.T)+1)] for _ in range(len(self.S)+1)]
        for i in range(1, len(self.S)+1):
            for j in range(1, len(self.T)+1):
                match = self.m if self.S[i-1] == self.T[j-1] else self.M
                matrix[i][j] = max(
                    0,
                    matrix[i-1][j-1] + match,
                    matrix[i-1][j] + self.g,
                    matrix[i][j-1] + self.g
                )
        return matrix

    def sw(self) -> float:
        matrix = self.alignment_matrix()
        return max(max(row) for row in matrix)



# Example usage:
if __name__ == '__main__':
    S = 'AGGGCT'
    T = 'AGGCA'
    sw = SmithWaterman(S, T, m=2, M=-2, g=-3)
    print(sw.sw())
    print(sw.alignment_matrix())
