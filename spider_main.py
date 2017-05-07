# coding:utf-8
import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
	def __init__(self):
		self.urls = url_manager.UrlManager()
		self.downloader = html_downloader.HtmlDownloader()
		self.parser = html_parser.HtmlParser()
		self.outputer = html_outputer.HtmlOutputer()

	def craw(self, root_url):
		count = 1
		self.urls.add_new_url(root_url)
		while self.urls.has_new_url():
			try:
				new_url = self.urls.get_new_url()
				# print('1111')
				html_cont = self. downloader.download(new_url)
				# print('2222')
				new_urls, new_data = self.parser.parse(new_url, html_cont)
				# print('3333')
				self.urls.add_new_urls(new_urls)
				# print('4444')
				self.outputer.collect_data(new_data)
				print("craw%d: %s" % (count, new_url))

				if count == 100:
					break

				count = count + 1

			except Exception as e:
				print(e)

		self.outputer.outputer_html()

if __name__ == "__main__":
	root_url = "https://www.taptap.com/topic/369401?page=1#postsList"
	obj_spider = SpiderMain()
	obj_spider.craw(root_url)
