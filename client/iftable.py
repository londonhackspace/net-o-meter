#!/usr/bin/env python
#
#

import os, sys, subprocess, time
from display import display
from histlist import historylist

host = "localhost"
community = "public"
cmd = "snmptable -Cf ,  -c " + community + " -v 2c -M /var/lib/mibs/ietf:/var/lib/mibs/iana -m IF-MIB:IANAifType-MIB " + host + "  ifTable"

def get_iftable():
    output = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
    output = output[0].split("\n")
    output = output[2:]
    header = output[0]
    header = header.split(',')
    output = output[1:]

    ret = {}
    for l in output:
        l = l.split(',')
        if len(l) != len(header):
            continue
        ret[l[0]] = {}
        for idx, item in enumerate(header):
            ret[l[0]][item] = l[idx]


    return ret

#['ifIndex', 'ifDescr', 'ifType', 'ifMtu', 'ifSpeed', 'ifPhysAddress', 'ifAdminStatus', 'ifOperStatus', 'ifLastChange', 'ifInOctets', 'ifInUcastPkts', 'ifInNUcastPkts', 'ifInDiscards', 'ifInErrors', 'ifInUnknownProtos', 'ifOutOctets', 'ifOutUcastPkts', 'ifOutNUcastPkts', 'ifOutDiscards', 'ifOutErrors', 'ifOutQLen', 'ifSpecific']

things = ['ifDescr', 'ifSpeed', 'ifInOctets', 'ifOutOctets']

for k in things:
    print k,
print

def get_speeds(ifname = 'eth1'):
    table = get_iftable()
    inoct = outoct = None
    for idx in table.keys():
#        print idx, table[idx]['ifType'], table[idx]['ifDescr'], table[idx]['ifSpeed']
        if table[idx]['ifType'] == 'ethernetCsmacd':
            if table[idx]['ifDescr'] == ifname:
                for k in things:
                    print table[idx][k],
                inoct = int(table[idx]['ifInOctets'])
                outoct = int(table[idx]['ifOutOctets'])                
                print
    return (inoct, outoct)

def fmt_speed(speed, period=5):
    print period
    speed = speed  * 8.0 # bits
    speed = speed / period # per second
    speed = speed / float(1000 * 1000) # mbit
    return "%.2f" % (speed)

def fmt_display(speed, link_speed = 380.0, period=5):
    link_speed = link_speed / 16.0
    print "speed per led:", link_speed, "speed",speed
    speed = float(fmt_speed(speed, period)) / link_speed
    print "speed:", int(speed)
    return int(speed)

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
downspeed = 18.55
upspeed = 2.59

period = 10

#speed = 380
(oin, oout) = get_speeds()
ntime = time.time()
time.sleep(period)

def speed_diff(ospeed, nspeed):
    # counter roll over
    # XXX python types vs. 2**32?
    if nspeed < ospeed:
        nspeed += 2 ** 32
    return nspeed - ospeed

# the period is wrong herecos if snmptable being slow, need to do this properly
iminlist = historylist(60 / period)
itenminlist = historylist(600 / period)

ominlist = historylist(60 / period)
otenminlist = historylist(600 / period)

counter = 0

while True:
    (nin, nout) = get_speeds()
    otime = ntime
    ntime = time.time()
    ispeed = speed_diff(oin, nin)
    ospeed = speed_diff(oout, nout)

    iminlist.append(ispeed)
    ominlist.append(ospeed)

    itenminlist.append(ispeed)
    otenminlist.append(ospeed)

    print "i,o", ispeed, ospeed

    legend = "%d Secs sample" % (period)

    # every other time
    if counter % 2 and ominlist.full():
        ispeed = iminlist.average()
        ospeed = ominlist.average()
        legend = "1 Min average"

    if ((counter % 6) == 0) and otenminlist.full():
        ispeed = itenminlist.average()
        ospeed = otenminlist.average()
        legend = "10 Min average"

    print ">>>", legend

    # these are in and out on the port, which is the wrong way round for the camp
    b = "In  " + fmt_speed(ispeed , ntime - otime) + " Mbits"
    t = "Out " + fmt_speed(ospeed, ntime - otime) + " Mbits"
    print t
    print b
    print
    d.clear()
    d.left(t, 0)
    d.left(b, 2)
    d.left(legend, 3)
    d.bottom(fmt_display(ispeed, downspeed, ntime - otime))
    d.top(fmt_display(ospeed, upspeed, ntime - otime))
    time.sleep(period)
    oin = nin
    oout = nout
    print "==" * 20
    counter += 1

