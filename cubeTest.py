import numpy as np
import matplotlib
import matplotlib.pyplot as plt

puzzle = np.array(
         [[['white','white','white']    for i in range(3)],
          [['red','red','red']          for i in range(3)],
          [['blue','blue','blue']       for i in range(3)],
          [['orange','orange','orange'] for i in range(3)],
          [['green','green','green']    for i in range(3)],
          [['yellow','yellow','yellow'] for i in range(3)]])

"""red facing, white down"""

def R():
    """displays rotated right side"""
    # #top
    # print('\t',end='  ')
    # print(puzzle[5][2][2],end=', ')
    # print(puzzle[5][1][2],end=', ')
    # print(puzzle[5][0][2])
    # #front, turned side, and back
    # print(puzzle[1][0][2],end=' ')
    # print(puzzle[4][0],end=' ')
    # print(puzzle[3][0][0])
    # 
    # print(puzzle[1][1][2],end=' ')
    # print(puzzle[4][1],end=' ')
    # print(puzzle[3][1][0])
    # 
    # print(puzzle[1][2][2],end=' ')
    # print(puzzle[4][2],end=' ')
    # print(puzzle[3][2][0])
    # #bottom
    # print('\t',end='  ')
    # print(puzzle[0][0][2],end=', ')
    # print(puzzle[0][1][2],end=', ')
    # print(puzzle[0][2][2])
    
    #rotate the face
    puzzle[4] = np.rot90(puzzle[4],-1)
    #conveyor the edges
    hold = (puzzle[5][0][2], puzzle[5][1][2], puzzle[5][2][2])
    #left to top
    puzzle[5][0][2], puzzle[5][1][2], puzzle[5][2][2] = (
    puzzle[1][2][2], puzzle[1][1][2], puzzle[1][0][2])
    #bottom to left
    puzzle[1][2][2], puzzle[1][1][2], puzzle[1][0][2] = (
    puzzle[0][2][2], puzzle[0][1][2], puzzle[0][0][2])
    #right to bottom
    puzzle[0][0][2], puzzle[0][1][2], puzzle[0][2][2] = (
    puzzle[3][2][0], puzzle[3][1][0], puzzle[3][0][0])
    #top to right
    puzzle[3][2][0], puzzle[3][1][0], puzzle[3][0][0] = hold
    
    # #top
    # print('\t',end='  ')
    # print(puzzle[5][0][2],end=', ')
    # print(puzzle[5][1][2],end=', ')
    # print(puzzle[5][2][2])
    # #front, turned side, and back
    # print(puzzle[1][0][2],end=' ')
    # print(puzzle[4][0],end=' ')
    # print(puzzle[3][0][0])
    # print(puzzle[1][1][2],end=' ')
    # print(puzzle[4][1],end=' ')
    # print(puzzle[3][1][0])
    # print(puzzle[1][2][2],end=' ')
    # print(puzzle[4][2],end=' ')
    # print(puzzle[3][2][0])
    # #bottom
    # print('\t',end='  ')
    # print(puzzle[0][0][2],end=', ')
    # print(puzzle[0][1][2],end=', ')
    # print(puzzle[0][2][2])

def R_p():
    R()
    R()
    R()

def L():
    #rotate the face
    puzzle[2] = np.rot90(puzzle[2],-1)
    #conveyor the edges
    hold = (puzzle[5][0][0], puzzle[5][1][0], puzzle[5][2][0])
    #left to top
    puzzle[5][0][0], puzzle[5][1][0], puzzle[5][2][0] = (
    puzzle[3][2][2], puzzle[3][1][2], puzzle[3][0][2])
    #bottom to left
    puzzle[3][2][2], puzzle[3][1][2], puzzle[3][0][2] = (
    puzzle[0][0][0], puzzle[0][1][0], puzzle[0][2][0])
    #right to bottom
    puzzle[0][0][0], puzzle[0][1][0], puzzle[0][2][0] = (
    puzzle[1][0][0], puzzle[1][1][0], puzzle[1][2][0])
    #top to right
    puzzle[1][0][0], puzzle[1][1][0], puzzle[1][2][0] = hold
    
def L_p():
    L()
    L()
    L()
    
def F():
    #rotate the face
    puzzle[1] = np.rot90(puzzle[1],-1)
    #conveyor the edges
    hold = (puzzle[5][2][0], puzzle[5][2][1], puzzle[5][2][2])
    #left to top
    puzzle[5][2][0], puzzle[5][2][1], puzzle[5][2][2] = (
    puzzle[2][2][2], puzzle[2][1][2], puzzle[2][0][2])
    #bottom to left
    puzzle[2][0][2], puzzle[2][1][2], puzzle[2][2][2] = (
    puzzle[0][0][0], puzzle[0][0][1], puzzle[0][0][2])
    #right to bottom
    puzzle[0][0][0], puzzle[0][0][1], puzzle[0][0][2] = (
    puzzle[4][2][0], puzzle[4][1][0], puzzle[4][0][0])
    #top to right
    puzzle[4][0][0], puzzle[4][1][0], puzzle[4][2][0] = hold

def F_p():
    F()
    F()
    F()

def D():
    #rotate the face
    puzzle[0] = np.rot90(puzzle[0],-1)
    #conveyor the edges
    hold = (puzzle[1][2][0], puzzle[1][2][1], puzzle[1][2][2])
    #left to top
    puzzle[1][2][0], puzzle[1][2][1], puzzle[1][2][2] = (
    puzzle[2][2][0], puzzle[2][2][1], puzzle[2][2][2])
    #bottom to left
    puzzle[2][2][0], puzzle[2][2][1], puzzle[2][2][2] = (
    puzzle[3][2][0], puzzle[3][2][1], puzzle[3][2][2])
    #right to bottom
    puzzle[3][2][0], puzzle[3][2][1], puzzle[3][2][2] = (
    puzzle[4][2][0], puzzle[4][2][1], puzzle[4][2][2])
    #top to right
    puzzle[4][2][0], puzzle[4][2][1], puzzle[4][2][2] = hold

def D_p():
    D()
    D()
    D()

color = {'white':(0.3,0.3,0.3),'red':(1.0,0.0,0.0),'blue':(0.0,0.0,1.0),
        'orange':(1.0,0.65,0.0),'green':(0.0,1.0,0.0),'yellow':(1.0,1.0,0.0)}


fig, ax = plt.subplots(9,12,True,True)
plt.ion()


#this will be super fun later...
def paint(puzzle):
    
    for a in ax:
        for b in a:
            b.clear()
            b.set_xticks([])
            b.set_yticks([])

    plt.subplots_adjust(wspace=0,hspace=0)
    
    for i in range(9):
        if i < 3:
            ax[3][i+0].imshow([[color[puzzle[4][0][i]]]],origin='lower')
            ax[3][i+3].imshow([[color[puzzle[1][0][i]]]],origin='lower')
            ax[3][i+6].imshow([[color[puzzle[2][0][i]]]],origin='lower')
            ax[3][i+9].imshow([[color[puzzle[3][0][i]]]],origin='lower')
            ax[6][i+3].imshow([[color[puzzle[0][0][i]]]],origin='lower')
            ax[0][i+3].imshow([[color[puzzle[5][0][i]]]],origin='lower')
            
        elif i < 6:
            ax[4][i-3].imshow([[color[puzzle[4][1][i-3]]]],origin='lower')
            ax[4][i+0].imshow([[color[puzzle[1][1][i-3]]]],origin='lower')
            ax[4][i+3].imshow([[color[puzzle[2][1][i-3]]]],origin='lower')
            ax[4][i+6].imshow([[color[puzzle[3][1][i-3]]]],origin='lower')
            ax[7][i+0].imshow([[color[puzzle[0][1][i-3]]]],origin='lower')
            ax[1][i+0].imshow([[color[puzzle[5][1][i-3]]]],origin='lower')
            
        else:
            ax[5][i-6].imshow([[color[puzzle[4][2][i-6]]]],origin='lower')
            ax[5][i-3].imshow([[color[puzzle[1][2][i-6]]]],origin='lower')
            ax[5][i+0].imshow([[color[puzzle[2][2][i-6]]]],origin='lower')
            ax[5][i+3].imshow([[color[puzzle[3][2][i-6]]]],origin='lower')
            ax[8][i-3].imshow([[color[puzzle[0][2][i-6]]]],origin='lower')
            ax[2][i-3].imshow([[color[puzzle[5][2][i-6]]]],origin='lower')

    fig.show()