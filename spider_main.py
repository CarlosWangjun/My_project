# coding:utf-8
import url_manager, html_downloader, html_parser, html_outputer
from urllib import request
from urllib import parse
import re
from bs4 import BeautifulSoup
import http.cookiejar


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url, opener):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                html_cont = self.downloader.download(new_url, opener)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                print("craw%d: %s" % (count, new_url))

                count = count + 1

            except Exception as e:
                print(e)

        self.outputer.outputer_html()


if __name__ == "__main__":
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '108',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.taptap.com',
        'Origin': 'https://www.taptap.com',
        'Referer': 'https://www.taptap.com/auth/login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/57.0.2987.133 Safari/537.36 '
    }

    login_url = r'https://www.taptap.com/auth/login'
    hosturl = r'https://www.taptap.com'

    cj = http.cookiejar.CookieJar()
    cookie_support = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(cookie_support, request.HTTPHandler)
    request.install_opener(opener)
    h = request.urlopen(hosturl)

    html_txt = request.urlopen(login_url).read()
    html_soup = BeautifulSoup(html_txt, 'html.parser')
    token = html_soup.find("input", {"name": "_token"})["value"]

    postData = {
        '_token': token,
        'email': 'wangjun@xindong.com',
        'password': 'xindong2015',
        'remember': 'on'
    }

    data = parse.urlencode(postData).encode(encoding='utf-8')

    request_url = request.Request(login_url, data, headers)
    response = opener.open(request_url)
    # response = request.urlopen(request_url)
    # text = response.read().decode(encoding="utf-8")
    # print(text)

    root_url = "https://www.taptap.com/user/4328310/played"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url, opener)
