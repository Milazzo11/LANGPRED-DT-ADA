"""
Generates attribute list.

:author: Max Milazzo
:email: mam9563@rit.edu
"""


NUM_ATTS = 12
# number of attributes to test for
    
    
def avg_len_check(words: list) -> bool:
    """
    Check for attribute 11.
    """
    
    len_total = 0
    
    for word in words:
        len_total += len(word)
    
    if (len_total / len(words)) < 5:
        return True
        
    return False
    
    
def e_rate_check(words: list) -> bool:
    """
    Check for attribute 10.
    """
    
    total = 0
    num_e = 0
    
    for word in words:
        for char in word:
            total += 1
            
            if char == "e":
                num_e += 1
                
    if (num_e / total) > 0.15:
        return True
        
    return False


def get_atts(words: list) -> list:
    """
    Generates attribute list.
    """
    
    atts = [False] * NUM_ATTS
    
    ###########
    ## ATT_0 ##
    ###########
    
    att0_words = ("the", "of", "and", "a", "to")
    
    for word in att0_words:
        if word in words:
            atts[0] = True
            break
            
    ###########
    ## ATT_1 ##
    ###########
    
    att1_words = ("de", "het", "van", "en", "een")
    
    for word in att1_words:
        if word in words:
            atts[1] = True
            break
            
    ###################
    ## ATT_2 - ATT_6 ##
    ###################

    seqs = ("th", "sh", "ae", "au", "aa")
    offset = 2
    
    for x in range(len(seqs)):
        for word in words:
            if seqs[x] in word:
                atts[offset + x] = True
                break
                
    ###########
    ## ATT_7 ##
    ###########
    
    for word in words:
        if not word.isascii():
            atts[7] = True
            break
            
    ###########
    ## ATT_8 ##
    ###########
    
    seqs = ("ee", "ii", "oo", "uu")

    for seq in seqs:
        for word in words:
            if seq in word:
                atts[8] = True
                break
                
    ###########
    ## ATT_9 ##
    ###########
    
    for word in words:
        if len(word) > 12:
            atts[9] = True
            break
    
    ####################
    ## ATT_9 - ATT_10 ##
    ####################
    
    atts[10] = e_rate_check(words)
    atts[11] = avg_len_check(words)
    
    return atts