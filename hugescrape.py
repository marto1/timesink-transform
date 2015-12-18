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
from copy import copy
from urlparse import urlparse
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
CHAN_CDN = 'http://i.4cdn.org/{0}/{1}{2}'

#so, so bad autoplay loop controls
IMG_TAG='<img src="{0}" /> '
VIDEO_TAG='<video src="{0}" autoplay loop controls />'
html_tmpl = unicode("""
<section id="{0}">
<center>
<p>{0}</p>
{2}
<p><a href="{1}"> {1} <a/></p>
</center>
</section>
""")

####FETCHING

def escape_html(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    #boileeeeeeerplate
    return unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def convert_hugelol(entry):
    r = {}
    r['title'] = entry[6]
    r['media'] = entry[5]
    r['rest'] = copy(entry)
    return r

def convert_chan(entry):
    r = {}
    r['title'] = ""
    if 'com' in entry:
        r['title'] = entry['com']
    r['media'] = ""
    if ('ext' in entry) and ('tim' in entry):
        r['media'] = CHAN_CDN.format(BOARD,
                                     entry['tim'],
                                     entry['ext'])
    r['rest'] = copy(entry)
    return r    

def fetch(link, last=None, stype="hugelol"):
    """
    Fetch link and gather data from it.
    Result is a list of dicts for all stypes, dict format:
    {
     'title' : "" title of the entry
     'media' : "" full url to the entry
     'rest' : [] stype specific data goes here(copy of raw fetch)
    }
    """
    j = json.loads
    p = {}
    if last:
        p["after"] = last
    if stype == "hugelol":
        raw = j(j(get(link, params=p).text))
        res = [convert_hugelol(e) for e in raw]
        return res
    elif stype == "chan":
        raw = j(get(link).text)[u'posts']
        res = [convert_chan(e) for e in raw]
        return res

####END FETCHING

####OUTPUT FORMATS
def format_html_entry(e):
    h = escape_html
    if e['media'].endswith(".webm"):
        media = VIDEO_TAG.format(e['media'])
    else:
        media = IMG_TAG.format(e['media'])
    return html_tmpl.format(h(e['title']),
                            h(e['media']),
                            media)
def format_html(data):
    """Very basic formatting. Title+image+link in center one after ."""
    res = '<head><meta charset="utf-8"></head>' #yep, even here
    entries = [format_html_entry(e) for e in data]
    res += u'\n'.join(entries)
    return res

def format_csv(data): #FIXME quoting
    u = unicode
    res = [u'{0}, {1}'.format(u(e["media"]),
                              u(e["title"])) for e in data]
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

def format_json(data):
    return json.dumps(data)

formats = {"csv": format_csv,
           "html": format_html,
           "sexp": format_sexp,
           "json": format_json}
####END OUTPUT FORMATS

####FILTERS
def filter_webm(entry):
    try:
        return entry['media'].endswith(".webm")
    except KeyError:
        return False

def filter_sound(entry):
    if entry["media"]: #TODO
        return True

filters= {"webm": filter_webm,
          "sound": filter_sound}

####END FILTERS


####COMMON
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

####END COMMON

def main(last, format, stype):
    data = fetch(MAIN, last, stype)
    if type(data) == "list" and type(data[-1]) == list:
        last = data[-1][0]
    data = filter_data(data, arguments['--filter'])
    d = data
    data = format_data(data, arguments['--raw'], format)
    sys.stdout.write(u'{0}\n'.format(data))
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
    if arguments['--input-type'] == "chan":
        BOARD = urlparse(MAIN).path.split("/")[1]
    while True:
        last = main(last,
                    arguments['--output'],
                    arguments['--input-type'])
        if arguments['--continuous']:
            time.sleep(int(arguments['--continuous']))
        else:
            break
