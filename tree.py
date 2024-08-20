import numpy as np
import matplotlib.pyplot as plt

class TreeNode():
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

class Tree():
    def __init__(self, S0=0, n=1, u=0, d=0, r=0, type='underlying', levels=None):
        self.root = TreeNode(S0) if type == 'underlying' else TreeNode(levels[0][0])
        if type == 'underlying':
            self.build_tree(self.root, n, u, d, {})
        elif type == 'option' or type == 'delta':
            self.build_tree_from_levels(levels)

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

    def build_tree_from_levels(self, levels):
        queue = [(self.root, 0, 0)]  # Initialize a queue with the root node, its depth, and its index
        
        while queue:
            node, depth, index = queue.pop(0)  # Pop the first node from the queue
            
            if depth + 1 in levels and index < len(levels[depth + 1]):
                left_value = levels[depth + 1][index]  # Get the value for the left child node
                node.left = TreeNode(left_value)  # Create the left child node
                queue.append((node.left, depth + 1, index))  # Add the left child node to the queue
            
            if depth + 1 in levels and index + 1 < len(levels[depth + 1]):
                right_value = levels[depth + 1][index + 1]  # Get the value for the right child node
                node.right = TreeNode(right_value)  # Create the right child node
                queue.append((node.right, depth + 1, index + 1))  # Add the right child node to the queue

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