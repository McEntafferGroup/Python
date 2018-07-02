import tkinter as tk
from tkinter import *
import math
import datetime
import astropy
import astropy.units as u
from astropy import coordinates
import astroplan
from astroplan import Observer
import jplephem
from astropy.coordinates import solar_system_ephemeris
solar_system_ephemeris.set('jpl')
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import struct
import time

step = 10

def set_step():
    global step
    
    if int(step_i.get()) < 0:
        step_button.config(text = 'No Negatives')
        return
    
    if int(step_i.get()) == 0:
        step_button.config(text = 'No Zeroes')
        return
    
    if int(step_i.get()) > 60:
        step_button.config(text = 'Less Than One Hour')
        return
    
    step = int(step_i.get())
    
    if step == 1:
        step_button.config(text = '1 minute')
    else:
        step_button.config(text = '{} minutes'.format(step))

def make_times():
    global year_i, month_i, day_i, ndays_i
    global times, window_x, window_y, ndays
    global step
    """read in from entry boxes"""
    year = year_i.get()
    month = month_i.get()
    day = day_i.get()
    ndays = int(ndays_i.get())
    """fix days so it works nicely"""
    while not ((60//step)*24//ndays) == ((60//step)*24/ndays):
        if ndays > (60/step)*24:
            print('Not Square')
            break
        
        print('STEP: {}\nDAYS: {}'.format(step, ndays))
        ndays = int(ndays+1)
    
    """make it GMT from local"""
    t = astropy.time.Time('{}-{}-{} {}:{}:{}'.format(year, month,
    day, 0, 0, 0), scale='utc')
    """make a list of times to create a Time array"""
    """used to make all further calculations substantially faster"""
    times = astropy.time.Time([(t+(i*step)*u.minute) for i in range((60//step)*24*ndays)])
    # times = astropy.time.Time([(t+(i*15)*u.minute) for i in range(96*int(ndays))])
    """labels for the plot later"""
    window   = [i.datetime for i in times]
    if ndays<=60:
        window_x = [i.date().strftime('%m-%d') for i in window[::(60//step)*24]]
    else:
        window_x = window[::(60//step)*24]
    window_y = [i for i in window[0:(60//step)*24+(60//step)+1]]
    # window_x = list()
    # window_y = [i.datetime for i in times[0:101]]
    # for T in times:
    #     if (((T+offset*u.hour).datetime.date())!=old_time.datetime.date()):
    #         window_x.append(((T+offset*u.hour).datetime))
    #     
    #     old_time = T+offset*u.hour
    """change button after press"""
    time_button.config(fg= 'black', bg='#FFE100')
    

def get_SMO_pos():
    global lat_i, long_i, RA_i, DEC_i, times, tname_i, option, places
    global coords_s, coords_m, coords_o, dist_sun, dist_moon, loc
    """read in from entry boxes"""
    
    ##handle if there is a look up to be done
    site = option.get()
    if(site is 'Anywhere Else'):
        lat = float(lat_i.get())
        long = float(long_i.get())
    
    else:
        if (places.get(site) is None):
            Label(master, bg='red', text='SITE NAME {} IS NOT VALID'.format(site.upper())).grid(row=5, column=3)
            
            return None
        else:
            lat, long = places[site]
    
    #loc = coordinates.EarthLocation(lat=lat*u.deg, lon=long*u.deg)
    loc = Observer(longitude=long*u.degree,latitude=lat*u.degree,name=site)
    
    tname = str(tname_i.get())
    if (tname is ''):
        RA = float(RA_i.get())
        DEC = float(DEC_i.get())
        """target's RA and DEC"""
        coords_o = coordinates.SkyCoord(ra=RA*u.hour, dec=DEC*u.degree, frame='gcrs')
    
    else:
        coords_o = coordinates.SkyCoord.from_name(tname, frame='gcrs')
    
    
    
    """Sun's RA and DEC throughout the given time"""
    coords_s = loc.sun_altaz (times)
    """Moon's RA and DEC at the location, throughout the given time"""
    coords_m = loc.moon_altaz(times)
    """get separation angles in radians for the Sun and Moon"""
    """this returns a value in the range [-180, 180]"""
    dist_sun  = (coords_s.separation(coords_o).degree)
    dist_moon = (coords_m.separation(coords_o).degree)
    """change button after press"""
    WHERE_button.config(fg= 'black', bg='#FFE100')
    
def get_angles():
    global sun_angle_i, moon_angle_i, sun_alt_i, moon_alt_i ,obj_alt_i
    global times, PI, loc
    global dist_sun, dist_moon, alt_s, alt_m, alt_o, obj_alt, sun_angle, moon_angle, sun_alt, moon_alt, dist_s, dist_m
    """read in from entry boxes"""
    sun_angle = float(sun_angle_i.get())
    moon_angle = float(moon_angle_i.get())
    sun_alt = float(sun_alt_i.get())
    moon_alt = float(moon_alt_i.get())
    obj_alt = float(obj_alt_i.get())
    
    """whether or not the object is far enough away"""
    """this returns values in the range [0, 180]; negatives do not matter"""
    dist_s = abs(dist_sun)>sun_angle
    dist_m = abs(dist_moon)>moon_angle
    """whether or not the altitudes are low enough"""
    alt_s = (coords_s.alt.degree<sun_alt)
    alt_m = (coords_m.alt.degree<moon_alt)
    """whether or not the altitude is high enough"""
    alt_o = (loc.target_is_up(times,coords_o, horizon=obj_alt*u.deg))
    """change button after press"""
    separ_button.config(fg= 'black', bg='#FFE100')
    
    
def plot_it():
    global dist_s, dist_m, alt_s, alt_m, alt_o, ndays, window_x, window_y
    global obj_alt, sun_alt, moon_alt, sun_angle, moon_angle
    global alt_m_chk, alt_o_chk, alt_s_chk, dist_m_chk, dist_s_chk
    
    """make it awesome"""
    #with plt.xkcd():
    
    fig = plt.figure(figsize=(18,9))
    ax = plt.subplot(111)
    
    """properly shape the truth table to display yays or nays"""
    aoc = (alt_o)if(alt_o_chk.get())else(True)
    
    dsc = (np.array(dist_s))if(dist_s_chk.get())else(True)
    
    asc = (alt_s)if(alt_s_chk.get())else(True)  
    
    dmc = (np.array(dist_m))if(dist_m_chk.get())else(True)
    
    amc = (alt_m)if(alt_m_chk.get())else(True)  
    
    window_t = aoc&dsc&asc&dmc&amc
    window_t = np.reshape(window_t, ((60//step)*24,ndays), order='F')
    # im = ax.imshow(window_t, matplotlib.cm.winter, origin="lower", extent=(0,(60//step)*24,0,(60//step)*24), vmin=0, vmax=1)#, interpolation='sinc')
    
    
    
    """set the proper number of ticks"""
    if ndays<=60:
        ext = (0,(60//step)*24,0,(60//step)*24)
        
        im = ax.imshow(window_t, matplotlib.cm.winter, origin="lower", extent=ext, vmin=0, vmax=1)
        
        xticks = range(0, (60//step)*24  , (60//step)*24//ndays)
        plt.xticks(xticks)
        ax.set_xticklabels(window_x, rotation=90)
    else:
        ext = (0,ndays,0,(60//step)*24)
        
        im = ax.imshow(window_t, matplotlib.cm.winter, origin="lower", extent=ext, vmin=0, vmax=1)
        
        xticks = range(0, ndays, 15)
        plt.xticks(xticks)
        ax.set_xticklabels([i.date().strftime('%m-%d') for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_x[0], window_x[-1], datetime.timedelta(days=15)))], rotation=90)
    
    plt.yticks(range(0, (60//step)*24+1, (60//step)))
    # plt.xticks(range(0, int(ndays), 15))
    # plt.yticks(range(0, 97, 4))
    
    """Drew complained about a title"""
    ax.set_title('POTENTIAL LAUNCH WINDOWS')
    """only use some of the labels so it is legible"""
    ax.set_yticklabels([i.time() for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_y[0], window_y[-1], datetime.timedelta(minutes=60)))])
    # ax.set_xticklabels([i.date() for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_x[0], window_x[-1], datetime.timedelta(days=15)))], rotation=90)
    # 
    # ax.set_yticklabels([i.time() for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_y[0], window_y[-1], datetime.timedelta(minutes=60)))])
    
    """some minor ticks for readability"""
    ax.minorticks_on()
    ax.grid()
    
    """label axes"""
    plt.ylabel('Universal Time')
    plt.xlabel('Universal Year {} - {}'.format(window_x[0].year,window_x[-1].year))
    
    """combination plots"""
    fig2 = plt.figure(figsize=(18,9))
    ax21 = plt.subplot(231)
    """first line reshapes data to show it all properly"""
    ax21.imshow(np.reshape(alt_o, ((60//step)*24,ndays), order='F'), matplotlib.cm.winter, origin="lower", extent=ext, vmin=0, vmax=1)
    """second line sets the title to be correct for inputs"""
    ax21.set_title("Object's altitude > {} degrees".format(obj_alt))
    """third line is to set y-axis to be labeled properly"""
    plt.yticks(range(0, (60//step)*24+1, (60//step)))
    plt.xticks(xticks)
    '''move plot position'''
    plt.subplots_adjust(hspace=0.3)
    
    ax22 = plt.subplot(232)
    ax22.imshow(np.reshape(dist_s, ((60//step)*24,ndays), order='F'), matplotlib.cm.winter, origin="lower", extent=ext, vmin=0, vmax=1)
    ax22.set_title("Object's distance from Sun > {} degrees".format(sun_angle))
    plt.yticks(range(0, (60//step)*24+1, (60//step)))
    plt.xticks(xticks)
    
    ax23 = plt.subplot(233)
    ax23.imshow(np.reshape(alt_s, ((60//step)*24,ndays), order='F'), matplotlib.cm.winter, origin="lower", extent=ext, vmin=0, vmax=1)
    ax23.set_title("Sun's altitude < {} degrees".format(sun_alt))
    plt.yticks(range(0, (60//step)*24+1, (60//step)))
    plt.xticks(xticks)
    
    ax25 = plt.subplot(235)
    ax25.imshow(np.reshape(dist_m, ((60//step)*24,ndays), order='F'), matplotlib.cm.winter, origin="lower", extent=ext, vmin=0, vmax=1)
    ax25.set_title("Object's distance from Moon > {} degrees".format(moon_angle))
    plt.yticks(range(0, (60//step)*24+1, (60//step)))
    plt.xticks(xticks)
    
    ax26 = plt.subplot(236)
    ax26.imshow(np.reshape(alt_m, ((60//step)*24,ndays), order='F'), matplotlib.cm.winter, origin="lower", extent=ext, vmin=0, vmax=1)
    ax26.set_title("Moon's altitude < {} degrees".format(moon_alt))
    plt.yticks(range(0, (60//step)*24+1, (60//step)))
    plt.xticks(xticks)
    
    """make all the y-axes readable"""
    ax21.set_yticklabels([i.time().hour for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_y[0], window_y[-1], datetime.timedelta(minutes=60)))])
    ax22.set_yticklabels([i.time().hour for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_y[0], window_y[-1], datetime.timedelta(minutes=60)))])
    ax23.set_yticklabels([i.time().hour for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_y[0], window_y[-1], datetime.timedelta(minutes=60)))])
    ax25.set_yticklabels([i.time().hour for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_y[0], window_y[-1], datetime.timedelta(minutes=60)))])
    ax26.set_yticklabels([i.time().hour for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_y[0], window_y[-1], datetime.timedelta(minutes=60)))])
    
    """now for good x-axes"""
    if ndays<=70:
        ax21.set_xticklabels(window_x, rotation=90)
        ax22.set_xticklabels(window_x, rotation=90)
        ax23.set_xticklabels(window_x, rotation=90)
        ax25.set_xticklabels(window_x, rotation=90)
        ax26.set_xticklabels(window_x, rotation=90)
    else:
        ax21.set_xticklabels([i.date().strftime('%m-%d') for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_x[0], window_x[-1], datetime.timedelta(days=15)))], rotation=90)
        ax22.set_xticklabels([i.date().strftime('%m-%d') for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_x[0], window_x[-1], datetime.timedelta(days=15)))], rotation=90)
        ax23.set_xticklabels([i.date().strftime('%m-%d') for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_x[0], window_x[-1], datetime.timedelta(days=15)))], rotation=90)
        ax25.set_xticklabels([i.date().strftime('%m-%d') for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_x[0], window_x[-1], datetime.timedelta(days=15)))], rotation=90)
        ax26.set_xticklabels([i.date().strftime('%m-%d') for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_x[0], window_x[-1], datetime.timedelta(days=15)))], rotation=90)
    
    """SHOW IT"""
    fig.show()
    fig2.show()
    
    """change button after press"""
    display_button.config(fg= 'black', bg='#FFE100')
    
def reset_the_GUI():
    """bring in all the globals"""
    global dist_s, dist_m, alt_s, alt_m, alt_o, ndays, window_x, window_y
    global obj_alt
    global times, loc
    global sun_angle, moon_angle, sun_alt, moon_alt
    global coords_s, coords_m, coords_o
    global dist_moon, dist_sun
    
    """reset all buttons and variables in order so the GUI looks nice"""
    del ndays, times, window_x, window_y
    time_button.config(bg='black', fg='#FFE100')
    del coords_s, coords_m, coords_o, dist_moon, dist_sun, loc
    WHERE_button.config(bg='black', fg='#FFE100')
    del alt_s, alt_m, alt_o, obj_alt, sun_angle, moon_angle, sun_alt, moon_alt, dist_s, dist_m
    separ_button.config(bg='black', fg='#FFE100')
    display_button.config(bg='black', fg='#FFE100')
    
def reset_all_but_time():
    """bring in all the globals"""
    global dist_s, dist_m, alt_s, alt_m, alt_o, ndays, window_x, window_y
    global obj_alt
    global times, loc
    global sun_angle, moon_angle, sun_alt, moon_alt
    global coords_s, coords_m, coords_o
    global dist_moon, dist_sun
    
    del coords_s, coords_m, coords_o, dist_sun, dist_moon, loc
    WHERE_button.config(bg='black', fg='#FFE100')
    del alt_s, alt_m, alt_o, obj_alt, sun_angle, moon_angle, sun_alt, moon_alt, dist_s, dist_m
    separ_button.config(bg='black', fg='#FFE100')
    display_button.config(bg='black', fg='#FFE100')

def no_angles():
    global dist_s, dist_m, alt_s, alt_m, alt_o, obj_alt, sun_angle, moon_angle, sun_alt, moon_alt
    
    del dist_s, dist_m, alt_s, alt_m, alt_o, obj_alt, sun_angle, moon_angle, sun_alt, moon_alt
    
    separ_button.config(bg='black', fg='#FFE100')
    display_button.config(bg='black', fg='#FFE100')
    
    

def check_box1():
    if(not dist_m_chk.get()):
        dist_m_chk.set(True)
    else:
        dist_m_chk.set(False)
    

def check_box2():
    if(not dist_s_chk.get()):
        dist_s_chk.set(True)
    else:
        dist_s_chk.set(False)


def check_box3():
    if(not alt_s_chk.get()):
        alt_s_chk.set(True)
    else:
        alt_s_chk.set(False)

   
def check_box4():
    if(not alt_m_chk.get()):
        alt_m_chk.set(True)
    else:
        alt_m_chk.set(False)

   
def check_box5():
    if(not alt_o_chk.get()):
        alt_o_chk.set(True)
    else:
        alt_o_chk.set(False)

    

def change_text():
    option.get()
    menu_label.config(text=option.get())
    print(option.get())
    
def update_site():
    new_lab = option.get()
    
    if(menu_label.text!=new_lab):
        menu_label.config(text=new_lab)
        menu_label.text=new_lab
    
    master.after(200, update_site)
    
    
"""make window"""
master = Tk()
"""name it"""
master.title('GO HAWKS')
master.config(bg='#FFE100')
"""need this for maths"""
PI = 3.1415926535897932384626433832795028841971693
"""make a dict of places to look-up"""
places = {'Wallops':(37.9367, -75.4699), 'White Sands':(33.2385, -106.3464),
        'Poker':(65.1367, -147.4472),'Kwajalein':(9.3966, 167.4716),
        'Andoya':(69.2943, 16.0207), 'Esrange':(67.8930, 21.0649),
        'Woomera':(-30, 134), 'Darwin':(-12.4634, 130.8456),
        'State College':(40.7934, -77.86)}
"""need this so rows don't piss me off anymore"""
row_counter = 0
"""space on top"""
Label(master, text='', bg='#FFE100').grid(row=row_counter)
"""increase RC after every row"""
row_counter+=1
Label(master, bg='#FFE100', fg='black', text = 'Timestep size (minutes):').grid(row=row_counter,column=0)
step_i = Entry(master, bg='black', fg='#FFE100')
step_i.grid(row=row_counter, column=1)
step_button = Button(master, bg= 'black', fg='#FFE100', text='{} minutes'.format(step), command=set_step)
step_button.grid(row=row_counter, column=3)
"""increase RC after every row"""
row_counter+=1
"""space to give gravitas to timestep"""
Label(master, text='', bg='#FFE100').grid(row=row_counter)
"""increase RC after every row"""
row_counter+=1
"""make label and entries for the date"""
Label(master, bg='#FFE100', text='UNIVERSAL DATE OF START TIME (YYYY:MM:DD):').grid(row=row_counter)
year_i  = Entry(master, bg='black', fg='#FFE100')
year_i.grid(row=row_counter, column=1)
Label(master, bg='#FFE100', text=':').grid(row=row_counter, column=2)
month_i = Entry(master, bg='black', fg='#FFE100')
month_i.grid(row=row_counter, column=3)
Label(master, bg='#FFE100', text=':').grid(row=row_counter, column=4)
day_i   = Entry(master, bg='black', fg='#FFE100')
day_i.grid(row=row_counter, column=5)
"""increase RC after every row"""
row_counter+=1

"""label and entry for length of window"""
Label(master, bg='#FFE100', text='Number of days to observe (best in range [90, 450]):').grid(row=row_counter)
ndays_i = Entry(master, bg='black', fg='#FFE100')
ndays_i.grid(row=row_counter, column=1)
"""increase RC after every row"""
row_counter+=1
"""button to create the time variables needed for calculations"""
time_button = Button(master, bg= 'black', fg='#FFE100', text='CREATE TIME', command=make_times)
time_button.grid(row=row_counter, column=1)
"""increase RC after every row"""
row_counter+=1
"""an extra line for readablity"""
Label(master, text='', bg='#FFE100').grid(row=row_counter)
"""increase RC after every row"""
row_counter+=1

"""add a launch place"""
option = StringVar()
option.set('Anywhere Else')

menu = Menubutton(master, text='Select a site')
opt = OptionMenu(menu, option, 'Anywhere Else')
menu.menu = opt['menu']
for i in places.keys():
    menu.menu.add_command(label=i, command=tk._setit(option, i))
menu['menu'] = menu.menu
menu.config(fg='#FFE100', bg='black', cursor='crosshair', relief='raised')
menu.grid(row=row_counter, column=0)


menu_label = Label(master, text=option.get(), bg='black', fg='#FFE100', width=17)
menu_label.text = option.get()
menu_label.grid(row=row_counter, column=1)

"""increase RC after every row"""
row_counter+=1
"""label and entry for longitude and latitude"""
Label(master, bg='#FFE100', text='Observer Latitude, Longitude (decimal degrees):').grid(row=row_counter)
lat_i  = Entry(master, bg='black', fg='#FFE100')
lat_i.grid(row=row_counter, column=1)
Label(master, bg='#FFE100', text='degrees, ').grid(row=row_counter, column=2)
long_i = Entry(master, bg='black', fg='#FFE100')
long_i.grid(row=row_counter, column=3)
Label(master, bg='#FFE100', text='degrees').grid(row=row_counter, column=4)
"""increase RC after every row"""
row_counter+=1

"""an entry for look-up to avoid the lat/lon BS"""
Label(master, text='Enter Target Object Name:', bg='#FFE100').grid(row=row_counter, column=0)
tname_i = Entry(master, bg='black', fg='#FFE100')
tname_i.grid(row=row_counter, column=1)
"""increase RC after every row"""
row_counter+=1

"""label/entry for RA and DEC of target"""
Label(master, bg='#FFE100', text='Right Ascension (decimal hours),\nDeclination (decimal degrees) of target:').grid(row=row_counter)
RA_i  = Entry(master, bg='black', fg='#FFE100')
RA_i.grid(row=row_counter, column=1)
Label(master, bg='#FFE100', text='hours, ').grid(row=row_counter, column=2)
DEC_i = Entry(master, bg='black', fg='#FFE100')
DEC_i.grid(row=row_counter, column=3)
Label(master, bg='#FFE100', text='degrees').grid(row=row_counter, column=4)
"""increase RC after every row"""
row_counter+=1
"""button to create arrays of objects positions in sky"""
WHERE_button = Button(master, bg= 'black', fg='#FFE100', text='WHERE THEY AT THO', command=get_SMO_pos)
WHERE_button.grid(row=row_counter, column=1)
"""increase RC after every row"""
row_counter+=1
"""another line for readability"""
Label(master, text='', bg='#FFE100').grid(row=row_counter)
"""increase RC after every row"""
row_counter+=1
"""warning label so GUI's use is obvious"""
warning_label = Label(master, text=' \nANGLES MUST BE INPUT INTO EVERY FIELD EVEN IF UNCHECKED TO AVOID ERRORS \n', bg='red', relief='ridge', bd=5)
warning_label.grid(row=row_counter, column=0, columnspan=6)
"""increase RC after every row"""
row_counter+=1
"""label/entry for Sun/Moon minimum angular distance"""
Label(master, bg='#FFE100', text='Minimum angular distance between target and:\nSun, Moon (in degrees)').grid(row=row_counter)
sun_angle_i = Entry(master, bg='black', fg='#FFE100')
sun_angle_i.grid(row=row_counter,column=1)
dist_s_chk = BooleanVar()
dist_s_chk.set(False)
Checkbutton(master, text='Sun Dist', fg='black', bg='#FFE100', variable=dist_s_chk, onvalue=True, offvalue=False, command=check_box2).grid(row=row_counter, column=2)
moon_angle_i = Entry(master, bg='black', fg='#FFE100')
moon_angle_i.grid(row=row_counter,column=3)
dist_m_chk = BooleanVar()
dist_m_chk.set(False)
Checkbutton(master, text='Moon Dist', fg='black', bg='#FFE100', variable=dist_m_chk, onvalue=True, offvalue=False, command=check_box1).grid(row=row_counter, column=4)
"""increase RC after every row"""
row_counter+=1
"""label/entry for altitude below horizon for Sun/Moon"""
Label(master, bg='#FFE100', text='Minimum altitude below horizon for\nproper occlusion of: Sun, Moon (in degrees [-90, 90])').grid(row=row_counter)
sun_alt_i = Entry(master, bg='black', fg='#FFE100')
sun_alt_i.grid(row=row_counter,column=1)
alt_s_chk = BooleanVar()
alt_s_chk.set(False)
Checkbutton(master, text='Sun Alt', fg='black', bg='#FFE100', variable=alt_s_chk, onvalue=True, offvalue=False, command=check_box3).grid(row=row_counter, column=2)
moon_alt_i = Entry(master, bg='black', fg='#FFE100')
moon_alt_i.grid(row=row_counter,column=3)
alt_m_chk = BooleanVar()
alt_m_chk.set(False)
Checkbutton(master, text='Moon Alt', fg='black', bg='#FFE100', variable=alt_m_chk, onvalue=True, offvalue=False, command=check_box4).grid(row=row_counter, column=4)
"""increase RC after every row"""
row_counter+=1
"""label/entry for target's minimum altitude"""
Label(master, bg='#FFE100', text='Minimum altitude of object for proper\nobservation (in degrees [-90, 90]):').grid(row=row_counter)
obj_alt_i = Entry(master, bg='black', fg='#FFE100')
obj_alt_i.grid(row=row_counter, column=1)
"""test checkboxes"""
alt_o_chk = BooleanVar()
alt_o_chk.set(False)
Checkbutton(master, text='Target Alt', fg='black', bg='#FFE100', variable=alt_o_chk, onvalue=True, offvalue=False, command=check_box5).grid(row=row_counter, column=2)
"""increase RC after every row"""
row_counter+=1
"""check the separation between the target and Sun/Moon/horizon/etc"""
separ_button = Button(master, bg= 'black', fg='#FFE100', text='ARE THEY GOOD ENOUGH', command=get_angles)
separ_button.grid(row=row_counter, column=1)
"""show the plots"""
display_button = Button(master, bg= 'black', fg='#FFE100', text='Put it all together', command=plot_it, cursor='trek')
display_button.grid(row=row_counter, column=3)
"""increase RC after every row"""
row_counter+=1
Label(master, text='', bg='#FFE100').grid(row=row_counter)
"""increase RC after every row"""
row_counter+=1
"""if new info is input, delete everything prior"""
kill_switch = Button(master, bg= 'black', fg='#FFE100', text='CLEAR ALL', command=reset_the_GUI)
kill_switch.grid(row=row_counter, column=0)
"""keep time and place"""
no_angles_button = Button(master, bg= 'black', fg='#FFE100', text='KEEP TIME AND PLACE', command=no_angles)
no_angles_button.grid(row=row_counter,column=3,columnspan=2)

"""if the time is unchanged, kill everything else"""
not_time = Button(master, bg= 'black', fg='#FFE100', text='KEEP TIME', command=reset_all_but_time)
not_time.grid(row=row_counter, column=5)
"""increase RC after every row"""
row_counter+=1
"""space at bottom"""
Label(master, text='', bg='#FFE100').grid(row=row_counter,column=6)
"""increase RC after every row"""
row_counter+=1

"""sign this shit so Drew doesn't take credit"""
Label(master, text='Awesome work here done by: Christopher Hillman (July 2017)', bg='#FFE100', fg='black').grid(row=row_counter, column=3, columnspan=4)

master.after(200, update_site)
"""wiki said i need this line"""
master.mainloop()