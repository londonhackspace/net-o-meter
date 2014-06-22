#!/usr/bin/env python
#
# from: https://github.com/bmhatfield/python-pidfile/blob/master/pidfile.py
#
# this could be included in python-daemon but oh no, that might actually
# make peoples lives easy! /sulk
#
## {{{ http://code.activestate.com/recipes/577911/ (r2)
import fcntl
import os, stat

class PidFile(object):
    """Context manager that locks a pid file. Implemented as class
not generator because daemon.py is calling .__exit__() with no parameters
instead of the None, None, None specified by PEP-343."""
    # pylint: disable=R0903

    def __init__(self, path):
        self.path = path
        self.pidfile = None

    def __enter__(self):
        self.pidfile = open(self.path, "a+")
        try:
            fcntl.flock(self.pidfile.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            raise SystemExit("Already running according to " + self.path)
        os.chmod(self.path, stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IROTH)
        self.pidfile.seek(0)
        self.pidfile.truncate()
        self.pidfile.write(str(os.getpid()))
        self.pidfile.flush()
        self.pidfile.seek(0)
        return self.pidfile

    def __exit__(self, exc_type=None, exc_value=None, exc_tb=None):
        try:
            self.pidfile.close()
        except IOError as err:
            # ok if file was just closed elsewhere
            if err.errno != 9:
                raise
        os.remove(self.path)