## 总结
## ^ 匹配字符串的开始。
## $ 匹配字符串的结尾。
## \b 匹配一个单词的边界。
## \d 匹配任意数字。
## \D 匹配任意非数字字符。
## x? 匹配一个可选的 x 字符 (换言之，它匹配 1 次或者 0 次 x 字符)。
## x* 匹配0次或者多次 x 字符。
## x+ 匹配1次或者多次 x 字符。
## x{n,m} 匹配 x 字符，至少 n 次，至多 m 次。
## (a|b|c) 要么匹配 a，要么匹配 b，要么匹配 c。
## (x) 一般情况下表示一个记忆组 (remembered group)。你可以利用 re.search 函数返回对象的 groups() 函数获取它的值。
## 正则表达式中的点号通常意味着 “匹配任意单字符”
import urllib
import urllib.request
from bs4 import BeautifulSoup
import requests
import re

def getHTML(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, "html.parser")
    return html
def getRating(url):
    page = urllib.request.urlopen(url).read().decode('gbkgba').encode('utf-8')
    return page
def getOriginalPic(url):
    page = urllib.request.urlopen(url)
    html = page.read().decode('utf-8')
    return html
def DownloadRequest(oriaddr,imagaddr):
    downloadHeader = {
        'Accept-Language' : 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }
    downloadHeader['Referer'] = oriaddr
    Fakeaddr = urllib.request.Request( imagaddr, headers = downloadHeader) #加入header模仿浏览器的行为
    decodeFakeAddr = urllib.request.urlopen(Fakeaddr)
    return decodeFakeAddr.read()
def DownloadPic(originalAddr,imageAddr):
    addr = dict(zip(originalAddr,imageAddr)) #图片的地址和图片网页的地址建立字典
    c = 1
    for i in originalAddr:
        p = re.compile(r'\d')
        id = [int(x) for x in p.findall(i)]  # 正则表达式提取图片id
        id_number = 0
        for j in range(len(id)):
            id_number = id_number * 10 + id[j]  # 把id从列表变为int数
        # print(id_number) #测试是否正确输出
        f = open('/users/mac/PycharmProjects/Pixiv/images/{}.jpg'.format(id_number), 'wb')
        f.write(DownloadRequest(i, addr.get(i)))
        print('正在保存第{}张图片'.format(c))
        c += 1


keyword = str(input("输入关键词： "))
min = int(input("输入起始页数： "))
max = int(input("输入终止页数:  "))
downloadlink = [] #图片的原地址
p_imag_download = [] #加过header之后可以直接下载的图片地址
j = 1
for i in range(min,max):
    url = "http://www.pixiv.net/search.php?word={}&order=date_d&p={}".format(keyword, i)
    #print(getHTML(url))
    Content = getHTML(url)
    Picture = Content.find_all('li', {'class': 'image-item'})
    for i in Picture:
        imagelink = i.find('a').get('href')
        downloadlink.append(imagelink)
        print('正在查找第{}张图片的地址'.format(j))
        j += 1
for i in downloadlink:
    print('少女祈祷中。。。')
    Image = getHTML('http://www.pixiv.net'+i)
    ImageDownload = Image.find_all('a', {'class': 'require-register medium-image _work '})
    for j in ImageDownload:
        MediumPicDownload = j.find('img').get('src')
        #print(MediumPicDownload) #直接打开图片链接会403，因为程序没有给服务器发送referer(打开大图必须要有原网页）
        p_imag_download.append(MediumPicDownload)
for i in range(len(downloadlink)):
    downloadlink[i] = 'http://www.pixiv.net' + downloadlink[i]
"""dict = dict(zip(downloadlink,p_imag_download)) #合并两个长度相同的数组成为字典
c = 1
for i in downloadlink:
    p = re.compile(r'\d')
    id = [int(x) for x in p.findall(i)] #正则表达式提取图片id
    id_number = 0
    for j in range(len(id)):
        id_number = id_number * 10 + id[j] #把id从列表变为int数
    #print(id_number) #测试是否正确输出
    f = open('/users/mac/PycharmProjects/Pixiv/images/{}.jpg'.format(id_number),'wb')
    f.write(DownloadRequest(i,dict.get(i)))
    print('正在保存第{}张图片'.format(c))
    c += 1"""

DownloadPic(downloadlink,p_imag_download) #p_imag_download是加过headers修饰的图片的地址














