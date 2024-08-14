import tree
from collections import defaultdict

class Option():
    def __init__(self, S0, K, r, T, u, d, type='call'):
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.u = u
        self.d = d
        self.p = (self.r - self.d) / (self.u - self.d)
        self.type = type
        self.tree = tree.Tree(S0, T, u, d, r)
        self.option_price = self.calculate_option_price()[0][0]

    def payoff(self, S):
        if self.type == 'call':
            return max(S - self.K, 0)
        elif self.type == 'put':
            return max(self.K - S, 0)
    
    def calculate_option_price(self):
        levels = self.tree.get_tree_levels(self.tree.root)
        max_depth = max(levels.keys())
        # option_values = {max_depth: [self.p * self.payoff(levels[max_depth][i+1]) + (1 - self.p) * self.payoff(levels[max_depth][i]) for i in range(len(levels[max_depth])-1)]}
        option_values = {max_depth: [self.payoff(S) for S in levels[max_depth]]}

        for depth in range(max_depth - 1, -1, -1):
            option_values[depth] = []
            for i in range(len(levels[depth])):
                option_values[depth].append((self.p * option_values[depth + 1][i+1] + (1 - self.p) * option_values[depth + 1][i]))
        
        # for k, v in option_values.items():
        #     print(k, v)

        return option_values