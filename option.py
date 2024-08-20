import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.sparse import lil_matrix
from underlying import Underlying

class Option():
    def __init__(self, S0, K, T, vol, r, n, option_type='call',):
        self.underlying = Underlying(S0, T, n, vol, r)
        self.type = option_type
        self.K = K
        self.T = T
        self.r = r
        self.n = n

        # Trees represented by level order traversal here
        self.underlying_tree = self.underlying.tree.get_tree_levels(self.underlying.tree.root)
        self.price_tree = self.calculate_option_prices()
        self.delta_tree = self.calculate_option_deltas()

    def payoff(self, S):
        if self.type == 'call':
            return max(S - self.K, 0)
        elif self.type == 'put':
            return max(self.K - S, 0)
    
    def calculate_option_prices(self):
        p = self.underlying.p
        levels = self.underlying_tree
        max_depth = max(levels.keys())

        option_values = {max_depth: [self.payoff(S) for S in levels[max_depth]]}

        for depth in range(max_depth - 1, -1, -1):
            option_values[depth] = []
            for i in range(len(levels[depth])):
                option_values[depth].append((p * option_values[depth + 1][i+1] + (1 - p) * option_values[depth + 1][i]))

        option_values[0][0] = option_values[0][0] * np.exp(-self.r * self.T)

        return option_values
    
    def calculate_option_deltas(self):
        option_levels = self.price_tree
        price_levels = self.underlying_tree
        max_depth = max(option_levels.keys())

        option_deltas = defaultdict(list)
        
        for depth in range(max_depth, -1, -1):
            for i in range(len(option_levels[depth]) - 1):
                option_deltas[depth-1].append((option_levels[depth][i+1] - option_levels[depth][i]) / (price_levels[depth][i+1] - price_levels[depth][i]))

        return option_deltas
    
    def plot_tree(self, type):
        nb_steps = self.n

        levels = None
        if type == 'option':
            levels = self.price_tree
        elif type == 'delta':
            levels = self.delta_tree
            nb_steps -= 1
        elif type == 'underlying':
            levels = self.underlying_tree
        
        mat = lil_matrix((nb_steps+1, nb_steps*2+1), dtype = np.float32)
        
        for i in range(nb_steps+1):
            value = levels[i]
            rows = np.zeros(i+1, dtype=np.int16) + i
            cols = np.arange(i+1)*2+nb_steps-i
            mat[rows, cols] = value
        
        fig = plt.figure(figsize=[5, 5])
        
        plt.axis('off')
        plt.title(f'{type.title()} Tree')
        
        for i in range(nb_steps):
            x = (np.arange(3 + i*2) % 2 == 0) + i
            y = np.arange(0, 2*(i+1)+1) - 1 + (nb_steps-i)
            v = mat[x, y].toarray()[0]
            plt.plot(x, v, 'bo-')
        
            for xi, vi in zip(x, v):
                plt.text(xi, vi, f'{vi:.2f}', fontsize=8, ha='center', va='bottom')
        