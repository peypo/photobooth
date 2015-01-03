# -*-coding:Utf-8 -*
#!/usr/bin/python3

"""
This is a photobooth.
When the button is pushed, it takes 4 pictures, merge them, then (if requested) print the result.
"""

import RPi.GPIO as GPIO, time, os, subprocess
from sys import exit


# VARIABLES
racine = '/home/pi/photobooth/'

# GPIO setup
GPIO.setmode(GPIO.BCM)

class Led(object):
    """docstring for Led"""
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)
        self.status = False # False = off || True = on

    def getStatus(self):
        return self.status

    def getPin(self):
        return self.pin

    def blink(self,times=10,delay=0.4):
        for i in range(0,times*2):
            self.lightToogle()
            time.sleep(delay)

    def lightOn(self):
        if self.status: # led was ON
            print("LED {} already on".format(self.pin))
        else: # led was OFF
            print("LED {} on".format(self.pin))
            GPIO.output(self.pin,True)
            self.status = True

    def lightOff(self):
        if self.status: # led was ON
            print("LED {} off".format(self.pin))
            GPIO.output(self.pin,False)
            self.status = False
        else: # led was OFF
            print("LED {} already off".format(self.pin))

    def lightToogle(self):
        if self.status: # led was ON
            print("LED {} toogled to off".format(self.pin))
            self.lightOff()
        else: # led was OFF
            print("LED {} toogled to on".format(self.pin))
            self.lightOn()

        
class Switch(object):
    """docstring for Switch"""
    def __init__(self, pin):
        super().__init__()
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def getPin(self):
        return self.pin
        

#test
def test(arg=''):
    print("TEST -- This is a test. It lights on all 3 leds.")
    PRINT_LED.lightOn()
    POSE_LED.lightOn()
    BUTTON_LED.lightOn()

#clean exit
def clean_exit(arg=''):
    print("--- Hope to see you soon!")
    GPIO.cleanup() # this ensures a clean exit on a GPIO point of view

# snap function
def pose():
    print("pose!")
    BUTTON_LED.lightOff()
    POSE_LED.blink(5,0.2) # blink fast
    POSE_LED.blink(5,0.1) # blink faster
    POSE_LED.lightOn()
    print("SNAP")
    #  --set-config focusmetermode=2
    gpout = subprocess.check_output("gphoto2 --set-config imagesize=2 --set-config f-number=1 --set-config isoauto=0 --set-config flashmode=0 --capture-image-and-download --keep --filename /home/pi/photobooth/pictures/tmp/photobooth_%Y%m%d_%H%M%S.jpg", stderr=subprocess.STDOUT, shell=True).decode("utf-8")
    print(gpout)
    gpout = gpout.lower()
    POSE_LED.lightOff()
    if "error" not in str(gpout) and "erreur" not in str(gpout): 
        return True
    else:
        return False

# print funtion (not yet set)
def printer():
    # Wait to ensure that print queue doesn't pile up
    # TODO: check status of printer instead of using this arbitrary wait time
    return

def remove_tmp_content(folder=racine+'pictures/tmp/'):
    print("delete ",len(os.listdir(folder))," items in ",folder)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                print("\tfile: ",file_path)
                os.unlink(file_path)
            else:
                print("\tfolder: ",file_path," -- NOT DELETED")
        except Exception as e:
            print(e)
    return

# complete shooting process
def shoot(arg=''):
    snap = 0
    while snap < 4:
        result = pose()
        if result: 
            snap += 1
        else:
            print("Error ?! I don\'t carre, I\'ll try again!")
    print("please wait while your photos are merged...", end='')
    # build image and send to printer
    subprocess.call("sudo /home/pi/photobooth/scripts/assemble_and_print.sh", shell=True)
    print("merge done!")
    PRINT_LED.lightOn()
    time.sleep(0.5) #let's take a breath
    #tmp = 'no' #default : no print
    #tmp = input("Do you want to print the result ? [Y/n]").lower()
    #if tmp in ("y", "yes", "") :
    #    print("Oki doki ; let's print!")
        #printer()
        #gestion de la file d'attente...
        #time.sleep(110)
    #else:
    #    print("No ?!? OK, as you wish...")
    print("ready for next round")
    PRINT_LED.lightOff()
    BUTTON_LED.lightOn()

# keep the script running function
def loop():
    while True:
        tmp = input(">>> ").lower()
        if tmp == "exit" :
            exit("--- (exit as requested)")
            return
        elif tmp == "help" :
            print("Don't worry, here are the keywords you case use: ")
            print("\t test -- ensure it works")
            print("\t exit -- close the photobooth application")
            print("\t start -- run the booth")
            print("\t clean -- clean the temp folder")
        elif tmp == "test" :
            test()
        elif tmp == "start" :
            remove_tmp_content()
            shoot("via commande")
        elif tmp == "clean" :
            remove_tmp_content()
        time.sleep(0.2)
    return


# Define a function to run when an interrupt is called
def shutdown(arg):
    print("--- Shutdown button pushed \n\r--- Good bye! ")
    #call('halt', shell=False)
    os.system("sudo shutdown -h now")

def gpio_setup():
    # set leds
    global PRINT_LED
    global POSE_LED
    global BUTTON_LED
    PRINT_LED = Led(22)
    POSE_LED = Led(18)
    BUTTON_LED = Led(23)

    # set switches
    global SHOOT_SWITCH
    global CANCEL_SWITCH
    global SHUTDOWN_SWITCH
    SHOOT_SWITCH = Switch(24)
    CANCEL_SWITCH = Switch(25) #pin number to be confirmed
    SHUTDOWN_SWITCH = Switch(26) #pin number to be confirmed
    # set switches event detect
    #GPIO.add_event_detect(SHUTDOWN_SWITCH.getPin(), GPIO.RISING, callback=shutdown, bouncetime=200) # Set up an interrupt to look for button presses
    GPIO.add_event_detect(SHOOT_SWITCH.getPin(), GPIO.RISING, callback=shoot, bouncetime=200) # Set up an interrupt to look for button presses
    #GPIO.add_event_detect(SHOOT_SWITCH.getPin(), GPIO.RISING, callback=test, bouncetime=200) # Set up an interrupt to look for button presses


if __name__ == "__main__": #in case the file is used in standalone mode
    os.system('clear')
    print("PHOTOBOOTH waits for order...")
    gpio_setup()
    
    # Run the loop function to keep script running
    try:        
        loop()

    except KeyboardInterrupt:  
        print("--- Exit using CTRL+C")

    except Exception as e:  
        print("--- Error or exception occurred! :(")
        print(str(e))

    finally:
        clean_exit()