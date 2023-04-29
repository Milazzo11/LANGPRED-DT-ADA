"""
AdaBoost forest builder.

:author: Max Milazzo
:email: mam9563@rit.edu
"""


from models import ADA
from build_DT import build_DT
from math import log


def update_weights(tree) -> tuple:
    """
    Updates data weights and get tree hypothesis weight.
    """
    
    T_data = tree.root.T_child.data
    F_data = tree.root.F_child.data
    
    T_label = tree.get_guess(tree.root.T_child)
    F_label = tree.get_guess(tree.root.F_child)
    
    err = 0
    
    for x in range(len(T_data)):
        if T_data[x][1] != T_label:
            err += T_data[x][2]
            
            T_data[x][2] *= -1
            # temporarily marks incorrectly labelled datapoints as negative so
            # they can be recognized without altering magnitute or needing
            # to rerun the tree
            
    for x in range(len(F_data)):
        if F_data[x][1] != F_label:
            err += F_data[x][2]
            
            F_data[x][2] *= -1
            # temporarily marks incorrectly labelled datapoints as negative so
            # they can be recognized without altering magnitute or needing
            # to rerun the tree
            
    data = T_data + F_data 
    update = err / (1 - err)
    weight_sum = 0

    for x in range(len(data)):
        if data[x][2] < 0:
            data[x][2] *= -1
            # undoes negation of incorrect values
            
        else:
            data[x][2] *= err
            
        weight_sum += data[x][2]
        
    norm_mult = 1 / weight_sum
    
    for x in range(len(data)):
        data[x][2] *= norm_mult
        
    return data, log((1 - err) / err)
    # returns updated data and hypothesis weight


def build_ADA(data: list, pos_label: str, neg_label: str, num_trees: int):
    """
    Builds ADA object.
    """
    
    forest = ADA(pos_label, neg_label, num_trees)
    
    for _ in range(num_trees):
        new_tree = build_DT(data, 1)
        data, hypothesis_weight = update_weights(new_tree)
        
        forest.add_tree(new_tree, hypothesis_weight)
        
    return forest