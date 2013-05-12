#!/bin/sh

echo "start" >> /tmp/runme.log

echo $ID_SERIAL_SHORT >> /tmp/runme.log
echo ${ID_SERIAL_SHORT} >> /tmp/runme.log

if [ x${ID_SERIAL_SHORT} = x101000000000000000000002F7F03B42 ] ; then
	echo >> /tmp/runme.log
	env >> /tmp/runme.log
	echo >> /tmp/runme.log
	case $ACTION in
	add)
		echo "added" >> /tmp/runme.log
		;;
	remove)
		echo "removed" >> /tmp/runme.log
		;;
	*)
		echo "action was $ACTION" >> /tmp/runme.log
		;;
	esac
fi

echo "done">> /tmp/runme.log
echo >> /tmp/runme.log
