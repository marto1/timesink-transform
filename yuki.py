#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Faster sequential viewer for yuki.la chan archive.
"""
import requests
from bs4 import BeautifulSoup
import sys

def extract_thread_entry(container):
    subject = container.find("span", attrs={"class": "subject"}).text
    content = container.find("blockquote", attrs={"class": "postMessage"}).text
    image = container.find("a", attrs={"class": "fileThumb"})['href']
    image = image.replace('//', '')
    image = "https://" + image
    return subject, content, image

def create_thread_html(subject, content, image):
    result = u"<div>"
    result += u"<h2>{}</h2>".format(subject)
    result += u"<p>{}</p>".format(content)
    result += u'<img src="{}" />'.format(image)
    result += u"</div>"
    return result

def main(starturl):
    #data = requests.get(starturl).text

    #writing
    # f = open("site.html", "w")
    # f.write(data.encode('utf8'))
    # f.close()

    #reading
    f = open("site.html", "r")
    data = f.read().decode('utf8')
    f.close()

    soup = BeautifulSoup(data, 'html.parser')
    result = u"<html><body>"
    for container in soup.find_all('div', attrs={"class": "post op"}):
        info = extract_thread_entry(container)
        result += create_thread_html(*info)
    result += u"</body></html>"
    print result

    f = open("out.html", "w")
    f.write(result.encode('utf8'))
    f.close()


if __name__ == '__main__':
    main(sys.argv[1])
