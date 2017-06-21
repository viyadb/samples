#!/usr/bin/env python2.7

from datetime import datetime
import re
import fileinput

log_re = re.compile(r'(\S+).*\[([^\]]+)\s[\-\+]\d+\]\s+"([A-Z]+)\s+(\S+)\s+([^"]+)"\s+(\d+)')
for line in fileinput.input():
    m = re.search(log_re, line)
    if m:
        vals = [m.group(i) for i in range(1, 7)]
        vals[1] = datetime.strptime(vals[1], "%d/%b/%Y:%H:%M:%S").strftime("%Y%m%d%H%M%S")
        print "\t".join(vals)
