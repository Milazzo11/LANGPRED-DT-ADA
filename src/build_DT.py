"""
Decision tree builder.

:author: Max Milazzo
:email: mam9563@rit.edu
"""


from models import DT, Node
from math import log2


def get_entropy(att_count: int, list_weight_sum: float, total_weight_sum: float) -> float:
    """
    Calculates entropy value using formula.
    """
    
    if len(att_count.keys()) == 1:
        return 0
        
    entropy = 0
        
    for key in att_count:
        att_frac = att_count[key] / list_weight_sum
        entropy += att_frac * log2(1 / att_frac)
        
    entropy *= (list_weight_sum / total_weight_sum)
    
    return entropy


def eval_question(node, question: int) -> tuple:
    """
    Evaluates a question and fetches its entropy.
    """
    
    T_list = []
    F_list = []
    
    for datapoint in node.data:
    # sorts datapoints into true and false lists
    
        if datapoint[0][question]:
            T_list.append(datapoint)
        else:
            F_list.append(datapoint)
            
    T_att_count = {}
    F_att_count = {}
    
    overall_total_weight = 0
    T_total_weight = 0
    F_total_weight = 0
    
    for elem in T_list:
    # gets label counts in true list

        if elem[1] in T_att_count:
            T_att_count[elem[1]] += elem[2]
        else:
            T_att_count[elem[1]] = elem[2]
            
        overall_total_weight += elem[2]
        T_total_weight += elem[2]
            
    for elem in F_list:
    # gets label counts in false list
    
        if elem[1] in F_att_count:
            F_att_count[elem[1]] += elem[2]
        else:
            F_att_count[elem[1]] = elem[2]
            
        overall_total_weight += elem[2]
        F_total_weight += elem[2]
            
    T_entropy = get_entropy(T_att_count, T_total_weight, overall_total_weight)
    F_entropy = get_entropy(F_att_count, F_total_weight, overall_total_weight)
    
    return T_entropy + F_entropy, T_list, F_list


def no_dupes(x: list) -> list:
    """
    Checks if no duplicate values exist in list.
    """
    
    uniques = []
    
    for val in x:
        if val[1] not in uniques:
            uniques.append(val[1])
    
    if len(uniques) == 1:
        return True
        
    return False


def build_DT_rec(node, max_depth: int) -> None:
    """
    Recursively builds DT.
    """

    if len(node.q_list) == 0:
        return
        # no more questions to ask
        
    if node.depth == max_depth:
        return
        # maximum tree depth reached
        
    if no_dupes(node.data):
        return
        # already perfectly categorized
    
    cur_entropy = 1
    
    for question in node.q_list:
        entropy, T_list, F_list = eval_question(node, question)

        if entropy <= cur_entropy:
            cur_entropy = entropy
            cur_question = question
            cur_T_list = T_list
            cur_F_list = F_list

    if len(cur_T_list) == 0 or len(cur_F_list) == 0:
        return
        # can't split data into 2 non-empty sets
    
    node.question = cur_question
    
    node.T_child = Node(
        question=None, depth=node.depth+1, q_list=node.q_list.copy(), data=cur_T_list.copy(),
        T_child=None, F_child=None, pred=None
    )
    
    node.F_child = Node(
        question=None, depth=node.depth+1, q_list=node.q_list.copy(), data=cur_F_list.copy(),
        T_child=None, F_child=None, pred=None
    )
    
    node.T_child.q_list.remove(node.question)
    node.F_child.q_list.remove(node.question)
    
    build_DT_rec(node.T_child, max_depth)
    build_DT_rec(node.F_child, max_depth)


def build_DT(data: list, max_depth: int):
    """
    Calls recursive DT builder.
    """
    
    root = Node(
        question=None, depth=0, q_list=[x for x in range(len(data[0][0]))],
        data=data, T_child=None, F_child=None, pred=None
    )
    
    tree = DT(root)
    build_DT_rec(root, max_depth)
    
    return tree