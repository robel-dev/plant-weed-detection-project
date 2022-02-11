from tkinter.ttk import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import filedialog
from tkinter import Menu
from tkinter import ttk
from tkinter import *
from tkinter import font as tkfont
import pexpect
import subprocess
import time
import glob
from PIL import ImageTk, Image
from itertools import cycle
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# plt.style.use('dark_background')
def show_frame(framewidget):
    '''
    make the passed frame on top
    '''
    framewidget.tkraise()
    root.config(menu=menu)

###############ROOT PAGE#####################################
root = Tk()
root.geometry('1000x500')
root.title('Weed Detection & Analysis Tool V1.0')
root.configure(bg= 'lime')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
##all widgets list for customization
allwidgets = []

def setup_color(widget, bgc='#1e1e1a', fgc='#ccddcc', fontsize=10):
    try:
        widget.configure(bg=bgc, fg=fgc, font = ('ubuntu %i bold'%fontsize))
    except:
        print('error')
    
def exit_app(self):
    sys.exit(0)


root.bind('<Escape>', exit_app)
#############################################################
##############Introduction page START########################
start_frame = Frame(root, bg='aqua')
start_frame.grid(row=0, column=0, sticky='nswe')
start_frame.grid_rowconfigure(0, weight=1)
start_frame.grid_columnconfigure(0, weight=1)

img = PhotoImage(file = './assets/bg.gif')
C = Canvas(start_frame)
background_label = Label(start_frame, height=400, width=start_frame['width'])
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.configure(image=img)
bottomframe = Frame(start_frame, height=100, bg='#1e1e1a')
C.pack()
progresslabel = Label(bottomframe, text = '')
progresslabel.pack(side='bottom', pady=5, anchor='center')
transfericon = PhotoImage(file='./assets/data-transfer.gif')
starticon = PhotoImage(file='./assets/power-button.gif')

def transfer_from_raspi():
    progresslabel.configure(text='Please wait...', fg='white')
    progresslabel.update()
    pexpect.run("sshpass -p 'raspberry' scp -r pi@10.42.0.219:/home/pi/Desktop/segmentation/* /home/robel/Desktop/app/App")
    # result = subprocess.check_output(['wget', 'https://code.jquery.com/jquery-3.3.1.min.js'])
    progresslabel.configure(text='Success!', fg='lime')
    transferbtn.configure(text='Start',image=starticon, command=lambda: show_frame(main_frame))
    setup_color(transferbtn)
    start_frame.update()

transferbtn = Button(bottomframe, text= 'Transfer Files', compound='left',image=transfericon,width=150,command=transfer_from_raspi)
transferbtn.pack(side='left', padx=425, ipadx=10, anchor='center')
transferbtn.config(highlightbackground = 'lime', highlightthickness=1)
bottomframe.pack(side='bottom', fill='x', anchor= 'center')
allwidgets.append(background_label)
allwidgets.append(progresslabel)
allwidgets.append(transferbtn)
##############Introduction page END##########################

#############################################################
##############Main Page START################################
#############################################################
main_frame = Frame(root, width=1000, height=500, bg='orange')
main_frame.grid(row=0, column=0, sticky='nswe')

left = Frame(main_frame, bg='#1e1e1a', width=400, height=500)
right = Frame(main_frame, bg='#1e1e1a', width=600, height=500)
left.grid(row = 0, column=0, sticky='nswe')
right.grid(row = 0, column=1, sticky='nswe')
lefttop = Frame(left, bg='#1e1e1a', width=left['width'], height=350)
leftbtm = Frame(left, bg='#1e1e1a', width = left['width'], height =150)
lefttop.grid(row = 0, column=0, sticky='we')
leftbtm.grid(row = 1, column=0, sticky='nswe')
lefttop.grid_rowconfigure(0, weight=1, uniform="2")
leftbtm.grid_rowconfigure(1, weight=1, uniform='3')

#####################LEFT_SIDE######ANALYSIS#############
#FROM MODEL
labels = ["Oranges", "Bananas", "Apples", "Kiwis", "Grapes", "Pears"]
values = [0.1, 0.4, 0.1, 0.2, 0.1, 0.1]
# now to get the total number of failed in each section
actualFigure = plt.figure(figsize = (6,6), dpi=70)
actualFigure.set_facecolor('#1e1e1a')
actualFigure.suptitle("Analysis Report", fontsize = 12, color='#4ae081')
# as explode needs to contain numerical values for each "slice" of the pie chart (i.e. every group needs to have an associated explode value)
explode = list()
# colours =['orange', 'green', 'purple', 'brown', 'blue']
for k in labels:
    explode.append(0.05)
pie = plt.pie(values, explode=explode, shadow=True, autopct='%1.1f%%')
plt.legend(pie[0], labels, bbox_to_anchor=(.86,.1),loc="center left", fontsize=10)

canvas = FigureCanvasTkAgg(actualFigure, lefttop)
canvas.get_tk_widget().grid(row=0, column=0, sticky='nswe')

lefttop.grid_propagate(0)
leftbtm.grid_propagate(0)
right.grid_propagate(0)
left.grid_propagate(0)

def analysisreport(val):
        namelabels = ['Total weed coverage:', 'Weed distribution(Broad:Grass):','Type of farm:']
        newlist = [i+' '+v for i,v in zip(namelabels, val)]
        for t,r in zip(newlist,[1,2,3]):
                namelabel = Label(lefttop, text=t)
                namelabel.grid(row= r+1, column=0, sticky='w', padx=10, pady=2)
                setup_color(namelabel)
def suggestion(weed, herbi, r, title=False):
        weedlabel = Label(leftbtm, text=weed)
        herbilabel = Label(leftbtm, text=herbi)
        weedlabel.grid(row= r, column=0, sticky='w', padx=10, pady=2)
        herbilabel.grid(row= r, column=2, sticky='w',padx=10, pady=2)
        setup_color(weedlabel)
        setup_color(herbilabel)
        if title:
                setup_color(weedlabel, fgc='#4ae081', fontsize=10)
                setup_color(herbilabel, fgc='#4ae081', fontsize=10)
analysisreport(['20%','60:40','Maize'])

ttk.Separator(leftbtm, orient="horizontal").grid(row=0, column=0,columnspan=20, sticky="we")
sugtitle = Label(leftbtm, text='Herbicide Suggestions')
sugtitle.grid(row=1, column=0, sticky='nw', padx=10)
setup_color(sugtitle, fgc='#4ae081', fontsize=11)
suggestion('Weed', 'Herbicide', 2, True)
for i in range(4):
        suggestion('weed '+str(i), 'herbi '+str(i), i+3)

###########################################
########RIGHT_SIDE######MAP PLOT###################
titleright = Label(right, text='GPS Locations')
titleright.grid(row=0, sticky='nw', padx=10)
setup_color(titleright,fgc='#4ae081', fontsize=11)
rightseparator = ttk.Separator(right, orient="horizontal")
rightseparator.grid(row=1, column=0, sticky="we", columnspan=50)
displaylabel = Label(right)
displaylabel.grid(row=2, column=0, sticky='ns')
displaylabel.grid_propagate(0)
allwidgets.append(displaylabel)


def change_label(widget, txt):
        widget.configure(text = txt)        
        widget.pack()
########################file chooser###################
def load_GPS_data_menu():
    file = filedialog.askopenfilename()
    with open(file, mode='r') as f:
        displaylabel.configure(text=f.read())

def load_GPS_data(self):
        file = filedialog.askopenfilename()
        with open(file, mode='r') as f:
                displaylabel.configure(text=f.read())

def help_info(self):
    pass

#######################################
##############MENU###################
main_frame.bind('<Control-L>', load_GPS_data)
main_frame.bind('<Control-l>', load_GPS_data)
main_frame.bind('<Escape>', exit_app)
main_frame.bind('<KeyPress-F1>', help_info)

menu = Menu(main_frame)
new_item = Menu(menu, tearoff=0)
new_item.add_command(label='Load', command=load_GPS_data_menu)
new_item.add_command(label='Exit', accelerator= 'Esc', command= lambda: sys.exit(0))

help_item = Menu(menu, tearoff=0)
help_item.add_command(label='Software Usage', accelerator= 'F1', command=help_info)

abt_item = Menu(menu, tearoff=0)
abt_item.add_command(label='Version 1.0')

menu.add_cascade(label='File', menu=new_item)
menu.add_cascade(label='Help', menu=help_item)
menu.add_cascade(label='About', menu=abt_item)

for w in [menu, new_item, help_item, abt_item]:
    setup_color(w)

##########coloring
for w in allwidgets:
        try:
                setup_color(w)
        except:
                pass
##############Main Page END##################################   
show_frame(start_frame)   
root.config(menu=Menu(root))   
root.resizable(0,0)
root.protocol('WM_DELETE_WINDOW', lambda: sys.exit(0)) 
root.mainloop()



