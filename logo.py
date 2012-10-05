#!/usr/bin/env python
#
#
#

import serial
from time import sleep
from serial.serialutil import SerialException

try:
  s = serial.Serial("/dev/ttyACM1", 9600)
except serial.serialutil.SerialException:
  s = serial.Serial("/dev/ttyACM0", 9600)

s.timeout = 1

def clear():
  s.write(chr(0x0c))

def start():
  s.write(chr(0x1b))
  s.write(chr(0x00))
  s.write(chr(0x00))

def pos(h, v):
  print "h,v", h, v
  s.write(chr(0x1b))
  s.write(chr(v))
  s.write(chr(h))
  sleep(0.5)
#  print s.read(2)


print "go"
clear()
start()
print "started"

hpos = 1

# E
pos(hpos, 0)
s.write(chr(0x7f))
s.write(chr(0xee) * 4)

pos(hpos,1)
s.write(chr(0x7f))
s.write(chr(0xef) * 4)

sleep(0.5)
pos(hpos,2)
sleep(0.5)
s.write(chr(0x7f))
sleep(0.5)

pos(hpos,3)
sleep(0.5)
s.write(chr(0x7f))
sleep(0.5)
s.write(chr(0xef) * 4)
sleep(0.5)

# M
hpos = 6 + 2
pos(hpos,0)
s.write(chr(0x7f))
s.write(chr(0xec))
s.write(' ')
s.write(chr(0xea))
s.write(chr(0x7f))

pos(hpos,1)
s.write(chr(0x7f))
s.write(chr(0xed))
s.write(chr(0xef))
s.write(chr(0xeb))
s.write(chr(0x7f))

pos(hpos,2)
s.write(chr(0x7f))
s.write(' ')
s.write(chr(0xee))
s.write(' ')
s.write(chr(0x7f))

pos(hpos,3)
s.write(chr(0x7f))
s.write(' ' * 3)
s.write(chr(0x7f))

# F
hpos = (6 * 2) + 3
pos(hpos,0)
s.write(chr(0x7f))
s.write(chr(0xee) * 4)

pos(hpos,1)
s.write(chr(0x7f))
sleep(0.2)
s.write(chr(0xef) * 4)

pos(hpos,2)
s.write(chr(0x7f))

pos(hpos,3)
s.write(chr(0x7f))

print s.read(10000)

s.close()
