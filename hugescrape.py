#!/usr/bin/env python
"""
Scrape huge/hiddenlol like site and print formatted to stdout.

Usage: 
hugescrape [--raw] [--continuous=<seconds>] [<url>]

Options:
  -h, --help
  --raw             print raw result from query.
  --continuous=<seconds> fetch entries countiniously each seconds.
"""

#TODO --legacy use non-api way to fetch items

from docopt import docopt
from requests import get
import time
import sys
import urllib
import json

MAIN = "http://hugelol.com/api/front.php"


def fetch(link, last=None):
    j = json.loads
    p = {}
    if last:
        p["after"] = last
    return j(j(get(link, params=p).text))

def format_data(data, raw=False):
    u = unicode
    if raw:
        return data
    res = [u'{0}, {1}'.format(u(e[5]),
                              u(e[6])) for e in data]
    res = u'\n'.join(res)
    return res

def main(last):
    data = fetch(MAIN, last)
    last = data[-1][0]
    data = format_data(data, arguments['--raw'])
    sys.stdout.write(u'{0}\n'.format(data))
    return last
if __name__ == '__main__':
    last = None
    arguments = docopt(__doc__)
    if arguments['<url>']:
        MAIN = urllib.quote_plus(arguments['<url>'])
    while True:
        last = main(last)
        if arguments['--continuous']:
            time.sleep(int(arguments['--continuous']))
        else:
            break
