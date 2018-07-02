import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import time

def mult(*args):
    """multiples of number, minimum value, largest value"""
    
    if len(args)==3:
        multiple, lower, total_num = args
    else:
        multiple, total_num = args
        lower = multiple+1
    
    fig = plt.figure(0, figsize=(10,10))
    plt.interactive(True)
    fig.show()
    
    for k in range(lower, total_num+1, 1):
        """theta's, r's"""
        plt.polar([i*np.pi*2/k for i in range(k+1)],[1]*(k+1), 
                c=(1,0,0))
        
        plt.thetagrids([None])
        plt.rgrids([30])
        plt.autoscale(False)
        
        for i in range(1,k+1):
            plt.polar((i*np.pi*2/k,((i*multiple)%k)*np.pi*2/k),
            [1]*2, c=(0,0,0))
            
            #with plt.xkcd(randomness=0):
            plt.annotate(i, xy=(i*np.pi*2/k,1.05), 
            horizontalalignment = 'center',
            verticalalignment   = 'center')
        
        
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.show(block=False)
        
        if not (k==total_num):
            fig.clear()
            time.sleep(0.4)

    
def single(multiple, total_num):
    fig = plt.figure(0, figsize=(10,10))
    fig.show()
    
    """theta's, r's"""
    plt.polar([i*np.pi*2/total_num for i in range(total_num+1)],[1]*(total_num+1), 
            c=(1,0,0))
    
    plt.thetagrids([None])
    plt.rgrids([30])
    plt.autoscale(False)
    
    for i in range(1,total_num+1):
        plt.polar((i*np.pi*2/total_num,((i*multiple)%total_num)*np.pi*2/total_num),
        [1]*2, c=(0,0,0))
        
        with plt.xkcd(randomness=0):
            plt.annotate(i, xy=(i*np.pi*2/total_num,1.05), 
            horizontalalignment = 'center',
            verticalalignment   = 'center')
    
    plt.show()