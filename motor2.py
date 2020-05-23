#!/usr/bin/env python3
#import sys
#sys.path.insert(1, './ev3/python-ev3dev2-2.1.0.post1/ev3dev2')
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, MoveSteering, MoveDifferential, SpeedRPM
#from ev3dev2.sensor import INPUT_1
from ev3dev2.wheel import EV3EducationSetRim
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from time import sleep
import threading

STUD_MM = 8

# TODO: Add code here

speed = 20
sound = Sound()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetRim, 16 * STUD_MM)
btn = Button()
arm = MediumMotor()
arm.position = 0
supply = PowerSupply()
mdiff.odometry_start()

movements = []
# drive in a turn for 5 rotations of the outer motor
# the first two parameters can be unit classes or percentages.


# drive in a different turn for 3 seconds
def set_default_speed():
    global speed
    speed = 30
    global travel #mm, distance to travel forwards and backwards
    travel = 100
    global brake
    brake = True
    global turn_degrees
    turn_degrees = 15
def forward():
    thing = 1
    #mdiff.on_for_distance(SpeedRPM(speed), travel)
    tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), 1)
    movements.append("f")
    print("ran forward()")

def backwards():
    #mdiff.on_for_distance(SpeedRPM(speed), travel-(travel*2))
    tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), -1)
    print("ran backwards()")
    movements.append("b")

def left():
    #mdiff.turn_left(SpeedRPM(speed), 45)
    #steering_drive.on_for_seconds(40, SpeedPercent(speed+10), 1)
    #steering_drive.on_for_degrees(-50, SpeedPercent(speed+10), 45)
    mdiff.turn_right(speed, turn_degrees, [True, [False]])  
    movements.append("l")
    #tank_drive.on_for_degrees(SpeedPercent(speed), SpeedPercent(speed-(speed*2)))

def right():
    #mdiff.turn_right(SpeedRPM(speed), 45)
    #steering_drive.on_for_degrees(50, SpeedPercent(speed+10), 45)
    #steering_drive.on_for_seconds(-40, SpeedPercent(speed+10), 1)
    mdiff.turn_left(speed, turn_degrees, [True, [False]])  
    movements.append("r")

def tts(message):
    sound.speak(message)

def go_home():
    reverse = movements[::-1]
    for i in range(len(reverse)):
        if (reverse[i] == 'f'):
            backwards()
        elif (reverse[i] == 'b'):
            forward()
        elif (reverse[i] == 'l'):
            right()
        elif (reverse[i] == 'r'):
            left()
    movements.clear()
    reverse.clear()
    #mdiff.on_to_coordinates(SpeedRPM(speed), 0, 0)

def speed_up():
    if (speed < 100):
        speed = speed + 10
        print("Speed changed to", speed)

def speed_down():
    if (speed > 10):
        speed = speed - 10
        print("Speed changed to", speed)

def arm_up():
    arm.on_to_position(30, 0)

def arm_down():
    arm.on_to_position(30, -917)

def volt_to_percent(volts):
    return ((volts-5)/2)*100

def check_battery():
    threading.Timer(600, check_battery).start()
    if (supply.measured_volts < 6):
        if (supplt.measured_volts > 5.5):
            tts("Battery getting low, {} percent battery left.".format(volt_to_percent(supply.measured_volts)))
        else:
            tts("Battery critically low, {} percent battery left.".format(volt_to_percent(supply.measured_volts)))


def handle(args):
    print(args)
    if (args['button']['command'] == 'u'):
        forward()
    elif (args['button']['command'] == 'd'):
        backwards()
    elif (args['button']['command'] == 'l'):
        left()
    elif (args['button']['command'] == 'r'):
        right()
    elif (args['button']['command'] == 'arm_up'):
        arm_up()
    elif (args['button']['command'] == 'arm_down'):
        arm_down()
    elif (args['button']['command'] == 'home'):
        go_home()
   #elif (args['button']['command'] == 'speed_up'):
    #   speed_up()
   #elif (args['button']['command'] == 'speed_down'):
    #   speed_down()

set_default_speed()

check_battery()

#btn.on_up(forward)
#btn.on_down(backwards)
#while True:
    #if (btn.check_buttons(['up'])):
        #forward()
    #elif (btn.check_buttons(['down'])):
        #backwards()

#sense.distance_centimeters_continuous()
#while True:
#    if us.distance_centimeters < 8: # to detect objects closer than 40cm
#        # In the above line you can also use inches: us.distance_inches < 16
#        backwards()

#    sleep (0.5) # Give the CPU a rest
#print(us.distance_centimeters)
