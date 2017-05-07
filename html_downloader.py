# coding:utf-8


class HtmlDownloader(object):
    def download(self, url, opener):
        if url is None:
            return None
        else:
            response = opener.open(url)

        if response.status != 200:
            return None
        else:
            return response.read()
