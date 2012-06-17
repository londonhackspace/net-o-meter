# author:  Vanessa Dannenberg
# email: vanessadannenberg@gmail.com
# dist-license: GPL
# use-license: unlimited

Element["" "EDGE34" "EDGE34" "" 255000 477500 10000 100000 3 100 ""]
(
	Pad[-40000 160000 0 160000 7499 2394 9893 "GND" "34" "square"]
	Pad[-40000 150000 0 150000 7499 2394 9893 "GND" "32" "square"]
	Pad[-40000 140000 0 140000 7499 2394 9893 "GND" "30" "square"]
	Pad[-40000 130000 0 130000 7499 2394 9893 "GND" "28" "square"]
	Pad[-40000 120000 0 120000 7499 2394 9893 "GND" "26" "square"]
	Pad[-40000 110000 0 110000 7499 2394 9893 "GND" "24" "square"]
	Pad[-40000 100000 0 100000 7499 2394 9893 "GND" "23" "square"]
	Pad[-40000 90000 0 90000 7499 2394 9893 "GND" "20" "square"]
	Pad[-40000 80000 0 80000 7499 2394 9893 "GND" "18" "square"]
	Pad[-40000 70000 0 70000 7499 2394 9893 "GND" "16" "square"]
	Pad[-40000 60000 0 60000 7499 2394 9893 "GND" "14" "square"]
	Pad[-40000 50000 0 50000 7499 2394 9893 "GND" "12" "square"]
	Pad[-40000 40000 0 40000 7499 2394 9893 "GND" "10" "square"]
	Pad[-40000 30000 0 30000 7499 2394 9893 "GND" "8" "square"]
	Pad[-40000 20000 0 20000 7499 2394 9893 "GND" "6" "square"]
	Pad[-40000 10000 0 10000 7499 2394 9893 "GND" "4" "square"]
	Pad[-40000 0 0 0 7499 2394 9893         "GND" "2" "square"]

# and the back.

	Pad[-40000 0 0 0 7499 2394 9893          "D7"  "1" "auto,square,onsolder"]
	Pad[-40000 10000 0 10000 7499 2394 9893  "D6"  "3" "auto,square,onsolder"]
	Pad[-40000 20000 0 20000 7499 2394 9893  "D5"  "5" "auto,square,onsolder"]
	Pad[-40000 30000 0 30000 7499 2394 9893  "D4"  "7" "auto,square,onsolder"]
	Pad[-40000 40000 0 40000 7499 2394 9893  "D3"  "9" "auto,square,onsolder"]
	Pad[-40000 50000 0 50000 7499 2394 9893  "D2"  "11" "auto,square,onsolder"]
	Pad[-40000 60000 0 60000 7499 2394 9893  "D1"  "13" "auto,square,onsolder"]
	Pad[-40000 70000 0 70000 7499 2394 9893  "D0"  "15" "auto,square,onsolder"]
	Pad[-40000 80000 0 80000 7499 2394 9893  "/WR" "17" "auto,square,onsolder"]
	Pad[-40000 90000 0 90000 7499 2394 9893  "A0"  "19" "auto,square,onsolder"]
	Pad[-40000 100000 0 100000 7499 2394 9893 "/RD"    "21" "auto,square,onsolder"]
	Pad[-40000 110000 0 110000 7499 2394 9893 "/SS"    "23" "auto,square,onsolder"]
	Pad[-40000 120000 0 120000 7499 2394 9893 "/TEST"  "25" "auto,square,onsolder"]
	Pad[-40000 130000 0 130000 7499 2394 9893 "BUSY"   "27" "auto,square,onsolder"]
	Pad[-40000 140000 0 140000 7499 2394 9893 "/BL"    "29" "auto,square,onsolder"]
	Pad[-40000 150000 0 150000 7499 2394 9893 "/RESET" "31" "auto,square,onsolder"]
	Pad[-40000 160000 0 160000 7499 2394 9893 "NC"     "33" "auto,square,onsolder"]

	ElementLine [-45000 -7500 5000 -7500 600]
	ElementLine [-45000 -7500 -45000 217500 600]
	ElementLine [5000 217500 -45000 217500 600]

	)
