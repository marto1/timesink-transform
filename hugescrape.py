#!/usr/bin/env python
"""
Scrape huge/hiddenlol like site and print formatted to stdout.
Default output format is csv.

Usage: 
hugescrape [--raw] [--output=<format>] [--continuous=<seconds>] [--input-type=<stype>] [--filter=<filters>] [<url>]

Options:
  -h, --help
  --raw             print raw result from fetching.
  --continuous=<seconds> fetch entries countiniously each seconds.
  --output=<format> choose output format[default: csv].
  --input-type=<stype> site type[default: hugelol].
  --filter=<filters> comma separated list of filters, executer sequentialy.
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

#?
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)
#?

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


def fetch(link, last=None, stype="hugelol"):
    j = json.loads
    p = {}
    if last:
        p["after"] = last
    if stype == "hugelol":
        return j(j(get(link, params=p).text))
    elif stype == "chan":
        return j(get(link).text)[u'posts']

def format_html(data):
    """Very basic formatting. Title+image+link in center one after ."""
    h = escape_html
    res = '<head><meta charset="utf-8"></head>' #yep, even here
    res += [html_tmpl.format(h(e[6]), h(e[5])) for e in data]
    res = u'\n'.join(res)
    return res

def format_csv(data): #FIXME quoting
    u = unicode
    res = [u'{0}, {1}'.format(u(e[5]),
                              u(e[6])) for e in data]
    res = u'\n'.join(res)
    return res

def format_sexp(data):
    """ Pairs (link title) """
    u = unicode
    res = "("
    resl = [u'("{0}" "{1}")'.format(u(e[5]),
                               u(e[6])) for e in data]
    res += u' '.join(resl) +")"
    return res

formats = {"csv": format_csv,
           "html": format_html,
           "sexp": format_sexp}

def filter_webm(entry):
    try:
        if entry[u'ext'] == ".webm":
            return True
        else:
            return False
    except KeyError:
        return False

def filter_sound(entry):
    if entry["tim"]:
        return True

filters= {"webm": filter_webm,
          "sound": filter_sound}


def format_data(data, raw=False, format="csv"):
    if raw:
        return data
    return formats[format](data)

def filter_data(data, in_filters):
    if not in_filters:
        return data
    for f in in_filters.split(","):
        data = filter(filters[f], data)
    return data

def main(last, format, stype):
    data = fetch(MAIN, last, stype)
    if type(data) == "list" and type(data[-1]) == list:
        last = data[-1][0]
    data = filter_data(data, arguments['--filter'])
    d = data
    data = format_data(data, arguments['--raw'], format)
    sys.stdout.write(u'{0}\n'.format(data))
    print len(d)
    return last

if __name__ == '__main__':
    last = None
    arguments = docopt(__doc__)
    if arguments['<url>']:
        MAIN = arguments['<url>']
    if not arguments['--output']: #what?
        arguments['--output'] = "csv"
    if not arguments['--input-type']:
        arguments['--input-type'] = "hugelol"
    while True:
        last = main(last,
                    arguments['--output'],
                    arguments['--input-type'])
        if arguments['--continuous']:
            time.sleep(int(arguments['--continuous']))
        else:
            break
