
net-o-meter
===========

This is the client code and vairous bits of hardware stuff for the london hackspace
network bandwidth meter.

The code for the mbed can be found here:

http://mbed.org/users/Jasper/code/net-o-meter/

You might need to download 
http://www.iana.org/assignments/ianaiftype-mib/ianaiftype-mib to
/var/lib/mibs/iana

talking to the mbed
-------------------

You can see a summary of this at http://net-o-meter.local/

    /v/r - reset the vfd.
    /v/c - clear the vfd.
    /v/p?x,y - set the cursor position to x,y. 0,0 is top left.
    /v/w?text - write text at the current cursor position

### led strip commands

#### top strip

/s/t?<num> switch on num leds of the top led strip. num is between 0-16 inclusive.

e.g. "/s/t?8" would switch on the first 8 leds.

#### bottom strip

/s/b?<num> switch on num leds of the bottom led strip. num is between 0-16 inclusive.

e.g. "/s/b?16" would switch on all the bottom leds.

#### setstrip

/s/set?<'t'|'b'>rgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgb Sets the leds on a strip to the 12 bit hex rgb value.

e.g.

* "/s/set?tf00f00f00f00f00f00f00f00f00f00f00f00f00f00f00f00" set the top strip to all red
* "/s/set?bf0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0f" set the bottom strip to all purple
* "/s/set?t000111222333444555666777888999aaabbbcccdddeeefff" set the top strip to gradually increasing white brightnesses

#### emf

/s/e (no args). switches all leds to a nice EMF blue colour.

e.g. "/s/e"

#### clear the strips

/s/clear switches the strips off.

### vfd display commands

#### write

/v/w?<text>. Writes "text" to the vfd starting at the current cursor position.

e.g. "/v/w?fish" would print "fish" on the vfd

#### position

/v/p?<x>,<y>. sets the vfd cursor position to x,y, x is 0 to 19 inclusive, and y is 0 to 3 inclusive. 0,0 is at the top left.

e.g.

* "/v/p?0,0" set the cursor to the origin.
* "/v/p?0,3" set the cursor to the beginning of the bottom line.

#### reset

/v/r (no args). toggles the VDF reset pin and then waits for it to come back online.

#### clear

/v/c (no args). clears all text on the vfd. does not reset the cursor position.

TODO
====

The client:
-----------

* ~~don't use snmp and instead get the stats from the kernel directly.~~
* logging.
* ~~demonise.~~
* double check the counter wrapping stuff
* get the actual line speed from the adsl modem rather than hardcodeing it.

The net-snmp code on linux only updates the network stats every 15 secs...

http://www.fineconnection.com/How_to_set_the_net-snmp_agent_update_or_counter_refresh_interval


The mbed code:
--------------

* ~~publish the mbed code and add the url here~~
* work out wtf's up with the busy signal
* ~~finish arbatry colour code~~
* gamma correction and other colour fiddling?
* ~~possibly re-write to use ethernet.~~
* upgrade mbed firmware: https://mbed.org/handbook/Firmware-LPC1768-LPC11U24
