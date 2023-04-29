"""
DT and ADA model types, as well as the Node type used by both.

:author: Max Milazzo
:email: mam9563@rit.edu
"""


from dataclasses import dataclass
from typing import Union


@dataclass
class Node:
    """
    DT node.
    """
    
    question: Union[int, None]
    depth: int
    q_list: list
    data: list
    # node data
    
    T_child: Union["Node", None]
    F_child: Union["Node", None]
    # children nodes
    
    pred: Union[str, None]
    # final prediction

    
class DT:
    def __init__(self, root: Node):
        self.root = root
    
    
    def get_guess(self, node):
        """
        Gets a DT guess given a node of data.
        """
        
        if node.pred is not None:
            return node.pred
        
        label_dict = {}
        
        for val in node.data:
            if val[1] in label_dict:
                label_dict[val[1]] += 1
            else:
                label_dict[val[1]] = 1
                
        max_val = 0
        guess = None
        
        for key in label_dict:
            if label_dict[key] > max_val:
                max_val = label_dict[key]
                guess = key
                
        node.pred = guess
        return guess


    def _rec_run(self, node, atts):
        """
        Recursively runs through DT.
        """
        
        if node.question is None:
            return self.get_guess(node)
        
        if atts[node.question]:
            return self._rec_run(node.T_child, atts)
        else:
            return self._rec_run(node.F_child, atts)
    
        
    def run(self, atts):
        """
        Runs DT.
        """
        
        return self._rec_run(self.root, atts)   
        
        
    def eval(self, test_set):
        """
        Evaluates DT performance.
        """
        
        total = 0
        success = 0
        
        for datapoint in test_set:
            if datapoint[1] == self.run(datapoint[0]):
                success += 1
            
            total += 1
        
        return success / total
    
    
    def _minimize_rec(self, node):
        """
        Recursively clears extra data used in model building process.
        """
        
        if node.question is None:
            self.get_guess(node)
        
        node.data.clear()
        node.q_list.clear()
        
        if node.T_child is not None:
            self._minimize_rec(node.T_child)
            
        if node.F_child is not None:
            self._minimize_rec(node.F_child)
    
        
    def minimize(self):
        """
        Minimizes data usage for object.
        """
        
        self._minimize_rec(self.root)


class ADA:
    def __init__(self, pos_label, neg_label, num_trees):
        self.pos_label = pos_label
        self.neg_label = neg_label
        self.num_trees = num_trees
        
        self.forest = []
        self.hypothesis_weights = []
        # DT trees in forest map to hypothesis weights of the same index
        
    
    def add_tree(self, tree, hypothesis_weight):
        """
        Adds tree to forest and stores its hypothesis weight.
        """
        
        self.forest.append(tree)
        self.hypothesis_weights.append(hypothesis_weight)


    def run(self, atts):
        """
        Runs ADA.
        """
        
        prediction = 0
        
        for x in range(self.num_trees):
            res = self.forest[x].run(atts)
            
            if res == self.pos_label:
                prediction += self.hypothesis_weights[x]
            else:
                prediction -= self.hypothesis_weights[x]
            
        if prediction > 0:
            return self.pos_label
        else:
            return self.neg_label
        
    
    def eval(self, test_set):
        """
        Evaluates ADA performance.
        """
        
        total = 0
        success = 0
        
        for datapoint in test_set:
            if datapoint[1] == self.run(datapoint[0]):
                success += 1
            
            total += 1
        
        return success / total
        
        
    def minimize(self):
        """
        Minimizes data usage for object.
        """
        
        for x in range(len(self.forest)):
            self.forest[x].minimize()