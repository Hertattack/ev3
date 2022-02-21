#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.port import LegoPort
from ev3dev2.sensor.lego import UltrasonicSensor

p2 = LegoPort(INPUT_2)
p2.mode = 'nxt-i2c'

sleep(0.5)

us = UltrasonicSensor(INPUT_2)

us.mode = us.MODE_US_DIST_CM
while True:
  print(us.distance_centimeters)
  sleep(1)

