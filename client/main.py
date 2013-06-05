#!/usr/bin/env python
#
#

import os, sys, time, logging, select, socket, textwrap
from logging.handlers import SysLogHandler
from display import display
from histlist import historylist
from ifstatslinux import get_sys_stats
from nickcolors import sixteenbit2fourbitcolour, nick2colour
from iftable import get_speeds_snmp

host = "boole"
community = "public"

def fmt_speed(speed, period=5):
    speed = speed  * 8.0 # bits
    speed = speed / period # per second
    speed = speed / float(1000 * 1000) # mbit
    return "%.2f" % (speed)

def fmt_display(speed, link_speed = 380.0, period=5):
    link_speed = link_speed / 16.0
#    print "speed per led:", link_speed, "speed",speed
    speed = float(fmt_speed(speed, period)) / link_speed
#    print "speed:", int(speed)
    return int(speed)

get_speeds = get_speeds_snmp
#get_speeds = get_sys_stats

logger = logging.getLogger('net-o-meter')
logger.setLevel(logging.DEBUG)
syslog = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_DAEMON)
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

logger.warn("net-o-meter starting up.")

iface = "eth1"

if len(sys.argv) > 1:
    iface = sys.argv[1]

d = display()
d.clear()
d.start()
d.bottom(0)
d.top(0)
d.centered("inbound", 0)
d.centered("outbound", 2)

ttuple = time.localtime()
date = time.strftime("%a %e %b", ttuple)
d.centered(date, 1)

#
# XXX get these automatticly
#
downspeed = 80.0
upspeed = 20.0

period = 5
tperiod = period # target period

#speed = 380
host = "bogwoppit"
iface = "ppp0"
(oin, oout) = get_speeds(host, iface)
ntime = time.time()
time.sleep(period)

def speed_diff(ospeed, nspeed):
    # counter roll over
    # XXX python types vs. 2**32?
    if nspeed < ospeed:
        nspeed += 2 ** 32
    return nspeed - ospeed

# the period is wrong here cos of snmptable being slow, need to do this properly
iminlist = historylist(60 / period)
itenminlist = historylist(600 / period)

ominlist = historylist(60 / period)
otenminlist = historylist(600 / period)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('<broadcast>', 50000))
s.setblocking(0)

state = "bw"
statecount = 0

event = serial = name = None

wrapper = textwrap.TextWrapper(width=20, expand_tabs=False)

counter = 0
while True:
    (nin, nout) = get_speeds(iface)
    otime = ntime
    ntime = time.time()
    ispeed = speed_diff(oin, nin)
    ospeed = speed_diff(oout, nout)

    iminlist.append(ispeed)
    ominlist.append(ospeed)

    itenminlist.append(ispeed)
    otenminlist.append(ospeed)

#    print "i,o", ispeed, ospeed

    legend = "%d Secs sample" % (tperiod)

    # every other time
    if counter % 2 and ominlist.full():
        ispeed = iminlist.average()
        ospeed = ominlist.average()
        legend = "1 Min average"

    if ((counter % 6) == 0) and otenminlist.full():
        ispeed = itenminlist.average()
        ospeed = otenminlist.average()
        legend = "10 Min average"

    # these are in and out on the port, which is the wrong way round for the camp
    t = "Down " + fmt_speed(ispeed , ntime - otime) + " Mbits"
    b = "Up   " + fmt_speed(ospeed, ntime - otime) + " Mbits"

    d.clear()

    if state == "card":
        name = name.replace('\n', ' ')
        # the display is 20 chars accross
        nchunks = wrapper.wrap(name)
        if len(nchunks) > 3:
            nchunks = nchunks[0:3]
        y = 0
        for n in nchunks:
            d.left(n, y)
            y += 1
        d.left("Opened the door.", y)
        colour = sixteenbit2fourbitcolour(nick2colour(name))
        d.strip('t', (colour,) * 16)
        d.strip('b', (colour,) * 16)
    elif state == "bell":
        d.left("Somebody is", 0)
        d.left("at the door.", 1)
        d.strip('t', ('000', '0f0') * 8)
        d.strip('b', ('0f0', '000') * 8)        
    else:
        d.left(t, 0)
        d.left(b, 2)
        d.left(legend, 3)
        d.top(fmt_display(ispeed, downspeed, ntime - otime))
        d.bottom(fmt_display(ospeed, upspeed, ntime - otime))

    if statecount > 0:
        statecount -= 1
        if statecount == 0:
            state = "bw"

    real_period = ntime - otime

    pdiff = real_period - period
    period = tperiod - pdiff

    if not d.connected:
        continue
        
    if period < 2:
        continue

    result = select.select([s], [], [], period)
    if len(result[0]) != 0:
        payload = result[0][0].recv(1024)
        try:
            (event, serial, name) = payload.split("\n")
        except ValueError:
            logger.error("Unparsable payload: >%s<" % payload )
            event = None
            serial = None
            name = None
        if payload.find("56C00DBA") > -1:
            # hello paddy
            event = 'RFID'
            serial = '56C00DBA'
            name = 'Padski'
        logger.info("%s %s %s" % (event, serial, name))
        if (event == 'RFID' and name):
            state = "card"
            statecount = 2
        elif (event == 'BELL'):
            state = "bell"
            statecount = 2

    oin = nin
    oout = nout

    counter += 1
