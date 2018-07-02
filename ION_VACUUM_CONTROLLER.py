from tkinter import *
import numpy as np
import serial
from serial.tools import list_ports
import time
import math

def send_packet(packet):
    """a test function to see how I made packets"""
    for i in packet:
        print('{} '.format(i),end='')
    

def update_graph():
    """call something to get LINE filled with new shit"""
    global LINEX, LINEY, g, LINE
    g+=1
    """for Y divide by height of graph and add (top of window 
    to top of graph) padding"""
    # LINE = np.array([LINEX,LINEY])
    
    """gives next y-value"""
    P = get_pressure()
    
    """timestamp values now and then"""
    if ((g%90==0)or(g==5)):
        canvas.create_text(g+3, canvas['height'], anchor=SW, text=(time.strftime("%H:%M:%S")+'\n'+str(P)+' Torr'), fill='green')
        canvas.create_line(g, canvas['height'], g, 0, fill='white')
    """scroll the graph automatically (which it does, just not well)"""
    if((g>=int(canvas['width']))) and (g%75==0):
        canvas.xview_scroll(1, UNITS)
        
    
    """increment x-axis (from g, above)"""
    LINEX.append(g)
    """in order to have values that fit the screen, process the y-values"""
    LINEY.append(abs((math.log(P,10)+3)*100))#+(int(canvas['height'])/2)))
    
    """create the new line"""
    canvas.create_line((LINEX[g-1], LINEY[g-1],LINEX[g],LINEY[g]), tag='PRESSURE', fill='yellow')
    
    """while the port is open, call this every 2 seconds"""
    if ser.isOpen():
        master.after(2000, update_graph)


##Pressure, Voltage, Current Functions
"""the next 3 sets of coupled functions all do the same thing but for different properties: as such, the first 2 will be fully commented to explain how they work, the folowing 2 are identical except for voltage instead of pressure, then the last 2 are for current"""

def update_pressure():
    """a function used to update the text label for pressure"""
    
    """get numeric value of pressure (or None if failed)"""
    press = get_pressure()
    """update the label in the GUI with current value"""
    pressure_d.config(text=str(press)+' Torr')
    """while port is open, call this every 2 seconds"""
    if ser.isOpen():
        master.after(2000, update_pressure)

def get_pressure():
    """a function used to return the numeric value of the pressure reading"""
    
    """command literal to send to controller"""
    cmdcd = '0B'
    """read response from sending the packet to the controller"""
    pressure = read_info(cmdcd)
    """if we get a response"""
    if(pressure[3:5]==b'OK'):
        """update the response log"""
        update_log(pressure.decode('utf-8'))
        """send the value back to whatever called this funtion"""
        return float(pressure[9:16].decode('utf-8'))
        
        """no response"""
    else:
        """update error logger"""
        update_log2('ERROR READING PRESSURE\n\t{}'.format(
        pressure.decode('utf-8')))
        """give the Null response"""
        return None
    
    



def update_voltage():
    volt = get_voltage()
    
    voltage_d.config(text=str(volt)+' V')
    
    if ser.isOpen():
        master.after(2000, update_voltage)
    
def get_voltage():
    cmdcd = '0C'
    
    voltage = read_info(cmdcd)
    
    if(voltage[3:5]==b'OK'):
        update_log(voltage.decode('utf-8'))
        return float(voltage[9:-4].decode('utf-8'))
        
    else:
        update_log2('ERROR READING VOLTAGE VALUE\n\t{}'.format(
        voltage.decode('utf-8')))
        return None
    
    
    
    
    
def update_current():
    curr = get_current()
    
    current_d.config(text=str(curr*1000)+' mA')
    
    if ser.isOpen():
        master.after(2000, update_current)
    
def get_current():
    cmdcd = '0A'
    
    current = read_info(cmdcd)
    
    if(current[3:5]==b'OK'):
        update_log(current.decode('utf-8'))
        return float(current[9:16].decode('utf-8'))
        
    else:
        update_log2('ERROR READING CURRENT VALUE\n\t{}'.format(
        current.decode('utf-8')))
        return None
    
    
    
    
def is_HV_on():
    """a function that displays whether or not the high voltage is currently 
    engaged"""
    
    """create command packet"""
    cmdcd = '61'
    """get response from sending the packet"""
    HV = read_info(cmdcd)
    """if we get a response"""
    if(HV[3:5]==b'OK'):
        """update response log"""
        update_log(HV.decode('utf-8'))
        """if HV is on"""
        if (HV[9:12]==b'YES'):
            """show label in red (red is dangerous and whatnot)"""
            HV_indicator.config(text='ON' , bg='red',  fg='white')
            """update label text (global variable to make things easier)"""
            HV_indicator.text = 'ON'
        
        else:
            """chow label in blue (blue is a safe color)"""
            HV_indicator.config(text='OFF', bg='blue', fg='white')
            """update label text (global variable to make things easier)"""
            HV_indicator.text = 'OFF'
        
        """no response"""
    else:
        """update error log"""
        update_log2('ERROR READING HIGH VOLTAGE STATE\n\t{}'.format(
        HV.decode('utf-8')))
    
    """while the port is open"""
    if ser.isOpen():
        """call this function every 2 seconds"""
        master.after(2000, is_HV_on)
    
def toggle_HV():
    """turn the pump on or off"""
    
    """if it is off"""
    if (HV_indicator.text is 'OFF'):
        """get response from trying to turn it on"""
        toggle = read_info('37')
        
        """if we get a response"""
        if (toggle[3:5]==b'OK'):
            """and it failed"""
            if(toggle[9:15]==b'*ERROR'):
                """update error log"""
                update_log2('ERROR STARTING PUMP\n\t{}'.format(
                toggle.decode('utf-8')))
                
                """if it worked"""
            else:
                """update response log"""
                update_log(toggle.decode('utf-8'))
            
            """if we receive no response"""
        else:
            """update error log"""
            update_log2('ERROR STOPPING PUMP\n\t{}'.format(
            toggle.decode('utf-8')))
        
        """if it is on"""
    else:
        """read response from trying to turn it off"""
        toggle = read_info('38')
        ##need to test the response packet for what it says
        """if we get a response"""
        if(toggle[3:5]==b'OK'):
            """update response log"""
            update_log(toggle.decode('utf-8'))
            
            """no response"""
        else:
            """incorrectly shows in error log even when working;
            must check response packet for correct formatting"""
            update_log2('ERROR STOPPING PUMP\n\t{}'.format(
            toggle.decode('utf-8')))

def set_pump_size():
    """used to cahnge the pump size in liters [4-7]"""
    
    """the only time we need to set data"""
    global DATA
    """set command code"""
    cmdcd = '12'
    """create DATA portion of packet"""
    DATA = format(int(pump_size_i.get()), '04d')
    """get response from sending the packet to alter the size"""
    set_packet = read_info(cmdcd)
    """if it sent"""
    if(set_packet[3:5]==b'OK'):
        """if it failed, but received the packet"""
        if (set_packet[9:15]==b'*ERROR'):
            """update error log with proper information"""
            update_log2('ERROR SETTING PUMP SIZE\n\t{}'.format(
            set_packet.decode('utf-8')))
            
            """if it worked, however"""
        else:
            """update the response log"""
            update_log(set_packet.decode('utf-8'))
        
        """failure in sending packet"""
    else:
        """proper error documenting"""
        update_log2('ERROR SETTING PUMP SIZE\n\t{}'.format(
        set_packet.decode('utf-8')))
    
    """reset global DATA so everything remains un-fucked"""
    DATA = ''
    
def close_port():
    """used in the GUI to close the port before termination of program so one 
    does not have to close it manually"""
    
    """gets the port"""
    global ser
    
    """closes it"""
    ser.close()
    
def port_validity():
    """checks that the port is still open (NOT that it is speaking with the
    controller)"""
    
    """the text shows whether the port is open or closed"""
    validity.text = ('PORT IS OPEN') if (ser.isOpen()) else ('CONNECTION INTERRUPT')
    """if it is"""
    if (ser.isOpen()):
        """button is green"""
        validity.config(bg='green',fg='white')
        
        """and call this function every 2 seconds"""
        master.after(2000, port_validity)
        
        """otherwise"""
    else:
        """button is red"""
        validity.config(bg='red',fg='white')
    
    """global variable handling (makes the labels easier to alter)"""
    validity.config(text=validity.text)
    
    

def create_packet(cmdcd):
    """general function used by almost all others in order to make packets to
    send to the controller"""
    
    """use the literals for creating a packet"""
    global START, ADDR, TERM, DATA
    
    """PACKT is the packet, a string"""
    PACKT = str()
    """add the start literal"""
    PACKT+=(START)
    """add a space"""
    PACKT+=str(' ')
    """add the port address"""
    PACKT+=(ADDR)
    """and a space"""
    PACKT+=str(' ')
    """include the command"""
    PACKT+=(cmdcd)
    """and a space"""
    PACKT+=str(' ')
    """if there is data to be sent (only one function uses this)"""
    if (DATA != ''):
        """add all the data to it"""
        PACKT+=DATA
        """and a space"""
        PACKT+=str(' ')
    """calculate the checksum"""
    CHKSM = format(((np.array([ord(i) for i in PACKT[1:]]).sum())%256), '02x')
    """add the checksum to the packet"""
    PACKT+=(CHKSM)
    """add the terminator literal"""
    PACKT+=(TERM)
    
    """send the created packet back to whatever called this function"""
    return PACKT

def read_info(cmdcd):
    """this is a general function used in almost every other function to 
    access the port and its responses"""
    
    """need the port"""
    global ser
    """a larger ASCII buffer than we will ever us, so the port behaves"""
    ser.set_buffer_size(100)
    """send the packet created by create_packet through the port"""
    ser.write(bytes(create_packet(cmdcd),'utf-8'))
    """read the entire response"""
    read = ser.read(100)
    """send the resonse back"""
    return read


def update_log(text):
    """called by other functions to update the proper log"""
    text = text + str('\n')
    
    """add text to the response log"""
    T1.insert(END, time.strftime("%H:%M:%S: \t")+text)
    T1.see('end')
    
def update_log2(text):
    """called by other functions to update the proper log"""
    text = text + str('\n')
    
    """add text to the error log"""
    T2.insert(END, time.strftime("%H:%M:%S: \t")+text)
    T2.see('end')

##END OF FUNCTIONS
RESP  = '01 OK 00 DIGITEL SPCe 46 1a\r'
"""pressure response = 01 OK 00 X.XE-XX UUU CK\r"""
"""global constants for packet creation"""
START = '~'    #'7e'
ADDR  = '01'
CMDCD = '0A'
DATA  = ''
TERM  = '\r'    #'0D'


"""find the USB to Serial Port and use that"""
useable_port = None
"""list of all the available ports"""
ports_list = [i for i in list_ports.comports()]
"""removed for more general solution"""
# prolific = [(i)if(ports_list[i][1][:8]=='Prolific')else(None) for i in range(len(ports_list))]
# for i in range(len(ports_list)):
#     if (prolific[i]==i):
#         useable_port = ports_list[i][0]
for i in ports_list:
    """open each port"""
    """error handle an empty wire"""
    try:
        ser = serial.Serial(i[0],115200,8,'N',1,xonxoff=0,rtscts=0,timeout=0.01)
        """send a packet and read response asking for device's name"""
        port_check = read_info('01')
        """if the response is what we expect"""
        if port_check == RESP:
            """leave the loop"""
            break
            
            """otherwise"""
        else:
            """close it and try again"""
            ser.close()
        
    except serial.serialutil.SerialException:
        ser.close()
    

"""if we had no successful connection"""
if not (ser.isOpen()):
    """make a window"""
    master = Tk()
    """proper title"""
    master.title('Failure to Locate Proper Port')
    """black background"""
    master.config(bg='black')
    """set its size"""
    master.geometry('840x640')
    """place text (centered) to inform end user of failure (go hawks)"""
    Label(master, text='NO AVAILABLE PORT TO ACCESS ION PUMP CONTROLLER', bg='black', fg='#FFE100').place(relx=0.5, rely=0.5, anchor=CENTER)
    """without this nothing appears"""
    master.mainloop()

    """if we had a successful connestion"""
else:
    """open proper port (should already be done)"""
    # ser = serial.Serial(useable_port, 115200, 8, 'N', 1, xonxoff=0, rtscts=0, timeout=0.01)
    
    """create GUI window"""
    master = Tk()
    """give it a title"""
    master.title('ION VACUUM PUMP')
    """black background for contrast"""
    master.config(bg='black')
    """set size"""
    master.geometry('840x640')
    
    """create plot for Pressure over time"""
    canvas = Canvas(master, bg='black', confine=False, scrollregion=(0,0,840000,400), width=840, height=400)
    canvas.create_line((0,0,0,0), tag='Pressure', fill='yellow')
    
    """scrollbar for the plot"""
    S3 = Scrollbar(master, orient='horizontal')
    """attach the scrollbar to the plot"""
    S3.config(command=canvas.xview)
    canvas.config(xscrollcommand=S3.set)
    
    """so the plot makes proper lines"""
    g=0
    LINEX = list()
    LINEY = list()
    LINE  = list()
    LINEX.append(g)
    """random value for some reason? does not affect GUI apparently"""
    LINEY.append(np.random.randint(0,400))
    LINE = [LINEX, LINEY]
    """scrollbar and text block for a response log"""
    S1 = Scrollbar(master)
    T1 = Text(master, width=40, height=90)
    """attach them"""
    S1.config(command=T1.yview)
    T1.config(yscrollcommand=S1.set)
    """scrollbar and text block for an error log"""
    S2 = Scrollbar(master)
    T2 = Text(master, width=40, height=90)
    """attach them"""
    S2.config(command=T2.yview)
    T2.config(yscrollcommand=S2.set)
    """label the logs"""
    T1.insert(END, 'COMMAND RESPONSE LOG\n========================================\n')
    T2.insert(END, 'ERROR LOG\n========================================\n')
    """pack the plot/scrollbar"""
    canvas.pack(side=TOP, fill=BOTH)
    S3.pack(side=TOP, fill=X)
    """pack the textbox/scrollbar"""
    T1.pack(side=LEFT, fill=Y)
    S1.pack(side=LEFT, fill=Y)
    """pack the textbox/scrollbar"""
    T2.pack(side=LEFT, fill=Y)
    S2.pack(side=LEFT, fill=Y)
    
    """label for whether or not the pump is on"""
    HV_label = Label(master, text='HIGH VOLTAGE', bg='red', fg='white')
    HV_label.pack(anchor=S, side=LEFT)
    HV_indicator = Label(master, text='N/A', bg='blue', fg='white')
    HV_indicator.text = 'N/A'
    HV_indicator.pack(anchor=S, side=LEFT)
    """label for the voltage"""
    volt_label = Label(master, text='VOLTAGE: ', bg='black', fg='cyan')
    volt_label.place(x=685, y=422)
    voltage_d = Label(master, text='N/A', bg='black', fg='cyan')
    voltage_d.place(x=748, y=422)
    """label for the pressure"""
    press_label = Label(master, text='PRESSURE: ', bg='black', fg='yellow')
    press_label.place(x=685, y=442)
    pressure_d = Label(master, text='N/A', bg='black', fg='yellow')
    pressure_d.place(x=748, y=442)
    """label for the current"""
    curr_label = Label(master, text='CURRENT: ', bg='black', fg='red')
    curr_label.place(x=685, y=462)
    current_d = Label(master, text='N/A', bg='black', fg='red')
    current_d.place(x=748, y=462)
    """button for setting the pump value in liters"""
    pump_button = Button(master, text='SET PUMP VALUE', bg='black', fg='white', command=set_pump_size)
    pump_button.place(x=685, y=482)
    pump_size_i = Entry(master, bg='white', fg='black')
    pump_size_i.place(x=685, y=512)
    """close the port before exiting GUI to ease restart"""
    port_close_button = Button(master, text='Close the Port', bg='yellow', fg='black', command=close_port)
    port_close_button.place(x=685, y=537)
    validity = Label(master, text='N/A')
    validity.text = 'N/A'
    validity.place(x=685, y=567)
    """button to turn pump on and off"""
    HV_toggle_button = Button(master, text='TOGGLE HIGH VOLTAGE', bg='black', fg='white', command=toggle_HV)
    HV_toggle_button.pack(anchor=W, before=HV_label, side=BOTTOM)
    
    """update everything all the time after the GUI opens"""
    master.after(1, port_validity)
    if ser.isOpen():
        master.after(1, update_pressure)
        master.after(1, update_current)
        master.after(1, update_voltage)
        master.after(1, is_HV_on)
        master.after(1, update_graph)
    """wihtout this nothing appears"""
    master.mainloop()