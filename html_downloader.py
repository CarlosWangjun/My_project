# coding:utf-8
from urllib import request


class HtmlDownloader(object):

	def download(self, url):
		if url is None:
			return None
		else:
			response = request.urlopen(url)

		if response.status != 200:
			return None
		else:
			return response.read()
