from tkinter import *

decision = False

def ZERO():
    print('ZEROED')

def CERTAINTY():
    
    '''accessable by other functions'''
    global decision
    
    '''make another window'''
    helper = Tk()
    helper.title('Reassurance')
    
    '''ask the question'''
    Label(helper, text='Are you sure this move will not damage anything?').grid(row=0, column=0, columnspan=3)
    
    '''make a button for yes'''
    yes = Button(helper, text='YES', command=lambda: Y_or_N(True, helper))
    yes.grid(row=1, column=0)
    
    '''and for no'''
    no  = Button(helper, text='NO!', command=lambda: Y_or_N(False, helper))
    no.grid(row=1, column=2)
    
    '''wait until that window closes before returning a value, 
    essentially pausing the program until a decision is made'''
    helper.wait_window()
    
    return decision
    
def Y_or_N(bool, window):
    
    '''access the variables'''
    global decision
    
    '''set its truth value, cannot be returned since button calls are void'''
    decision = bool
    
    '''close the window'''
    window.destroy()
    
def resetDecision():
    '''function used by all commands to ensure closing the window sends a 
    negative response'''
    
    global decision
    
    decision = False
    
def Xabs():
    move = Xabs_v.get()
    try:
        move = float(move)
        
        '''call a function to open another window for a decision'''
        dec = CERTAINTY()
        
        '''reset the decision global to False so closing the window
        also sends a negative request removing possibility of breakage'''
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving to absolute X = {}'.format(move))
            
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Yabs():
    move = Yabs_v.get()
    try:
        move = float(move)
        
        dec = CERTAINTY()
        
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving to absolute Y = {}'.format(move))
            
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Zabs():
    move = Zabs_v.get()
    try:
        move = float(move)
        
        dec = CERTAINTY()
        
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving to absolute Z = {}'.format(move))
            
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Aabs():
    move = Aabs_v.get()
    try:
        move = float(move)
        
        '''call a function to open another window for a decision'''
        dec = CERTAINTY()
        
        '''reset the decision global to False so closing the window
        also sends a negative request removing possibility of breakage'''
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving to absolute A = {}'.format(move))
            
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Babs():
    move = Babs_v.get()
    try:
        move = float(move)
        
        '''call a function to open another window for a decision'''
        dec = CERTAINTY()
        
        '''reset the decision global to False so closing the window
        also sends a negative request removing possibility of breakage'''
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving to absolute B = {}'.format(move))
            
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Cabs():
    move = Cabs_v.get()
    try:
        move = float(move)
        
        '''call a function to open another window for a decision'''
        dec = CERTAINTY()
        
        '''reset the decision global to False so closing the window
        also sends a negative request removing possibility of breakage'''
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving to absolute C = {}'.format(move))
            
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Xrel():
    move = Xrel_v.get()
    try:
        move = float(move)
        
        dec = CERTAINTY()
        
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving X by {}'.format(move))
            Xrel_v.curr += move
            Xrel_l.config(text='Rel X: {}'.format("%.5f" % Xrel_v.curr))
        
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Yrel():
    move = Yrel_v.get()
    try:
        move = float(move)
        
        dec = CERTAINTY()
        
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving Y by {}'.format(move))
            Yrel_v.curr += move
            Yrel_l.config(text='Rel Y: {}'.format("%.5f" % Yrel_v.curr))
        
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Zrel():
    move = Zrel_v.get()
    try:
        move = float(move)
        
        dec = CERTAINTY()
        
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving Z by {}'.format(move))
            Zrel_v.curr += move
            Zrel_l.config(text='Rel Z: {}'.format("%.5f" % Zrel_v.curr))
        
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Arel():
    move = Arel_v.get()
    try:
        move = float(move)
        
        dec = CERTAINTY()
        
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving A by {}'.format(move))
            Arel_v.curr += move
            Arel_l.config(text='Rel A: {}'.format("%.5f" % Arel_v.curr))
        
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Brel():
    move = Brel_v.get()
    try:
        move = float(move)
        
        dec = CERTAINTY()
        
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving B by {}'.format(move))
            Brel_v.curr += move
            Brel_l.config(text='Rel B: {}'.format("%.5f" % Brel_v.curr))
        
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

def Crel():
    move = Crel_v.get()
    try:
        move = float(move)
        
        dec = CERTAINTY()
        
        resetDecision()
        
        if dec:
            '''where the real funciton call goes'''
            print('moving C by {}'.format(move))
            Crel_v.curr += move
            Crel_l.config(text='Rel C: {}'.format("%.5f" % Crel_v.curr))
        
        else:
            print('Movement Cancelled')
    
    except ValueError:
        print('INVALID ARGUMENT')

'''so I do not need to change everything to add a new feature'''
row_counter = 0
'''make the window'''
master = Tk()
'''name it'''
master.title('HEXAPOD GUI IN PYTHON')

'''a button to zero the hexapod'''
ZERO_b = Button(master, text='Return to Zero', command=ZERO)
ZERO_b.grid(row=row_counter, column=1)
'''increment every row'''
row_counter+=1

'''ABSOLUTE MOVES'''

'''absolute x move button'''
Xabs_b = Button(master, text='Abs X: ', command=Xabs, font=("Helvetica", 16))
Xabs_b.grid(row=row_counter,column=0)
'''absolute x move entry field'''
Xabs_v = Entry(master)
Xabs_v.grid(row=row_counter,column=1)

Label(master, text='   ').grid(row=row_counter,column=2)

'''absolute y move button'''
Yabs_b = Button(master, text='Abs Y: ', command=Yabs, font=("Helvetica", 16))
Yabs_b.grid(row=row_counter,column=3)
'''absolute y move entry field'''
Yabs_v = Entry(master)
Yabs_v.grid(row=row_counter,column=4)

Label(master, text='   ').grid(row=row_counter,column=5)

'''absolute z move button'''
Zabs_b = Button(master, text='Abs Z: ', command=Zabs, font=("Helvetica", 16))
Zabs_b.grid(row=row_counter,column=6)
'''absolute z move entry field'''
Zabs_v = Entry(master)
Zabs_v.grid(row=row_counter,column=7)
'''increment every row'''
row_counter+=1

'''absolute a move button'''
Aabs_b = Button(master, text='Abs A: ', command=Aabs, font=("Helvetica", 16))
Aabs_b.grid(row=row_counter,column=0)
'''absolute a move entry field'''
Aabs_v = Entry(master)
Aabs_v.grid(row=row_counter,column=1)

'''absolute b move button'''
Babs_b = Button(master, text='Abs B: ', command=Babs, font=("Helvetica", 16))
Babs_b.grid(row=row_counter,column=3)
'''absolute b move entry field'''
Babs_v = Entry(master)
Babs_v.grid(row=row_counter,column=4)

'''absolute c move button'''
Cabs_b = Button(master, text='Abs C: ', command=Cabs, font=("Helvetica", 16))
Cabs_b.grid(row=row_counter,column=6)
'''absolute c move entry field'''
Cabs_v = Entry(master)
Cabs_v.grid(row=row_counter,column=7)
'''increment every row'''
row_counter+=1

'''for readability'''
Label(master, text='   ').grid(row=row_counter,column=5)
row_counter+=1
Label(master, text='   ').grid(row=row_counter,column=5)
row_counter+=1

'''RELATIVE MOVES'''

'''relative x move button'''
Xrel_b = Button(master, text='Rel X: ', command=Xrel, font=("Helvetica", 16))
Xrel_b.grid(row=row_counter,column=0)
'''relative x move entry field'''
Xrel_v = Entry(master)
'''current value of x'''
Xrel_v.curr = 0

Xrel_l = Label(master, text='Rel X: {}'.format("%.5f" % Xrel_v.curr), font=("Helvetica", 20))
Xrel_l.grid(row=row_counter-1,column=1)

Xrel_v.grid(row=row_counter,column=1)

Label(master, text='   ').grid(row=row_counter,column=2)

'''relative y move button'''
Yrel_b = Button(master, text='Rel Y: ', command=Yrel, font=("Helvetica", 16))
Yrel_b.grid(row=row_counter,column=3)
'''relative y move entry field'''
Yrel_v = Entry(master)
Yrel_v.curr = 0

Yrel_l = Label(master, text='Rel Y: {}'.format("%.5f" % Yrel_v.curr), font=("Helvetica", 20))
Yrel_l.grid(row=row_counter-1,column=4)

Yrel_v.grid(row=row_counter,column=4)

Label(master, text='   ').grid(row=row_counter,column=5)

'''relative z move button'''
Zrel_b = Button(master, text='Rel Z: ', command=Zrel, font=("Helvetica", 16))
Zrel_b.grid(row=row_counter,column=6)
'''relative z move entry field'''
Zrel_v = Entry(master)
Zrel_v.curr = 0

Zrel_l = Label(master, text='Rel Z: {}'.format("%.5f" % Zrel_v.curr), font=("Helvetica", 20))
Zrel_l.grid(row=row_counter-1,column=7)

Zrel_v.grid(row=row_counter,column=7)

'''increment every row'''
row_counter+=1
'''increment every row'''
row_counter+=1

'''relative a move button'''
Arel_b = Button(master, text='Rel A: ', command=Arel, font=("Helvetica", 16))
Arel_b.grid(row=row_counter,column=0)
'''relative a move entry field'''
Arel_v = Entry(master)
Arel_v.curr = 0

Arel_l = Label(master, text='Rel A: {}'.format("%.5f" % Arel_v.curr), font=("Helvetica", 20))
Arel_l.grid(row=row_counter-1,column=1)

Arel_v.grid(row=row_counter,column=1)

Label(master, text='   ').grid(row=row_counter,column=2)

'''relative b move button'''
Brel_b = Button(master, text='Rel B: ', command=Brel, font=("Helvetica", 16))
Brel_b.grid(row=row_counter,column=3)
'''relative b move entry field'''
Brel_v = Entry(master)
Brel_v.curr = 0

Brel_l = Label(master, text='Rel B: {}'.format("%.5f" % Brel_v.curr), font=("Helvetica", 20))
Brel_l.grid(row=row_counter-1,column=4)

Brel_v.grid(row=row_counter,column=4)

Label(master, text='   ').grid(row=row_counter,column=5)

'''relative c move button'''
Crel_b = Button(master, text='Rel C: ', command=Crel, font=("Helvetica", 16))
Crel_b.grid(row=row_counter,column=6)
'''relative c move entry field'''
Crel_v = Entry(master)
Crel_v.curr = 0

Crel_l = Label(master, text='Rel C: {}'.format("%.5f" % Crel_v.curr), font=("Helvetica", 20))
Crel_l.grid(row=row_counter-1,column=7)

Crel_v.grid(row=row_counter,column=7)

'''increment every row'''
row_counter+=1

master.mainloop()