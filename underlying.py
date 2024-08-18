import yfinance as yf
import numpy as np

class Underlying():
    def __init__(self, ticker, date_from):
        self.ticker = yf.Ticker(ticker)
