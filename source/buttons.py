import RPi.GPIO as GPIO
from time import sleep
import uinput



def sendLeft():
    device.emit_click(uinput.KEY_LEFT)
    print('Sent left')

def sendRight():
    device.emit_click(uinput.KEY_RIGHT)
    print('Sent right')

def sendSpace():
    device.emit_click(uinput.KEY_ENTER)
    print('Sent space')

def sayHi(arg): print(arg)


##
# Pins:
# Left: 7
# Center: 18
# Right: 37
# because connected to ground, looking for LOW

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

device = uinput.Device([
        uinput.KEY_LEFT,
        uinput.KEY_RIGHT,
        uinput.KEY_ENTER])


#GPIO.add_event_detect(7, GPIO.FALLING, callback=sendLeft, bouncetime=500) 
#GPIO.add_event_detect(18, GPIO.FALLING, callback=sendSpace, bouncetime=500)
#GPIO.add_event_detect(37, GPIO.FALLING, callback=sendRight, bouncetime=500)

sleep_time = .4

while True:
    if not GPIO.input(7):
        sendLeft()
        sleep(sleep_time)
    elif not GPIO.input(18):
        sendSpace()
        sleep(sleep_time)
    elif not GPIO.input(37):
        sendRight()
        sleep(sleep_time)

    sleep(.1)
    

GPIO.cleanup()
