import numpy as np
from collections import defaultdict
from underlying import Underlying
from tree import Tree

class Option():
    def __init__(self, S0, K, T, vol, r, n, option_type='call',):
        self.underlying = Underlying(S0, T, n, vol, r) # has S0, 
        self.type = option_type
        self.K = K
        self.T = T
        self.r = r
        self.n = n
        self.price_tree = self.calculate_option_prices() # Tree(type='option', levels=self.calculate_option_prices())
        self.delta_tree = self.calculate_option_deltas() # Tree(type='delta', levels=self.calculate_option_deltas())

    def payoff(self, S):
        if self.type == 'call':
            return max(S - self.K, 0)
        elif self.type == 'put':
            return max(self.K - S, 0)
    
    def calculate_option_prices(self):
        p = self.underlying.p
        levels = self.underlying.tree.get_tree_levels(self.underlying.tree.root)
        max_depth = max(levels.keys())

        option_values = {max_depth: [self.payoff(S) for S in levels[max_depth]]}

        for depth in range(max_depth - 1, -1, -1):
            option_values[depth] = []
            for i in range(len(levels[depth])):
                option_values[depth].append((p * option_values[depth + 1][i+1] + (1 - p) * option_values[depth + 1][i]))

        option_values[0][0] = option_values[0][0] * np.exp(-self.r * self.T)

        return option_values #[0][0] * np.exp(-self.r * self.T)
    
    def calculate_option_deltas(self):
        option_levels = self.price_tree
        price_levels = self.underlying.tree.get_tree_levels(self.underlying.tree.root)
        max_depth = max(option_levels.keys())

        option_deltas = defaultdict(list)
        
        for depth in range(max_depth, -1, -1):
            for i in range(len(option_levels[depth]) - 1):
                option_deltas[depth-1].append((option_levels[depth][i+1] - option_levels[depth][i]) / (price_levels[depth][i+1] - price_levels[depth][i]))

        return option_deltas

        