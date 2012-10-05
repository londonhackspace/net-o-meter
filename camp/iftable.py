#!/usr/bin/env python
#
#

import os, sys, subprocess, time
from display import display

host = "rt1.bsqmk.emfcamp.org"
community = "emf"
cmd = "snmptable -Cf ,  -c " + community + " -v 2c " + host + "  ifTable"

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

def get_speeds(ifname = 'GigabitEthernet0/2'):
    table = get_iftable()
    inoct = outoct = None
    for idx in table.keys():
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

def fmt_display(speed, link_speed = 380.0):
    link_speed = link_speed / 16.0
    speed = float(fmt_speed(speed)) / link_speed
    return int(speed)

d = display()
d.clear()
d.start()
d.centered("inbound", 0)
d.centered("outbound", 2)

ttuple = time.localtime()
date = time.strftime("%a %e %b", ttuple)
d.centered(date, 1)

speed = 380
(oin, oout) = get_speeds()
ntime = time.time()
time.sleep(5)

def speed_diff(ospeed, nspeed):
    # counter roll over
    if nspeed < ospeed:
        nspeed += 2 ** 32
    return nspeed - ospeed

while True:
    (nin, nout) = get_speeds()
    otime = ntime
    ntime = time.time()
    ispeed = speed_diff(oin, nin)
    ospeed = speed_diff(oout, nout)
    # these are in and out on the port, which is the wrong way round for the camp
    b = "out " + fmt_speed(ispeed , ntime - otime) + " Mbits"
    t = "in " + fmt_speed(ospeed, ntime - otime) + " Mbits"
    print t
    print b
    d.clear()
    d.left(t, 0)
    d.left(b, 2)
    d.bottom(fmt_display(ispeed))
    d.top(fmt_display(ospeed))
    time.sleep(5)
    oin = nin
    oout = nout
