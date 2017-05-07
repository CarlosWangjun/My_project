# coding:utf-8


class HtmlOutputer(object):
	def __init__(self):
		self.datas = []

	def collect_data(self, data):
		if data is None:
			return
		self.datas.append(data)

	def outputer_html(self):
		# print(len(self.datas))
		fout = open('output.html', 'w', encoding="utf-8")

		fout.write("<html>")
		fout.write("<head>")
		fout.write('<meta http-equiv="content-type" content="text/html;charset=utf-8">')
		fout.write("<body>")
		fout.write("<table>")

		for data in self.datas:
			# print(len(data['username']))
			for x in range(0, len(data['username'])):

				fout.write("<tr>")
				# fout.write("<td>%s</td>" % data['url'])
				fout.write("<td>%s</td>" % data['username'][x])
				fout.write("<td>%s</td>" % data['reviews'][x])
				fout.write("<td>%s</td>" % data['pid'][x])
				fout.write("<td>%s</td>" % data['score'][x])
				fout.write("</tr>")

		fout.write("</table>")
		fout.write("</body>")
		fout.write("</head>")
		fout.write("</html>")

		fout.close()
