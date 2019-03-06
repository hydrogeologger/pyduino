from gpiozero import Button

class UQ_RainFall:
    '''
    UQ_RainFall class, set up a bucket pin with approprisate debouncing time (time required for
    a tipping duration to be register), name, volume of each tip and debug flag
    Requires to run config after initialisation to allow automatic counting
    '''
    def __init__(self, pin = 2, debounce = 0.05, name = "Bucket 1" , volume = 0.2794, debug = True):
        #base on the Button class of gpiozero, pull_up = True means the reading pin default state is
        #high, so connect one pin to GND and one pin to the reading pin
        self.sensor_pin = Button(pin, pull_up = True, bounce_time = debounce)
        self.name = name
        self.debug = debug
        self.count = 0
        self.volume = volume

    def update(self):
        self.count = self.count + 1
        if self.debug is True:
            print(self.name + " tipped, new count = " + str(self.count))

    def config(self):
        #assign the event when_pressed to function update
        self.sensor_pin.when_pressed = self.update

    def reset(self):
        self.count = 0

#==================================================#
'''
This is for testing
Adjust the value debounce for best performance. Note 0.01 is
the minimum value.
'''
print("Testing")

test1 = UQ_RainFall(pin = 10, debounce = 0.01, name = "Bucket 1")
test2 = UQ_RainFall(pin = 21, debounce = 0.01, name = "Bucket 2")
test3 = UQ_RainFall(pin = 22, debounce = 0.01, name = "Bucket 3")
#Once config, the tipping is count automatically as an hardware event
#and immune to sleep in the main thread
test1.config()
test2.config()
test3.config()
print("Start observing")
while True:
    
    continue
#==================================================#


