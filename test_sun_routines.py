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
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm
import struct
import time


places = {'Wallops':(37.9367, -75.4699), 'White Sands':(33.2385, -106.3464),
        'Poker':(65.1367, -147.4472),'Kwajalein':(9.3966, 167.4716),
        'Andoya':(69.2943, 16.0207), 'Esrange':(67.8930, 21.0649),
        'Woomera':(-30, 134), 'Darwin':(-12.4634, 130.8456),
        'State College':(40.7934, -77.86)}


step = 10

ndays = 180

year, month, day = 2018, 4, 1

site = 'Wallops'

lat, long = places[site]

sun_alt = -15



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
"""labels for the plot later"""
window   = [i.datetime for i in times]
if ndays<=60:
    window_x = [i.date().strftime('%m-%d') for i in window[::(60//step)*24]]
else:
    window_x = window[::(60//step)*24]
window_y = [i for i in window[0:(60//step)*24+(60//step)+1]]


loc = Observer(longitude=long*u.degree,latitude=lat*u.degree,name=site)


"""Sun's RA and DEC throughout the given time"""
coords_s = loc.sun_altaz (times)
"""get separation angles in radians for the Sun and Moon"""

"""whether or not the altitudes are low enough"""
alt_s  = (sun_alt -coords_s.alt.degree)


fig = plt.figure(figsize=(18,9))
ax = plt.subplot(111)

"""set the proper number of ticks"""
if ndays<=60:
    ext = (0,(60//step)*24,0,(60//step)*24)
    
    xticks = range(0, (60//step)*24  , (60//step)*24//ndays)
    plt.xticks(xticks)
    ax.set_xticklabels(window_x, rotation=90)
else:
    ext = (0,ndays,0,(60//step)*24)
    
    xticks = range(0, ndays, 15)
    plt.xticks(xticks)
    ax.set_xticklabels([i.date().strftime('%m-%d') for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_x[0], window_x[-1], datetime.timedelta(days=15)))], rotation=90)

plt.yticks(range(0, (60//step)*24+1, (60//step)))

"""only use some of the labels so it is legible"""
ax.set_yticklabels([i.time() for i in matplotlib.dates.num2date(matplotlib.dates.drange(window_y[0], window_y[-1], datetime.timedelta(minutes=60)))])

ax.imshow(np.reshape(alt_s, ((60//step)*24,ndays), order='F'), matplotlib.cm.plasma, origin="lower", extent=ext, vmin=0)

ax.set_title("Sun's altitude < {} degrees".format(sun_alt))

plt.yticks(range(0, (60//step)*24+1, (60//step)))
plt.xticks(xticks)

plt.show()