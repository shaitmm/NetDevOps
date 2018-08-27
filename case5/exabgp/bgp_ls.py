#!/usr/bin/env python

import sys
import os
import time
import json

f = open("/root/exabgp/test.log", "a+")

while True:
    line = sys.stdin.readline().strip()
    if line and "exabgp" in line:
        f.write(line + "\n" )
        f.flush()
