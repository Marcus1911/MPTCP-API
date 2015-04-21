#!/usr/bin/python



import matplotlib.pyplot as plt
from pylab import *
import gtk
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure
import random
import time
import os
import gobject
import numpy



step = 0.2

# We set a simple GTK window (not GTKAgg)

win = gtk.Window()

win.connect("destroy", lambda x: gtk.main_quit())

win.set_default_size(700,900)

win.set_title("MultiPath TCP")

# We create the Figure and the plot

f = Figure(figsize=(4.66,6), dpi=150)
a = f.add_subplot(111)



subplots_adjust(bottom=0.09)
subplots_adjust(top=0.97)
subplots_adjust(left=0.28)
subplots_adjust(right=0.97)



# We stablish the values for X (representig time)

x = 0
t = list(numpy.arange(0,15,step))



#xticks(np.arange(min(t), max(t)+1, step))

setp(a.get_xticklabels(), visible=False)



# We stablish the values for Y (representing any signal)
y = 0
ard1 = [0]*len(t)

    

# Create a plot and set some parameters

a.plot(t, ard1 , 'r-', linewidth=1.5)
a.yaxis.grid(True)
a.set_ylim(0, 1)


a.set_title('MultiPath TCP')
a.set_ylabel('Goodput (Gbps)')

# This is the function that waits 1 second to redraw, then sets a random
# value for y and adds it to the 'ard1' array. For 't' we add 1 to the x
# value so it will simulate seconds.

def counter():

    x = 30
    start = time.time()
    last = 0

    while True:

        time.sleep(step)
        t.append(x)
        t.pop(0)



        x += time.time() - start
        start = time.time()



        if start - last >= 1:
            os.system("ssh marcus@127.0.0.1 tail -n 1 /tmp/10gig > /tmp/10gig")
            last = time.time()
            fi = open("/tmp/10gig.zip")
            s = fi.readline()
            fi.close()
            s.rstrip("\n")
            
            if len(s) != 0 :
                 y = float(s)/1000
                 
            else:
                 y = 0
        else:
            y = ard1[len(ard1)-1]

            ard1.append(y)
            ard1.pop(0)
            clf()
            cla()

            a.plot(t, ard1, 'r-', linewidth=1.5)
            a.set_xlim(min(t), max(t)+1)
            a.set_ylim(0, 1)
            f.canvas.draw()



# Create the widget, a FigureCanvas containing our Figure
canvas = FigureCanvas(f)
win.add(canvas)

# This gobject tells GTK to run the function while idle
gobject.idle_add(counter)

# And here we go!
win.show_all()

gtk.main()
