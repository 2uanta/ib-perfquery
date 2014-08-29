ib-perfquery
============

Simple Python script to parse a command output using Python "exec".

The output of the command to parse looks like this:

# Port extended counters: Lid 996 port 1 (CapMask: 0x200)
PortSelect:......................1
CounterSelect:...................0x0000
PortXmitData:....................5602171943357
PortRcvData:.....................2004499376220
PortXmitPkts:....................11149272223
PortRcvPkts:.....................4628512230
PortUnicastXmitPkts:.............355674034
PortUnicastRcvPkts:..............4613858498
PortMulticastXmitPkts:...........587
PortMulticastRcvPkts:............1933493


The script will create variables by importing their names from the command output and not hardcoded.

This is mainly done with the #exec# function.

Other Python functions/features used:

* getopt to parse command line option in the standard way
* sleep timer
* subprocess to run the command and capture the stdout
* re for regular expression substitution
* get and print datetime 
* locale to format number with thousands seperator
* intercept KeyboardInterrupt to avoid stack trace when CTL-C during timer sleep
* print , to avoid adding newline when printing
* programmatically initialize a variable for the first time


