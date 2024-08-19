from tree import Tree
import yfinance as yf
import numpy as np

class Underlying():
    def __init__(self, S0, T, n, vol, r):
        self.dt = T / n
        self.a = np.round(np.exp(r * self.dt), 4)
        self.u = np.round(np.exp(vol * np.sqrt(self.dt)), 4)
        self.d = np.round(np.exp(-vol * np.sqrt(self.dt)), 4)
        self.p = (self.a - self.d) / (self.u - self.d)
        self.tree = Tree(S0, n, self.u, self.d, self.a, type='underlying')