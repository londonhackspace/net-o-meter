
net-o-meter
===========

This is the client code and vairous bits of hardware stuff for the london hackspace
network bandwidth meter.

The code for the mbed can be found here:

http://mbed.org/users/Jasper/code/net-o-meter/

talking to the mbed
-------------------

each command starts with a single letter and ends with newlines or carrage returns

### led strip commands

#### top

't'<num> switch on num leds of the top led strip. num is between 0-16 inclusive.

e.g. "t8" would switch on the first 8 leds.

#### bottom

'b'<num> switch on num leds of the bottom led strip. num is between 0-16 inclusive.

e.g. "b16" would switch on all the bottom leds.

#### setstrip

's'<'t'|'b'>rgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgbrgb Sets the leds on a strip to the 12 bit hex rgb value.

e.g.

* "stf00f00f00f00f00f00f00f00f00f00f00f00f00f00f00f00" set the top strip to all red
* "sbf0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0ff0f" set the bottom strip to all purple
* "st000111222333444555666777888999aaabbbcccdddeeefff" set the top strip to gradually increasing white brightnesses

#### emf

'e' (no args). switches all leds to a nice EMF blue colour.

e.g. "e"

### vfd display commands

#### write

'w'<text>. Writes "text" to the vfd starting at the current cursor position.

e.g. "wfish" would print "fish" on the vfd

#### position

'p' <x>,<y>. sets the vfd cursor position to x,y, x is 0 to 19 inclusive, and y is 0 to 3 inclusive. 0,0 is at the top left.

e.g.

* "p0,0" set the cursor to the origin.
* "p0,3" set the cursor to the beginning of the bottom line.

#### reset

'r' (no args). toggles the VDF reset pin and then waits for it to come back online.

#### clear

'c' (no args). clears all text on the vfd. does not reset the cursor position.

TODO
====

The client:
-----------

* ~~don't use snmp and instead get the stats from the kernel directly.~~
* logging.
* demonise.
* double check the counter wrapping stuff
* get the actual line speed from the adsl modem rather than hardcodeing it.

The mbed code:
--------------

* ~~publish the mbed code and add the url here~~
* work out wtf's up with the busy signal
* ~~finish arbatry colour code~~
* gamma correction and other colour fiddling?
* possibly re-write to use ethernet.
* upgrade mbed firmware: https://mbed.org/handbook/Firmware-LPC1768-LPC11U24
