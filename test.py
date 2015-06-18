#!/usr/bin/env python

import urllib2, HTMLParser
from lxml.html import parse

class Worker():
	def __init__(self):
		self.main_url = ''
		self.worker_id = -1
		self.urls = []

	def get_links(self):
		parsed_html = parse(urllib2.urlopen(self.main_url))
		links = parsed_html.findall('.//tr/td/h4/a')
		for link in links:
			self.urls.append(link.get('href'))


class Status:
	def intro(self):
		print "Welcome, this web crawler is designed to look at IBM's developerworks webpage and summarize the problems."
		print "\nThe web crawling is about to begin."

def init_workers(n_pages, url):
	workers = []
	for i in range(n_pages):
		current_url = url + str(i)
		worker = Worker()
		worker.main_url = current_url
		worker.worker_id = i
		worker.get_links()
		workers.append(worker)
		print "Worker %i has found %i forums." % (worker.worker_id, len(worker.urls))
	return workers


def main():
	status = Status()
	status.intro()
	
	# hard-coded in for now
	number_of_pages = 2
	# starting url is the developer works webpage
	main_url = "https://www.ibm.com/developerworks/community/forums/html/forum?id=11111111-0000-0000-0000-000000000842#topicsPg="

	workers = init_workers(number_of_pages, main_url)


if __name__ == "__main__":
	main()