# Info:    
#   Project Home Smart Home
#   Server control control.py
#
# Description:
#   Main control script of the server
#
# Edit:    
#   Aug 2014
#   Version 1.0
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
power_pin = 22

#use board numbers
GPIO.setmode(GPIO.BOARD)

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
status = 0 #set status  to ready after startup
iterator = 0 #set startup-counter to 0

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
    status = 1

def coffee():
    print "LOG: A coffee is being poured ..."
    GPIO.output(coffee_pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(coffee_pin, GPIO.LOW)
    global status
    status = 1

class index: 
	#render form on http request
    def GET(self):
        # if GPIO.input(on_pin) == True: #in case of a running machine [HYPOTHETICAL]
        #     if status == 0: #in case of ready
                print "LOG: Ready for orders."
                return render.ready('')
        #     if status == 1: #in case of busy
        #         print "LOG: Machine is busy, try later."
        #         return render.busy('')
            
        # else: #in case of a sleeping machchine [HYPOTHETICAL]
        #     startup()
        #     return render.startup('')

    #show output
    def POST(self):
        x = web.input(form_action = 'espresso')

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

        #To reset status
        if x.form_action == 'reset':
            print "LOG: Resetting..."
            global status
            status = 0
            print "LOG: Ready for orders."
            return render.ready('')

if __name__=="__main__":
    app.run()

# --------------- END OF HSH CONRTOL --------------- #