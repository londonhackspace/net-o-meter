#!/usr/bin/env python
#
# get the incoming and outgoing bandwidth usage of an interface from the kernel
#

#
def get_sys_stats(iface="eth1"):
  path = "/sys/class/net/%s/statistics/" % (iface)
  ret = []
  for t in ("rx_bytes","tx_bytes"):
    fh = open(path + "/" + t)
    ret.append(int(fh.read()))
    fh.close()
  return ret

  
if __name__ == "__main__":
  print get_stats()

