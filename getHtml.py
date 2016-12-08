# coding: utf-8
import gzip
import re
import urllib
from io import StringIO

import requests
from lxml import etree
from bs4 import BeautifulSoup



def getHtml():
    url = 'http://huaban.com/favorite/quotes/';
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie':'__auc=11e5713e153ea82cfc00a237be9; CNZZDATA1256914954=1391414995-1473148893-http%253A%252F%252Fwww.cssmoban.com%252F%7C1473214405; _ga=GA1.2.1459091775.1459928354; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1481164599558; CNZZDATA1256903590=148064653-1459925249-null%7C1481160183; sid=UpqKa2OFIbulHhdGo6Caq4KXhzd.DB0xQSj3DNXiH9AFFmtvtbTjTKcSyLwdqBGBwl74Bqw',
        'Host': 'huaban.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    req = urllib.request.Request(url=url, headers=headers)
    page =  urllib.request.urlopen(req)
    isGzip = page.headers.get('Content-Encoding')
    if isGzip :
        compresseddata = page.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data = gzipper.read()
    else:
        data = page.read()
    return data


#解压gzip
def gzdecode(data) :
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()   # 读取解压缩后数据
    return data2

def getSoup(html):
    if None == html:
        return
    return BeautifulSoup(html, "html.parser");


def parse(soup):
    if None == soup:
        return
    all_a = soup.findAll(name='div', attrs={'class': 'img'});
    if None != all_a:
        for a_a in all_a:
            img_url = a_a.findAll('img').attrs['src'];
            print(img_url);


def xpath_parse(html):
    if None == html:
        return
    selector = etree.HTML(html)
    content = selector.xpath('//*[@id="waterfall"]/div[5]/div[3]/div/div/div[1]/a')  # 这里使用starts-with方法提取div的id标签属性值开头为a的div标签
    for each in content:
        print(each);

# 后缀都是固定的
# 列表小图 http://img.hb.aicdn.com/daa44953fc2ff0ef4b7c39b152aa8d19ecc85759e09d-AxWwdW_fw192
# 详情大图 http://img.hb.aicdn.com/daa44953fc2ff0ef4b7c39b152aa8d19ecc85759e09d-AxWwdW_fw554

def getPins():
    # pin_id = 48145457
    # response = requests.get('http://huaban.com/favorite/quotes')
    pin_id = 948413941
    limit = 20
    # response = requests.get('http://huaban.com/favorite/quotes/?fetch&iwg2kra4&max='+str(pin_id)+'&limit='+str(limit)+'&wfl=1')
    response = requests.get('http://huaban.com/favorite/quotes/')
    content =  response.content
    content = content.decode('utf-8')
    # appPins = re.findall(r'app\.page\["pins"\].*',content)
    #### 获取HTML源码里面的app.page["pins"]部分，主要图片ID位于此部分
    app_page_pins_re = re.compile(r'app.page\[\"pins\"\].*', re.S)
    appPins = re.findall(app_page_pins_re,content)
    print(appPins)


    reg = re.compile('"pin_id":(.*?),.+?"file":{"farm":"farm1", "bucket":"hbimg",.+?"key":"(.*?)",.+?"type":"image/(.*?)"', re.S)
    groups = re.findall(reg, content)
    print(groups)

    for att in groups:
        pin_id = att[0]
        att_url = att[1] + '_fw554'
        img_type = att[2]
        img_url = 'http://img.hb.aicdn.com/' + att_url
        print(img_url)

        # if (urllib.urlretrieve(img_url, 'beauty/' + att_url + '.' + img_type)):
        #     print(img_url + '.' + img_type + ' download success!')
        # else:
        #     print(img_url + '.' + img_type + ' save failed')


# http://huaban.com/favorite/quotes/?fetch&iwg2kr9x&since=948800541&limit=100&wfl=1
# http://huaban.com/favorite/quotes/?iwg2kra4&max=948413941&limit=20&wfl=1
# http://huaban.com/favorite/quotes/?iwg2krac&max=946290746&limit=20&wfl=1


# http://huaban.com/favorite/quotes/?iwg2y5s6&max=947737573&limit=20&wfl=1
# http://huaban.com/favorite/quotes/?iwg2y5s9&max=946290746&limit=20&wfl=1
# http://huaban.com/favorite/quotes/?iwg2y5sf&max=944748210&limit=20&wfl=1
# http://huaban.com/favorite/quotes/?iwg2y5sj&max=943386695&limit=20&wfl=1



# z13.cnzz.com/stat.htm?id=1256903590&r=&lg=zh-cn&ntime=1481181619&cnzz_eid=17048614-1473400184-null&showp=1920x1080&p=http://huaban.com/favorite/quotes/?max=943386695&limit=20&wfl=1&cv=is-logon|logged-out|1481184402098&t=美图美文_花瓣，陪你做生活的设计师（发现、采集你喜欢的美文美图）_花瓣网&h=1&rnd=271079851
# http://huaban.com/favorite/quotes/?iwg2y5sj&max=943386695&limit=20&wfl=1



if __name__ == '__main__':
    getPins()
    # html = getHtml()
    # str_html =  gzdecode(html)
    # soup = getSoup(html)
    # parse(soup);
    # xpath_parse(html)
