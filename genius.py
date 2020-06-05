from time import sleep
from RPi import GPIO
import random

GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

### Constants ###
LED1 = 6
LED2 = 11
LED3 = 10
LED4 = 17
LED_LIST = [LED1,LED2,LED3,LED4]

BUTTON1 = 12
BUTTON2 = 8
BUTTON3 = 24
BUTTON4 = 18

N = 2
MICRO_TIME = .1
HALF_TIME = .5

### Variables ###
selectedColor = None
colors = []

### GPIO Setup ###
GPIO.setup(BUTTON1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)
GPIO.setup(N, GPIO.OUT)

# Check all outputs and start off
GPIO.output(N,1)
sleep(MICRO_TIME)
GPIO.output(LED1,1)
sleep(MICRO_TIME)
GPIO.output(LED2,1)
sleep(MICRO_TIME)
GPIO.output(LED3,1)
sleep(MICRO_TIME)
GPIO.output(LED4,1)
sleep(HALF_TIME)
GPIO.output(LED4,0)
sleep(MICRO_TIME)
GPIO.output(LED3,0)
sleep(MICRO_TIME)
GPIO.output(LED2,0)
sleep(MICRO_TIME)
GPIO.output(LED1,0)
sleep(MICRO_TIME)
GPIO.output(N,0)

### Functions ###

# gets the color pressed by the user
def getColor():
        while True:
                if(GPIO.input(BUTTON1) == 0):
                        return LED1
                elif(GPIO.input(BUTTON2) == 0):
                        return LED2
                elif(GPIO.input(BUTTON3) == 0):
                        return LED3
                elif(GPIO.input(BUTTON4) == 0):
                        return LED4

# plays the note for a given time
def playNote(t):
        GPIO.output(N,1)
        sleep(t)
        GPIO.output(N,0)

# lights a given LED for a given time
def lightLED(led,t):
        GPIO.output(led,1)
        sleep(t)
        GPIO.output(led,0)

# plays note and lights LED
def playColor(led,t):
        GPIO.output(led,1)
        GPIO.output(N,1)
        sleep(t)
        GPIO.output(N,0)
        GPIO.output(led,0)

# gets a random color/LED
def getRandColor():
        randomInt = random.randint(1,4)
        if(randomInt==1):
                return LED1
        elif(randomInt==2):
                return LED2
        elif(randomInt==3):
                return LED3
        else:
                return LED4

# plays the sequence for the user
def playSequence():
        for led in colors:
                playColor(led,0.3)
                sleep(0.3)

# adds new random color to the colors array
def addColor():
        randomColor = getRandColor()
        colors.append(randomColor)

# terminates the game in an amazing way
def playEndGame():
        print ("\n\n*** THE USER HAS LOST! ***\n\n")
        sleep(0.1)
        GPIO.output(LED_LIST,1)
        for i in range(0,7):
                playNote(0.15)
                sleep(0.15)
        GPIO.output(LED_LIST,0)
        GPIO.cleanup()  # cleans up the "mess"
        exit()

# gets all the sequence, dealing with failure
def getColorSequence():
        selectedColor = None
        for color in colors:
                selectedColor = getColor()
                playColor(selectedColor,0.3)
                if(selectedColor != color):
                        playEndGame()


# Wait one second before the game starts
sleep(1)

# Buzz sound warning the program started
for i in range(0,5):
        playNote(0.15)
        sleep(0.15)

# Wait one second before the game starts
sleep(1)

# Run
try:
        while True:
                addColor()
                playSequence()
                getColorSequence()
                sleep(.5)

except KeyboardInterrupt:
        playNote(0.5)
        GPIO.cleanup()
        print ("\nProgram is over!")
