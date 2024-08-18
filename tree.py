import numpy as np
import matplotlib.pyplot as plt

class TreeNode():
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

class Tree():
    def __init__(self, S0, n=1, u=0, d=0, r=0):
        self.root = TreeNode(S0)
        self.build_tree(self.root, n, u, d, {})

    def build_tree(self, root, periods, u, d, nodes_cache):
        if periods == 0:
            return
        
        # Calculate values for the right (up) and left (down) nodes
        up_value = root.val * u
        down_value = root.val * d
        
        # Create or retrieve the right node
        tolerance = 1e-5

        # Create or retrieve the right node
        found_right = False
        for value, node in nodes_cache.items():
            if abs(up_value - value) <= tolerance:
                root.right = node
                found_right = True
                break

        if not found_right:
            root.right = TreeNode(up_value)
            nodes_cache[up_value] = root.right

        # Create or retrieve the left node
        found_left = False
        for value, node in nodes_cache.items():
            if abs(down_value - value) <= tolerance:
                root.left = node
                found_left = True
                break

        if not found_left:
            root.left = TreeNode(down_value)
            nodes_cache[down_value] = root.left

        # Recursively build the tree for the right and left nodes
        self.build_tree(root.right, periods - 1, u, d, nodes_cache)
        self.build_tree(root.left, periods - 1, u, d, nodes_cache)

    def get_tree_levels(self, node, depth=0, levels=None):
        if levels is None:
            levels = {}
        
        if depth not in levels:
            levels[depth] = []  # Using a list instead of a set
        
        if node.val not in levels[depth]:  # Check if the value already exists in the list
            levels[depth].append(node.val)  # Append the value to the list
        
        if node.left is not None:
            self.get_tree_levels(node.left, depth + 1, levels)
        
        if node.right is not None:
            self.get_tree_levels(node.right, depth + 1, levels)
        
        return levels

    def print_text_tree(self):
        levels = self.get_tree_levels(self.root)
        max_depth = max(levels.keys())
        
        for depth in range(max_depth + 1):
            level = sorted(levels[depth])  # Sort the levels to maintain order
            indent = " " * (2 ** (max_depth - depth) - 1)
            spacing = " " * (2 ** (max_depth - depth + 1) - 1)
            line = indent + spacing.join(f"{v:.2f}" for v in level)
            print(line)
            print("\n" * (2 ** (max_depth - depth) - 1))

    def count_nodes(self):
        unique_nodes = set()

        def traverse_and_count(node):
            if node is None or node.val in unique_nodes:
                return
            unique_nodes.add(node.val)
            traverse_and_count(node.left)
            traverse_and_count(node.right)

        traverse_and_count(self.root)
        return len(unique_nodes)

# u, d = np.round(np.exp(0.1*np.sqrt(1/3)), 4), np.round(np.exp(-0.1*np.sqrt(1/3)), 4)
# # floating point and rounding is the killer
# tree = Tree(100, 3, u, d, 0)
# print(tree.count_nodes())

# idea: traverse left and right subtree post order but when reaching root instead of 'visiting' compute its new value as root.left*down_prob + root.right*up_prob