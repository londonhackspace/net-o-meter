#!/usr/bin/env python

import serial, time, random

class display:
  def __init__(self, dev="/dev/ttyACM0"):
#    dev = "/dev/cu.usbmodem1d12"
#    dev = "/dev/tty.usbmodem1d12"
    self.s = serial.Serial(dev, 9600)

  def send(self,thing):
    s = self.s
    s.write(thing + "\n\r")
    time.sleep(0.25)
    s.drainOutput()

  def clear(self):
    self.send("c")

  def start(self):
    self.clear()
    self.send("p0,0")

  def pos(self, h, v):
    wstr = "p%d,%d" % (h,v)
    self.send(wstr)

  def centered(self, str, h=1):
    x = (20 - len(str)) / 2
    self.pos(x,h)
    out = "w" + str
    self.send(out)

  def left(self, str, h=1):
    self.pos(0,h)
    out = "w" + str
    self.send(out)

  def top(self, val):
    print "top",val
    self.send("t%d" % (val))

  def bottom(self, val):
    print "bot", val
    self.send("b%d" % (val))

  def close(self):
    self.s.close()

if __name__ == "__main__":
  d = display()
  d.start()

  ttuple = time.localtime()
  date = time.strftime("%a %e %b", ttuple)
  d.centered(date, 0)

  t = time.time()

  while True:
    ttuple = time.localtime()
    tstr = time.strftime("%H:%M:%S", ttuple)
    date = time.strftime("%a %e %b",ttuple)
    d.centered(date, 0)
    d.centered(tstr, 2)
    time.sleep(0.1)
    nt = time.time()
    if (nt - t) > 5:
      t = time.time()
      d.send("b%d" % (random.randint(1,16)) )
      d.send("t%d" % (random.randint(1,16)) )
      if random.randint(1,10) == 1:
        d.send("e")

  d.close()
