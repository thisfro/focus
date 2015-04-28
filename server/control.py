# -*- coding: utf-8 -*-

# Info:
#   Project focus
#   Server control control.py
#
# Description:
#   Main control script of the server
#
# Edit:
#   Apr 2015
#   Version 1.1
#
# (c) Jannis Portmann

import web #import web.py library
from web import form #import form-web.py library
import RPi.GPIO as GPIO	#import GPIO library
import time #being used for intervals

# ----- GPIO Definitions -------
#GPIO-pin 4 (Coffee)
coffee_pin = 16

#GPIO-pin 5 (Espresso)
espresso_pin = 18

#GPIO-pin 2
motor_pin = 13

#GPIO-pin 3 (Distance)
distance_pin = 15

#use board numbers and ignore warnings
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#use pin 4, 22, 23 and 25 as output
GPIO.setup(espresso_pin, GPIO.OUT)
GPIO.setup(coffee_pin, GPIO.OUT)
#GPIO.setup(rotary_pin, GPIO.OUT)
GPIO.setup(motor_pin, GPIO.OUT)
GPIO.setup(distance_pin, GPIO.IN)

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
    status(str('write'),int(1))
    # cleft('sub')

def coffee():
    print "LOG: A coffee is being poured ..."
    GPIO.output(coffee_pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(coffee_pin, GPIO.LOW)
    status(str('write'),int(1))

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

def transport():
    print 'trasporting...'

class index:
	#render form on http request
    def GET(self):
        s = status('get','')
        print s
        str(s)
        if s == 0:
            print 'LOG: Ready for orders!'
            return render.ready('')
        elif s == 1:
            print 'LOG: Machine is busy, try later!'
            return render.noreset('') # not resetting
        else:
            print 'ERROR: Unexpected error'
            return render.error('')

    #show output
    def POST(self):
        s = status('get','') #Update of status

        x = web.input(form_action = 'By my heel, I care not!') #Whatever...

        if x.form_action == 'reset':
            # transport()
            status(str('write'),int(0))
            print "LOG: Status set back to 0"
            return render.ready('')

        if s == 1:
            print 'LOG: Machine is busy, try later!'
            return render.noreset('')

        elif s == 0:
            #When Espresso is clicked
            if x.form_action == 'espresso':
                print "Right decision!"
                espresso()
                return render.busy('')

            #When Coffee is clicked
            if x.form_action == 'coffee':
                print "You fool!"
                coffee()
                return render.busy('')

            if x.form_action == 'normal':
                status(str('write'),int(0))
                print "LOG: Status set to 0"
                return render.ready('')

        else:
            print 'ERROR: Unexpected error'
            return render.error('')
if GPIO.input(distance_pin) == 1:
    print 'LOG: Distance <10'

if __name__=="__main__":
    app.run()


# --------------- END OF FOCUS CONRTOL --------------- #
# -------------------- YEAH MAN! --------------------- #
