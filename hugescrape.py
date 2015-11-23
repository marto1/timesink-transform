#!/usr/bin/env python
"""
Scrape huge/hiddenlol like site and print formatted to stdout.
Default output format is csv.

Usage: 
hugescrape [--raw] [--output=<format>] [--continuous=<seconds>] [<url>]

Options:
  -h, --help
  --raw             print raw result from query.
  --continuous=<seconds> fetch entries countiniously each seconds.
  --output=<format> choose output format[default: csv].

"""

#TODO --legacy use non-api way to fetch items

from docopt import docopt
from requests import get
import time
import sys
import urllib
import json
import codecs
import locale

sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)  #?


MAIN = "http://hugelol.com/api/front.php"

#so, so bad
html_tmpl = unicode("""
<section id="{0}">
<center>
<p>{0}</p>
<img src="{1}" /> 
<p><a href="{1}"> {1} <a/></p>
</center>
</section>
""")

def escape_html(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    #boileeeeeeerplate
    return unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')


def fetch(link, last=None):
    j = json.loads
    p = {}
    if last:
        p["after"] = last
    return j(j(get(link, params=p).text))

def format_html(data):
    """Very basic formatting. Title+image+link in center one after ."""
    h = escape_html
    res = [html_tmpl.format(h(e[6]), h(e[5])) for e in data]
    res = u'\n'.join(res)
    return res

def format_csv(data):
    u = unicode
    res = [u'{0}, {1}'.format(u(e[5]),
                              u(e[6])) for e in data]
    res = u'\n'.join(res)
    return res
    
formats = {"csv": format_csv,
           "html": format_html}

def format_data(data, raw=False, format="csv"):
    if raw:
        return data
    return formats[format](data)


def main(last, format):
    data = fetch(MAIN, last)
    last = data[-1][0]
    data = format_data(data, arguments['--raw'], format)
    sys.stdout.write(u'{0}\n'.format(data))
    return last

if __name__ == '__main__':
    last = None
    arguments = docopt(__doc__)
    if arguments['<url>']:
        MAIN = urllib.quote_plus(arguments['<url>'])
    if not arguments['--output']: #what?
        arguments['--output'] = "csv"

    while True:
        last = main(last, arguments['--output'])
        if arguments['--continuous']:
            time.sleep(int(arguments['--continuous']))
        else:
            break
