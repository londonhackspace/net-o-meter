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
    print thing
#    if thing.startswith("t") or thing.startswith("b") or thing.startswith("s"):
#      pass
#    else:
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

  def strip(self, strip, vals):
    assert len(vals) == 16, "only 16 leds per strip!"
    out = "s" + strip + ''.join(vals)
    assert len(out) == 1 + 1 + (16 * 3), "wrong length of something!"
    print out
    self.send(out)

  def close(self):
    self.s.close()

def randcol():
  return "%x%x%x" % (random.randint(0,15), random.randint(0,15), random.randint(0,15))

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
      a = randcol()
      b = randcol()
      z = [a for i in range(0,random.randint(0,14))]
      print z
      d.strip('t', z + [b for i in range(0, 16 - len(z))])

      a = randcol()
      b = randcol()
      z = [a for i in range(0,random.randint(0,14))]
      d.strip('b', z + [b for i in range(0, 16 - len(z))])

#      d.strip('t', [randcol() for i in range(0,16)])
#      d.strip('b', [randcol() for i in range(0,16)])

#      d.send("b%d" % (random.randint(1,16)) )
#      d.send("t%d" % (random.randint(1,16)) )
#      if random.randint(1,10) == 1:
#        d.send("e")

  d.close()
