"""
Batch convert a dir of webms to mixtape.moe links.
"""
import requests
import os
from glob import glob

#https://github.com/nokonoko/Pomf/blob/master/js/cheesesteak.js
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0",
    "Host": "mixtape.moe",
    "Referer": "https://mixtape.moe/",
}

# {u'files': [{u'url': u'https://my.mixtape.moe/gqptuo.webm', u'hash': u'd0696ebb233acf64e0e867d13bcf0bef9ca84e04', u'name': u'1524986429237.webm', u'size': 1485880}, {u'url': u'https://my.mixtape.moe/axriin.webm', u'hash': u'7c2cbc4d0cb214f5d4dd735789377d6a106ff8b6', u'name': u'1525270065166.webm', u'size': 1581628}], u'success': True}           

URL = "https://mixtape.moe/upload.php"
PATH = "/home/user/webms/*.webm"
RFILE = "/home/user/wlist.txt"


if __name__ == '__main__':
    flist = glob(PATH)
    o = os.path.basename
    webms = [("files[]", open(fil, "r")) for fil in flist]
    response = requests.post(URL, files=webms, headers=headers)
    # print repr(response.request.body)[:200]
    # print response.request.headers
    result = response.json()["files"]
    with open(RFILE, "w") as f:
        for entry in result:
            f.write("{}\n".format(entry["url"]))
