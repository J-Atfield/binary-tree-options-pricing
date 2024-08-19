import numpy as np
from underlying import Underlying

class Option():
    def __init__(self, S0, K, T, vol, r, n, option_type='call',):
        self.underlying = Underlying(S0, T, n, vol, r) # has S0, 
        self.type = option_type
        self.K = K
        self.T = T
        self.r = r
        self.n = n
        self.price = self.calculate_option_price()

    def payoff(self, S):
        if self.type == 'call':
            return max(S - self.K, 0)
        elif self.type == 'put':
            return max(self.K - S, 0)
    
    def calculate_option_price(self):
        p = self.underlying.p
        levels = self.underlying.tree.get_tree_levels(self.underlying.tree.root)
        max_depth = max(levels.keys())

        option_values = {max_depth: [self.payoff(S) for S in levels[max_depth]]}

        for depth in range(max_depth - 1, -1, -1):
            option_values[depth] = []
            for i in range(len(levels[depth])):
                option_values[depth].append((p * option_values[depth + 1][i+1] + (1 - p) * option_values[depth + 1][i]))

        return option_values[0][0] * np.exp(-self.r * self.T)