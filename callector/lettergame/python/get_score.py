#!/usr/bin/python

def get_score_position(scoreList, currentScore):
    
    position = 1
    
    for i in scoreList:
        if currentScore >= i:
            break;
        print(i)
        position += 1
    
    print ("Position:")
    print(position)
    
    return position
 
