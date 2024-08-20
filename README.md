# Pricing Options with Binary Trees

## Overview
In this project we implement the well know binomial tree pricing model for European options. We allow for pricing of both puts and calls, as well as computation of the delta of a contract at each step. The price trees and delta tree can also be visualised.

The mathematics in this project is following the well known 'Options, Futures and Other Derivatives' (Chapter 12) by John C. Hull. The book in fact served as the inspiration for the undertaking of the project.

Please note that the implementation of the model here is by no means the most efficient as the possible future prices of the underlying asset are stored using a propriatry tree data structure. The decision to do this and not follow a standard implementation was mostly to gain some exposure to designing ones own data structure.

## Classes
### Option:
* Define a contract with `Option(S0, K, T, vol, r, n, option_type='call')`
    * `S0` - Current price of underlying asset.
    * `K` - Strike price.
    * `T` - Time to expiry (years).
    * `vol` - Volatility of the underlying (as a decimal i.e. 0.2).
    * `r` - Risk free rate (as a decimal).
    * `n` - Number of steps in tree (determines time grid).
    * `option_type` - 'put' or 'call'.
* When initialised contract will automatically generate an instance of `Underlying` representing the asset, a tree of its own prices and a tree of delta values. Note these are stored as a level order traversal.
    * `underlying_tree`
    * `price_tree`
    * `delta_tree`
* Trees can be visualised with `plot_tree`. Specify tree type as `option`, `delta` or `underlying`.

### Underlying:
* Define an asset with `Underlying(S0, T, n, vol, r)`.
    * `S0` - Current price of underlying asset.
    * `T` - Time to expiry of option (years).
    * `n` - Number of steps in tree (determines time grid).
    * `vol` - Volatility of the underlying (as a decimal i.e. 0.2).
    * `r` - Risk free rate (as a decimal).
* Currently has no functionality other than representing an asset. This may change in future.

### Tree
* Define a tree as `Tree(S0, n, u, d)`.
    * `S0` - Current price of underlying asset.
    * `n` - Number of levels in tree.
    * `u` - Price rise factor.
    * `d` - Price fall factor.
* When initialised a tree is generated recursively using `build_tree`.
* Note that as of current the only purpose of this class is to represent a tree of possible stock prices, thus it is very minimal in nature.

## Looking Forward:
It is obvious that much can be optimised here, but as mentioned above this project is not about the 'best' implementation, instead it is something I have done to better understand options and some of the mathematics surrounding them.

In future I may come back to this and include further features such as a dashboard, generation of a hedging strategy based upon a sample price path of the underlying asset and fitting an option to some real data. Any comments or further suggestions are certainly welcome.
