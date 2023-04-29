"""
Takes a formatted dataset and creates a data list.

:author: Max Milazzo
:email: mam9563@rit.edu
"""


import string
from attributes import get_atts
from random import random


LIST_LEN = 15
# required word list length


TEST_SET_SIZE = 0.1
# fractional size of test set
# (10% chance of any piece of data is moved to the test set)


def set_default_weights(train_set: list) -> list:
    """
    Sets default weights for training set such that they sum to 1.
    """
    
    weight = 1 / len(train_set)
    
    for x in range(len(train_set)):
        train_set[x].append(weight)
        train_set[x] = train_set[x]
        
    return train_set


def train_test_split(data: list) -> tuple:
    """
    Splits training and testing data.
    """
    
    train_set = []
    test_set = []
    
    for elem in data:
        if random() < TEST_SET_SIZE:
            test_set.append(elem)
        else:
            train_set.append(elem)
    
    return train_set, test_set
    

def build_data(file: str) -> list:
    """
    Builds data list from file.
    """
    
    data = []
    
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            word_split = line.split("|")
            
            words = word_split[1]
            words = words.lower()
            words = words.translate(str.maketrans("", "", string.punctuation))
            # properly formats words
            
            word_list = words.split()
            
            if len(word_list) != LIST_LEN:
                continue
                
            atts = get_atts(word_list)
            data.append([atts, word_split[0]])
            # gets attributes and formats in data list
            
    return data