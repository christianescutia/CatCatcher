# Code used to run on a Raspberry Pi

# import needed to connect to postgress server
import mysql.connector

# import for sleep function
from time import sleep

# import for sms messageing
from twilio.rest import Client

# imports needed for server motor
import RPi.GPIO as GPIO
import pigpio, time, os

# Global variables
Cage_ID = "CatCage00" # Set Unique per Cage
PORT = '65535'
gmail_user = ''
gmail_password = ''
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
TrapTriggered = False

# Use GPIO pin lables
GPIO.setmode(GPIO.BCM)

# Make variables for all the GPIO pins used
blueR = 13
greenR = 16
redR = 20
blueL = 19
greenL = 26
redL = 21
open = 22
close = 27
servo = 23

# Variable used in detection of door opening and closing
openBool = False

# setup the LEDs and limit switch
GPIO.setup(redR, GPIO.OUT)
GPIO.setup(greenR, GPIO.OUT)
GPIO.setup(blueR, GPIO.OUT)
GPIO.setup(redL, GPIO.OUT)
GPIO.setup(greenL, GPIO.OUT)
GPIO.setup(blueL, GPIO.OUT)
GPIO.setup(open, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(close, GPIO.IN, pull_up_down = GPIO.PUD_UP)

# start the pi gpio daemon
os.system("sudo pigpiod")

# Function that runs when the cage door is set
#       This function will flash the green LED
#       This function will also save the state of the door in openBool
def cage_door_set():
    global openBool

    # If the cage is already in the open state, return
    if openBool:
        return
    GPIO.output(greenR, GPIO.HIGH)
    print("Congrats, you set up the cage")
    sleep(10)
    GPIO.output(greenR, GPIO.LOW)
    openBool = True

# Function that runs when the cage door is closed
#       This function will flash the red LED
#       This function will also save the state of the door in openBool
#       This function will also run the function ActivateServoMotor
def cat_captured():
    global openBool

    # If the cage is already in the closed state, return
    if not openBool:
        return
    GPIO.output(redR, GPIO.HIGH)
    print("You caught the cat!!")
    ActivateServoMotor()
    sleep(1)
    GPIO.output(redR, GPIO.LOW)
    openBool = False

# Function that runs when tcat_captured is run
#       This function will take images at three angles
#       This function will also run the sendPicsGroup.py program
def ActivateServoMotor():

    # Setting up the servo
    pwm = pigpio.pi()
    pwm.set_mode(servo, pigpio.OUTPUT)
    pwm.set_PWM_frequency( servo, 50 )

    # Set servo position
    pwm.set_servo_pulsewidth( servo, 1150 )
    time.sleep(1)

    # Take a picture and save it under /home/pi/rightImage.jpg
    os.system("libcamera-jpeg -n -o /home/pi/rightImage.jpg")
    time.sleep(2)

    pwm.set_servo_pulsewidth( servo, 1650 )
    time.sleep(1)
    os.system("libcamera-jpeg -n -o /home/pi/middleImage.jpg")
    time.sleep(2)

    pwm.set_servo_pulsewidth( servo, 2150 )
    time.sleep(1)
    os.system("libcamera-jpeg -n -o /home/pi/leftImage.jpg")
    time.sleep(2)

    pwm.set_servo_pulsewidth( servo, 1650 )
    time.sleep(3)

    # Turning off servo
    pwm.set_PWM_dutycycle(servo, 0)
    pwm.set_PWM_frequency( servo, 0)

    # Run the program to send the pictures
    os.system("python3 sendPicsGroup.py")

# Tests internet connection and registers the cage
#       Also clears the list of image requests for this cage
def SendCageInfo():
    # define database connection data
    mydb = mysql.connector.connect(
        host='us-cdbr-east-04.cleardb.com',
        user='',
        password='',
        database= ''
    )

    # create cursor
    c = mydb.cursor()

    # check if previous entry if found delete
    sql_command = "SELECT cage_id FROM cages WHERE cage_id = \'Cage00\'"
    c.execute(sql_command)
    isEmpty = True
    for x in c:
        isEmpty = False

    if isEmpty == False:
        sql_command = "DELETE from cages WHERE cage_id = \'Cage00\'"
        c.execute(sql_command)
        mydb.commit()

    # update entry to current
    sql_command = "INSERT INTO cages (cage_id) VALUES (\'Cage00\')"
    c.execute(sql_command)

    # clear message board for this cage
    sql_command = "DELETE FROM msg_board WHERE box_id = \'Cage00\'"
    c.execute(sql_command)

    # commit changes
    mydb.commit()

    # close database connection
    mydb.close()

# Turns off all the LEDs
def lightsOff():
    GPIO.output(redL, GPIO.LOW)
    GPIO.output(greenL, GPIO.LOW)
    GPIO.output(blueL, GPIO.LOW)
    GPIO.output(redR, GPIO.LOW)
    GPIO.output(greenR, GPIO.LOW)
    GPIO.output(blueR, GPIO.LOW)

# Main function that runs on startup
def main():
    lightsOff()

    # Flash green to show the user that the program is running
    GPIO.output(greenL, GPIO.HIGH)
    GPIO.output(greenR, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(greenL, GPIO.LOW)
    GPIO.output(greenR, GPIO.LOW)
    time.sleep(3)

    # send current cage data to Heroku Database
    try:
        SendCageInfo()
    except:
        print("Something went wrong with Database Connection")
        GPIO.output(redL, GPIO.HIGH)
        GPIO.output(redR, GPIO.HIGH)
        time.sleep(3)
        lightsOff()
        return
    else:
        print("Database Data Sent")
        GPIO.output(blueL, GPIO.HIGH)
        GPIO.output(blueR, GPIO.HIGH)
        sleep(3)
        lightsOff()

    # Main for loop that will detect a change in the limit switch state
    try:
        while True:
            if(GPIO.input(open)):
                cage_door_set()
            if(GPIO.input(close)):
                cat_captured()
            os.system("python3 checkForRequests.py")
            sleep(15)

    except KeyboardInterrupt:
   	    GPIO.cleanup()


if __name__ == "__main__":
    main()
