#!/usr/bin/env python3
#import sys
#sys.path.insert(1, './ev3/python-ev3dev2-2.1.0.post1/ev3dev2')
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering, MoveDifferential, SpeedRPM
#from ev3dev2.sensor import INPUT_1
from ev3dev2.wheel import EV3EducationSetRim
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
from ev3dev2.button import Button
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from time import sleep
import robot_util
import threading
import importlib
tts_module = importlib.import_module('tts.ev3')

STUD_MM = 8

# TODO: Add code here

speed = 20
sound = Sound()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_B, EV3EducationSetRim, 16 * STUD_MM)
btn = Button()
arm = MediumMotor()
lightswitch = LargeMotor(OUTPUT_D)
lightswitch.position = 0
arm.position = 0
supply = PowerSupply()
mdiff.odometry_start()
scriptname = "/hardware/ev3.py"
debug = True
stationary_mode = False

movements = []
# drive in a turn for 5 rotations of the outer motor
# the first two parameters can be unit classes or percentages.

def debug_log(message):
    global debug
    if (debug):
        print(message)

# drive in a different turn for 3 seconds
def setup(robot_config):
    global speed
    speed = 70
    global travel #mm, distance to travel forwards and backwards
    travel = 100
    global brake
    brake = True
    global turn_degrees
    turn_degrees = 32.5
    global stationary_mode
    stationary_mode = False
def forward():
    thing = 1
    #mdiff.on_for_distance(SpeedRPM(speed), travel)
    tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), 1)
    debug_log("ran forward()")
    tank_drive.wait_until_not_moving()
    tank_drive.reset()
    if (tank_drive.is_stalled):
        tts_module.say("Oops, I might be stuck!")
        tank_drive.reset()
        backwards()
    else:
        movements.append("f")
        

def backwards():
    #mdiff.on_for_distance(SpeedRPM(speed), travel-(travel*2))
    tank_drive.on_for_rotations(SpeedPercent(speed), SpeedPercent(speed), -1)
    debug_log("ran backwards()")
    tank_drive.wait_until_not_moving()
    tank_drive.reset()
    if (tank_drive.is_stalled):
        tts_module.say("Oops, I might be stuck!")
        tank_drive.reset()
        forward()
    else:
        movements.append("b")

def left():
    #mdiff.turn_left(SpeedRPM(speed), 45)
    #steering_drive.on_for_seconds(40, SpeedPercent(speed+10), 1)
    #steering_drive.on_for_degrees(-50, SpeedPercent(speed+10), 45)
    mdiff.turn_right(speed, turn_degrees, [True, [False]])  
    mdiff.wait_until_not_moving()
    mdiff.reset()
    if (mdiff.is_stalled):
        tts_module.say("Oops, I might be stuck!")
        mdiff.reset()
        #right()
    else:
        movements.append("l")
    #tank_drive.on_for_degrees(SpeedPercent(speed), SpeedPercent(speed-(speed*2)))

def right():
    #mdiff.turn_right(SpeedRPM(speed), 45)
    #steering_drive.on_for_degrees(50, SpeedPercent(speed+10), 45)
    #steering_drive.on_for_seconds(-40, SpeedPercent(speed+10), 1)
    mdiff.turn_left(speed, turn_degrees, [True, [False]])  
    mdiff.wait_until_not_moving()
    mdiff.reset()
    if (mdiff.is_stalled):
        tts_module.say("Oops, I might be stuck!")
        mdiff.reset()
        #left()
    else:
        movements.append("r")

def connection(source):
    global scriptname
    print("{}: connected to {}".format(scriptname, source))

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

def get_battery():
    return volt_to_percent(supply.measured_volts)

def speed_up():
    if (speed < 100):
        speed = speed + 10
        debug_log("Speed changed to", speed)

def speed_down():
    if (speed > 10):
        speed = speed - 10
        debug_log("Speed changed to", speed)

def arm_up():
    arm.on_to_position(30, 0)

def arm_down():
    arm.on_to_position(30, -917)

def volt_to_percent(volts):
    return ((volts-5)/3)*100

def check_battery():
    threading.Timer(20, check_battery).start()
    if (supply.measured_volts < 6):
        if (supply.measured_volts > 5.5):
            tts_module.say("Battery getting low, {} percent battery left.".format(volt_to_percent(supply.measured_volts)))
        else:
            tts_module.say("Battery critically low, {} percent battery left.".format(volt_to_percent(supply.measured_volts)))

def lights_on():
    lightswitch.on_to_position(30, -28)
def lights_off():
    lightswitch.on_to_position(30, 0)

def stationary_on():
    global stationary_mode
    stationary_mode = True
    debug_log("ran stationary_on()")

def stationary_off():
    global stationary_mode
    stationary_mode = False
    debug_log("ran stationary_off()")

def move(args):
    print(args)
    global stationary_mode
    if (args['button']['command'] == 'u' and stationary_mode == False):
        forward()
    elif (args['button']['command'] == 'd' and stationary_mode == False):
        backwards()
    elif (args['button']['command'] == 'l' and stationary_mode == False):
        left()
    elif (args['button']['command'] == 'r' and stationary_mode == False):
        right()
    elif (args['button']['command'] == 'arm_up' and stationary_mode == False):
        arm_up()
    elif (args['button']['command'] == 'arm_down' and stationary_mode == False):
        arm_down()
    elif (args['button']['command'] == 'home' and stationary_mode == False):
        go_home()
    elif (args['button']['command'] == 'lights_on'):
        lights_on()
    elif (args['button']['command'] == 'lights_off'):
        lights_off()
    elif (args['button']['command'] == 'clear_buffer'):
        movements.clear()
        tts_module.say("Movement buffer cleared.")
        robot_util.sendChatMessage("Movement buffer cleared.")
   #elif (args['button']['command'] == 'speed_up'):
    #   speed_up()
   #elif (args['button']['command'] == 'speed_down'):
    #   speed_down()



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
