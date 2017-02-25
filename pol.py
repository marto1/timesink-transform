#!/usr/bin/env python
"""
Gathering memes from /pol/ on steroids.
"""
from os import system
from commands import getoutput
import sys

JSFILE = "imagewall.js"
DATA= "var data = {0};\n"
A="python hugescrape.py --filter=image --input-type chan --output json '{0}'"

json_data = getoutput(A.format(sys.argv[1] + ".json"))
res = DATA.format(json_data)
with open(JSFILE, "w") as f:
    f.write(res)
