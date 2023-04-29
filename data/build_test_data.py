"""
Builds dataset from article files.

:author: Max Milazzo
:email: mam9563@rit.edu
"""


WORD_COUNT = 15
# defines the number of words per datapoint


DATASET_FILE = "data.txt"
# dataset file to append to


def file_loop(file: str, label: str) -> None:
    """
    Loops through files and writes data.
    """
    
    with open(file, "r", encoding="utf8") as f:
        data = f.read()
        
    words = data.split()
    cur_word = 0
    words_str = ""
    
    with open(DATASET_FILE, "a", encoding="utf8") as f:
        for word in words:
            if cur_word == WORD_COUNT:
                f.write(label + "|" + words_str.strip() + "\n")
                
                words_str = ""
                cur_word = 0
                
            words_str += word + " "
            cur_word += 1 


def main() -> None:
    """
    Program entry point.
    """
    
    file = input("input raw data filename\n> ")
    label = input("input data label\n> ")
    
    file_loop(file, label)


if __name__ == "__main__":
    main()