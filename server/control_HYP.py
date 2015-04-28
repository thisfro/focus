# Info:
#   Project focus
#   Server control control.py
#
# Description:
#   Main control script of the server
#
# Edit:
#   Mar 2015
#   Version 1.1
#
# (c) Jannis Portmann

import web #import web.py library
from web import form #import form-web.py library
import RPi.GPIO as GPIO	#import GPIO library
import time #being used for intervals

# ----- GPIO Definitions -------
#GPIO-pin 17 (Machine) -- 240V detect [HYPOTHETICAL - 3V pin for demonstration purposes]
on_pin = 11

#GPIO-pin 4 (Coffee)
coffee_pin = 7

#GPIO-pin 22 (Espresso)
espresso_pin = 15

#GPIO-pin 23 (Rotary-Press)
rotary_pin = 16

#GPIO-pin 25 (Machine power) -- 240V relay [HYPOTHETICAL - No current]
#power_pin = 22

#use board numbers and ignore warnings
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#use pin 4, 22, 23 and 25 as output
GPIO.setup(espresso_pin, GPIO.OUT)
GPIO.setup(coffee_pin, GPIO.OUT)
GPIO.setup(rotary_pin, GPIO.OUT)

#use pin 17 as input
GPIO.setup(on_pin, GPIO.IN)

# ----- Web.py Definitions -----
render = web.template.render('templates/')

urls = ('/','index')
app = web.application(urls, globals())

# ----- Event Definitions -----
 #set status  to ready after startup
iterator = 0 #set startup-counter to 0
cupsleft = 0 #set amount of left cups to 0 (worst case)

#press rotary to get the coffee machine up and running
def startup():
    print "LOG: Starting up machine..."
    GPIO.output(rotary_pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(rotary_pin, GPIO.LOW)

def espresso():
    print "LOG: An espresso is being poured ..."
    GPIO.output(espresso_pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(espresso_pin, GPIO.LOW)
    global status
    status = status(str('write'),int(1))
    # cleft('sub')

def coffee():
    print "LOG: A coffee is being poured ..."
    GPIO.output(coffee_pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(coffee_pin, GPIO.LOW)
    global status
    status = status(str('write'),int(1))

def status(option, value):
    if option == 'get':
        print 'LOG: Reading status...'
        f = open('status.txt','r')
        stat = f.read()
        print 'LOG: Status is ' + str(stat)
        return int(stat)
    if option == 'write':
        f = open('status.txt','w')
        f.write(str(value))
        stat = value
        print 'LOG: Status set to ' + str(stat)
    f.close

class index:
	#render form on http request
    def GET(self):
        s = status(str('get'),str(''))
        print s
        str(s)
        if s == 0:
            print 'LOG: Ready for orders!'
            return render.ready('',cupsleft)
        elif s == 1:
            print 'LOG: Machine is busy, try later!'
            return render.busy('',cupsleft)
        else:
            print 'ERROR: Unexcepted error'
            return render.error('',cupsleft)

        # ----- [HYPOTHETICAL] ---------------------------------------------------------*
        # if GPIO.input(on_pin) == True: #in case of a running machine [HYPOTHETICAL]   |H
        #     if status == 0: #in case of ready                                         |Y
        #        cleft('read')                                                          |P
        #        print "LOG: Ready for orders. Cups left: " + cupsleft                  |O
        #        return render.ready('',cupsleft)                                       |T
        #     if status == 1: #in case of busy                                          |H
        #         print "LOG: Machine is busy, try later."                              |E
        #         return render.busy('')                                                |T
        #                                                                               |I
        # else: #in case of a sleeping machchine [HYPOTHETICAL]                         |C
        #     startup()                                                                 |A
        #     return render.startup('')                                                 |L
        # ------------------------------------------------------------------------------*

    #show output
    def POST(self):
        x = web.input(form_action = 'dafuq') #no comment

        #When Espresso is clicked
        if x.form_action == 'espresso':
            print "Right decision!"
            espresso()
            return render.busy('',cupsleft)

        #When Coffee is clicked
        if x.form_action == 'coffee':
            print "You fool!"
            coffee()
            return render.busy('',cupsleft)

        if x.form_action == 'normal'
            status = status(str('write'),int(0))
            print "LOG: Status set to 0"
            return render.ready('',cupslaeft)

        #---------------------------------------------------------------

        # #To reset status
        # if x.form_action == 'reset':
        #     print "LOG: Resetting..."
        #     global status
        #     status = 0
        #     cleft('read')
        #     cleft('read')
        #     global cupsleft
        #     cl = int(cupsleft)
        #     if cl > 0:
        #         print "LOG: Ready for orders. Cups left: " + cupsleft
        #         return render.ready('',cupsleft)
        #     if cl <= 0:
        #        return render.nocups()
        #
        # #Continue
        # if x.form_action == 'yes':
        #     global cupsleft
        #     cupsleft = '-';
        #     fw = open('cupsleft.txt','w')
        #     fw.write(cupsleft) #write new amount
        #     fw.close()
        #     return render.ready('',cupsleft)
        #
        # #Reset cup value
        # if x.form_action == 'settousual':
        #     global cupsleft
        #     cupsleft = '5';
        #     fw = open('cupsleft.txt','w')
        #     fw.write(cupsleft) #write new amount
        #     fw.close()
        #     return render.ready('',cupsleft)
        #
        # #LOOOOL
        # if x.form_action == 'panic':
        #     #Coming soon!
        #     global cupsleft
        #     return render.ready('',cupsleft)

# status = status('write',0)

if __name__=="__main__":
    app.run()

# --------------- END OF FOCUS CONRTOL --------------- #