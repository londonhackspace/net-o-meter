#!/bin/sh


if [ x${ID_SERIAL_SHORT} = x101000000000000000000002F7F03B42 ] ; then
	case $ACTION in
	add)
		screen -S netometer -d -m su -c "/home/netometer/net-o-meter/client/iftable.py ppp0" - netometer
		;;
	remove)
		screen -S netometer -X quit
		;;
	*)
		echo "action was $ACTION" >> /tmp/runme.log
		;;
	esac
fi

