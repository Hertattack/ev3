#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor

us = UltrasonicSensor(INPUT_2)

us.mode = us.MODE_US_DIST_CM
print(us.distance_centimeters);


