#!/usr/bin/python
# Run command several times and display delta value for each run
# $ perfquery -x
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
import locale
import datetime

interval = 1
times = 3
first = True

def main(argv):
  global interval, times
  version = "5.1.0"
  optl = False
  optT = False
  optx = False

  def help():
    print "Usage: " + \
      sys.argv[0] + ' -h -v -l -T -x -i|--interval <seconds> -t|--times <number of times>'
    print "-h	: help"
    print "-v	: print version"
    print "-l	: output in /var/log format"
    print "-T	: do not print header"
    print "-x	: show unicast/multicast packets"
    print "Ouput will be displayed after the first time interval"

  def calc_rate(output):
    global first
    output = re.sub('\.','',output)
    output = re.sub(':','=',output)
    if not first and optl:
      print datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ";",
    # magic here is to use variable name from the output received
    if optx:
      end = 11
    else:
      end = 7
    for e in output.split('\n')[3:end]:
      exec(e) in globals()
      portvar, value = e.split('=')
      var = re.sub('Port','',portvar)
      prevvar = "Prev" + var
      varrate = var + "Rate"
      if prevvar not in globals():
        stmt = prevvar + "=0"
        exec(stmt) in globals()
      calc = varrate + "=(" + portvar + "-" + prevvar + ") / interval" 
      exec(calc) in globals()
      save = prevvar + "=" + portvar
      exec(save) in globals()
      if not first:
        #printvar = "print " + varrate + ","
        if optl:
          printname = "print '" + varrate + ": ',"
          exec(printname) in globals()
          printvar = \
            "print locale.format('%12d'," + varrate + ",grouping=True)+" + "';'," 
        else:
          printvar = \
            "print locale.format('%12d'," + varrate + ",grouping=True)" + "," 
        exec(printvar) in globals()
    if not first:
      print
    else:
      first = False
    
  try:
    opts, args = getopt.getopt(argv,"hvlTxi:n:",["interval=","times="])
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
    elif opt == '-l':
      optl = True
    elif opt == '-T':
      optT = True
    elif opt == '-x':
      optx = True
    elif opt in ("-i", "--interval"):
      interval = int(arg)
    elif opt in ("-n", "--times"):
      times = int(arg)

  if not optT and not optl:
    print "  XmitData/s    RcvData/s " + \
          "  XmitPkts/s    RcvPkts/s",
    if optx:
      print \
	  " UXmitPkts/s   URcvPkts/s " + \
	  " MXmitPkts/s   MRcvPkts/s"
    print
  locale.setlocale(locale.LC_ALL, 'en_US')
  for i in range(1,times+2):
    p = subprocess.Popen(["/usr/sbin/perfquery", "-x"],stdout=subprocess.PIPE)
    output = p.communicate()[0]
    calc_rate(output)

    try:
      time.sleep(interval)
    except KeyboardInterrupt:
      print "Bye"
      sys.exit()
 
if __name__ == "__main__":
  main(sys.argv[1:])
