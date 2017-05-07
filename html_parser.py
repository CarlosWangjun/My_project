# coding:utf-8
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin


class HtmlParser(object):

	def _get_new_urls(self, page_url, soup):
		new_urls = set()

		try:
			# self.links = soup.findAll('a', href=re.compile("app/41908/review\?order=default&page=\d+#review-list"))
			links = []
			for i in range(2, 12):
				link = soup.new_tag("a", href="/topic/369401?page=%s#postsList" % i)
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
		pid = []
		score = []
		res_data = {}

		# url
		# res_data['url'] = page_url

		try:
			title_node = soup.findAll("div", class_="posts-item collapse in")
			for i in title_node:
				x = i.find("a", href=re.compile("/user/\d+"))
				link = x['href']
				user_name.append(link)
			# res_data['title'] = title_node.get_text()
		except Exception as e:
			print(e)

		summary_node = soup.findAll('div', {'class': 'posts-item collapse in'})
		# res_data['summary'] = summary_node.get_text()
		for j in summary_node:
			b = j.find('div', class_="item-text-body bbcode-body").get_text()
			view.append(b)

		player_node = soup.findAll('div', {'class': 'posts-item collapse in'})
		# 写入模式改为追加
		# f = open(r"E:\My_Project\tapid_spider\id.txt", "a")
		try:
			for i in player_node:
				text = i.find('div', class_="item-text-body bbcode-body").get_text()
				c = re.search(r'(\d+)', text)
				if c is None:
					pid.append(c)
				else:
					pid.append(str(c.group()))
					# f.write("'" + str(c.group()) + '\n')
		except Exception as e:
			print(e)
		# finally:
		# 	f.close()

		score_node = soup.findAll('div', {'class': 'posts-item collapse in'})
		for i in score_node:
			full_text = i.find('div', class_="item-text-body bbcode-body").get_text()
			score_text = re.search(r'(伤害：|伤害:|伤害: |伤害|伤害 )(\d+)', full_text)
			# score_text_str = re.search(r'(\d+)', score_text)
			if score_text is None:
				score.append(score_text)
			else:
				score.append(str(score_text.group(2)))

		res_data['username'] = user_name
		res_data['reviews'] = view
		res_data['pid'] = pid
		res_data['score'] = score

		return res_data

	def parse(self, page_url, html_cont):
		if page_url is None or html_cont is None:
			return

		soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
		new_urls = self._get_new_urls(page_url, soup)
		new_data = self._get_new_data(page_url, soup)
		return new_urls, new_data
