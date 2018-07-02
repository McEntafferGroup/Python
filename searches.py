import numpy as np

def depth_first(board):
    
    dest  = [-1,-1]
    start = [-2,-2]
    """(y,x)"""
    dest  = np.array(np.where(board==3))
    start = np.array(np.where(board==2))
    
    dest = dest.flatten()
    start = start.flatten()
    
    x_move = 0
    y_move = 0
    
    found = (start == dest).all()
    
    loc = start
    
    while (not found):
        
        if (loc[1] < dest[1]):
            if not (board[loc[0]][loc[1]+1]==1):
                x_move += 1
                
            else:
                """make a move when an x is impossible"""
                y_move +=1
        
        elif (loc[1] > dest[1]):
            if not (board[loc[0]][loc[1]-1]==1):
                x_move -= 1
                
            else:
                """make a move when an x is impossible"""
                y_move -=1
        
        else:
            
            if (loc[0] < dest[0]):
                if not (board[loc[0]+1][loc[1]]==1):
                    y_move += 1
                
                else:
                    """make a move when a y is impossible"""
                    x_move +=1
            
            elif  (loc[0] > dest[0]):
                if not (board[loc[0]-1][loc[1]]==1):
                    y_move -= 1
                    
                else:
                    """make a move when a y is impossible"""
                    x_move -=1
        
        
        loc = np.array([start[0]+y_move,start[1]+x_move])
        
        found = (loc == dest).all()
        
        