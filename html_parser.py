# coding:utf-8
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):
        new_urls = set()

        try:
            # self.links = soup.findAll('a', href=re.compile("app/41908/review\?order=default&page=\d+#review-list"))
            f = open(r'E:\My_Project\gun_girls\id.txt')
            id = []
            links = []
            id_lines = f.readlines()
            for line in id_lines:
                id.append(str(line.strip('\n')))
            f.close()
            for i in id:
                # https://www.taptap.com/topic/271858?page=1#postsList
                link = soup.new_tag("a", href="/user/%s/played" % i)
                links.append(link)
            for link in links:
                new_url = link['href']
                new_full_url = urljoin(page_url, new_url)
                new_urls.add(new_full_url)
            return new_urls
        except Exception as e:
            print(e)

    def _get_new_data(self, page_url, soup):
        user_name = []
        view = []
        res_data = {}

        # url
        # res_data['url'] = page_url

        title_node = soup.find("section", class_="user-page-header")
        user_id = title_node.find("span").get_text()
        real_id = re.search(r'(\d+)', user_id)
        user_name.append(real_id.group())
        # res_data['title'] = title_node.get_text()

        summary_node = soup.find("section", class_="user-apps-list")
        # res_data['summary'] = summary_node.get_text()
        app_name = summary_node.findAll("h2")
        text = ""
        for i in app_name:
            item = i.get_text()
            text = text + "/" + item
        view.append(text)

        res_data['username'] = user_name
        res_data['reviews'] = view

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
