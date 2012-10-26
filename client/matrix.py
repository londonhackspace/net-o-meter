#!/usr/bin/env python
#
#
#

from display import display
import time, random, os

def line():
  out = []
  for i in range(0,20):
    if random.randint(0,100) > 80:
      out.append("%c" % random.randint(0xa0, 0xa0 + 64))
    else:
      out.append(' ')
  return ''.join(out)

#
# duration is in seconds
#
def matrix(d, duration=None):
  stime = time.time()
  lines = [line(), line(), line(), line()]
  print len(line())
  while True:
    if duration != None and (time.time() - stime) > duration:
      return
    d.pos(0,0)
    d.write(lines[0])
    d.write(lines[1])
    d.write(lines[2])
    d.write(lines[3])
    lines.insert(0,line())
    del(lines[4])
    time.sleep(0.1)
  print len(lines)

if __name__ == "__main__":
  if os.path.exists("/dev/ttyACM0"):
    d = display("/dev/ttyACM0")
  else:
    d = display()
  d.start()
  d.top(0)
  d.bottom(0)
  matrix(d, 10)
