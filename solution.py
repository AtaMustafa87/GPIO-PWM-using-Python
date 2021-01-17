# Importing Libraries

import RPi.GPIO as GPIO
import time
from tkinter import *
from tkinter import messagebox
import tkinter.font
# Libraries Imported successfully

# Raspberry Pi 3 Pin Settings

LED = 32 # pin12
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # We are accessing GPIOs according to their physical location
GPIO.setup(LED, GPIO.OUT) # We have set our LED pin mode to output
GPIO.output(LED, GPIO.LOW) # When it will start then LED will be OFF

PwmValue = GPIO.PWM(LED, 5000)
PwmValue.start(0)

# Raspberry Pi 3 Pin Settings
w,h = 480,320
# tkinter GUI basic settings
window = Tk()
window.title("PWM Using RPi")
window.geometry(f"{w}x{h}")
window.config(background= "#0080FF")
Font1 = tkinter.font.Font(family = 'Helvetica', size = int(w/24), weight = 'bold')
mainBtnFont = tkinter.font.Font(family = 'Helvetica', size = 20, weight = 'bold')
lblFont = tkinter.font.Font(family = 'Helvetica', size = 16, weight = 'bold')
smallBtnFont = tkinter.font.Font(family = 'Helvetica', size = 20)
isPowerButtonEnabled = False
isPumpOn = False
disableColor = "#555555"
onColor = "#00FF00"
offColor = "#FF0000"

# Utility functions
def ChangePWM(e):
    global PwmValue,Scale1
    PwmValue.ChangeDutyCycle(Scale1.get())

def turnPumpOn():
    global PwmValue,powerButton
    PwmValue.ChangeDutyCycle(100)
    powerButton.config(background = onColor,text="ON")
    messagebox.showinfo(title="Status",message = "Pump Turned ON")

def turnPumpOff():
    global PwmValue,powerButton
    PwmValue.ChangeDutyCycle(0)
    powerButton.config(background = offColor,text="OFF")
    messagebox.showinfo(title="Status",message = "Pump Turned OFF")

def powerOnOffHandler(event):
    global isPowerButtonEnabled,isPumpOn,offColor,onColor,disableColor
    btn = event.widget
    if isPowerButtonEnabled:
        if isPumpOn:
            isPumpOn = False
            btn.config(background = offColor,text="OFF")
            turnPumpOff()
        else:
            isPumpOn = True
            btn.config(background = onColor,text="ON")
            turnPumpOn()
        
def powerEnableHandler(event):
    global isPowerButtonEnabled,isPumpOn,offColor,onColor,disableColor,PwmValue,Scale1
    btn = event.widget
    if isPowerButtonEnabled:
        isPowerButtonEnabled = False
        btn.config(background = disableColor,text="Disabled")
        PwmValue.ChangeDutyCycle(Scale1.get())
    else:
        isPowerButtonEnabled = True
        if isPumpOn:
            btn.config(background = onColor,text="ON")
            turnPumpOn()
        else:
            btn.config(background = offColor,text="OFF")
            turnPumpOff()
def actionToPerform():
    turnPumpOff()
onDuration = -1
def oneMinuteHandler(e):
    global onDuration,Scale1,isPowerButtonEnabled
    if isPowerButtonEnabled:
        messagebox.showerror(title="Error",message="Please disable power button to turn on for specified period")
    else:
        messagebox.showinfo(title="Status",message="Pump Turned ON for ONE minute with Duty Cycle = "+str(Scale1.get()))
        onDuration = 60
def fiveMinuteHandler(e):
    global onDuration,Scale1,isPowerButtonEnabled
    if isPowerButtonEnabled:
        messagebox.showerror(title="Error",message="Please disable power button to turn on for specified period")
    else:
        onDuration = 60*5
        messagebox.showinfo(title="Status",message="Pump Turned ON for FIVE minute with Duty Cycle = "+str(Scale1.get()))

def tenMinuteHandler(e):
    global onDuration,Scale1,isPowerButtonEnabled
    if isPowerButtonEnabled:
        messagebox.showerror(title="Error",message="Please disable power button to turn on for specified period")
    else:
        onDuration = 60*10
        messagebox.showinfo(title="Status",message="Pump Turned ON for TEN minute with Duty Cycle = "+str(Scale1.get()))

def timerHandler():
    global window,PwmValue,Scale1,isPowerButtonEnabled,onDuration
    if not isPowerButtonEnabled:
        if onDuration > 0:
            onDuration = onDuration - 1
            powerButton.config(background = onColor,text="ON")
            PwmValue.ChangeDutyCycle(Scale1.get())
        elif onDuration == 0:
            onDuration = -1
            turnPumpOff()
    window.after(1000,timerHandler)
    

def addButton(window,x,y,w,h,txt,f,handler=None):
    btn = Button(master=window,text=txt,width=w,height=h,font=f)
    if handler:
        btn.bind("<Button-1>", handler)
    btn.place(x=x,y=y)
    return btn

    

Scale1 = Scale(window, from_=0, to=100, orient = HORIZONTAL, length=w-170, width=int(h/20), sliderlength=40, resolution = 1, command = ChangePWM)
Scale1.place(x=157,y=h-50)
Label(window,text='PUMP SPEED', font = lblFont, bg = '#0080FF', fg='#FFFFFF').place(x=7,y=h-40)
x,y= 20,15
dy = 55
w,h = 8,2
powerButton = addButton(window,x,y,w,h,"Power",mainBtnFont,powerOnOffHandler)
powerButton.bind("<Button-3>",powerEnableHandler)
x = 320
addButton(window,x,y,w,h,"Menu",mainBtnFont)
x = 20
y = y + 90
h = 1
addButton(window,x,y,w,h,"1 Minute",smallBtnFont,oneMinuteHandler)
y = y + dy
addButton(window,x,y,w,h,"5 Minute",smallBtnFont,fiveMinuteHandler)
y = y + dy
addButton(window,x,y,w,h,"10 Minute",smallBtnFont,tenMinuteHandler)
x = 320
addButton(window,x,y,w,h,"Button",smallBtnFont)

timerHandler()
window.mainloop()