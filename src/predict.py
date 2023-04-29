"""
Makes predictions using an existing model.

:author: Max Milazzo
:email: mam9563@rit.edu
"""


import sys
import string
import pickle
from attributes import get_atts


def main(args: list) -> None:
    """
    Program entry point.
    """
    
    with open(args[0], "rb") as f:
        model = pickle.load(f)
        # load model
        
    with open(args[1], "r") as f:
        for words in f:
            words = words.lower()
            words = words.translate(str.maketrans("", "", string.punctuation))
            word_list = words.split()
            # formats each line
            
            atts = get_atts(word_list)
            print(model.run(atts))
            # runs model on line and displays result


if __name__ == "__main__":
    num_args = 3
    args = sys.argv
    # gets arguments and defines expected argument length
    
    if len(args) == num_args:
        main(args[1:])
        # calls main with command line arguments
        
    else:
        print("usage: py predict.py <hypothesis> <file>")