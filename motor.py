#!/usr/bin/env python3
import sys
sys.path.insert(1, './ev3/python-ev3dev2-2.1.0.post1/ev3dev2')
from motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from sensor import INPUT_1
from sensor.lego import TouchSensor
from led import Leds
from button import Button

# TODO: Add code here


tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
btn = Button()
# drive in a turn for 5 rotations of the outer motor
# the first two parameters can be unit classes or percentages.


# drive in a different turn for 3 seconds
def forward():
    tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 3)
    print("ran forward()")

def backwards():
    tank_drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 3)
    print("ran backwards()")

#btn.on_up(forward)
#btn.on_down(backwards)
while True:
    if (check_buttons(['up'])):
        forward()
    elif (check_buttons(['down'])):
        backwards()