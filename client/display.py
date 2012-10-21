#!/usr/bin/env python

import serial, time, random, logging

class display:
  def __init__(self, dev="/dev/netmeter"):
#    dev = "/dev/cu.usbmodem1d12"
#    dev = "/dev/tty.usbmodem1d12"
    self.dev = dev
    self.s = serial.Serial(dev, 9600)
    self.connected = True
    logging.basicConfig()
    self.l = logging.getLogger(__name__)
    print dir(self.l)
    self.start()
    if self.connected:
      self.l.info("Connected to display board")

  def reinit(self):
    if self.connected:
      try:
        self.s.close()
      except Exception, e:
        self.connected = False
        self.l.warning(e)
        time.sleep(10)
        return
    try:
      self.s = serial.Serial(self.dev, 9600)
      self.connected = True
      self.start()
    except Exception, e:
      self.l.warning(e)
      self.connected = False
      time.sleep(10)

  def send(self,thing):
    if not self.connected:
      self.reinit()
      return
    try:
      self.s.write(thing + "\n\r")
    except OSError, e:
      # device may of gone away
      self.l.warning("lost device? : " + str(e))
      self.reinit()
#    print thing
#    if thing.startswith("t") or thing.startswith("b") or thing.startswith("s"):
#      pass
#    else:
    time.sleep(0.25)
    try:
      self.s.drainOutput()
    except Exception, e:
      self.l.warning("oops: " + str(e))
      self.reinit()

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
    if val > 16:
      val = 16
    self.send("t%d" % (val))

  def bottom(self, val):
    if val > 16:
      val = 16
    self.send("b%d" % (val))

  def strip(self, strip, vals):
    assert len(vals) == 16, "only 16 leds per strip!"
    out = "s" + strip + ''.join(vals)
    assert len(out) == 1 + 1 + (16 * 3), "wrong length of something!"
    self.l.info(out)
    self.l.warn(out)
    self.send(out)

  def close(self):
    self.s.close()

def randcol():
  return "%x%x%x" % (random.randint(0,15), random.randint(0,15), random.randint(0,15))

if __name__ == "__main__":
  d = display()
  d.start()
  d.top(0)
  d.bottom(0)

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
#    time.sleep(0.1)
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
