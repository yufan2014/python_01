#codeing:utf-8
import gzip
import urllib
from io import StringIO

import requests
import os


# print(os.getcwd());
# r = requests.get("https://item.taobao.com/item.htm?spm=a230r.1.14.1.q1QXUk&id=540089343657&ns=1&abbucket=2#detail")
#
# print(r.url);
# print(r.content);
# print(r.links);
#
#
# print('''1
# 2
# 3''')
#
# name = "tom";
# age = 3;
#
# print(name+" is "+str(age)+" year ")

def findUrlGzip(url):
    request = urllib.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    pener = urllib.build_opener()
    f = pener.open(request)
    isGzip = f.headers.get('Content-Encoding')
    #print isGzip
    if isGzip :
        compresseddata = f.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data = gzipper.read()
    else:
        data = f.read()
    return data

def findUrlTitle(url):
    html = findUrlGzip(url)
    html = html.lower()
    spos = html.find("<title>")
    epos = html.find("</title>")
    if spos != -1 and epos != -1 and spos < epos:
        title = html[spos+7:epos]
        title = title[:-9]
    else:
        title = ""
    return title

if __name__ == "__main__":
    url = 'http://business.sohu.com/20101010/n275509607.shtml'
    title = findUrlTitle(url)
    print(title)