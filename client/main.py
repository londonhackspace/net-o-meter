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

class Speed:
    def __init__(self, callback, args, inspeed, outspeed, period = 5):
        self.cb = callback
        self.args = args
        self.inspeed = None
        self.outspeed = None
        self.lasttime = None
        self.time = None
        self.in_max_speed = inspeed
        self.out_max_speed = outspeed
        self.lastin = None

        # the period is wrong here cos of snmptable being slow,
        # need to do this properly
        #
        # the period isn't right (it changes with how
        # slow snmptable is or isn't).
        #
        # need to have histlist know it's length in time
        # and discard samples older than the duration we are interested in.
        #
        self.iminlist = historylist(60 / period)
        self.itenminlist = historylist(600 / period)

        self.ominlist = historylist(60 / period)
        self.otenminlist = historylist(600 / period)
    
    def update(self):
        inspeed, outspeed = self.cb(*self.args)
        if inspeed == None or outspeed == None:
            # didn't get it for some reason
            return
        self.lastin = self.inspeed
        self.lastout = self.outspeed
        self.inspeed, self.outspeed = inspeed, outspeed
        self.lasttime = self.time
        self.time = time.time()

    def speed_diff(self, ospeed, nspeed):
        # counter roll over
        # XXX python types vs. 2**32?
        if nspeed < ospeed:
            nspeed += 2 ** 32
        return nspeed - ospeed

    def rate(self):
        for t in self.inspeed, self.outspeed, self.lastin, self.time, self.lasttime:
            if t == None:
                return (None, None)
        
        period = self.time - self.lasttime
        inspeed = self.speed_diff(self.lastin, self.inspeed) / period
        outspeed = self.speed_diff(self.lastout, self.outspeed) / period
        self.iminlist.append(inspeed)
        self.ominlist.append(outspeed)
        self.itenminlist.append(inspeed)
        self.otenminlist.append(outspeed)
        return (inspeed, outspeed)

    def onemin(self):
        return (self.iminlist.average(), self.ominlist.average())

    def onemin_mbit(self):
        return (self.mbit(self.iminlist.average()),
                self.mbit(self.ominlist.average()))

    def tenmin(self):
        return (self.itenminlist.average(), self.otenminlist.average())

    def tenmin_mbit(self):
        return (self.mbit(self.itenminlist.average()),
                self.mbit(self.otenminlist.average()))

    def mbit(self, speed):
        if speed == None:
            return "0.0"
        speed = speed  * 8.0 # bits
        speed = speed / float(1000 * 1000) # mbit
        return "%.2f" % (speed)
        
    def rate_mbit(self):
        inspeed, outspeed = self.rate()
        return (self.mbit(inspeed), self.mbit(outspeed))

    def display_mangle(self, speed, link_speed):
        link = link_speed / 16.0
        speed = int(float(speed) / link)
        return speed

    def rate_display(self):
        # also busted period
        inspeed, outspeed = self.rate_mbit()
        ret = []
        for rate, link_speed in ((inspeed, self.in_max_speed), (outspeed, self.out_max_speed)):
            ret.append(self.display_mangle(rate, link_speed))
        return ret

    def onemin_display(self):
        inspeed, outspeed = self.onemin_mbit()
        ret = []
        for rate, link_speed in ((inspeed, self.in_max_speed), (outspeed, self.out_max_speed)):
            ret.append(self.display_mangle(rate, link_speed))
        return ret
    
    def tenmin_display(self):
        inspeed, outspeed = self.tenmin_mbit()
        ret = []
        for rate, link_speed in ((inspeed, self.in_max_speed), (outspeed, self.out_max_speed)):
            ret.append(self.display_mangle(rate, link_speed))
        return ret

logger = logging.root
logger.setLevel(logging.DEBUG)
syslog = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_DAEMON)
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
syslog.setFormatter(formatter)
logger.addHandler(syslog)

logger.info("net-o-meter starting up.")

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

host = "boole"

#speeds = (('ppp0', 80.0, 20.0), ('ppp1', 80.0, 20.0))
zeniface = Speed(get_speeds_snmp, [host, 'ppp0'], downspeed, upspeed)

# I'm not sure about the up and down speeds
# but i think this is right.
aaiface = Speed(get_speeds_snmp, [host, 'ppp1'], 40.0, 10.0)

ifaces = [["Zen (IPv4)", zeniface, 0], ["A&A (IPv6)", aaiface, 0]]

for ispname, iface, c in ifaces:
    iface.update()

ntime = time.time()
time.sleep(period)

def bcast_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('<broadcast>', port))
    s.setblocking(0)
    return s

s = bcast_socket(50000)
s_bell = bcast_socket(50002)

state = "bw"
statecount = 0

event = serial = name = None
iselect = 0

wrapper = textwrap.TextWrapper(width=20, expand_tabs=False)

while True:
    for ispname, iface, c in ifaces:
        iface.update()
    otime = ntime
    ntime = time.time()

    ispname, iface, counter = ifaces[iselect]
    ifaces[iselect][2] += 1
    if iselect == 1:
        iselect = 0
    else:
        iselect = 1

    ispeed, ospeed = iface.rate_mbit()
    indisplay, outdisplay = iface.rate_display()

    legend = "%d Secs sample" % (tperiod)

    # every other time
    if counter % 2 and iface.ominlist.full():
        (ispeed, ospeed) = iface.onemin_mbit()
        indisplay, outdisplay = iface.onemin_display()
        legend = "1 Min average"

    if ((counter % 6) == 0) and iface.otenminlist.full():
        (ispeed, ospeed) = iface.tenmin_mbit()
        indisplay, outdisplay = iface.tenmin_display()
        legend = "10 Min average"

    # these are in and out on the port
    t = "Down " + str(ispeed) + " Mbits"
    b = "Up   " + str(ospeed) + " Mbits"

    d.clear()

    if state == "card":
        name = name.replace('\n', ' ')
        colour = sixteenbit2fourbitcolour(nick2colour(name))
        name = name + " Opened the %s door." % (source)
        # the display is 20 chars accross
        nchunks = wrapper.wrap(name)
        if len(nchunks) > 3:
            nchunks = nchunks[0:3]
        y = 0
        for n in nchunks:
            d.left(n, y)
            y += 1
        d.strip('t', (colour,) * 16)
        d.strip('b', (colour,) * 16)
    elif state == "bell":
        d.left("Somebody is", 0)
        d.left("at the door.", 1)
        d.strip('t', ('000', '0f0') * 8)
        d.strip('b', ('0f0', '000') * 8)        
    else:
        d.left(t, 0)
        d.left("ISP: " + ispname, 1)
        d.left(b, 2)
        d.left(legend, 3)
        d.top(indisplay)
        d.bottom(outdisplay)

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

    result = select.select([s, s_bell], [], [], period)
    source = None
    if len(result[0]) != 0:
        payload = result[0][0].recv(1024)

        # we only read from the 1st id.
        # if we get 2 packets at the same time do we lose the 2nd?
        if result[0][0] == s:
            source = "back"

        if result[0][0] == s_bell:
            source = "front"

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
        logger.info("%s: %s %s %s" % (source, event, serial, name))
        if (event == 'RFID' and name):
            state = "card"
            statecount = 2
        elif (event == 'BELL'):
            state = "bell"
            statecount = 2
