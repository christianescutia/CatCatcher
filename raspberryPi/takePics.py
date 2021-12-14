#!/usr/bin/python3
import pigpio, time, os

servo = 23

# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth

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

# turning off servo
pwm.set_PWM_dutycycle(servo, 0)
pwm.set_PWM_frequency( servo, 0 )

