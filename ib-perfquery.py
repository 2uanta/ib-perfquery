#!/usr/bin/python
# Run command several times and display delta value for each run
#
# # Port extended counters: Lid 274 port 1 (CapMask: 0x200)
# PortSelect:......................1
# CounterSelect:...................0x0000
# PortXmitData:....................4372366170488
# PortRcvData:.....................4395837050794
# PortXmitPkts:....................15541365352
# PortRcvPkts:.....................15589048273
# PortUnicastXmitPkts:.............23547071
# PortUnicastRcvPkts:..............65353049
# PortMulticastXmitPkts:...........764
# PortMulticastRcvPkts:............1890846

import sys, getopt
import subprocess
import time
import re

interval = 1
times = 5
PrevXmitData = 0
PrevRcvData = 0
PrevXmitPkts = 0
PrevRcvPkts = 0
PrevUnicastXmitPkts = 0
PrevUnicastRcvPkts = 0
PrevMulticastXmitPkts = 0
PrevMulticastRcvPkts = 0

def main(argv):
  global interval, times
  version = "1.0.0"

  def help():
    print "Usage: " + \
      sys.argv[0] + ' -i|--interval <seconds> -t|--times <number of times>'

  def calc_rate(output):
    global PrevXmitData, PrevRcvData
    global PrevXmitPkts, PrevRcvPkts
    global PrevUnicastXmitPkts, PrevUnicastRcvPkts 
    global PrevMulticastXmitPkts, PrevMulticastRcvPkts
    output = re.sub('\.','',output)
    output = re.sub(':','=',output)
    # import variable name and value from the output
    for e in output.split('\n')[2:11]:
      exec(e) in locals()
    
    XmitDataRate = (PortXmitData - PrevXmitData) / interval
    RcvDataRate = (PortRcvData - PrevRcvData) / interval
    XmitPktsRate = (PortXmitPkts - PrevXmitPkts) / interval
    RcvPktsRate = (PortRcvPkts - PrevRcvPkts) / interval
    UnicastXmitPktsRate = (PortUnicastXmitPkts - PrevUnicastXmitPkts) / interval
    UnicastRcvPktsRate = (PortUnicastRcvPkts - PrevUnicastRcvPkts) / interval
    MulticastXmitPktsRate = (PortMulticastXmitPkts - PrevMulticastXmitPkts) / \
	interval
    MulticastRcvPktsRate = (PortMulticastRcvPkts - PrevMulticastRcvPkts) / \
	interval

    PrevXmitData = PortXmitData
    PrevRcvData = PortRcvData
    PrevXmitPkts = PortXmitPkts
    PrevRcvPkts = PortRcvPkts
    PrevUnicastXmitPkts = PortUnicastXmitPkts
    PrevUnicastRcvPkts = PortUnicastRcvPkts
    PrevMulticastXmitPkts = PortMulticastXmitPkts
    PrevMulticastRcvPkts = PortMulticastRcvPkts

    print XmitDataRate , ", ", \
          RcvDataRate , ", ", \
          XmitPktsRate , ", ", \
          RcvPktsRate , ", ", \
          UnicastXmitPktsRate , ", ", \
          UnicastRcvPktsRate , ", ", \
          MulticastXmitPktsRate , ", ", \
          MulticastRcvPktsRate 
    
  try:
    opts, args = getopt.getopt(argv,"hvi:n:",["interval=","times="])
  except getopt.GetoptError:
    help()
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      help()
      sys.exit()
    elif opt == '-v':
      print version
      sys.exit()
    elif opt in ("-i", "--interval"):
      interval = int(arg)
    elif opt in ("-n", "--times"):
      times = int(arg)
  # print 'Interval is ', interval
  # print 'Times is ', times

  print "XmitDataRate, RcvDataRate, " + \
	"XmitPktsRate, RcvPktsRate," + \
	"UnicastXmitPktsRate, UnicastRcvPktsRate, " + \
	"MulticastXmitPktsRate, MulticastRcvPktsRate"
  for i in range(1,times+1):
    p = subprocess.Popen(["/usr/sbin/perfquery", "-x"],stdout=subprocess.PIPE)
    output = p.communicate()[0]
    # print output
    calc_rate(output)
    time.sleep(interval)

    
    
if __name__ == "__main__":
  main(sys.argv[1:])
