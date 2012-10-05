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
  s.write("c\r")

def start():
  clear()
  s.write("p0,0\r")

def pos(h, v):
  print "h,v", h, v
  s.write("p%d,%d\r" % (h,v))

print "go"
clear()
start()
print "started"

hpos = 1

s.write("wfish\r")

# E
pos(hpos, 0)
s.write("wX" + chr(0xee) * 4 + "\r")
#s.write("X")
#s.write( )
#s.write("\r")

pos(hpos,1)
s.write("wX")
s.write(chr(0xef) * 4)
s.write("\r\n")

pos(hpos,2)
s.write("wX")
s.write("\r\n")

pos(hpos,3)
s.write("wX")
s.write(chr(0xef) * 4)
s.write("\r\n")

# M
hpos = 6 + 2
pos(hpos,0)
s.write("wX")
s.write(chr(0xec))
s.write(' ')
s.write(chr(0xea))
s.write("X")
s.write("\r\n")

pos(hpos,1)
s.write("wX")
s.write(chr(0xed))
s.write(chr(0xef))
s.write(chr(0xeb))
s.write("X")
s.write("\r\n")

pos(hpos,2)
s.write("wX")
s.write(' ')
s.write(chr(0xee))
s.write(' ')
s.write("X")
s.write("\r\n")

pos(hpos,3)
s.write("wX")
s.write(' ' * 3)
s.write("X")
s.write("\r\n")

# F
hpos = (6 * 2) + 3
pos(hpos,0)
s.write("wX")
s.write(chr(0xee) * 4)
s.write("\r\n")

pos(hpos,1)
s.write("wX")
s.write(chr(0xef) * 4)
s.write("\r\n")

pos(hpos,2)
s.write("wX")
s.write("\r\n")

pos(hpos,3)
s.write("wX")
s.write("\r\n")

print s.read(10000)

s.close()
